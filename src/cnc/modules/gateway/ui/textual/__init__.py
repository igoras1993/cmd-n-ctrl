from plug_in import Hosted
from textual.app import App

from cnc.modules.gateway.ui.textual.host.host import CncHostApp
from cnc.shared.ioc.root import root_router
from cnc.shared.settings.app import AppSettings


@root_router.manage()
def create_textual_app(settings: AppSettings = Hosted()) -> App:
    return CncHostApp()
