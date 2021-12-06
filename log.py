

import datetime
import os

# Inline formatting of date and time, thanks @Pieter on StackOverflow: https://stackoverflow.com/a/48779287
try:
    os.mkdir("logs")
    if os.path.isfile(".nocol") == False:
        print("[!] Looks like this is your first run. Let's configure colour settings really quickly!")
        print("\033[91m[!] Does this text look red to you? (y/n)")
        nocol = input("[?] ")
        if nocol == "n" or nocol == "N":
            print("[!] Okay. We'll disable colours to make this app easier to use!")
            print("[!] If you didn't mean to do this, delete the 'logs' folder to reconfigure.")
            try:
                nocolfile = open(".nocol","w+")
                nocolfile.write("This file was automatically generated at {date:%Y-%m-%d_%H%M%S} to disable colours!".format(date=datetime.datetime.now()))
                nocolfile.close()
            except:
                print("[!] There was a problem creating the .nocol file!")
        else:
            print("[!] Okay. We'll leave colours enabled to make this app prettier!")
            print("[!] If you didn't mean to do this, delete the 'logs' folder to reconfigure.")
except:
    print("[~] Logs directory already exists. Continuing.")

dt = "{date:%Y-%m-%d_%H%M%S}".format(date=datetime.datetime.now())

logfirst = open("logs/chillzone-" + dt + ".txt","w+")
logfirst.write("[{date:%H:%M:%S} | ".format(date=datetime.datetime.now()) + "CHILL" + "] " + "Logging started." + "\n")
logfirst.close()

# print("[~] Started logging at {date:%H:%M:%S}".format(date=datetime.datetime.now()))

def debugHelp():
    print("[!] If you need help debugging, please visit https://git.io/nsissuse or join https://discord.gg/yTxrCGR")

def addLog(level,message):
    """
    Adds one line to the current log file.

    Level should be a three letter code as below:
    - LOD: Initalization
    - INF: Info
    - WRN: Warn
    - ERR: Error
    - FTL: Fatal

    Message is a string of unlimited length.
    """
    log = open("logs/chillzone-" + dt + ".txt","a")
    log.write("[{date:%H:%M:%S} | ".format(date=datetime.datetime.now()) + level + "] " + message + "\n")
    log.close()
