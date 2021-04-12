# This file is part of Pi-Appliance, Copyright (C) Todd D. Esposito 2021.
# Distributed under the MIT License (see https://opensource.org/licenses/MIT).

# Entry point for the pi appliance

#===============================================================================
#
# NOTE: In general, don't touch this code!
# Appliance logic should be in src/appliance.py
#
#===============================================================================

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
    logger = configure_logger()

    app = Appliance(logger)

    # we exit with these values:
    # - 0: normal exit (usually via SIGINT, but maybe voluntary)
    # - 10: already running (or, at least, pid file exists)
    # - 20: pre_flight_checks failed
    # - 30: unhandled exception
    # NOTE: these aren't currently processed by the framework.
    exitcode = 0
    if lock_pid():
        logger.info("Applicance starting up.")
        if app.pre_flight_checks():
            try:
                logger.info("Appliance running.")
                while app.run():
                    ... # keep on truckin'
                logger.info("Appliance shutting down.")
                app.shutdown()
            except KeyboardInterrupt as e:
                app.shutdown()
                logger.info("SIGINT (Ctrl+C) caught; exiting.")
            except Exception as e:
                logger.error(f"Encountered an unhandled exception: {str(e)}; Exiting.")
                exitcode = 30
        else:
            logger.info("Applicance won't start; Exiting.")
            exitcode = 20
        unlock_pid()
    else:
        print("Applicance seems to be running already; Exiting.")
        exitcode = 10
    sys.exit(exitcode)
