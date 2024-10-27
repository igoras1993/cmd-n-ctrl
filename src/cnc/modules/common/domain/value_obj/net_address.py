from abc import ABC
from typing import Literal

from attr import dataclass
from netaddr import EUI, IPAddress

from cnc.modules.common.domain.enums.net_address import NetAddressType


@dataclass(frozen=True)
class NetworkAddress(ABC):
    type: NetAddressType


@dataclass(frozen=True)
class MacAddress(NetworkAddress):
    value: EUI
    type: Literal[NetAddressType.MAC] = NetAddressType.MAC


@dataclass(frozen=True)
class IpAddress(NetworkAddress):
    value: IPAddress
    type: Literal[NetAddressType.IP] = NetAddressType.IP
