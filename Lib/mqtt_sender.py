"""
(C) 2023 Pralish Satyal
New MQTT Library to allow data to be sent to Thingsboard AND Azure
"""

import json
import sys
import time
import paho.mqtt.client as mqtt
import logging

# Enable Logger
logging.basicConfig(level = logging.DEBUG)

# MqttPublisher class for sending data to Broker IoT Hub
class MqttPublisher:
    def __init__(self, JsonWrapper, connection_details_filename):
        """Initialise the MqttPublisher Class"""

        self.load_connection_details(connection_details_filename)

        # Initialise the data converters
        self.JsonWrapper = JsonWrapper
        self.mod_dat = self.JsonWrapper.Res

        print(f"JSON WRAPPER IS {self.JsonWrapper}")

        if self._broker_hostname == "vv-iot-hub.azure-devices.net":
            print("Azure detected, loading certificate")
            self.client = mqtt.Client(client_id= self._client_id)
            self.client.tls_set(r'Lib/Azure_Connection/azure-cert.pem')
            self.client.username_pw_set(str(self._username), str(self._password))

            # Ensure data is JSON wrapped for Azure
            self.telemetry_json = json.dumps(self.mod_dat)
        else:
            print("Thingsboard detected")
            self.client = mqtt.Client()
            self.client.username_pw_set("") #REDACTED

            print("Changing the json wrapped data")
            telemetry_data = self.mod_dat['values']
            self.telemetry_json = json.dumps(telemetry_data)

        # Common client setup
        self.client.connect(self._broker_hostname, int(self._broker_port), 60) # keep alive for 60 seconds
        self.client.enable_logger()


    def load_connection_details(self, filename):
        """Load the connection details from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Initialise variables for connection details
        self._broker_hostname = (data["time_series_conn_info"]["host"])
        self._broker_port = (data["time_series_conn_info"]["port"])
        self._topic = (data["time_series_conn_info"]["topic"])
        self._client_id = (data["time_series_conn_info"]["client_id"])
        self._username = (data["time_series_conn_info"]["username"])
        self._password = (data["time_series_conn_info"]["password"])


    def send_mqtt(self):
        """Send data to MQTT Broker using data from Serial Class"""
        self.client.publish(self._topic, self.telemetry_json, qos=1)
        print(f"Sent Metered data to MQTT Broker: \n{self.telemetry_json}\n\n\n")

    # def send_mqtt(self, device_data):
    #     # if self._broker_hostname == "vv-iot-hub.azure-devices.net":
    #     #     telemetry_json = json.dumps(device_data)
    #     # else:
    #     #     telemetry_data = device_data['values']
    #     #     telemetry_json = json.dumps(telemetry_data)

    #     # self.client.publish(self._topic, telemetry_json, qos=1)
    #     # print(f"Sent Metered data to MQTT Broker: \n{telemetry_json}\n\n\n")



    def start_loop(self):
        """Function to start connection loop"""
        print("Starting loop to send data\n")
        self.client.loop_start()

    def stop_loop(self):
        """Function to stop connection loop"""
        print("\nStopping loop\n")
        sys.exit()
