#!/bin/bash
#%% VNC Server

echo -e 'Enabling VNC...'
sudo systemctl enable vncserver-x11-serviced >/dev/null 2>&1
if [ $? -eq 0 ]; then
  sudo systemctl start vncserver-x11-serviced >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo -e '\a\nEnabled but could not start VNC server'
  fi
else
  echo -e '\a\nCould not enable VNC server'
  exit 100
fi
