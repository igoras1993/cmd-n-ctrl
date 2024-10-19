from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent.parent.parent.parent.absolute().joinpath("env")


class LoggingSettings(BaseSettings):
    """
    Application logging may be parametrized using this class. The `coloredlogs`
    lib used to make logs pretty.

    Environment variables:
        * LOGGING_COLOR_<LEVEL> - each log level may has an own color
        * LOGGING_COLOR_<FIELD> - each log field may has an own color
        * LOGGING_FORMAT_<FIELD> - flag determines if field is added to logs
        * LOGGING_DATETIME_FORMAT - DATETIME field format
        * LOGGING_LEVEL - root log level
        * LOGGING_LEVEL_PER_LOGGER - comma separated <LOGGER_NAME>:<LEVEL>
            values change the level of particular logger

    color values:
        * 0 - black
        * 1 - red
        * 2 - green
        * 3 - yellow
        * 4 - blue
        * 5 - magenta
        * 6 - cyan
        * 7 - white

    more info: https://coloredlogs.readthedocs.io/en/latest/api.html#about-the-defaults
    """

    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

    LOGGING_COLOR_DEBUG: int = 2
    LOGGING_COLOR_INFO: int = 7
    LOGGING_COLOR_WARNING: int = 3
    LOGGING_COLOR_ERROR: int = 1
    LOGGING_COLOR_FATAL: int = 1

    LOGGING_COLOR_HOSTNAME: int = 5
    LOGGING_COLOR_NAME: int = 4
    LOGGING_COLOR_LEVELNAME: int = 6
    LOGGING_COLOR_ASCTIME: int = 5

    LOGGING_FORMAT_DATETIME: bool = True
    LOGGING_FORMAT_NAME: bool = True
    LOGGING_FORMAT_LEVELNAME: bool = True
    LOGGING_FORMAT_HOSTNAME: bool = False
    LOGGING_FORMAT_PROCESS: bool = False

    LOGGING_DATETIME_FORMAT: str = "%Y/%m/%d %H:%M:%S"

    LOGGING_LEVEL: str = "DEBUG"
    LOGGING_LEVEL_PER_LOGGER: dict[str, str] = Field(
        default_factory=lambda: {"unit-tests": "WARNING", "access-log": "DEBUG"}
    )

    @field_validator(
        "LOGGING_COLOR_DEBUG",
        "LOGGING_COLOR_INFO",
        "LOGGING_COLOR_WARNING",
        "LOGGING_COLOR_ERROR",
        "LOGGING_COLOR_FATAL",
        "LOGGING_COLOR_HOSTNAME",
        "LOGGING_COLOR_NAME",
        "LOGGING_COLOR_LEVELNAME",
        "LOGGING_COLOR_ASCTIME",
    )
    def check_val(cls, v):
        """
        Checks if color value is between 0 and 255
        """
        if v < 0 or v > 255:
            raise ValueError("color value must be between 0 and 255")
        return v

    def level_styles(self):
        """
        Log level styles definition
        """
        return {
            "debug": {"color": self.LOGGING_COLOR_DEBUG},
            "info": {"color": self.LOGGING_COLOR_INFO},
            "warning": {"color": self.LOGGING_COLOR_WARNING},
            "error": {"color": self.LOGGING_COLOR_ERROR},
            "critical": {"color": self.LOGGING_COLOR_FATAL, "bold": True},
        }

    def field_styles(self):
        """
        Log field styles definition
        """
        return {
            "hostname": {"color": self.LOGGING_COLOR_HOSTNAME},
            "name": {"color": self.LOGGING_COLOR_NAME},
            "levelname": {"color": self.LOGGING_COLOR_LEVELNAME, "bold": True},
            "asctime": {"color": self.LOGGING_COLOR_ASCTIME},
        }

    def format(self):
        """
        Log format definition
        Default "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        """
        fields = []
        if self.LOGGING_FORMAT_DATETIME:
            fields.append("%(asctime)s")
        if self.LOGGING_FORMAT_HOSTNAME:
            fields.append("%(hostname)-10s")
        if self.LOGGING_FORMAT_PROCESS:
            fields.append("%(process)-6s")
        if self.LOGGING_FORMAT_LEVELNAME:
            fields.append("%(levelname)-8s")
        if self.LOGGING_FORMAT_NAME:
            fields.append("%(name)s")
        result = " | ".join(fields)
        return f"{result}: %(message)s"

    def datetime_format(self):
        """
        Datetime field format
        """
        return self.LOGGING_DATETIME_FORMAT
