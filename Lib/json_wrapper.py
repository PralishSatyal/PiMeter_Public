"""
(C) 2023 Pralish Satyal
21/08/2023
www.pralish.com

A library for json wrapping data

Made by Pralish Satyal
pralishbusiness@gmail.com
"""

# Import relevant libraries and modules
import pandas as pd
import json
import time
import math
from datetime import datetime
from threading import Timer
import os
from Lib.vv_modbus import vvModbus, ModbusRTU, ModbusTCP, minimalmodbus
import glob

# =============================JSON WRAPPER============================  #

class JsonWrapper:
    def __init__(self, station_name, register_file):
        """Initialise the DataProcessing Class"""
        self.station_name = station_name
        self.register_file_location = register_file
        self.new_dat = None

        self.load_config('config/config.json', slave_id = None) # Default no slave id

        self.build_dictionary()


    def load_config(self, filename, slave_id):
        """Load configuration details from file"""
        with open(filename, 'r') as f:
            self.data = json.load(f)
        print(f"The modbus config sent is for {self.data['modbus_type']} communication only")
        print(f"The config file data is {self.data}")

        if self.data['modbus_type'] == 'TCP':
            print("TCP Configuration Loading")
            print("Loading IP Address and slave_id")
            ip_addresses = self.data['ip_address']

            self.slave_id = self.data['slave_ids'][0] # test with one ip

            print(f"The list of ip's in the config file are {ip_addresses}")

            print("Trying to read registers for each IP address")
            print(f"Note that our register file was parsed as {self.register_file_location}")
            for ip_address in ip_addresses:
                print(f"Trying to read IP for {ip_address}")
                self.modbus = ModbusTCP(ip_address, self.register_file_location)

                print("Now trying read_registers function")
                self.modbus.read_registers()

        elif self.data['modbus_type'] == 'RTU':
            print("RTU Configuration Loading")
            print("Loading all necessary variables")
            baudrate = int(self.data['baud rate'])
            bytesize = int(self.data['data bits'])
            stopbits = int(self.data['stop bits'])
            timeout = float(self.data['time out'])
            port = self.data['port']
            slave_id = self.data['slave_ids'][0]  # Setting slave_id from config for RTU

            if self.data['parity'] == 'None':
                parity = minimalmodbus.serial.PARITY_NONE
            elif self.data['parity'] == 'Odd':
                parity = minimalmodbus.serial.PARITY_ODD
            elif self.data['parity'] == 'Even':
                parity = minimalmodbus.serial.PARITY_EVEN
            else:
                print("Invalid parity option read. Please check the Config file")

            # Instantiate RTU Modbus Class
            self.modbus = ModbusRTU(port, slave_id, self.register_file_location, baudrate, bytesize, parity, stopbits, timeout)
            self.modbus.read_multiple_register()

    def build_dictionary(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        dictionary = {
            "ts": timestamp,
            "StationName": self.station_name,
            "values": self.modbus.response,
            "slave_id": self.slave_id
        }

        self.new_dat = json.loads(json.dumps(dictionary, indent = 2))
        print(self.new_dat)
        return self.new_dat

    def write_json(self, data, file_name):
        """
        Write JSON data to a JSON file
        """
        with open(file_name, 'a') as json_file:
            json.dump(data, json_file, indent=2)
            json_file.write('\n')

    @property
    def Res(self):
        print(self.new_dat)
        return self.new_dat
