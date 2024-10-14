from plug_in.types.proto.core_registry import CoreRegistryProtocol
from db.src.custom.ioc import ioc_router


def configure_mounts(reg: CoreRegistryProtocol) -> None:
    ioc_router.mount(reg)
