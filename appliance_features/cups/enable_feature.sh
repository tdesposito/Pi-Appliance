#!/bin/bash
#%% CUPS

echo -e 'Enabling CUPS...'
sudo apt-get install cups --yes --quiet >/dev/null 2>&1
if [ $? -eq 0 ]; then
  sudo usermod -a -G lpadmin pi
  sudo bash -c "sed -i 's/^Listen localhost/Listen 0.0.0.0/' /etc/cups/cupsd.conf"
  sudo bash -c "sed -i 's/^Browsing .*$/Browsing off/' /etc/cups/cupsd.conf"
  sudo bash -c 'cat <<ENDSCRIPT >> /etc/cups/cupsd.conf
<Location />
  Allow 0.0.0.0/0
</Location>
<Location /admin>
  Allow 0.0.0.0/0
</Location>
<Location /admin/conf>
  Allow 0.0.0.0/0
</Location>
<Location /admin/logs>
  Allow 0.0.0.0/0
</Location>
ENDSCRIPT'
else
  echo -e '\a\nCould not install CUPS'
  exit 100
fi
