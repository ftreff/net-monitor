#!/usr/bin/env python3
#uhubctl is required to run this scrip, this is what powers the usb port on and off to signal the powerstrip to turn on and off.
#        This reboots the modem and/or router depending on your setup and useage needs.

#Change Log
#v1      code based on internet example and edited
#v1.1    added log file
#v1.2    added time stamp
#v2      entire code rewritten from scratch
#v2.1    overhauled print & log messages, and added color
#v2.2    added loop counter, runtimer, and conectivity timer, fix logfile status spacing, added divider to log when program is launched, fixed timer/counter from starting at 10 min
#v2.3    added CPU status mssage woth cpt usage, temp, freq, load adverage, mem usage, displayed at launch, and onc eevery 60min
#v2.4    edited log messages, fixed spacing
#v2.5    added speedtest info. 9-29-24
#               (" git clone https://github.com/sivel/speedtest-cli.git" is now required to be installed prior to this scrip running.
#
#planned updates     adding key press commands, insant internet check, system status, print timers and counters, manual modem reboot, exit

import os
import subprocess
import requests
import time
from datetime import datetime
import psutil

rcounter = 0
icounter = 0

print("FTreff's Modem Rebooter if Internet Connection Drops")
print("██████╗ ██████╗ ██████╗       ██╗███╗   ██╗████████╗")
print("██╔══██╗██╔══██╗╚════██╗      ██║████╗  ██║╚══██╔══╝")
print("██████╔╝██████╔╝ █████╔╝█████╗██║██╔██╗ ██║   ██║")
print("██╔══██╗██╔═══╝  ╚═══██╗╚════╝██║██║╚██╗██║   ██║")
print("██║  ██║██║     ██████╔╝      ██║██║ ╚████║   ██║")
print("╚═╝  ╚═╝╚═╝     ╚═════╝       ╚═╝╚═╝  ╚═══╝   ╚═╝")
print("Raspberry Pi 3 - Internet Checking Modem Rebooter")
print("\033[1;33;40m        You'll never be offline again!\033[0m")
print("                  VERSION 2.5")
print("By:")
print("\033[1;32;40m ▄▄████▒▄▄██████▓ ██▀███  ▓█████   █████▒ █████▒")
print("▓██   ▒ ▓  ██▒ ▓▒▓██ ▒ ██▒▓█   ▀ ▓██   ▒▓██   ▒")
print("▒████ ░ ▒ ▓██░ ▒░▓██ ░▄█ ▒▒███   ▒████ ░▒████ ░")
print("░▓█▒  ░ ░ ▓██▓ ░ ▒██▀▀█▄  ▒▓█  ▄ ░▓█▒  ░░▓█▒  ░")
print("░▒█░ ██   ▒██▒ ░ ░██▓ ▒██▒░▒████▒░▒█░   ░▒█░")
print(" ▒ ░      ▒ ░░   ░ ▒▓ ░▒▓░░░ ▒░ ░ ▒ ░    ▒ ░")
print(" ░          ░      ░▒ ░ ▒░ ░ ░  ░ ░      ░")
print(" ░ ░      ░        ░░   ░    ░    ░ ░    ░ ░")
print("                    ░        ░  ░\033[0m 9/29/2024")
print("\033[0m\n")
print("")
print("Current Version is in testing with ASUS Router DHCP Continuous Mode")
time.sleep(1)
print("")

def convert_sec_to_time(seconds):
    # Calculate days and remaining seconds
    days, seconds = divmod(seconds, 86400)
    # Calculate hours and remaining seconds
    hours, seconds = divmod(seconds, 3600)
    # Calculate minutes and remaining seconds
    minutes, seconds = divmod(seconds, 60)
    # Return time in DD:HH:MM format
    return f"{int(days):02d}:{int(hours):02d}:{int(minutes):02d}"

def check_internet_connection():
    try:
        req = requests.get("http://clients3.google.com/generate_204")
        if req.status_code == 204:
            # Run code here when there is an internet connection
            global rcounter
            global icounter
            RCounterSEC = rcounter * 600
            ICounterSEC = icounter * 600
            rtime = convert_sec_to_time(RCounterSEC)
            itime = convert_sec_to_time(ICounterSEC)
            print_ts(f"\033[1;44;37m Internet \033[m\033[32m   Connected\033[m\033[1;30m      ({rcounter}/{icounter})   Runtime {rtime} / Uptime {itime}\033[m")
            log_message(f"[Internet]   Connected      ({rcounter}/{icounter})   Runtime {rtime} / Uptime {itime}")
            if rcounter % 6 == 0:
                time.sleep(.1)
                # Run speedtest-cli and capture the output
                result = subprocess.run(['speedtest-cli', '--simple'], capture_output=True, text=True)
                time.sleep(.1)
                # Check if the command was successful
                if result.returncode == 0:
                    # Parse the output
                    output_lines = result.stdout.splitlines()
                    download_speed = float(output_lines[0].split(' ')[1])
                    upload_speed = float(output_lines[1].split(' ')[1])
                    ping = float(output_lines[2].split(' ')[1])

                    # Print the results
                    print_ts(f"\033[1;44;37m Internet \033[0m  \033[35m Speed Test    \033[33m Download: {download_speed} Mbps  /  Upload: {upload_speed} Mbps  /  Ping: {ping} ms\033[m")
                    log_message(f"[Internet]   Speed Test      Download: {download_speed} Mbps / Upload: {upload_speed} Mbps / Ping: {ping}")
                    #print(f"Download: {download_speed} Mbps")
                    #print(f"Upload: {upload_speed} Mbps")
                    #print(f"Ping: {ping} ms")
                else:
                    #print("Error running speedtest-cli:", result.stderr)
                    print_ts("\033[1;44;37m Internet \033[0m  \033[35m Speed Test     \033[31m Error running speedtest\033[m")
                    log_message("[Internet]   Speed Test      Error running speedtest")
                time.sleep(.1)
                # Get cpu temp
                cputemp = psutil.sensors_temperatures()['cpu_thermal'][0].current
                # Convert the temperature to an integer
                cputemp = int(cputemp)
                # Get CPU usage
                cpu_usage = psutil.cpu_percent(interval=1)
                # Get load average
                _, _, load15 = psutil.getloadavg()
                # Get memory usage
                memory_info = psutil.virtual_memory()
                # get clock speed
                cpu_speed = psutil.cpu_freq().current
                # Convert the temperature to an integer
                cpu_speed = int(cpu_speed)
                print_ts(f"\033[1;47;37m CPU      \033[m\033[1;36m   Usage: {cpu_usage}% / Temp: {cputemp}°c / Freq: {cpu_speed} MHz / Load: {load15} / Memory Usage: {memory_info.percent}%\033[m")
                log_message(f"[CPU     ]   Speed Test      Usage: {cpu_usage}% / Temp: {cputemp}°c / Freq: {cpu_speed} MHz / Load: {load15} / Memory Usage: {memory_info.percent}%")
                time.sleep(.1)
            rcounter += 1
            icounter += 1
            return True
        else:
            # run code here when no internet coneection is discovered
            icounter = 1
            print_ts("\033[1;44;37m Internet \033[m\033[31m   Disconnected\033[m\033[2m      No internet access!\033[m")
            log_message(f"[Internet]   Disconnected      (No internet access!)")
            return False
    except requests.ConnectionError:
            # run code for when there is an error checking internet connection, treated as no internet connection
            icounter = 1
            print_ts("\033[1;44;37m Internet \033[m\033[31m   Disconnected\033[m\033[2m   No internet access!\033[m\033[1;31m      [ERROR!]\033[m ")
            log_message(f"[Internet]   Disconnected      (No internet access!)      [ERROR!]")
            return False

def print_ts(message): #print function with time stamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #set time stamp
    print(f"[{timestamp}] {message}") #print message

def log_message(message): #save message to log file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #set time stamp
   # print(f"[{timestamp}] {message}\n") #print message   **function used to print and log the same message, this was changed in v2.1 when color was added and messages overhauled 4/19/24
    with open("rtrb.log", "a") as log_file:  #open log file
        log_file.write(f"[{timestamp}] {message}\n")  #print to log file

def main():
    while True:
        if not check_internet_connection():
            # Run your specific code here when there's no internet connection
            #rcounter += 1
            print_ts("\033[1;46;37m Info     \033[m\033[1;31m   Rebooting Cable Modem!\033[m\033[2m      Modem will power off for 30 seconds.\033[m")
            log_message("[Info    ]   Rebooting Cable Modem!      (Modem will power off for 30 seconds)")
            time.sleep(1)
            print_ts("\033[1;45;37m Power    \033[m\033[33m   Turning cable modem off\033[m\033[2m\033[m")
            log_message("[Power   ]   Turning cable modem off")
            CMD = "sudo /home/frank/rtrb/uhubctl -l 1-1 -p 2 -a off"
            subprocess.run(CMD, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
            time.sleep(30)
            print_ts("\033[1;45;37m Power    \033[m\033[33m   Turning cable modem on\033[m\033[2m\033[m")
            log_message("[Power   ]   Turning cable modem on")
            CMD = "sudo /home/frank/rtrb/uhubctl -l 1-1 -p 2 -a on"
            subprocess.run(CMD, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
            time.sleep(5)
            print_ts("\033[1;46;37m Info     \033[m   Modem power cycle complete!\033[m\033[2m     Modem may take a few moments to boot up.\033[m")
            log_message("[Info    ]   Modem power cycle complete!    (Modem may take a few moments to boot up)")
            time.sleep(.5)
            print_ts("\033[1;46;37m Info     \033[m   Connectivity counter and timer reset.\033[m")
            time.sleep(.3)
            print_ts("\033[1;46;37m Info     \033[m\033[2m   Runtime counter and timer will not reset until progam is closed.\033[m")
            log_message("[Info    ]   Connectivity counter and timer reset.    (Runtime counter and timer only reset when program is closed)")
            # add print and log counters and timers here?
            # not sure if needed?
            time.sleep(.5)
            print_ts("\033[1;46;37m Info     \033[m   Internet access monitoring will resume in 10 minutes.\033[m")
            time.sleep(.3)
            print_ts("\033[1;46;37m Info     \033[m\033[2m   This will give the modem time to boot and connect.\033[m")
            time.sleep(.3)
            print_ts("\033[1;46;37m Info     \033[m   If connectivity has not been restored in 10 minutes modem will powercycle again.\033[m")
            time.sleep(.3)
            print_ts("\033[1;46;37m Info     \033[m\033[2m   This will continue until internet access is restored. \033[m")

        # Wait for 10 minutes before checking again
        time.sleep(600)

print ("")
print_ts("\033[1;46;37m Info     \033[m   Internet Access Monitoring Modem Rebooting Script Launched!\033[m")
time.sleep(.3)
print_ts("\033[1;46;37m Info     \033[m\033[36m   Python script by Frank Treffiletti - v2.5 -  9/29/2024\033[m")
log_message("************************************************************************")
log_message("[INFO    ]   Internet Access Monitoring Modem Rebooting Script Launched!")
time.sleep(.3)
print_ts("\033[1;46;37m Info     \033[m   Checks for internet connectivity every 10 minutes\033[m")
time.sleep(.3)
print_ts("\033[1;46;37m Info     \033[m   Checks internet connection speed every 60 minutes (Download, Upload, Ping)\033[m")
time.sleep(.3)
print_ts("\033[1;46;37m Info     \033[m   Checks system status every 60 minutes (CPU Useage, Temp, Freq, Load, and Memory Usage\033[m")
time.sleep(.3)


if __name__ == "__main__":
    main()
