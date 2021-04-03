#!/bin/bash

if [ -z $2 ]; then
  echo "Usage: $0 {{hostname}} {{password}}"
  exit 1
fi

hostname=$1
password=$2
exitcode=10

echo -e "\n\nInitial setup starting... Coffee recommended...\n"

echo -e 'Setting hostname and password'
sudo bash <<SCRIPT
  echo "$hostname" > /etc/hostname
  sed -i -e 's/raspberrypi/$hostname/g' /etc/hosts
  echo -e "$password\n$password" | passwd pi
SCRIPT

echo -e 'Updating system software package lists...'
if sudo apt-get update --yes --quiet 2>&1 | grep -q '^[WE]:'; then
  echo -e '\a\nError encountered running apt-get update; exiting.'
  exit $exitcode
fi
exitcode=$((exitcode+10))

echo -e 'Upgrading system software...'
if sudo apt-get upgrade --yes --quiet 2>&1 | grep -q '^[WE]:'; then
  echo -e '\a\nError encountered running apt-get upgrade; exiting.'
  exit $exitcode
fi
exitcode=$((exitcode+10))

echo -e 'Installing git...'
if sudo apt-get install git --yes --quiet 2>&1 | grep -q '^[WE]:'; then
  echo -e '\a\nError encountered installing git'
  exit $exitcode
fi
exitcode=$((exitcode+10))

echo -e 'Setting our python environment...'
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 1 >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\nError setting default python environment (py2)"
  exit $exitcode
fi
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 2 >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\nError setting default python environment (py3)"
  exit $((exitcode+1))
fi
exitcode=$((exitcode+10))

echo -e 'Getting appliance code...'
cp /boot/git-credentials /home/pi/.git-credentials
cp /boot/gitconfig /home/pi/.gitconfig
repo=$(grep -vE "^\s*#" /boot/repository | tr "\n" " ")
if [ ! -z "{{$repo// }}" ]; then
  git clone $repo ~/appliance >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo -e "\a\nError cloning repository. Run:\n\tgit clone $repo ~/appliance"
    exit $exitcode
  fi
fi
exitcode=$((exitcode+10))

cd ~/appliance
python -m installer
if [ $? -ne 0 ]; then
  exit $exitcode
fi

echo -e '\a\nConfiguration complete.'
echo -e "\nUse:\n\tssh pi@$hostname.local\n from now forward."
echo -e '\nRebooting...\n'
sudo reboot
