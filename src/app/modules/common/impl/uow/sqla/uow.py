from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any, AsyncGenerator, Callable
from uuid import UUID
from venv import logger

from plug_in import Hosted

from app.shared.ioc.root import root_router

from app.modules.common.app.msg_bus.protocol.bus import MessageBus
from app.modules.common.app.uow.enum import WorkloadStrategy
from app.modules.common.app.uow.errors import MissingUowContext
from app.modules.common.app.uow.uow import UnitOfWork
from app.modules.common.domain.msg_bus.msg import Message
from app.modules.common.impl.repository.sqla.repo import (
    SqlAlchemyRepository,
)
from app.modules.common.impl.uow.sqla.config import SqlAlchemyUowConfig
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from app.modules.common.impl.uow.sqla.ctx_data import (
    CtxData,
)
from app.shared.logging import get_logger
from app.shared.singleton import HashMapSingleton


log = get_logger(__name__)


class SqlAlchemyUow(UnitOfWork, metaclass=HashMapSingleton):
    """
    This UoW is desired to work with async SQLAlchemy and asyncio event loop. It is
    hash-mapped singleton (i.e. it's constructor hashes the instances) that bases on init
    config parameter. Whenever `config` parameter has the same hash as other one, then
    the same instance will be used. For configs that are differing, other instance will
    be used.

    This UoW is meant to be used in highly concurrent environment. It's consistency
    guarantees are emerging from SQL transactions atomicity. Implementation ensures
    that consistency boundaries are spanning **across the asyncio task context**.
    Whenever this Uow is used in one asyncio task scope, all `CONSISTENT` message
    pushes will be handled in one SQL transaction.

    All its API is coroutine safe, due to task-contextual work model.

    You can manually commit/rollback, however, as long as You work inside UoW context
    (using `async with uow.start(): ...`) commit will happen automatically when no
    exceptions are raised inside context, and rollback will happen automatically if some
    exceptions are raised (and not caught) inside context.

    Beware that the manual commit / rollback will interfere with consistency guarantees
    of UoW. You can do this, but then You cannot assume anything on atomicity or
    non-atomicity either.

    ```
    uow.start() (first call in this task)
        \\
         | (something happens)
        C|
        T|  uow.start() (another call somewhere else in this task)
        X|//            (already existing context is utilized)
         |
        A| (something happens)
        L|
        I|\\
        V|  __exit__ (last start() call ends it life)
        E|//
         |          (But since there is only one ctx, and it is alive)
         |          ( - nothing changes, there is still the same context)
         |
        //
    __exit__ (original start() call ends its live, now there is no context)

    bus.dispatch(NON_CONSISTENT_MESSAGE) - Messages pushed with non-consistent
    strategy are dispatched at this point.
    ```
    """

    def __init__(self, config: SqlAlchemyUowConfig):
        self._config = config
        self._engine = create_async_engine(self._config.uri, echo=self._config.echo)
        self._session_factory = async_sessionmaker(
            self._engine, autoflush=False, expire_on_commit=False
        )
        self._scoped_session_factory = async_scoped_session(
            self._session_factory, scopefunc=self.ctx_id
        )

    # HashMapSingleton requirement
    @classmethod
    def get_args_hash(cls, config: SqlAlchemyUowConfig, *_, **__) -> SqlAlchemyUowConfig:
        return config

    @staticmethod
    def _add_deferred_msg(msg: Message) -> None:
        SqlAlchemyUow.ctx().deferred_messages.append(msg)

    @staticmethod
    @root_router.manage()
    def _get_bus(bus: MessageBus = Hosted()) -> MessageBus:
        return bus

    @staticmethod
    def ctx() -> CtxData:
        try:
            ctx = _sqla_uow_ctx.get()
        except LookupError:
            raise MissingUowContext(
                "No context available for this request. Ensure that You are working "
                "inside async with UnitOfWork(): ... context"
            )
        else:
            return ctx

    @staticmethod
    def ctx_id() -> UUID:
        return SqlAlchemyUow.ctx().id

    def get_repository(self) -> SqlAlchemyRepository:
        return SqlAlchemyRepository(session=self.get_session())

    def get_session(self) -> AsyncSession:
        return self._scoped_session_factory()

    def get_preferred_sessionmaker(self) -> tuple[Callable[[], AsyncSession], bool]:
        """
        Decide about possible sessionmaker that is trasactionlly preferred by a
        queries.

        Prefers to return scoped factory, bound to context. If No context is available
        then returns standalone session maker.

        In every case, a tuple of `(sessionmaker, is_standalone)` is returned.
        `is_standalone` flag indicates the type of sessionmaker that was returned
        """

        try:
            self.ctx()
        except MissingUowContext:
            return self._session_factory, True
        else:
            return self._scoped_session_factory, False

    def get_standalone_session(self) -> AsyncSession:
        """
        This method returns a session instance that is detached from UoW consistency
        guarantees.
        This means that the caller is responsible for managing of transaction state.
        """
        return self._session_factory()

    async def push(
        self,
        msg: Message,
        workload_strategy: WorkloadStrategy,
    ) -> None:

        match workload_strategy:
            case WorkloadStrategy.CONSISTENT:
                await self._get_bus().dispatch(msg)

            case WorkloadStrategy.NON_CONSISTENT:
                self._add_deferred_msg(msg)

            case _:
                raise RuntimeError(f"{workload_strategy=} not supported by {self=}")

    async def commit(self, **kwargs: Any) -> None:
        session = self.get_session()
        await session.commit()

    async def rollback(self, **kwargs: Any) -> None:
        session = self.get_session()
        await session.rollback()

    @asynccontextmanager
    async def start(self) -> AsyncGenerator[None, None]:

        try:
            SqlAlchemyUow.ctx()
        except MissingUowContext:
            # Brand new context, I am the one to handle it
            token = _sqla_uow_ctx.set(CtxData())
            session = self._scoped_session_factory()

            exception: Exception | None = None
            async with session:

                try:
                    yield
                except Exception as e:
                    # Exit due to exception
                    exception = e
                else:
                    await session.commit()
                finally:
                    deferred_msg_queue = self.ctx().deferred_messages

                    # Reset ctx
                    _sqla_uow_ctx.reset(token)

            # After resetting, dispatch deferred messages
            # But only if there was no exception
            if exception is None:
                bus = self._get_bus()
                while deferred_msg_queue:
                    # FIFO, so popleft
                    msg = deferred_msg_queue.popleft()
                    logger.debug("Dispatching deferred message: %s", msg)
                    await bus.dispatch(msg)
            else:
                logger.info(
                    "Skipping %s messages due to exception %s",
                    len(deferred_msg_queue),
                    exception,
                )
                # Reraise
                raise exception

        else:
            # Already in context, just continue, other generator is responsible
            # for teardown
            yield


_sqla_uow_ctx: ContextVar[CtxData] = ContextVar(
    "sqla_uow_ctx",
)
