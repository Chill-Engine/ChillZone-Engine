import pypresence
import time
import os
import sys
import datetime
import json

from log import addLog as aal  # Logging operations
from log import debugHelp as dgh  # Send the same message each time
from conf import configs as c  # Configurations


try:
    import pypresence as pypr
    from json import loads  # API uses json
    import requests  # Connection to API requires requests
except Exception as e:  # If module could not be imported
    # Let the user know there was a problem
    print("[!] Мы столкнулись с проблемой. " + str(e))
    dgh()  # Print the debug message
    aal("FTL", "Не удалось импортировать модули: " + str(e))  # Output error to log


aal("LOD", "Chill Zone v" + c.ver +
    " запустился. Спасибо что используете ChillZone :)")  #  Test logging
aal("LOD", "If you ever need to debug something, please send this log to https://discord.gg/yTxrCGR.") ## Needs to be translated!


try:
    open(".nocol", "r")  # If we can open .nocol, it must exist
    from mansi import nocolours as p  # Import the disabled colour scheme
    aal("INF", "Disable terminal color")  # Output info to log
except:
    from mansi import colours as p  # Import the enabled colour scheme
    aal("INF", "Enable terminal color")  # Output info to log



rpc = pypr.Presence(c.client)
rpc.connect()


def setStatus(silent, large, small, ltext, stext, details, state):
    try:
        rpc.update(large_image=large, small_image=small, large_text=ltext, small_text=stext,
                   details=details, state=state, start=int(time.time()))  #  Update presence
        aal("INF", "Обновить presence: " + str(silent) + ", " + str(large) + ", " + str(small) + ", " +
            str(ltext) + ", " + str(stext) + ", " + str(details) + ", " + str(state))  #  Output presence to log
        if silent == 0:
            print(p.success + "Presence обновлен.")  # Give success message
    except Exception as e:
        # Presence update failed, print error message
        print(p.fail + "Произошла ошибка при обновлении вашего presence: " + str(e))
        aal("ERR", "Не удалось обновить presence: " + str(e))  # Output error to log
        aal("ERR", "Неудачный presence:" + str(silent) + ", " + str(large) + ", " + str(small) + ", " +
            str(ltext) + ", " + str(stext) + ", " + str(details) + ", " + str(state))  #  Output presence to log


def info():
    print(p.info + " ChillZone App v" + c.ver + " | Made by Nick Salt ")
    print(p.info + " Original code [INKCORD] by M4xic [https://github.com/m4xic] ")
    if c.ver != gitver:
        print(p.info + " Needs update?: Yes")
    if c.ver == gitver:
        print(p.info + " Needs update?: No")

def eastereggs(eggname, code):
    if eggname == "Starship" and code == "1231":
        print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    pass

def help():
    print(p.info + "--------------------------------------------------------------------------")
    print(p.info + "lobby         ---  Лобби приложения (Default).                            ")
    print(p.info + "chill         ---  Лобби приложения (Server Lobby).                       ")
    print(p.info + "chillZone.jam ---  Комманда для информации о следующих или данных евентов.")
    print(p.info + "private       ---  Приватная группа.                                      ")
    print(p.info + "check         ---  Проверить связь с сервером.                            ")
    print(p.info + "help          ---  Список комманд.                                        ")
    print(p.info + "info          ---  Информация о программе.                                ")
    print(p.info + "--------------------------------------------------------------------------")

def menu():
    setStatus(1, "chill_zone", "menu", c.ver + "|" + c.vern,
              "Menu", "In lobby", "Chill_SV#1")  # Default presence

    while True:
        opt = input(p.cmd)
##        if opt.startswith("chill"):
        if opt == ("chill"):
            setStatus(0, "chillmodee", "chill", c.ver + "|" +
                      c.vern, "Chill", "Chill Lobby", "Chill_SV#1")


        elif opt == ("lobby"):
            setStatus(0, "chill_zone", "menu", c.ver + "|" + c.vern,
              "Menu", "In lobby", "Chill_SV#1")


        elif opt == ("private"):
            priv = (input(p.ask + "Название приватной группы: "))
            privnm = (input(p.ask + "Количество юзеров в группе: "))
            if int(privnm) <= 2:
                print("Ошибка! Число участников меньше 2")
                menu()
            print(p.info + "Название группы: " + priv + "\n" +
                  p.info + "Число участников: " + privnm)
            rpc.update(large_image="chill_zone", small_image="lock", large_text=c.ver + " | " + c.vern, small_text="Group",
                       details="Private group", state=priv, party_size=[1, int(privnm)], start=int(time.time()))


        elif opt == ("chillZone.jam"):
            print(p.warn + "В данный момент не работает!")


        elif opt == ("devMenu.login"):
            print(p.info + "В данный момент не работает!")


        elif opt == ("help"):
            help()


        elif opt == ("info"):
            info()


        elif opt == ("starship"+"1231"):
            eastereggs("Starship", "1231")


        elif opt == "exit":
            print(p.success + "Выходим...")
            aal("INF", "Exited via command with status code 0")
            sys.exit(0)

            
        else:
            print(p.warn + "That's not a valid command! Try again.")



print(p.smile + "Добро пожаловать в ChillZone v" + c.ver + "!")
gitver = str(requests.get(
    "https://nicksaltfoxu.ml/versions/ChillZoneRPC/version").text[:4])
offwebsiten = "NickSaltFoxu Repos"
if c.ver != gitver:
    print(p.warn + "У вас устаревшая версия программы! В данный момент актуальна версия на " +
          offwebsiten + " = " + gitver + ". Обновите её здесь https://github.com/BlueBerrySans365/chill-zone-DRPC!")
else:
    print(p.success + "У вас актуальная версия программы. Спасибо что используете ChillZoneRPC!")
print(p.warn + "Questions, comments, rants? Head to https://git.io/nsissuse or https://discord.gg/yTxrCGR!")


try:
    menu()
except KeyboardInterrupt:
    print()
    print(p.warn + "Exiting...")
    aal("ERR", "Exited via keyboard interrupt with status code 1")
