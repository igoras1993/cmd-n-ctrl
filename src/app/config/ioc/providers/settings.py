from app.shared.settings.app import AppSettings
from app.shared.settings.log import LoggingSettings


def provide_app_settings() -> AppSettings:
    # .env feeding
    return AppSettings()  # type: ignore


def provide_log_settings() -> LoggingSettings:
    # .env feeding
    return LoggingSettings()  # type: ignore
