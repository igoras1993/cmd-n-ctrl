from typing import Any
from plug_in.types.proto.core_plugin import CorePluginProtocol
from plug_in import plug

from db.src.config.ioc.plugins.settings import settings_provider
from db.src.custom.settings import AlembicSettings


def all_plugins() -> tuple[CorePluginProtocol[Any, Any], ...]:
    return (plug(settings_provider).into(AlembicSettings).via_provider("lazy"),)
