#!/usr/bin/python3
from subprocess import run
from time import sleep

run('sudo /home/pi/bin/stop-appliance'.split(' '))
sleep(3)
print('Status: 204 No Content\n')
