#!/bin/bash
#%% Auto-Reboot the Appliance
#%@ reboot_hour Reboot at Hour (UTC)
#%@ reboot_day Reboot on day of the week (0-6 or SUN-SAT)
#%< auto-reboot.cron

echo -e 'Enabling Auto-Reboot...'
tab="/var/spool/cron/crontabs/pi"
sudo touch $tab
sudo chmod 600 $tab
sudo chown pi:crontab $tab
sudo bash -c "cat </home/pi/.templatefiles/auto-reboot/auto-reboot.cron >>$tab"
