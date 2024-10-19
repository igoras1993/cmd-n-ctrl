import sys
from pathlib import Path
from typing import Generator
from contextlib import contextmanager


@contextmanager
def src_ctx() -> Generator[Path, None, None]:
    this_path = Path(__file__).parent.absolute()
    src_path = this_path.parent.parent.absolute()
    src_str_path = str(src_path)

    # Set path
    sys.path.insert(0, src_str_path)
    try:
        yield src_path
    finally:
        # Reset
        try:
            sys.path.remove(src_str_path)
        except ValueError:
            pass
