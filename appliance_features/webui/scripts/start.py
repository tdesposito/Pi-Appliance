#!/usr/bin/python3

from subprocess import run
run('sudo /usr/bin/pkill -t tty1'.split(' '))
pid = None
while not pid:
    pid = str(run(["sudo", "/home/pi/bin/get-pid"], capture_output=True).stdout, 'utf-8').strip()

print('Status: 204 No Content\n')
