import inspect
from pathlib import Path
from typing import TypeGuard


class CssLoader:
    """
    Args:
        css_path: Path to the css file to be used. If given as a relative,
            a base path of the class owning CssLoader definition is used.
            If not given, assumes that css file is named `<owning_class_name>.tcss`
            and located at the `<owning_class_file_directory>/css/` directory.
    """

    def __init__(
        self, path: str | None = None, populate_into: str | None = "DEFAULT_CSS"
    ):
        self.css_path = Path(path) if path is not None else None
        self.populate_into = populate_into

    @staticmethod
    def is_path_absolute(path: Path | None) -> TypeGuard[Path]:
        """
        Returns `True` if given `path` is in absolute format, and
        `False` otherwise.
        """
        if path is None:
            return False
        else:
            return path.is_absolute()

    def get_static_path(self) -> Path:
        """
        Returns path to the css file assuming that `self.css_path` is given
        as absolute. If this assumption is not satisfied, then `AssertionError`
        will be raised

        Raises:
            AssertionError: If `path` passed to the init method is not absolute
        """
        if self.is_path_absolute(self.css_path):
            return self.css_path
        else:
            raise AssertionError(f"{self.css_path=} is not absolute path")

    @staticmethod
    def owner_directory_path(owner: type) -> Path:
        """
        Returns path to the directory containing owner class. If owner is not
        a regular file-level defined class, raises `AssertionError`
        """
        owner_module = inspect.getmodule(owner)

        # Sanity check
        if owner_module is None or owner_module.__file__ is None:
            raise AssertionError(f"Given owner class cannot be localized: {owner=}")

        return Path(owner_module.__file__).parent.absolute()

    @staticmethod
    def owner_name(owner: type) -> str:
        return owner.__name__

    @classmethod
    def default_path_for(cls, owner: type) -> Path:
        """
        Returns default relative path for given owner:
        `<owning_class_file_directory>/css/<owning_class_name>.tcss`
        """
        return (
            cls.owner_directory_path(owner)
            .joinpath("css")
            .joinpath(f"{cls.owner_name(owner)}.tcss")
        )

    def get_path_for(self, owner: type) -> Path:
        """
        Gets path for css file assuming that passed owner owns `CssLoader`.
        """
        # If already absolute, return without analysis
        if self.is_path_absolute(self.css_path):
            return self.css_path

        # If not given, return default
        if self.css_path is None:
            return self.default_path_for(owner)

        # Given is relative to the owner
        return self.owner_directory_path(owner).joinpath(self.css_path)

    def fetch_css_for(self, owner: type) -> str:
        """
        Loads and caches css file
        """
        return self.get_path_for(owner).read_text()

    def do_populate(self, owner: type) -> None:
        """
        Set loaded CSS into attribute given by `.populate_into`.
        """
        if self.populate_into is not None:
            setattr(owner, self.populate_into, self.fetch_css_for(owner))

    def __set_name__(self, owner: type, name: str) -> None:
        self.owner = owner
        self.name = name
        self.do_populate(owner)

    # def __get__(self, obj: object | None, owner: type) -> str:
    #     """
    #     Return loaded CSS value
    #     """
    #     return self.fetch_css_for(owner)
