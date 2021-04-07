import re
import json

from . import *

def edit_params(term):
    def update_secrets_list(term, secrets):
        spacing = ' '*5
        arrow = f" {term.bright_blue}>>  "

        prep_screen(term, "Edit Secret Parameters")
        print("Use ⌃ and ⌄ keys to navigate")
        print("Press ⤶ (Enter) to edit the parameter, or 'R' to remove it.")
        print("Press 'S' to save and exit, or 'X' to exit without saving.")
        print("")

        # Our editable form will be [{key}, {prompt}, {regex}, {value}]
        editable = [[k, v[0], v[1], secrets.get(k)] for k,v in SECRETS_NAMES.items()]

        with term.location():
            for secret in editable:
                print(f"{spacing}{secret[1]}: {secret[3]}")
        line = 0
        while True:
            with term.location():
                echo(f"{arrow}{term.bright_white}{editable[line][1]}: {editable[line][3]}{term.white}")
            with term.cbreak(): key = term.inkey()
            if key.upper() == 'X':
                return False, []

            if key.upper() == 'S':
                return True, editable

            with term.location():
                echo(f"{term.white}{spacing}{editable[line][1]}: {editable[line][3]}")
            if key.upper() == 'R':
                editable[line][3] = ""
                with term.location():
                    echo(f"{term.white}{spacing}{editable[line][1]}: {' '*50}")
            elif key.is_sequence:
                if key.code == term.KEY_DOWN and line < len(editable) - 1:
                    line += 1
                    echo(term.move_down)
                elif key.code == term.KEY_UP and line > 0:
                    line -= 1
                    echo(term.move_up)
                elif key.code == term.KEY_ENTER:
                    error = ""
                    with term.location():
                        # clear
                        echo(f"{arrow}{term.bright_green}{editable[line][1]}: {term.bright_white}{' '*50}")
                    with term.location():
                        echo(f"{arrow}{term.bright_green}{editable[line][1]}: {term.bright_white}")
                        newsecret = input()
                    if newsecret:
                        if re.match(editable[line][2], newsecret):
                            editable[line][3] = newsecret
                        else:
                            error = f" {term.bright_red}Reverted; New Entry Invalid{term.white}"
                    with term.location():
                        echo(f"{term.white}{spacing}{editable[line][1]}: {editable[line][3]}{error}")

    secrets = load_secrets()
    update, newlist = update_secrets_list(term, secrets)
    if update:
        save_secrets({e[0]:e[3] for e in newlist})
