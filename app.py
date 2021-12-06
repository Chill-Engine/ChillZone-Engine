import pypresence as pr
import time
import os
import sys
import datetime
import json
import requests

from data.logsystem import addLog, debugHelp
clear = lambda: os.system('cls')

# Начальная инфа... Да, я серьезно ._.

AppVersion = "notSoReadyy" 
AppBranch = "Beta"
versionURL = "https://nicksaltfoxu.ml/versions/ChillZoneRPC/stable.json"

# Ну что ж, погнали.

clear()
try: # Проверка версии
    testVersion = requests.get(versionURL)
    updi = testVersion.json()
    if updi['chillengine']['versionCode'] == AppVersion:
        UpdateStatus = False
        addLog("INF", f"We successfully checked github version with app version, and it's same! [URL: {versionURL}]")
    else:
        UpdateStatus = True


except Exception as e: # Если проверка версии прошла не успешно
    print("We found a problem! " + str(e))
    debugHelp() 
    addLog("FTL", "Can't check right version: " + str(e))
    sys.exit(0)

addLog("LOD", f"Chill Engine v{updi['chillengine']['version']} started. Thanks for using Chill Engine :)")  
addLog("LOD", "If you ever need to debug something, please send this log to https://git.io/nsissuse.")

with open('config.json') as json_file:
    config = json.load(json_file)

try:
    rpc = pr.Presence(config['appID'])
    rpc.connect()
except Exception as e:
    print(f"We found a problem in presence loading! \n{str(e)}")
    addLog("FTL", f"Presence error: \n {str(e)}")

def setStatus(silent, large, small, ltext, stext, details, state):
    try:
        rpc.update(large_image=large, small_image=small, large_text=ltext, small_text=stext,
                   details=details, state=state, start=int(time.time()))
        addLog("INF", "Updating presence: " + str(silent) + ", " + str(large) + ", " + str(small) + ", " +
            str(ltext) + ", " + str(stext) + ", " + str(details) + ", " + str(state))
        if silent == 0:
            print("Presence updated.") 
    except Exception as e:
        print("We found an error with presence: " + str(e))
        addLog("ERR", "Failed to update presence: " + str(e))
        addLog("ERR", f"Failed presence:" + str(silent) + ", " + str(large) + ", " + str(small) + ", " +
            str(ltext) + ", " + str(stext) + ", " + str(details) + ", " + str(state))

def info():
    print(f"\nChillZone App v{updi['chillengine']['version']} | Made by Nick Salt ")
    print("Original code [INKCORD] by M4xic [https://github.com/m4xic] ")
    if UpdateStatus == True:
        updn = requests.get(f"{updi['chillengine']['note']}")
        print("\nNeeds update?: Yes")
        print(f"Update info: \n\n{updn.text}\n")
    if UpdateStatus == False:
        print("Needs update?: No")

def help():
    print("--------------------------------------------------------------------------")
    print("lobby         ---  Лобби приложения (Default).                            ")
    print("chill         ---  Лобби приложения (Server Lobby).                       ")
    print("private       ---  Приватная группа.                                      ")
    print("check         ---  Проверить связь с сервером.                            ")
    print("help          ---  Список комманд.                                        ")
    print("info          ---  Информация о программе.                                ")
    print("--------------------------------------------------------------------------")

def menu():
    setStatus(1, "chill_zone", "menu", f"{updi['chillengine']['version']} | {AppBranch}", "Menu", "In lobby", "Chill_SV#1")  # Default presence

    while True:
        opt = input("> ")
        match opt:
            case "chill":
                setStatus(0, "chillmodee", "chill", f"{updi['chillengine']['version']} | {AppBranch}", "Chill", "Chill Lobby", "Chill_SV#1")


            case "lobby":
                setStatus(0, "chill_zone", "menu", f"{updi['chillengine']['version']} | {AppBranch}", "Menu", "In lobby", "Chill_SV#1")


            case "help":
                help()


            case "info":
                info()


            case "exit":
                print("Выходим...")
                addLog("INF", "Exited via command with status code 0")
                sys.exit(0)

                
            case _:
                print("That's not a valid command! Try again.")

print(f"Welcome!\n ChillZone v{updi['chillengine']['version']}!\n")
time.sleep(2.5)
match UpdateStatus:
    case False:
        print("You have newest version of app. Thanks for using Chill Engine!")
    case True:
        print(f"You have old version of app! Update it here {updi['chillengine']['link']}!")


print("Questions, comments, rants? Head to https://git.io/nsissuse or https://discord.gg/yTxrCGR!\n")


try:
    menu()
except KeyboardInterrupt:
    print()
    print("Exiting...")
    addLog("ERR", "Exited via keyboard interrupt with status code 1")