from plug_in.types.proto.core_registry import CoreRegistryProtocol

from db.src.config.ioc.mounts import configure_mounts
from db.src.config.ioc.registry import configure_plugin_registry


def configure_ioc() -> CoreRegistryProtocol:
    reg = configure_plugin_registry()
    configure_mounts(reg)
    return reg
