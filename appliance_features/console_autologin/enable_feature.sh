#!/bin/bash
#%% Console Auto-Login

echo -e 'Enabling Console Auto Login...'
sudo systemctl set-default multi-user.target >/dev/null 2>&1
sudo ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service >/dev/null 2>&1
sudo bash -c 'cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin pi --noclear %I \$TERM
EOF'
