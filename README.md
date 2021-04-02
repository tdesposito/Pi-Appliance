# Pi-Appliance Framework

Pi-Appliance is a Template Repo for building appliances in Python on the
RaspberryPi. We are focused on appliances which connect to various AWS services,
so we assume an AWS environment configuration.

It includes a configuration manager ("builder") to configure and package the
appliance code for your Pi, and an installer ("installer") which bootstraps the
appliance, including installing any features, packages and configuration
settings needed for the appliance's operations.

## Getting Started

1. [Download](https://github.com/tdesposito/Pi-Appliance/archive/refs/heads/release.zip) this repo. You don't want to clone; this is intended to be a _template_, after all.
1. Extract the file to wherever you want to work with it. You'll likely want to extract the top-level folder from the ZIP file into your project directory.
1. Install [Poetry](https://python-poetry.org) is you haven't already.
1. Run `poetry install` to create and populate the Virtual Environment for the project.
1. Write your code. See **Write Your Appliance Code**, below. Write, test, repeat.
1. **COMMIT AND PUSH YOUR CODE**
1. Use the **Builder** (see below) to configure the appliance and write that configuration to your Pi's SD Card.
1. Boot the Pi, run `initial-setup`, rejoice in the magic.

## Write Your Appliance Code
All appliance code goes in the `appliance` folder, in `appliance.py` and any other code files you deem necessary. `appliance.py` contains a skeleton you can use to start your work. See the [appliance README](appliance/README.md) for futher details.

## `builder:` Configure Your Appliance
The `builder` directory contains a Python module which will help you configure the features and requirements of your appliance, thusly:

```console
$ poetry run python -m builder
```
![Builder Main Menu](builder-menu.png)

### Add/Remove System Packages
You can manipulate a list of additional software packages to install during setup of the Pi. These are installed via `apt-get`.

### Select Appliance Features
We include code and configuration to enable (optionally):
* Console Auto-login (if not running a desktop)
* Graphical appliance auto-start (if running a desktop)
* Automatic reboot of the appliance on your schedule
* CUPS print server
* VNC Server (if running a desktop)
* A Web-based User Interface which allows you to monitor, configure and control the appliance
* Automatic update of appliance code (both custom and system) upon appliance startup

### Configure Secrets
Here we collect the various secrets
We store passwords, access keys and other secrets in `./secrets/secrets.json` which is **EXCLUDED FROM VERSION CONTROL BY .`gitignore`**.



### Deploy To SD Card
