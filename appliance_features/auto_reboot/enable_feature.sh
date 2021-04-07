#!/bin/bash
#%% Auto-Reboot the Appliance
#%@ reboot_hour Reboot at Hour (UTC)  [NOT YET IMPLEMENTED]
#%@ reboot_day Reboot on day of the week (0-6 or SUN-SAT)  [NOT YET IMPLEMENTED]
#%< auto_reboot.cron  [NOT YET IMPLEMENTED]

echo -e 'Enabling Auto-Reboot...'
tab="/var/spool/cron/crontabs/pi"
sudo touch $tab
sudo chmod 600 $tab
sudo chown pi:crontab $tab
sudo bash -c "cat </home/pi/appliance_features/auto_reboot/auto_reboot.cron >>$tab"
