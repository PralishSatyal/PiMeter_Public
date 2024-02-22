VoltVision

Project Voltron Installation Document

A lesson into installing the software required to set-up the Voltron Meter Device

Pralish Satyal


# Project Voltron Installation and Set-up guide. 

Project Voltron Installation and Set-up guide
Contents Page	

- [Document Overview](#Document-Overview)
	- [Additional Information](#Additional-Information)
- [Pre-requisite Steps](#Pre-requisite-Steps)
	- [Installation-of-Raspbian](#Installation-of-Raspbian)
	- [Configuration of Raspberry Pi to read LCL Device](#Configuration-of-Raspberry-Pi-to-read-LCL-Device)
	- [Changing the Configuration File for the LCL Device](#Changing-the-Configuration-File-for-the-LCL-Device)
- [Importing the Voltron Software](#Importing-the-Voltron-Software)
	- [Set-up GitHub and Pull Source Code](#Set-up-GitHub-and-Pull-Source-Code)
	- [Include Additional Files, Software Structure](#Include-Additional-Files,-Software-Structure)
	- [Install required dependencies](#Install-required-dependencies)
- [Set-up systemd services](#Set-up-systemd-services)
	- [Python Script on boot](#Python-Script-on-boot)
	- [OVPN Script on boot](#OVPN-Script-on-boot)
- [Restricting IP Addresses](#Restricting-IP-Addresses)
	- [How to restrict IP access](#How-to-restrict-IP-access)
	- [FAQ/Error Handling in Firewall Process](#FAQ/Error-Handling-in-Firewall-Process)
	- [Block Wi-Fi Access](#Block-Wi-Fi-Access)
- [Useful Commands to Help you](#Useful-Commands-to-Help-you)
	- [Check CPU Temperature](#Check-CPU-Temperature)
	- [Check Active/Running Processes](#Check-Active/Running-Processes)
		- [Check Log File in case of error](#Check-Log-File-in-case-of-error)
	- [Other useful System commands](#Check-Log-File-in-case-of-error)
- [Additional Comments](#Check-Log-File-in-case-of-error)
	- [Software Development](#Software-Development)
	- [Hardware Development](#Hardware-Development)
- [References](#References)



 

## Document-Overview

This document outlines how to set-up a Raspberry Pi 4 to make a Voltron Meter device. The instructions cover how to set up the Pi with the VoltVision software to read data from the LCL device. Additional instructions are included to cover the secure connection details, and on how to make the device more cyber secure. This document also covers how to ensure that the device is working properly and what to do if something goes wrong.

### Additional-Information

Project Voltron faces continuous development which means that the information in this document may be out of date. To reduce the impact of having out-of-date information, this document will be continuously updated with new information for each production level ready Voltron Software.  For any additional information, clarification or issues which need resolution, please contact Pralish via the contact information above.

In this current release, we are using the 4CT3V1T LCL device, although work will be done in the future to create our own device. If the data is parsed in the same format, it can be used with Voltron Software. The current version of the software at the time of writing is v0.4.2.1.


## Pre-requisite-Steps

Prior to installing the Voltron Software on the Pi, we need to configure the Raspberry Pi device so that it can read data from the LCL device, meaning that only the Pi will require setting up. The LeChacal device comes pre-loaded with the program on-board, however if this is not the case we will need to manually install the program for the LCL board. For additional information, we can check the LeChacal website. [1]

### Installation-of-Raspbian

To install Raspbian for the Raspberry Pi, we can use the imager and parse in the following details. As the software for Voltron is just CLI based, we only need to select the Raspberry Pi OS Lite 32-bit version (this is also incredibly lightweight).

Set the hostname to something useful (keep a note of this as we can connect to the Pi via this hostname). Add in a username and password, keeping note of your details. As we configure the pi, we add our Wi-Fi connection details too. Later we will be disabling Wi-Fi access and only using ethernet connection.

![Graphical user interface, application, TeamsDescription automatically generated](file:///C:/Users/rober/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png)

Figure 1- A snapshot showing the Raspberry Pi Imager dashboard

  

### Configuration-of-Raspberry-Pi-to-read-LCL-Device

1. Connect to the Raspberry Pi via SSH on an IDE of your choice. I would personally recommend Visual Studio Code, although if you’re weird you can just use putty. Use the details that you used for setup. For any further information, please check the LeChacal Wiki. [2]

2. Run the raspi-config tool and enable serial port hardware access.

```sh
sudo raspi-config
```

Then disable the login uart

```sh
3 Interface Options     <<-- Use option _5 Interfacing Options_ instead if using the image before 12 DEC 2020

P6 Serial
```

**Would you like a login shell to be accessible over serial?**  
Select **No** to the login shell question.

**Would you like the serial port hardware to be enabled?**  
Select **Yes** to the serial port hardware to be enabled question.

Select **Ok** at the summary.

Back at the menu select **finish**.

**Would you like to reboot now?**  
Select **No** to the reboot question (we will do that later).

3. Edit the /boot/config.txt file to disable Bluetooth overlay as this interferes with the serial connection access. If we want Bluetooth access to the Raspberry PI, we don’t need to do step 4 (however this means that our serial device will appear as ttyS0 rather than ttyAMA0).

```sh
sudo nano /boot/config.txt
```

At the end of the file add the following line:
```
dtoverlay=disable-bt
```
Enter the line exactly as it is show above without adding whitespaces.

Save and Exit the file.

4.[OPTIONAL] Disable other related services
```
sudo systemctl disable hciuart
```
5. Reboot the Pi to ensure that the changes can take into effect.

sudo reboot & exit

Return to the ssh session again once the raspberry pi is up and running again.

  

6. Insert the RPICT board on the RPI. Configure and read from serial port
```
stty -echo -F /dev/ttyAMA0 raw speed 38400

cat /dev/ttyAMA0
```
At that point, the data will be shown on the terminal, as shown in Figure 2.

![[2 - LCL Serial Communication.png]]

Figure 2- A snapshot showing the terminal output from the LCL serial device

  
Note. Once step number 7 below completed you will be able to run these two commands using lcl-run.
```sh
lcl-run
```
It might be useful to get the board with all utilities ready at this point. Just issue the commands below to install them.

7. Install python3-serial
```
sudo apt-get install python3-serial
```
  

### Changing-the-Configuration-File-for-the-LCL-Device

Once the Raspberry Pi has been configured and is able to correctly read data from the serial port, it may be useful to configure the LCL device to get the correct polling rate that we want. The polling rate on this device can be anything >1000ms, as this can then be constrained within the Voltron software afterwards. If the configuration file is not present, we can manually install the configuration set-up via the commands shown below. [3]

1. Install the configuration utility:
```sh
wget lechacal.com/RPICT/tools/lcl-rpict-package_latest.deb

sudo dpkg -i lcl-rpict-package_latest.deb
```
2. Run the configuration utility to copy the contents within the eeprom to a local file:
```sh
lcl-rpict-config.py -a
```
3. Edit the file using the nano text editor, changing parameter values to what you want:
```
nano /tmp/rpict.conf
```
4. Update the configuration file stored within the EEPROM (and update the LCL program)
```sh
lcl-rpict-config.py -a -w /tmp/rpict.conf
```
For your specific configuration file, we can install the specific package using the Hardware key obtained when you purchased the product. This hardware key is unique, and includes a unique configuration that was done by LCL for your application:
```sh
wget lechacal.com/hardware/c/XXXX.conf
lcl-rpict-config.py -w XXXX.conf
```

For the CT4W3T1 Device, we can follow the general commands of:
```sh
wget lechacal.com/RPICT/sketch/RPICT4W3T1_v4.0.2.ino.hex

lcl-upload-sketch.sh RPICT4W3T1_v4.0.2.ino.hex
```
If you would prefer an online configuration tool, you can start a server instance on the Raspberry Pi by running:

lcl-server.sh

In the case that running the lcl-rpict-config.py does not correctly restart the LCL device, simply press the BOOTSEL button on the device.  

## 3.0 Importing-the-Voltron-Software

To import the Voltron software onto the Raspberry Pi device, we need to pull the source code from GitHub. The VoltVisionGithub account contains the source code to run Voltron, however as stated within the README file, there are some secure documents and folders that will manually need to be entered in regarding connection to Azure.

The README file contains information regarding the software structure and the purpose of each node. It is recommended to read this prior to these instructions.

### Set-up-GitHub-and-Pull-Source-Code

Ensure that you have GitHub installed on your Pi device. Run the installation script for the required dependencies to do this (step 3.2). After this, configure your GitHub Account via running the instructions from the source here. [4]

Please note that you can only pull the source code if you have the invite link, or if you are on the VoltVisionGithub account. Once you are logged in, you can pull the code via running:
```sh
git clone https::/github.com/VoltVisionGithub/Voltron.git
```
You will be required to enter your username and password. Please note that you may have to use a Personal Access Token rather than your password in logging in to GitHub. [5]

### Include-Additional-Files,-Software-Structure

The software for the Meter is under the Meter_Product/ directory.
![[3 - File Structure.png]]

Figure 3- A screenshot showing the required file hierarchy for Running the Voltron Software

Figure 3 shows the directory structure within the parent GitHub folder ‘Voltron.’ This structure will be different to yours as you need to manually parse in the connection details and open VPN connection script to the Azure_Connection/ directory. This data is currently stored on a secure hard drive and will need manual transfer, however, plans to make this more efficient are in progress.

Aside from the program files, you may not have an error.log file (as the program has not been run yet).

Ensure you copy over the following files:

1. azure-cert.pem – The certificate your device needs to connect to Azure via MQTT.

2. connection_details.json – A json file that has connection details to be read when connecting the Pi to Azure via MQTT.

3. xyz.ovpn – The OpenVPN file used to configure the devices connection so it is connected to Azure.

4. ovpn.sh – The script to start the OpenVPN connection to Azure when device is booted up.

### Install-required-dependencies

Using either the requirements.sh file or the requirements.txt file, we can install all relevant dependencies for the Voltron Meter Device.

To do this:

1. Navigate to the Lib folder:
```sh
cd /Voltron/Meter_Product/Lib 
```
2. Install all dependencies
```sh
sudo chmod +x Lib/requirements.sh
./requirements.sh
```

If you are interested in which version each python package is, you can read the ‘requirements.txt’ file. Once you have run the installation script, the Raspberry Pi device will reboot, and you will be prompted to login again. For this, you can run:
```sh
pip install requirements.txt
```
  

## Set-up-systemd-services

This section explores how to set-up systemd services regarding starting the OpenVPN connection and the main program as soon as the Pi is booted. This is useful as it means that the device can be plug and play, with minimal need for a user/client to set anything up. If the device goes offline, it can be power cycled as this means that the scripts can be simply restarted.

### Python-Script-on-boot

The python script will need to be started on boot so that data can be sent to Azure as soon as the device is plugged in. This can be done by completing the following commands. [6]

First, create your service file.
```
sudo nano /lib/system/system/voltron.service
```
Once the service file has been created, we need to tell systemd what script we want to run on boot. When the above command has been run, fill it in with the following information with whatever description/details are relevant for you (you may need to change the directory, or the user based on how you configured your device).
```
[Unit]

Description=My Script Service

After=multi-user.target

[Service]

Type=idle

ExecStart=/usr/bin/python /home/pi/Voltron/Meter_Product/main.py

WorkingDirectory=/home/pi/Voltron/Meter_Product/

User=devkit1

[Install]

WantedBy=multi-user.target

After this, we need to ensure that the unit file has the highest permission level so that it can run with no errors, via the command below. [7]

sudo chmod 644 /lib/system/system/voltron.service 

After defining the unit file, we need to tell the systemd to start the unit file during the boot sequence:

sudo systemctl daemon – reload

sudo systemctl enable voltron.service 

  
```

### How-to-restrict-IP-access

To ensure that the device auto-connects to the OpenVPN to Azure, please complete the following commands:
```sh
sudo nano /lib/system/system/ovpn.service
```
Once you have created your configuration file (that tells systemd what script we want to run and when), we need to fill in the following details into systemd, replacing yours where fit:
```
[Unit]

Description=My Script Service

After=multi-user.target

[Service]

Type=idle

ExecStart=/home/pi/Voltron/Meter_Product/Azure_Connection/ovpn.sh

WorkingDirectory=/home/pi/Voltron/Meter_Product/Azure_Connection/

User=devkit1

[Install]

WantedBy=multi-user.target
```
After this, we need to ensure that the unit file has the highest permission level so that it can run with no errors, via:
```sh
sudo chmod 644 /lib/system/system/ovpn.service 
```
After defining the unit file, we need to tell the systemd to start the unit file during the boot sequence:
```sh
sudo systemctl daemon – reload

sudo systemctl enable ovpn.service

sudo reboot now 
```
How do we see if the two scripts have loaded correctly and are running?
```sh
sudo systemctl status voltron.service 

sudo systemctl status ovpn.service
```
If the python script runs correctly, you will see something like in Figure 4.

![alt text](4 - Status of Voltron.png)



Figure 4- A snapshot the status of voltron.service

If the OpenVPN script runs correctly, you will see something like the following:
![[5 - Ovpn Service.png]]

![TextDescription automatically generated](file:///C:/Users/rober/AppData/Local/Temp/msohtmlclip1/01/clip_image009.png)

Figure 5- A snapshot showing the status of ovpn.service

If the service is running on boot and you would like to kill the process, you can either kill it via the kill command (provided you can find the PID from the above commands), or you can stop and restart the services:
```sh
kill -9 PID

sudo systemctl stop voltron.service 

sudo systemctl start voltron.service

sudo systemctl restart voltron.service #this stops and starts in one command
```
**BE CAREFUL IF YOU ARE TRYING TO RESTART THE VPN. IF YOU HAVE A DEVICE AT A REMOTE LOCATION AND STOP THE VPN RATHER THAN RESTARTING THE SERVICE, YOU WILL LOSE CONNECTION AND WILL HAVE TO POWER CYCLE IT MANUALLY.**

To configure OpenVPN and select a correct profile, please follow the guide outlined in reference. [8]

## Restricting-IP-Addresses

To increase the cybersecurity of the device, we will need to restrict the devices that can connect via SSH through both disabling the Wi-Fi (meaning the only connection is via ethernet), and through only allow IP’s within the range of that on the Azure IoT Hub. This ensures that only users with a VPN connection to Azure can access the Pi. [9]

### How-to-restrict-IP-access
```sh
sudo ufw allow from 10.12.0.0/24 to any port 22 proto tcp

sudo ufw default deny incoming

sudo ufw default allow outgoing

sudo ufw enable

sudo reboot
```

If you want to see what IP rules you have (to only allow connections from 10.12.0.X), run the following commands:
```sh
sudo ufw status verbose

sudo ufw show added
```
The first command should show you something like this, where you only have two IPS for incoming and outgoing access:

![[6 - Status of Firewall.png]]

Figure 6- A snapshot showing the status of the Uncomplicated Firewall in detail

The second command shows you the rules you have added, you should only see two rules as shown below:
![[7 - Firewall Rules.png]]

Figure 7- A snapshot listing firewall rules that have been added since last UFW reset/enabling period

If this is not the case and you have multiple rules, you can remove them through running the following commands:
```sh
sudo ufw delete x

sudo ufw delete 
```

After this, ensure you reload the firewall through running:
```sh
sudo ufw reload
```
To ensure that this has worked (while it should be instant), you can reboot the Pi. Please note that if you do this, you will need to connect via the IP address assigned on the Azure IoT Hub. Please keep a note of this, this should be with the 10.12.0. prefix.

You can still use Visual Studio code, but the hostname will no longer be accessible for connection. You also won’t be able to connect via the local IP address.

### FAQ/Error-Handling-in-Firewall-Process

In the case that the firewall settings have been incorrectly set-up and you have locked yourself out of the Raspberry Pi, you will need to plug in a keyboard and mouse to re-login to the Device. Therefore, you will **only** want to mess with the firewall/IP address restrictions prior to sending out the device to a client. After this, you are likely to never come across this setting again.

### Block-Wi-Fi-Access

To ensure that the only connection the Pi has to the internet is via the Ethernet connection, we can disable the Wi-Fi from the Pi by completing the following commands.
```sh
sudo apt install rfkill

sudo rfkill block wifi
```

#if we want to unblock wifi
```sh
sudo rfkill unblock wifi 
```
  

## Useful-Commands-to-Help-you

The commands listed below are incredibly useful for if you have an issue with the device, get locked out or something goes awry. Of course, as this project progresses the list will keep growing larger and larger.

### Check-CPU-Temperature

To check the CPU temperature, simply query the on-board temperature sensor via:
```
vcgencmd measure_temp
```
If you’d like to track the temperature every second and get live updates, you can watch the command via the following command:

watch -n 1 vcgencmd measure_temp

### Check-Active/Running-Processes

To see all running processes with a graphical utility, you can run either command:
```
htop

top
```
If you’re wondering about the status of your startup scripts, you can also run
```sh 
systemctl status voltron.service

systemctl status ovpn.service
```
### Check-Log-File-in-case-of-error

If an error has occurred and data is not being sent to Azure, you will need to restart the python script. You will need to check that the scripts are running or if a failure is present. After this you will need to read the log-file which should include the error along with the timestamp at which this occurred.

Once you have fixed the issue/debugged, you can restart and reload the program script via the following commands:
```sh
systemctl status voltron.service

sudo restart voltron.service

systemctl status voltron.service
```
### Other-useful-System-commands

There are a lot of commands that are incredibly useful when configuring or working with the Voltron Meter Device. You can get information regarding what each command does below by running ‘man command’.

#### Systemctl/Systemd-commands

##### Manuals 
```
man systemd

man systemctl
```

```sh
systemctl list-units --type=service # lists all systemd processes

systemctl status ssh.service # outputs verbose information of processes

systemctl list-units –type=service –state=active #list active systemd services
```
As well as starting, stopping, restarting, and reloading system processes, we can use journalctl to see continuous data regarding the system processes. This can be an incredibly useful tool if you have had a failure in the script and want to monitor the process over an extended period to see if it works.

#### - commands
```sh
journalctl -f -u voltron.service # get data from process every 25s

# get data every second of the output from the voltron.service

while true; do sudo journalctl --since "1 second ago" -u voltron.service; sleep 1; done 
```
#### Network-utility-commands
```sh
ifconfig #shows details of device connection

arp -a #lists everything device can see on network

ping xx.xx.x #pings an IP address
```

#### Serial-connection-commands
```sh
dmesg | grep tty #list all tty devices connected

lsusb #list any usb connections
```
#### System-commands
```sh
whoami #outputs which user is connected

sudo reboot now #reboots the device immediately

  
```

## Additional-Comments

While this project is one that will always be in continuous development, I must bring attention to a few things. The comments below are for if you wish to develop this project in the future.

### Software-Development

This project has taken quite a while with regards to developing software to run successfully on the Pi. If you are developing this Project, please add modules or edits rather than changing the whole framework as this task could take a long time and would render all this redundant.

Please try follow PEP8 guidelines with regards to your structure and commenting style, however if you are in doubt please read the latest Project Proposal document as this highlights how I call each feature update.

A lot of the software has been released in the form of v0.x.y where the number after the ‘v’ indicates whether it is a production ready piece or not (the first main updates were non-production ready). Information regarding the naming convention I have followed is found in the New Direction Project Proposal document.

### Hardware-Development

The most recent hardware configuration includes the use of a LeChacal 4CT 3 Voltage (1 temperature) device which is mounted on top of the Raspberry Pi device. For a final version, we could create our own PCB’s. However, I strongly believe that we should make one fully functional MVP before considering this (or at least do this in parallel).

A bumper/MVP case is in production and being designed by Pralish. A case is also being designed for the Raspberry PI device with collaboration between Robbie and Pralish. When the Meter device is mounted into the case, with the case being mounted into a testing box, we will be able to test our first MVP device.

## 8.0 References

[1] Lechacal. (2023, Mar. 23).  _Raspberrypi Current and Temperature Sensor Adaptor_ [Online]. Available: [http://lechacal.com/wiki/index.php/Raspberrypi_Current_and_Temperature_Sensor_Adaptor](http://lechacal.com/wiki/index.php/Raspberrypi_Current_and_Temperature_Sensor_Adaptor)

[2] Lechacal. (2023, Mar. 9). _Howto setup Raspbian for serial read_ [Online]. Available:  [http://lechacal.com/wiki/index.php?title=Howto_setup_Raspbian_for_serial_read](http://lechacal.com/wiki/index.php?title=Howto_setup_Raspbian_for_serial_read)

[3] Lechacal. (2023, Feb. 11). _First Configuration RPICT_ [Online]. Available: [http://lechacal.com/wiki/index.php?title=First_Configuration_RPICT](http://lechacal.com/wiki/index.php?title=First_Configuration_RPICT)

[4] Cartwrightraspberrypiprojects. _Github Tutorial_ [Online]. Available: [https://sites.google.com/site/cartwrightraspberrypiprojects/home/ramblings/tutorials/using-github](https://sites.google.com/site/cartwrightraspberrypiprojects/home/ramblings/tutorials/using-github)  

[5] VoltVision. (2023,  Mar. 23). _Project Voltron GitHub Page_ [Online]. Available: [https://github.com/VoltVisionGithub/Voltron](https://github.com/VoltVisionGithub/Voltron)

[6] RPiSpy. (2015, Oct. 12). _How to Autorun A Python Script On Boot Using systemd_ [Online]. Available: [https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/](https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/)

[7] Dexter Industries. (2023). _Five Ways To Run a Program On Your Raspberry Pi at Startup_ [Online]. Available: [https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)

[8] IPVanish. (2023, Feb.). _OpenVPN: Linux Command-Line_ [Online]. Available:[https://support.ipvanish.com/hc/en-us/articles/115002080433-OpenVPN-Linux-Command-Line-](https://support.ipvanish.com/hc/en-us/articles/115002080433-OpenVPN-Linux-Command-Line-)

[9] PiMyLifeUp. (2022, Jan. 30). _How to Disable your Raspberry Pi’s Wi-Fi_ [Online]. Available: [https://pimylifeup.com/raspberry-pi-disable-wifi/](https://pimylifeup.com/raspberry-pi-disable-wifi/)

[10] Internet Archive. (2023). [Online]. Available: [https://web.archive.org/](https://web.archive.org/)

**Addendum**

Please note that the sources used have been snapshotted manually onto the Internet archive in the case that the source pages are removed. [10]
