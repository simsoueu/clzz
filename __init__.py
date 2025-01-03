from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from .config_dialog import ConfigDialog
from .manage_dialog import ManageDialog

def on_clzz_config():
    dialog = ConfigDialog()
    dialog.exec()

def on_create_clzz_card():
    on_clzz_config()

def on_manage_clzz():
    dialog = ManageDialog()
    dialog.exec()

action = QAction("Clzz", mw)
action.triggered.connect(on_clzz_config)

# Create sub-menu
clzz_menu = QMenu("Clzz", mw)
clzz_menu.addAction("Create new Clzz card", on_create_clzz_card)
clzz_menu.addAction("Manage Clzz", on_manage_clzz)
action.setMenu(clzz_menu)

mw.form.menuTools.addAction(action)
