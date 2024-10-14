from app.config.ioc.plugins import all_plugins
from app.shared.ioc.root import root_config


def configure_ioc() -> None:
    root_config.init_root_registry(
        plugins=all_plugins(), include_default_plugins=True, reg_kwargs={}
    )
