"""
(C) 2023 Pralish Satyal
21/08/2023
www.pralish.com

A library for reading modbus data via modbus tcp
and returning this to user

Made by Pralish Satyal
pralishbusiness@gmail.com
"""

import struct
import time
import json
import math
import csv
import pdb 
from datetime import datetime 
from pyModbusTCP.client import ModbusClient
import minimalmodbus


class vvModbus:

    def __init__(self, address, register_file, port = 502, s_id = 255) -> None:
        self.response= {}
        self.registers = []
        self.mod = ModbusClient(host = address, port=port, unit_id= s_id, auto_open=True)

        try:
            print("Reading register file")
            with open(register_file, 'r') as file:
                self.reader = csv.reader(file)
                for i in self.reader:
                    self.registers.append(i)
        except: 
            print('There was an error ')
            pass
    

    def convert_int_float(self, int_list):
        '''Convert s the Modbus response to a float as it returns a
        '''
        float_list = []
        for i in range(0, len(int_list), 2):
            if i + 1 < len(int_list):
                combined_int = (int_list[i] << 16) + int_list[i + 1]
                float_value = struct.unpack('>f', struct.pack('>I', combined_int))[0]  
                float_list.append(float_value)
            else:
                raise ValueError("Invalid input list length. Expected an even number of integers.")
        return float_value
    
    
    def read_registers(self):
        print("Reading registers")
        for register in self.registers :
            Name = register[0]
            hold_register = int(register[3])
            byte_count =  int(register[2])
            self.response[Name] = self.convert_int_float(self.mod.read_holding_registers(hold_register, byte_count))
        return self.response

    
    def read_input_register(self):
        for register in self.registers:
            self.response[register[0]] = self.convert_int_float(self.mod.read_input_registers(int(register[3]), int(register[2])))

            pass
        pass
        return self.response


class ModbusTCP:

    def __init__(self, address, register_file, port=502, s_id=255) -> None:
        self.response = {}
        self.registers = []
        self.mod = ModbusClient(host=str(address), port=port, unit_id=s_id, auto_open=True)

        self._load_register_file(register_file)

    def _load_register_file(self, register_file):
        try:
            print("Reading register file")
            with open(register_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.registers.append(row)
                    print(row)
        except Exception:
            print('There was an error loading the register file')

    def convert_int_to_float(self, int_list):
        """Convert the Modbus response to a float as it returns a list of integers."""
        float_list = []
        for i in range(0, len(int_list), 2):
            if i + 1 < len(int_list):
                combined_int = (int_list[i] << 16) + int_list[i + 1]
                float_value = struct.unpack('>f', struct.pack('>I', combined_int))[0]
                float_list.append(float_value)
            else:
                raise ValueError("Invalid input list length. Expected an even number of integers.")
        return float_list

    def read_registers(self):
        print("Reading registers")
        for register in self.registers:
            name = register[0]
            hold_register = int(register[3])
            byte_count = int(register[2])
            self.response[name] = self.convert_int_to_float(self.mod.read_holding_registers(hold_register, byte_count))
            print(f"Modbus TCP Reading: {self.response[name]}")
        return self.response


    def read_input_register(self):
        for register in self.registers:
            name = register[0]
            hold_register = int(register[3])
            byte_count = int(register[2])
            self.response[name] = self.convert_int_to_float(self.mod.read_input_registers(hold_register, byte_count))
        return self.response


class ModbusRTU:

    def __init__(self, port, slave_address, register_file, baudrate, bytesize, parity, stopbits, timeout):
        self.response = {}
        self.registers = []
        self.sensor = minimalmodbus.Instrument(port, slave_address)

        # Setup sensor parameters
        self._setup_sensor(baudrate, bytesize, parity, stopbits, timeout)

        # Load register file
        self._load_register_file(register_file)

    def _setup_sensor(self, baudrate, bytesize, parity, stopbits, timeout):
        self.sensor.serial.baudrate = baudrate
        self.sensor.serial.bytesize = bytesize
        self.sensor.serial.parity = parity
        self.sensor.serial.stopbits = stopbits
        self.sensor.serial.timeout = timeout
        self.sensor.mode = minimalmodbus.MODE_RTU
        self.sensor.clear_buffers_before_each_transaction = True
        self.sensor.close_port_after_each_call = True

    def _load_register_file(self, register_file):
        try:
            print("Reading register file")
            with open(register_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.registers.append(row)
        except Exception:
            print('There was an error loading the register file')

    def output_setup(self):
        print(self.sensor)

    def convert_data(self, data):
        byte_data = struct.pack('>HH', *data)
        value = struct.unpack('>f', byte_data)[0]
        return value

    def read_single_register(self, register):
        single_data = self.sensor.read_register(int(register), 1, 3, False)
        print(f"Single register data = {single_data}")
        return single_data

    def read_multiple_register(self):
        print("Reading registers from modbus map")
        for register in self.registers:
            name = register[0]
            hold_register = int(register[3])
            byte_count = int(register[2])
            self.response[name] = self.convert_data(self.sensor.read_registers(hold_register, byte_count, 3))
            # print(f"Translated data from device {self.response[name]}")
        return self.response

    def close_serial(self):
        self.sensor.serial.close()
        print("Ports are now closed")
