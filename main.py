"""
(C) 2023 Pralish Satyal
21/08/2023
www.pralish.com

A program that reads Modbus Data from any device and sends this to an MQTT Portal IoT portal. 
Current patch is just TCP and Azure but RTU will be worked on and other portals will
be allowed.

Made by Pralish Satyal
pralishbusiness@gmail.com
"""

import sys
import time
from datetime import datetime
import logging
import threading 
import glob
import json

from Lib.json_wrapper import JsonWrapper
from Lib.mqtt_sender import MqttPublisher
from Lib.vv_modbus import vvModbus
from Lib.TimeDifference import DifferenceTime

# Initialise file locations
CONNECTION_FILE = 'Lib/Azure_Connection/connection_details.json'
jw = JsonWrapper('P3133Meter', 'modbus_dir/PM5000-RegistersTest.csv')
mp = MqttPublisher(jw, CONNECTION_FILE)


if __name__ == '__main__':

    # Start the MQTT Connection thread. We want one MQTT Connection thread but multiple messages
    mp.start_loop()
    try:
        while True:
            jw.build_dictionary()
            mp.send_mqtt()
            time.sleep(5)
    except KeyboardInterrupt:
        print('Stopping program')
        mp.stop_loop()
        sys.exit()

