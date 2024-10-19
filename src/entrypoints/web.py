#! /usr/bin/env python3

from pathlib import Path
from typing import Any
from tools import src_ctx
from argparse import ArgumentParser, Namespace
from textual_serve.server import Server


class PathArgument(str):

    @classmethod
    def get_default_app(cls) -> str:
        with src_ctx() as src_path:
            return str(src_path.joinpath("entrypoints").joinpath("tui.py").absolute())

    @classmethod
    def get_path(cls, v: str) -> Path:
        app_path = Path(v)
        # Absolute will inject cwd if string is in relative format
        return app_path.absolute()


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description="""
            This program starts the production server for the Command and control
            textual web interface. Production server is based on textual_serve
            package. It is more or less a UI-to-TUI proxy. All user actions done
            on the browser side are communicated to the textual TUI via websocket
            protocol.

            For each client, separate process is spawned in the host server. Keep
            this in mind as this is a major issue in this server performance.

            I highly recommend to limit maximum number of active connections to the
            main production server process, e.g. through intermediate proxy.
        """,
    )

    # App path
    parser.add_argument(
        "--app",
        action="store",
        default=PathArgument.get_default_app(),
        help=(
            "Path to the TUI application to be served. "
            "When passed as relative, assumes PWD as a relative base. "
            "Defaults to %(default)s"
        ),
        type=PathArgument.get_path,
        dest="app_path",
    )
    # Host
    parser.add_argument(
        "--host",
        action="store",
        default="localhost",
        help="Host address to listen on. Defaults to %(default)s",
        dest="host",
    )
    # Port
    parser.add_argument(
        "--port",
        action="store",
        default=8080,
        help="Host port to listen on. Defaults to %(default)s",
        dest="port",
    )
    # Debug a.k.a verbose
    parser.add_argument(
        "-v",
        "--verbose",
        "--debug",
        action="store_true",
        help="Verbose mode, enables debug logs from the main server process",
        dest="debug",
    )
    return parser.parse_args()


def run_server(
    app_path: Path | None = None,
    host: str = "localhost",
    port: int = 8080,
    title: str = "Command and control",
    statics_path: Path | None = None,
    templates_path: Path | None = None,
    debug: bool = False,
) -> None:
    """
    Create and run server for textual application.

    Args:
        app_path: Path to the executable that runs textual application.
            If not given, defaults to main TUI application:
            `src/entrypoints/tui.py`
        host: Host string on which server should listen
        port: Port on which server should listen
        statics_path: path to the static directory. Defaults to textual_serve.Server
            param default of the same name
        templates_path: path to the templates directory. Defaults to textual_serve.Server
            param default of the same name
        debug: Passing `True` here enabled debug logging from the server process
    """

    # Prepare default args
    default_kwargs: dict[str, Any] = {}
    if statics_path is not None:
        default_kwargs["statics_path"] = str(statics_path)

    if templates_path is not None:
        default_kwargs["templates_path"] = str(templates_path)

    # Prepare command
    command: Path = (
        app_path
        if app_path is not None
        else PathArgument.get_path(PathArgument.get_default_app())
    )

    server = Server(
        command=str(command), host=host, port=port, title=title, **default_kwargs
    )

    server.serve(debug=debug)


def main():
    arguments = parse_arguments()
    run_server(
        app_path=arguments.app_path,
        host=arguments.host,
        port=arguments.port,
        debug=arguments.debug,
    )


if __name__ == "__main__":
    main()
