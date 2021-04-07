from pathlib import Path

import blessed

from . import *
from .app_features import app_features
from .deploy import deploy
from .edit_params import edit_params
from .repo_ops import init_repo, commit_repo, get_uncommitted
from .system_packages import system_packages

if __name__ == '__main__':
    term = blessed.Terminal()
    menu = {}
    if not Path("./.git").is_dir():
        menu['I'] = ["Initialize Repository", init_repo]
    menu.update({
        'P': ["Add/Remove System Packages", system_packages],
        'F': ["Select Appliance Features", app_features],
        'S': ["Edit Secret Parameters", edit_params],
    })
    if Path("./.git").is_dir() and get_uncommitted():
        menu['C'] = ["Commit Updates To Repository", commit_repo]
    menu.update({
        'D': ["Deploy To SD Card", deploy],
    })
    with term.fullscreen():
        do_menu(term, "Main Menu", menu)
