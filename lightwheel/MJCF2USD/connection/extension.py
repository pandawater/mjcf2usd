import omni.ext
import omni.ui as ui
from .window import MJCF2USDWindow

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MJCF2USDExt(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[MJCF2USD.Ext] startup")

        self._window = MJCF2USDWindow("MJCF2USD", width=500, height=500)


    def on_shutdown(self):
        self._window.destroy()
        print("[MJCF2USD.Ext] shutdown")
