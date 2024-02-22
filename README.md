# Project Prime


This GitHub Repository contains software that can read serial data from the Current Sensor devices, package these into our json format, and send this data to the Azure IOT Hub. Calculations are included to send RMS current values rather than just variable current values. This project has been separated into the following nodes shown below:

| Index|    Task Nodes       |
|-----:|---------------------|
|     1| MQTT Connection     |
|     2| Serial Connection   |
|     3| JSON Wrapping       |



## Node Hierarchy
The MQTT Connection node is present within the python_mqtt.py class. This class handles the connection to Azure, with loop control as well as a method to send data from the Serial Connection class.

The Serial Connection class handles connecting to the 3 separate serial devices in which we obtain our CT Sensor Data. This data is retrieved simultaneously meaning that that the current measurements are obtained at the same time. This data is then packaged within methods in the same class, which is part of the data handling node.



## Installation Instructions and Program Dependencies
Prior to running the software, ensure that you have the Azure Certificate and the Connection Details in their respective folders. Also, ensure that you have the required dependencies/modules to run this software as shown within the Lib/requirements.py file. If you are installing the software from GitHub, ensure you run the requirements.py file via running the following:

```
sudo chmod +x Lib/requirements.sh
sudo Lib/requirements.sh
```

In the case that the requirements Linux does not run, please check the requirements.txt file for details relating to required modules and install these manually.

The program will can be run upon connection, however it can also be run manually via entering the following command via ssh:

```
python main.py
```

## Program Auto-Run on Boot
To ensure that the program runs on boot, please complete the following commands:

```
sudo nano /lib/systemd/system/Prime.service
```

Once you have created your configuration file (that tells systemd what script we want to run and when), we need to fill in the following details into systemd, replacing yours where fit:

```
[Unit]
Description=My Script Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/Prime/Meter_Product/main.py
WorkingDirectory=/home/pi/Prime/Meter_Product/
User=devkit1

[Install]
WantedBy=multi-user.target
```

After this, we need to ensure that the unit file has the highest permission level so that it can run with no errors, via:

```
sudo chmod 644 /lib/systemd/system/Prime.service
```

After defining the unit file, we need to tell the systemd to start the unit file during the boot sequence:
```
sudo systemctl daemon-reload
sudo systemctl enable Prime.service
```
## Program Auto-Connect to OpenVPN on Boot

To ensure that the device auto-connects to the OpenVPN to Azure, please complete the following commands:

```
sudo nano /lib/systemd/system/ovpn.service
```

Once you have created your configuration file (that tells systemd what script we want to run and when), we need to fill in the following details into systemd, replacing yours where fit:

```
[Unit]
Description=My Script Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/home/pi/Prime/Meter_Product/Azure_Connection/ovpn.sh
WorkingDirectory=/home/pi/Prime/Meter_Product/Azure_Connection/
User=devkit1

[Install]
WantedBy=multi-user.target
```

After this, we need to ensure that the unit file has the highest permission level so that it can run with no errors, via:

```
sudo chmod 644 /lib/systemd/system/ovpn.service
```

After defining the unit file, we need to tell the systemd to start the ovpn unit file during the boot sequence:
```
sudo systemctl daemon-reload
sudo systemctl enable ovpn.service
```

Finally, reboot the Pi and you should have a working Prime Device.
```
sudo reboot now
```

If you'd like to check the status of your program or your openvpn service, run:
```
sudo systemctl status Prime.service
sudo systemctl status ovpn.service
```

If the service is running on boot and you'd like to kill the process, use 'htop' to find the PID of the task, then kill it.
```
htop
kill -9 PID
```

Similarly if you'd like to naturally kill the service, you can run the following commands. Ensure you DO NOT kill the ovpn.service as the PI will go offline.
```
sudo systemctl stop Prime.service #kill the process
sudo systemctl status Prime.service #verify that the process is killed
sudo systemctl start Prime.service #ensure that the process is started again
```

To restart the services (which you can do for both the vpn service and the python script), run the following.
```
sudo systemctl restart Prime.service
sudo systemctl restart ovpn.service #this will temperarily disconnect the Pi from the VPN. You will need to re-login to the device.
```

To ensure remote connection, please follow the guide outlined here:
>'https://support.ipvanish.com/hc/en-us/articles/115002080433-OpenVPN-Linux-Command-Line-'

The connection is as follows. There are a total of two open VPN connections, which allow the user's PC to act as a client
in connecting to the Azure VPN Server. The DevKit also acts as a VPN client, connecting to the Azure VPN Server. As both devices will be connected to the same server, it allows the user to SSH into the DevKit device. This means that the user (Pralish) will be able to remotely reboot, or program the device.

## Error Handling

In the case of an error, the program should log the error to a logging file stored under error-log-events/error.log 
This file should contain any errors in the running of this program. You can then diagnose the issue and restart the
script via:
```
sudo systemctl restart Prime.service
```

## Contact
For any more information, please contact Pralish:

pralishbusiness@gmail.com

Embedded Systems
  
## Additional Resources 
Please note that the sources used have been snapshotted manually onto the Internet archive
in the case that the source pages are removed:
>'https://web.archive.org/'

Other sources used:
>'https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/'
>'https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/'
