#! /usr/bin/env python3

from tools import src_ctx

if __name__ == "__main__":
    with src_ctx():
        import asyncio
        from cnc.config import configure_app
        from cnc.modules.gateway.ui.textual import create_textual_app

        configure_app()
        app = create_textual_app()
        asyncio.run(app.run_async())
