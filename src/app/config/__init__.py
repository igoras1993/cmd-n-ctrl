from plug_in.core.host import CoreHost
from app.config.ioc.configure import configure_ioc
from app.config.logging import configure_logging
from app.shared.ioc.root import root_config
from app.shared.settings.log import LoggingSettings


def configure_app():
    configure_ioc()

    logging_settings = root_config.get_registry().sync_resolve(CoreHost(LoggingSettings))

    configure_logging(
        level=logging_settings.LOGGING_LEVEL,
        fmt=logging_settings.format(),
        datefmt=logging_settings.datetime_format(),
        level_styles=logging_settings.level_styles(),
        field_styles=logging_settings.field_styles(),
        level_per_logger=logging_settings.LOGGING_LEVEL_PER_LOGGER,
    )
