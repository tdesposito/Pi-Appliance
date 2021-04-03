from pathlib import Path

from . import *

def app_features(term):
    def update_features_list(term, features):
        spacing = ' '*5
        prep_screen(term, "Select Appliance Features")
        print("Use ⌃ and ⌄ keys to navigate, then press ⤶ (Enter) to toggle a feature.")
        print("Press 'S' to save and exit, or 'X' to exit without saving.")
        print("")

        with term.location():
            for feature in features:
                if feature[2]:
                    print(f"{spacing}{term.bright_green}{feature[1]}{term.white}")
                else:
                    print(f"{spacing}{term.bright_red}{feature[1]}{term.white}")
        line = 0
        while True:
            if len(features):
                with term.location():
                    if features[line][2]:
                        echo(f" {term.bright_blue}>>  {term.bright_green}{features[line][1]}{term.white}")
                    else:
                        echo(f" {term.bright_blue}>>  {term.bright_red}{features[line][1]}{term.white}")
            with term.cbreak(): key = term.inkey()
            if len(features):
                with term.location():
                    if features[line][2]:
                        echo(f"{spacing}{term.bright_green}{features[line][1]}{term.white}")
                    else:
                        echo(f"{spacing}{term.bright_red}{features[line][1]}{term.white}")
            if key.upper() == 'X':
                return False, []

            if key.upper() == 'S':
                return True, [p[0] for p in features if p[2]]

            if key.is_sequence:
                if key.code == term.KEY_DOWN and line < len(features) - 1:
                    line += 1
                    echo(term.move_down)
                elif key.code == term.KEY_UP and line > 0:
                    line -= 1
                    echo(term.move_up)
                elif key.code == term.KEY_ENTER:
                    features[line][2] = not features[line][2]

    config = load_config()
    loc = Path(__file__).parent.parent / "appliance_features"
    features = []
    for p in loc.rglob('enable_feature.sh'):
        with open(p, 'r') as _:
            for line in _.read().split("\n"):
                if line.startswith('#%%'):
                    feature = p.parts[-2]
                    features.append([feature, line[4:].strip(), feature in config['appliance_features']])
                    break
    update, newlist = update_features_list(term, features)
    if update:
        config['appliance_features'] = newlist
        save_config(config)
