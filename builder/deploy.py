import json
from pathlib import Path
from urllib.parse import quote

from . import *
from .repo_ops import get_uncommitted

def deploy(term):
    prep_screen(term, "Deploy To SD Card")

    config = load_config()
    secrets = load_secrets()

    if len([k for k,v in secrets.items() if v]) != len(secrets):
        return press_any_key(term, f"\n{term.bright_red}Error:{term.bright_white} Your secrets are not complete. Can't deploy yet.")

    if get_uncommitted():
        print(f"\n{term.bright_yellow}Warning:{term.bright_white} You have un-staged/un-commited changes.{term.white}")
        print(f"\n{term.bright_white}It is {term.on_red}HIGHLY{term.on_black} recommended that you commit before continuing.")
        echo(f"\n{term.bright_blue}Press 'Y' to continue, any other key to go back: ")
        with term.cbreak(): key = term.inkey()
        if key not in 'Yy':
            return
        print("\n")

    target = None
    while True:
        with term.location():
            echo(f"{term.bright_blue}Deploy Location (blank to exit): {' '*50}")
        with term.location():
            echo(f"{term.bright_blue}Deploy Location (blank to exit): {term.bright_white}")
            targetname = input()
            if targetname:
                target = Path(targetname)
                if target.is_dir():
                    break
                else:
                    print(f"\n{term.bright_red}Error: {term.bright_white}'{targetname}' is not a valid location.")
                    print("Please be sure your SD Card is mounted, and you've entered the mount point correctly.")
            else:
                target = None
                break

    if target:
        with term.location():
            print(" "*term.width)
            print(" "*term.width)
            print(" "*term.width)
            print(" "*term.width)
        print(f"{term.bright_green}Deploying to {target} {' '*50}{term.white}\n")

        config.update({'secrets': secrets})
        config['secrets']['git_pwd_quoted'] = quote(secrets['git_pwd'], safe='')

        print(f"Writing {term.bright_green}config file{term.white}...")
        with open(target / "appliance_config.json", 'w', newline="\n") as _:
            json.dump(config, _, indent=4)

        src = Path(__file__).parent.parent / "filesystem" / "boot"
        for f in src.rglob('*'):
            with term.location():
                echo(f"Copying {term.bright_green}{f.name}{term.white}...{' '*term.width}")
            with open(f, 'r') as _, open(target / f.name, 'w', newline='\n') as __:
                __.write(str(_.read()).format(**secrets))

        press_any_key(term, f"\n{term.bright_green}Done.{term.white} You may eject the SD card now.")
