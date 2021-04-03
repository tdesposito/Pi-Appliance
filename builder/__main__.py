import blessed

from . import *

from .app_features import app_features
from .deploy import deploy
from .edit_params import edit_params
# from .repo_ops import init_repo, commit_repo
from .system_packages import system_packages

if __name__ == '__main__':
    term = blessed.Terminal()
    with term.fullscreen():
        do_menu(term, "Main Menu", {
            # 'I': ["Initialize Repository", init_repo],
            'P': ["Add/Remove System Packages", system_packages],
            'F': ["Select Appliance Features", app_features],
            'S': ["Edit Secret Parameters", edit_params],
            # 'C': ["Commit Configuration To Repository", commit_repo],
            'D': ["Deploy To SD Card", deploy],
        })
