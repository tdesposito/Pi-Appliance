from . import *

def system_packages(term):
    def update_package_list(term, packages):
        spacing = ' '*5
        prep_screen(term, "Add/Remove System Packages")
        print("Press 'A' to add a new package.")
        print("Use ⌃ and ⌄ keys to navigate, then press 'R' to (un-)remove a package.")
        print("Press 'S' to save and exit, or 'X' to exit without saving.")
        print("")

        # [0] -> package name, [1] (bool) -> delete?
        pkglist = [[x, False] for x in packages]

        with term.location():
            for pkg in pkglist:
                print(f"{spacing}{pkg[0]}")
        line = 0
        while True:
            if len(pkglist):
                with term.location():
                    if pkglist[line][1]:
                        echo(f" {term.bright_blue}>>  {term.bright_magenta}{pkglist[line][0]}{term.white}")
                    else:
                        echo(f" {term.bright_blue}>>  {term.bright_blue}{pkglist[line][0]}{term.white}")
            with term.cbreak(): key = term.inkey()
            if key.upper() == 'X':
                return False, []

            if key.upper() == 'S':
                return True, [p[0] for p in pkglist if not p[1]]

            if key.upper() == 'R' and len(pkglist):
                pkglist[line][1] = not pkglist[line][1]
            if len(pkglist):
                with term.location():
                    if pkglist[line][1]:
                        echo(f"{spacing}{term.bright_red}{pkglist[line][0]}")
                    else:
                        echo(f"{spacing}{term.white}{pkglist[line][0]}")
            if key.upper() == 'A':
                with term.location():
                    echo(f"{term.move_down(len(pkglist) - line)}{term.green}Add: {term.white}")
                    newpkg = input()
                    echo(f"{term.move_up}{spacing}")
                if newpkg:
                    echo(term.move_down(len(pkglist) - line))
                    line = len(pkglist)
                    pkglist.append([newpkg, False])
            elif key.is_sequence:
                if key.code == term.KEY_DOWN and line < len(pkglist) - 1:
                    line += 1
                    echo(term.move_down)
                elif key.code == term.KEY_UP and line > 0:
                    line -= 1
                    echo(term.move_up)

    config = load_config()
    update, newlist = update_package_list(term, config['system_packages'])
    if update:
        config['system_packages'] = newlist
        save_config(config)
