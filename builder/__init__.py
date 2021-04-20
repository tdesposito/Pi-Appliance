# Builder - common functions
import functools
import json
from pathlib import Path
import subprocess
from urllib.parse import urlparse

CONFIG_FILE = Path(__file__).parent.parent / "appliance_config.json"
SECRETS_DIR = Path(__file__).parent.parent / 'secrets'
SECRETS_FILE = SECRETS_DIR / 'secrets.json'
SECRETS_NAMES = {
    'aws_access_key_id': ('AWS Access Key ID', '[A-Z0-9]{20}'),
    'aws_secret_access_key': ('AWS Secret Access Key', '\S{40}'),
    'region': ('AWS Region', 'us-(east|west)-[1-9]'),
    'git_user': ('Git User Name', '\S{5}'),
    'git_pwd': ('Git Password', '\S{5}'),
    'repo_host': ('Repository Host', '^\S+\.(com|org|net)'),
    'repo_url': ('Repository URL (skip https://)', '^\S+'),
}

echo = functools.partial(print, end='', flush=True)

def do_menu(term, title, menu):
    def draw_menu(term, title, menu):
        prep_screen(term, title)
        for key, item in menu.items():
            print(f"   {key}) {item[0]}")
        print("   x) Exit\n")
        echo(f"{term.bright_blue}Option?{term.white} ")

    with term.fullscreen():
        draw_menu(term, title, menu)
        while True:
            with term.cbreak(): key = term.inkey()
            if key == 'x' or key == 'X':
                return False
            if key.upper() in menu.keys():
                menu[key.upper()][1](term)
                return True # Forces re-build of menu options
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


def press_any_key(term, msg):
    print(msg)
    echo(f"\n{term.bright_blue}Press any key to return to the menu: {term.white}")
    with term.cbreak(): term.inkey()
    return


def runcmd(cmd, params=None):
    c = cmd.split(' ')
    if params:
        c.append(params)
    return subprocess.run(c, capture_output=True)


def save_config(config):
    with open(CONFIG_FILE, 'w') as _:
        json.dump(config, _, indent=2, sort_keys=True)


def save_secrets(secrets):
    if not SECRETS_DIR.exists():
        SECRETS_DIR.mkdir()
    with open(SECRETS_FILE, 'w') as _:
        json.dump(secrets, _, indent=2, sort_keys=True)


def try_command(cmd, error, params=None):
    proc = runcmd(cmd, params)
    if proc.returncode:
        raise Exception(f"{error}: {proc.stderr}")

__all__ = [
    "do_menu",
    "echo",
    "load_config",
    "load_secrets",
    "prep_screen",
    "press_any_key",
    "runcmd",
    "save_config",
    "save_secrets",
    "SECRETS_NAMES",
    "try_command",
]
