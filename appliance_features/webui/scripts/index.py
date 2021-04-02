#!/usr/bin/python3

import os
from subprocess import run

with open('/home/pi/appliance/webui/templates/index.html') as _:
    template = _.read()

def calc_mem():
    try:
        m = str(run(["bash", "-c", "free | grep Mem | awk '{print $3/$2 * 100.0}'"], capture_output=True).stdout, 'utf-8').strip()
        return str(int(round(float(m), 0)))
    except Exception as e:
        return "(unavailable)"

params = {
    'hostname': str(run('hostname', capture_output=True).stdout, 'utf-8').strip(),
    'hostip': str(run(["bash", "-c", "hostname -I | cut -f 1 -d ' '"], capture_output=True).stdout, 'utf-8').strip(),
    'pid': str(run(["sudo", "/home/pi/bin/get-pid"], capture_output=True).stdout, 'utf-8').strip(),
    'diskpct': str(run(["bash", "-c", "df -h --output=pcent / | tail -n 1"], capture_output=True).stdout, 'utf-8').strip(),
    'mempct': calc_mem(),
    'cups_status': 'enabled' if os.path.isfile('/boot/EH_CONFIG/enabled/cups.sh') else 'disabled',
    'vnc_status': 'enabled' if os.path.isfile('/boot/EH_CONFIG/enabled/vnc.sh') else 'disabled',
}
running = bool(params['pid'])
params.update({
    'appliance_status': "Running" if running else "NOT RUNNING",
    'appliance_status_class': "info" if running else "danger",
    'start_status': "disabled" if running else "enabled",
    'stop_status': "enabled" if running else "disabled",
})


body = template.format(**params)

print("Status: 200 OK")
print("Content-Type: text/html; charset=utf-8")
print(f"Content-Length: {len(body)}")
print("")
print(body)
