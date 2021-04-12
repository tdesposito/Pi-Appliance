# Pi-Appliance Framework

Pi-Appliance is a template for building appliances in Python on the
RaspberryPi. We are focused on appliances which connect to various AWS services,
so we assume an AWS environment configuration.

It includes:
* a configuration manager ("builder") to configure and package the
appliance code for your Pi
* an installer ("installer") which bootstraps the appliance
* a web UI for the appliance
* a minimal framework for building and running your appliance code

## Getting Started

1. [Download](https://github.com/tdesposito/Pi-Appliance/archive/refs/heads/main.zip) this repo. You don't want to clone; this is intended to be a _template_, after all.
1. Extract the file to wherever you want to work with it. You'll likely want to extract the top-level folder from the ZIP file into your project directory.
1. Install [Poetry](https://python-poetry.org) is you haven't already.
1. Run `poetry install` to create and populate the Virtual Environment for the project.
1. Write your code. See **Write Your Appliance Code**, below. Write, test, repeat.
1. Use the **Builder** (see below) to configure the appliance and write that configuration to your Pi's SD Card.
1. Boot the Pi, run `initial-setup`, rejoice in the magic.

## Write Your Appliance Code
All appliance code goes in the `appliance` folder, in `appliance.py` and any
other code files you deem necessary. `appliance.py` contains a skeleton you can
use to start your work. See the [appliance README](appliance/README.md) for
futher details.

## `builder:` Configure Your Appliance
The `builder` module configures the features and requirements of your appliance.

Run it as:
```console
$ poetry run python -m builder
```
Read more in the [builder module](builder/README.md) docs.

## Bootstrapping the Pi
After you've used the `builder` to deploy the bootstrap files to the SD card:

1. Unmount the SD card
1. Install it into the Pi, and boot the Pi
1. (Use `ping raspberrypi.local` to see when it comes on-line)
1. SSH into the Pi using your favorite tool; password defaults to `raspberry`
    * [Putty](https://www.putty.org/) on Windows
    * Command line: `ssh pi@raspberrypi.local`
    * If you're working on your n-th pi, the "raspberrypi.local" host is probably already in your known_hosts file; remove it as needed.
1. Run `bash /boot/initial-setup.sh {new-hostname} {new-password}`
    * Use a *new-hostname* which is NOT already on your network
    * Make sure to note (or use an established pattern for) the *new-password*
1. Take another coffee break while ↑ completes
    * This will clone the repository your appliance code is in. Make sure it's pushed to the remote!
1. Unless there are errors - watch the screen - the Pi will reboot and start running your appliance code

## Automatic Update
Every time the appliance starts up, either due to reboot, or by operation of the
WebUI, the appliance will pull all code updates from the repository's default
branch (whatever you define that as). To update your appliance code, just push
it to the default branch and reload/reboot the appliance.
