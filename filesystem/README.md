# Pi-Appliance `filesystem`

This directory contains source files which get copied onto the Pi during the
_build_ and _initial-setup_ processes.

## `/boot`
Contains the files (and template files) we will copy onto the `/boot` partition
of the Pi's SD Card. This includes the `initial-setup.sh` script you'll use to
bootstrap the appliance.

## `/home/pi`
Contains the files we'll copy into the default user's (`pi`) home directory on
the Pi. These files are copied un-altered. There are template files, under
`/templates`.
