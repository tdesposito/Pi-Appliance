from pathlib import Path
from subprocess import run

__version__ = "0.1.0"

def install_appliance_requirements(config):
    print("Installing Appliance Requirements...")
    runcmd("python -m pip install /home/pi/appliance/requirements.txt")


def install_features(config):
    print("Installing Appliance Features...")
    for feature in config['appliance_features']:
        # TODO: if the feature has parameters to set, handle it.
        runcmd(f"bash /home/pi/appliance/appliance_features/{feature}/enable_feature.sh")


def install_home_directory(config):
    def copytree(src, dest, tplvars):
        for entry in src.glob('*'):
            t = dest / entry.name
            if entry.is_dir():
                t.mkdir()
                copytree(entry, t)
            else:
                with open(entry, 'rb') as _, open(t, 'wb') as __:
                    if tplvars:
                        __.write(str(_.read(), 'utf-8').format(**tplvars))
                    else:
                        __.write(_.read())

    print("Installing home directory...")
    dest = Path("/home/pi")

    copytree(Path("/home/pi/appliance/filesystem/home/pi"), dest)
    copytree(Path("/home/pi/appliance/templates"), dest, config['secrets'])

    for entry in (dest / "bin").glob(*):
        entry.chmod (0o744)


def install_system_packages(config):
    print("Installing System Packages...")
    for pkg in config.get('system_packages'):
        runcmd(f"sudo apt-get install {pkg} --yes --quiet")


def runcmd(cmd):
    # Will throw if the command fails, to be caught by __main__
    run(cmd.split(' '), capture_output=True, check=True)


__all__ = [
    "install_appliance_requirements",
    "install_features",
    "install_home_directory",
    "install_system_packages",
]
