from abc import abstractmethod
from typing import Protocol

from cnc.modules.common.domain.value_obj.net_address import MacAddress


class NetworkDevice(Protocol):

    @property
    @abstractmethod
    def mac_address(self) -> MacAddress: ...


class NetworkParticipant(NetworkDevice, Protocol):

    @property
    @abstractmethod
    def ip_address(self) -> MacAddress: ...
