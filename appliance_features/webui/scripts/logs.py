#!/usr/bin/python3

import os
from subprocess import run

with open('/home/pi/appliance/appliance_features/webui/templates/logs.html') as _:
    template = _.read()

params = {
    'hostname': str(run('hostname', capture_output=True).stdout, 'utf-8'),
    'logs': str(run(["tail", "-n", "20", "/home/pi/log/appliance.log"], capture_output=True).stdout, 'utf-8').strip(),
}

body = template.format(**params)

print("Status: 200 OK")
print("Content-Type: text/html; charset=utf-8")
print(f"Content-Length: {len(body)}")
print("")
print(body)
