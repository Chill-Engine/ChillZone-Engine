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
    aal("INF", "Отключены цвета терминала")  # Output info to log
except:
    from mansi import colours as p  # Import the enabled colour scheme
    aal("INF", "Включены цвета терминала")  # Output info to log


# Open an RPC connection with the Splatoon 2 client ID
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


def help():
    print(p.info + "chill         ---  Лобби приложения.                                      ")
    print(p.info + "chiZone.jam   ---  Комманда для информации о следующих или данных евентов.")
    print(p.info + "private       ---  Приватная группа.                                      ")
    print(p.info + "help          ---  Список комманд.                                        ")


def menu():
    setStatus(1, "chill_zone", "menu", c.ver + "|" + c.vern,
              "Menu", "In lobby", "Chill_SV#1")  # Default presence
    while True:
        opt = input(p.cmd)
        if opt.startswith("chill"):
            setStatus(0, "chillmodee", "chill", c.ver + "|" +
                      c.vern, "Chill", "Chill Lobby", "Chill_SV#1")
        elif opt.startswith("private"):
            priv = (input(p.ask + "Название приватной группы: "))
            privnm = (input(p.ask + "Количество юзеров в группе: "))
            if int(privnm) <= 2:
                print("Ошибка! Число участников меньше 2")
                menu()
            print(p.info + "Название группы: " + priv + "\n" +
                  p.info + "Число участников: " + privnm)
            rpc.update(large_image="privaaaat", small_image="lock", large_text=c.ver + " | " + c.vern, small_text="Group",
                       details="Private group", state=priv, party_size=[1, int(privnm)], start=int(time.time()))
        elif opt.startswith("chiZone.jam"):
            print(p.warn + "В данный момент не работает!")
        elif opt.startswith("devMenu.login"):
            print(p.info + "В данный момент не работает!")
        elif opt.startswith("help"):
            help()
        elif opt == "exit":
            print(p.success + "Выходим...")
            aal("INF", "Exited via command with status code 0")
            sys.exit(0)
        else:
            print(p.warn + "That's not a valid command! Try again.")


print(p.smile + "Добро пожаловать в ChillZone v" + c.ver + "!")
gitver = str(requests.get(
    "https://nicksaltfoxu.ml/versions/ChillZoneRPC/version").text[:4])
offwebsiten = "NickSaltFoxu Repo"
if c.ver != gitver:
    print(p.warn + "У вас устаревшая версия программы! В данный момент актуальна версия на " +
          offwebsiten + " = " + gitver + ". Обновите её здесь https://git.io/JTOhv!")
else:
    print(p.success + "У вас актуальная версия программы. Спасибо что используете ChillZoneRPC!")
print(p.warn + "Questions, comments, rants? Head to https://git.io/JTOhv или https://discord.gg/yTxrCGR!")


try:
    menu()
except KeyboardInterrupt:
    print()
    print(p.warn + "Exiting...")
    aal("ERR", "Exited via keyboard interrupt with status code 1")
