# This file is part of Pi-Appliance, Copyright (C) Todd D. Esposito 2021.
# Distributed under the MIT License (see https://opensource.org/licenses/MIT).

# Entry point for the pi appliance
#
#===================================================
# In general, don't touch this code!
# Appliance logic should be in src/appliance.py
#===================================================

import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from appliance import Appliance

PIDFILE = '/var/run/user/1000/appliance.pid'
LOGFILE = '/home/pi/log/appliance.log'

def configure_logger():
    logformatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    consolelogger = logging.StreamHandler()
    consolelogger.setFormatter(logformatter)
    filelogger = RotatingFileHandler(LOGFILE, maxBytes=128*1024, backupCount=4)
    filelogger.setFormatter(logformatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(consolelogger)
    logger.addHandler(filelogger)

    return logger

def lock_pid():
    if os.path.isfile(PIDFILE):
        log.error(f"Won't start: {PIDFILE} exists.")
        return False
    try:
        with open(PIDFILE, 'w') as p:
            p.write(str(os.getpid()))
        return True
    except Exception as e:
        log.error(f"Can't write {PIDFILE}; exiting.")
        return False


def unlock_pid():
    os.remove(PIDFILE)


if __name__ == '__main__':
    # we exit with these values:
    # - 0: normal exit (usually via SIGINT)
    # - 1: already running (or, at least, pid file exists)
    # - 2: unhandled exception
    # - Whatever Appliance.run() returns, must be > 10
    logger = configure_logger()

    app = Appliance(logger)

    rval = 1
    if lock_pid():
        logger.info("Applicance starting up.")
        if app.pre_flight_checks():
            try:
                logger.info("Appliance running.")
                while True:
                    rval = app.run()
                    if rval > 10:
                        app.shutdown()
                        logger.info("Appliance voluntarily shutting down.")
                        break
            except KeyboardInterrupt as e:
                logger.info("SIGINT (Ctrl+C) caught; exiting.")
                rval = 0
            except Exception as e:
                logger.error(f"Encountered an unhandled exception: {str(e)}; Exiting.")
                rval = 2
        unlock_pid()
    sys.exit(rval)
