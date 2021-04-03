import json
from pathlib import Path
from urllib.parse import quote

from . import *

def deploy(term):
    prep_screen(term, "Deploy To SD Card")

    config = load_config()
    secrets = load_secrets()

    if len([k for k,v in secrets.items() if v]) != len(secrets):
        print(f"\n{term.bright_red}Error:{term.bright_white} Your secrets are not complete. Can't deploy yet.")
        echo(f"\n{term.bright_blue}Press any key to return to the menu: ")
        with term.cbreak(): term.inkey()
        return

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

        print(f"Writing {term.bright_green}config.json{term.white}...")
        with open(target / "appliance_config.json", 'w', newline="\n") as _:
            json.dump(config, _, indent=4)

        src = Path(__file__).parent.parent / "filesystem" / "boot"
        for f in src.rglob('*'):
            print(f"Copying {term.bright_green}{f.name}{term.white}...")
            with open(f, 'r') as _, open(target / f.name, 'w', newline='\n') as __:
                __.write(str(_.read()).format(**secrets))

        print(f"\n{term.bright_green}Done.{term.white} You may eject the SD card now.")
        print(f"\n{term.bright_blue}Press any key to return to the menu: ")
        with term.cbreak(): term.inkey()
