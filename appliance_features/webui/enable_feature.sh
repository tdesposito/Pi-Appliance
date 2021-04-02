#!/bin/bash
#%% Web Interface

echo -e 'Enabling Web Interface...'

if sudo apt-get install lighttpd --yes --quiet | grep -q '^[WE]:'; then
  echo -e "\a\nError installing lighttpd."
  exit 100
fi

sudo lighty-enable-mod cgi >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\a\nError enabling mod-cgi."
  exit 101
fi

sudo bash -c "sed -i 's:^server.document-root\s*=.*:server.document-root = \"/home/pi/appliance/appliance_features/webui/docroot\":' /etc/lighttpd/lighttpd.conf" >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\a\nError setting document root."
  exit 102
fi

sudo bash -c "echo -e '\$HTTP[\"url\"] =~ \"^/cgi-bin/\" {\n\tcgi.assign := ( \".py\" => \"/usr/bin/python3\" )\n}\n' >> /etc/lighttpd/lighttpd.conf" >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\a\nError setting cgi config."
  exit 103
fi

sudo rmdir /usr/lib/cgi-bin >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\a\nError removing existing cgi-bin."
  exit 104
fi

sudo ln -sf /home/pi/appliance/appliance_features/webui/scripts /usr/lib/cgi-bin >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\a\nError linking cgi-bin."
  exit 105
fi

sudo cp /home/pi/appliance/appliance_features/webui/020_lighttpd /etc/sudoers.d/ >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\a\nError creating lighttpd sudoers file."
  exit 106
fi

sudo chmod 0440 /etc/sudoers.d/020_lighttpd >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo -e "\a\nError setting mode on lighttpd sudoers file."
  exit 107
fi
