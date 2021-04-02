# This file is part of Pi-Appliance, Copyright (C) Todd D. Esposito 2021.
# Distributed under the MIT License (see https://opensource.org/licenses/MIT).

import subprocess
from time import sleep

class Appliance():
    def __init__(self, logger):
        """ Initialize the Appliance.

        :param logger: the system "logger" object.
        """
        self.logger = logger
        # TODO: Add any additional initialization here.

    @staticmethod
    def run_command(cmd):
        """ Run an external shell command

        :param cmd: the command line to run.
        :return: True if the command completed successfully, False otherwise.
        """
        p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        data = p.communicate()
        return p.returncode == 0

    def pre_flight_checks(self):
        """ Validate we are good to start.

        :return: True if we're ready to start; False if not.
        """
        # TODO: Place any system checks here.
        return True

    def run(self):
        """ Run the appliance's function.

        :return: 0 to continue, or something > 10 to signal exit.
        """

        # TODO: Replace this do-nothing code with some which does something.
        # Don't worry about looping (though you can), since this will be called
        # over and over again by the main appliance loop.
        self.logger.info('Nothing to do; sleeping for a while.')
        sleep(10)

        # Return 0 to continue, or something > 10 to signal voluntary exit.
        return 0

    def shutdown(self):
        """ Run any clean up needed.

        :return: Return value doesn't matter; we're done.
        """
        # TODO: Place any cleanup code here.
        return
