from plug_in import Hosted

from cnc.modules.common.app.uow.uow import UnitOfWork
from cnc.modules.common.domain.repository import Repository
from cnc.modules.common.impl.repository.sqla.repo import SqlAlchemyRepository
from cnc.modules.common.impl.service.query_session.sqla import SqlalchemySessionManager
from cnc.modules.common.impl.uow.sqla.config import SqlAlchemyUowConfig
from cnc.shared.ioc.root import root_router
from cnc.modules.common.impl.uow.sqla.uow import SqlAlchemyUow
from cnc.shared.settings.app import AppSettings


@root_router.manage()
def provide_uow(settings: AppSettings = Hosted()) -> SqlAlchemyUow:
    config = SqlAlchemyUowConfig(uri=settings.get_db_url(), echo=settings.DB_ECHO)
    uow = SqlAlchemyUow(config=config)
    return uow


@root_router.manage()
def provide_repo(uow: UnitOfWork = Hosted()) -> Repository:
    return uow.get_repository()


@root_router.manage()
def provide_sqla_repo(sqla_uow: SqlAlchemyUow = Hosted()) -> SqlAlchemyRepository:
    return sqla_uow.get_repository()


@root_router.manage()
def provide_query_session_manager(
    sqla_uow: SqlAlchemyUow = Hosted(),
) -> SqlalchemySessionManager:
    sessionmaker, is_standalone = sqla_uow.get_preferred_sessionmaker()
    sqla_manager = SqlalchemySessionManager(
        preferred_sessionmaker=sessionmaker, is_standalone=is_standalone
    )
    return sqla_manager
