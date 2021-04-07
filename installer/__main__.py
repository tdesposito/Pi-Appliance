import json
import sys

from . import *

def install_appliance():
    with open("/boot/appliance_config.json", 'r') as _:
        config = json.load(_)

    install_system_packages(config)
    install_home_directory(config)
    install_features(config)
    install_appliance_requirements(config)
    # run_post_install_tasks(config)

if __name__ == '__main__':
    try:
        install_appliance()
    except Exception as e:
        print(f"\n\nEncountered error '{e}'")
        sys.exit(100)
