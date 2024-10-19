from typing import Any, Callable
from plug_in import plug
from plug_in.types.proto.core_plugin import CorePluginProtocol

from sqlalchemy.ext.asyncio import AsyncSession

from cnc.config.ioc.providers.services import (
    provide_query_session_manager,
    provide_repo,
    provide_sqla_repo,
    provide_uow,
)
from cnc.config.ioc.providers.settings import provide_app_settings, provide_log_settings
from cnc.config.ioc.providers.tools import provide_http_client_reg
from cnc.modules.common.app.service.query_session import QuerySessionManager
from cnc.modules.common.app.uow.uow import UnitOfWork
from cnc.modules.common.domain.repository import Repository
from cnc.modules.common.impl.repository.sqla.repo import SqlAlchemyRepository
from cnc.modules.common.impl.service.query_session.sqla import SqlalchemySessionManager
from cnc.modules.common.impl.tools.http.client import SharedHttpClient
from cnc.modules.common.impl.tools.http.client_reg import SharedHttpClientRegistry
from cnc.modules.common.impl.uow.sqla.uow import SqlAlchemyUow
from cnc.shared.settings.app import AppSettings
from cnc.shared.settings.log import LoggingSettings


def all_plugins() -> tuple[CorePluginProtocol[Any, Any], ...]:
    http_client_reg = provide_http_client_reg()
    return (
        # AppSettings
        plug(provide_app_settings).into(AppSettings).via_provider("lazy"),
        # LoggingSettings
        plug(provide_log_settings).into(LoggingSettings).via_provider("lazy"),
        # UoW
        plug(provide_uow).into(UnitOfWork).via_provider("lazy"),
        plug(provide_uow).into(SqlAlchemyUow).via_provider("lazy"),
        # Repository
        plug(provide_repo).into(Repository).via_provider("factory"),
        plug(provide_sqla_repo).into(SqlAlchemyRepository).via_provider("factory"),
        # QuerySessionManager
        plug(provide_query_session_manager)
        .into(QuerySessionManager[AsyncSession])
        .via_provider("factory"),
        plug(provide_query_session_manager)
        .into(SqlalchemySessionManager)
        .via_provider("factory"),
        # Http client registry
        plug(http_client_reg).into(SharedHttpClientRegistry).directly(),
        plug(http_client_reg).into(Callable[[str], SharedHttpClient]).directly(),
    )
