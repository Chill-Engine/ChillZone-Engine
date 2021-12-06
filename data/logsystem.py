import datetime
import os
import json
import time

try:
#    os.mkdir("log")
    if os.path.isfile("config.json") == False:
        print("Looks like this is your first run. Let's configure setting for you really quickly!")
        username = input("Please, enter your new nickname: ")
        idSysCheck = input("Do you want to use your personal app ID? [y/n] (Default: n) ")
        match idSysCheck.lower:
            case "y":
                appIDW = int(input("Ok, please enter your app ID: "))
            case "n":
                print("Ok, app will use default ID.")
                appIDW = 619183056636477466
            case _:
                print("Ok, app will use default ID.")
                appIDW = 619183056636477466
        print("Okay. We'll save your settings. You can change them in the future.")
        if appIDW == "":
            print("Error: Provided empty Application ID. Using default ID.")
            appIDW = 619183056636477466
        
        data = {
            "username": f"{username}",
            "appID": f"{appIDW}",
            "modules":{
                "SFXAudio": False
            }
        }
        json_object = json.dumps(data)

        writeBlet = open("config.json", "w+")
        writeBlet.write(json_object)
        writeBlet.close()

        time.sleep(2)
        
    


except:
    print("Config file already exists. Continuing.")

dt = "{date:%Y-%m-%d_%H%M%S}".format(date=datetime.datetime.now())


logfirst = open("log/chillengine-" + dt + ".txt","w+")
logfirst.write("[{date:%H:%M:%S} | ".format(date=datetime.datetime.now()) + "CHILLENGINE] Logging started. \n")
logfirst.close()

# Debug thing!
# print("[~] Started logging at {date:%H:%M:%S}".format(date=datetime.datetime.now()))

def debugHelp():
    print("[!] If you need help debugging or fix problem, please visit https://git.io/nsissuse.")

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
    log = open("log/chillengine-" + dt + ".txt","a")
    log.write("[{date:%H:%M:%S} | ".format(date=datetime.datetime.now()) + level + "] " + message + "\n")
    log.close()