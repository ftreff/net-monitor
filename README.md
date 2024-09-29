# net-monitor
Internet Monitor &amp; modem/router rebooter

This script was writen for a Raspberry Pi 3, it checks for an internect connection every 10 minutes.
when no internet connections is detected to powers down the usb ports.
the usb port has a plug that goes to a powerstrip control port, that powers the items pluged into the strip when it detects the 5v from the usb port.
when the usb port powers down, the power stip powers down the modem/router.
after 60 seconds it the scrip powers the usb ports on again, powering the modem and router.
The scrips then waits 10 minuts and checks for internet again, it will reboot every 10 min until an internet connection is detected.

the script also checks internet connection ping, upload and download speeds every 60 minutes
It also checks the system cpu useage, load, temp, freq, and memory useage every 60 mintes.

This scrip was created for when my internet would drop out while I was not home and no one was available to reboot the modem.
Eversince I wrote this scipt I have near 100% internet uptime.

I will soon add the full list of hardware/devices I have in use to make this all work.
