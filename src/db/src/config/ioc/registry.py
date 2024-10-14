from plug_in.core.registry import CoreRegistry
from db.src.config.ioc.plugins import all_plugins


def configure_plugin_registry() -> CoreRegistry:
    return CoreRegistry(plugins=all_plugins())
