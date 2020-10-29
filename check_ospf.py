#!/bin/env python

# To get a logger for the script
import logging
import json
# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie
from genie.abstract import Lookup

# import the genie libs
from genie.libs import ops # noqa

# Get your logger for your script
log = logging.getLogger(__name__)


###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # CommonSetup have subsection.
    # You can have 1 to as many subsection as wanted

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect()
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))

            device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)


###################################################################
#                     TESTCASES SECTION                           #
###################################################################


class OSPF_Information(aetest.Testcase):
    """ This is user Testcases section """

    # First test section
    @ aetest.test
    def learn_ospf(self):
        """ Sample test section. Only print """
        self.all_ospf = {}
        for dev in self.parent.parameters['dev']:
            log.info(banner("Gathering OSPF Information from {}".format(
                dev.name)))
            ospf = dev.learn('ospf')
            ospf.learn()
            if hasattr(ospf, 'info'):
                self.all_ospf[dev.name] = ospf.info
            else:
                self.failed("Failed to learn OSPF info from device %s" % dev.name, 
                            goto=['common_cleanup'])

    @ aetest.test
    def check_ospf(self):
        """ Sample test section. Only print """
        failed_dict = {}
        mega_tabular = []
        for device, ospf in self.all_ospf.items():
            log.info("Device {d} Table:\n".format(d=device))
            log.info(ospf)
        self.passed('OSPF passed')

# #####################################################################
# ####                       COMMON CLEANUP SECTION                 ###
# #####################################################################


# This is how to create a CommonCleanup
# You can have 0 , or 1 CommonCleanup.
# CommonCleanup can be named whatever you want :)
class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    # CommonCleanup follow exactly the same rule as CommonSetup regarding
    # subsection
    # You can have 1 to as many subsections as wanted
    # here is an example of 1 subsection

    @aetest.subsection
    def clean_everything(self):
        """ Common Cleanup Subsection """
        log.info("Aetest Common Cleanup ")


if __name__ == '__main__':  # pragma: no cover
    aetest.main()