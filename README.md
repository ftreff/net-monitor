# net-monitor
Internet Monitor &amp; modem/router rebooter

This script was writen for a Raspberry Pi 3, it checks for an internect connection every 10 minutes.
If no internet connections is detected to powers down the usb ports.
the usb port has a plug that goes to a powerstrip control port, that powers the items pluged into the strip when it detects the 5v from the usb port.
when the usb port powers down, the power stip powers down the modem/router.
after 60 seconds it the scrip powers the usb ports on again, powering the modem and router.
The scrips then waits 10 minuts and checks for internet again, it will reboot every 10 min until an internet connection is detected.
When an internet connection is deteced it prints a status message confirming internet connection is active, print internet connection uptime, and how long scrip has been running.
Once an hour it prints system stats, and internet download and uploads speeds and ping.

the script also checks internet connection ping, upload and download speeds every 60 minutes
It also checks the system cpu useage, load, temp, freq, and memory useage every 60 mintes.

This scrip was created for when my internet would drop out while I was not home and no one was available to reboot the modem.
Eversince I wrote this scipt I have near 100% internet uptime.

Hardware used with this script:

Raspbarry Pi 3B

![image](https://github.com/user-attachments/assets/82c20307-4aba-4e3a-829b-a06413a2a232)

USB 2.0 A Screw Terminal Block Connector USB 2.0 A Male Plug to 5 Pin/Way Female Bolt Screw Shield Terminals

Amazon - ASIN	B07H53X194

![image](https://github.com/user-attachments/assets/a0ce6af9-efe2-4a3f-8acb-775b1bb92176)

Iot Relay - Enclosed High-Power Power Relay

Amazon - ASIN	B00WV7GMA2

![image](https://github.com/user-attachments/assets/1cff10ca-20e1-472c-be56-b1cac4c1d8dd)
