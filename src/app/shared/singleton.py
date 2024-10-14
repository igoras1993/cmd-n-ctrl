from abc import abstractmethod
from threading import RLock
from typing import Any, Hashable, Protocol


class HashMapSingleton[**Ps](type(Protocol)):  # type: ignore
    _instances: dict[Hashable, Any] = {}
    _lock = RLock()

    def __call__(cls, *args: Ps.args, **kwargs: Ps.kwargs):  # type: ignore
        with cls._lock:
            arg_hash = hash((cls, cls.get_args_hash(*args, **kwargs)))
            if cls not in cls._instances:
                instance = super(HashMapSingleton, cls).__call__(*args, **kwargs)
                cls._instances[arg_hash] = instance
                return instance
            return cls._instances[arg_hash]

    @abstractmethod
    def get_args_hash(cls, *args: Ps.args, **kwargs: Ps.kwargs) -> Hashable:
        """
        HasMapSingleton classes must implement this as a class method. Instances
        are considered the same as long as hash of their `(cls, inst.get_args_hash())`
        is equal.
        """
        ...
