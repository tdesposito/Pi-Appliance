# Builder - common functions
import functools
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "appliance_config.json"
SECRETS_DIR = Path(__file__).parent.parent / 'secrets'
SECRETS_FILE = SECRETS_DIR / 'secrets.json'

echo = functools.partial(print, end='', flush=True)

def do_menu(term, title, menu):
    def draw_menu(term, title, menu):
        prep_screen(term, title)
        for key, item in menu.items():
            print(f"   {key}) {item[0]}")
        print("   x) Exit\n")
        echo(f"{term.bright_blue}Option?{term.white} ")

    draw_menu(term, title, menu)
    while True:
        with term.cbreak(): key = term.inkey()
        if key == 'x' or key == 'X':
            return
        if key.upper() in menu.keys():
            menu[key.upper()][1](term)
            draw_menu(term, title, menu)


def load_config():
    with open(CONFIG_FILE, 'r') as _:
        return json.load(_)


def load_secrets():
    try:
        if SECRETS_FILE.exists():
            with open(SECRETS_FILE, 'r') as _:
                return json.load(_)
    except:
        pass

    return {k:"" for k in SECRETS_NAMES.keys()}


def prep_screen(term, title=None):
    echo(term.home + term.clear)
    print(term.center(f"{term.green}PiAppliance -- Configure and Build{term.white}"))
    if title:
        print(f"\n{term.bright_yellow}{title}{term.white}\n")


def save_config(config):
    with open(CONFIG_FILE, 'w') as _:
        json.dump(config, _, indent=2, sort_keys=True)


def save_secrets(secrets):
    if not SECRETS_DIR.exists():
        SECRETS_DIR.mkdir()
    with open(SECRETS_FILE, 'w') as _:
        json.dump(secrets, _, indent=2, sort_keys=True)


__all__ = [
    "do_menu",
    "echo",
    "load_config",
    "load_secrets",
    "prep_screen",
    "save_config",
    "save_secrets",
]
