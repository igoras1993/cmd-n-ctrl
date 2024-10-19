import coloredlogs
import logging

from typing import Any


def configure_logging(
    level: str,
    fmt: str,
    datefmt: str,
    level_styles: dict[str, Any],
    field_styles: dict[str, Any],
    level_per_logger: dict[str, str],
    isatty: bool = True,
    **kwargs
) -> None:
    coloredlogs.install(
        level=level,
        fmt=fmt,
        datefmt=datefmt,
        level_styles=level_styles,
        field_styles=field_styles,
        isatty=isatty,
        **kwargs
    )

    for logger_name, logger_level in level_per_logger.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(coloredlogs.level_to_number(logger_level))
