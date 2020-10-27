#Import's START
from pypresence import Presence
import time
import pip
import os
import random
from random import randint
import sys
from chznlog import addLog as al # Logging operations
from chznlog import debugHelp as dh # Send the same message each time
from chznconf import configs as c # Configurations
#Import's END

try:
    import pypresence as pp # pypresence handles Discord communication
    from json import loads # API uses json
    import requests # Connection to API requires requests
except Exception as e: # If module could not be imported
    print("[!] We ran in to a problem. " + str(e)) # Let the user know there was a problem
    dh() # Print the debug message
    al("FTL","Failed to import a module: " + str(e)) # Output error to log

al("INK","Chill Zone v" + c.ver + " started. Thanks for using Chill Zone :)") # Test logging
al("INK","If you ever need to debug something, please send this log to discord.gg/Tx7ratd.")

try:
    open(".nocol","r") # If we can open .nocol, it must exist
    from mansi import nocolours as p # Import the disabled colour scheme
    al("INF","Disabled terminal colours") # Output info to log
except:
    from mansi import colours as p # Import the enabled colour scheme
    al("INF","Enabled terminal colours") # Output info to log

rpc = pp.Presence(c.client) # Open an RPC connection with the Splatoon 2 client ID
rpc.connect()
def setStatus(silent,large,small,ltext,stext,details,state):
    try:
        rpc.update(large_image=large,small_image=small,large_text=ltext,small_text=stext,details=details,state=state,start=int(time.time())) # Update presence
        al("INF","Updated presence: " + str(silent) + ", " + str(large) + ", " + str(small) + ", " + str(ltext) + ", " + str(stext) + ", " + str(details) + ", " + str(state)) # Output presence to log
        if silent == 0:
            print(p.success + "Presence updated.") # Give success message
    except Exception as e:
        print(p.fail + "There was a problem updating your presence: " + str(e)) # Presence update failed, print error message
        al("ERR","Couldn't update presence: " + str(e)) # Output error to log
        al("ERR","Failed presence:" + str(silent) + ", " + str(large) + ", " + str(small) + ", " + str(ltext) + ", " + str(stext) + ", " + str(details) + ", " + str(state)) # Output presence to log

def salmonRun():
    try:
        schedule = requests.get("https://splatoon2.ink/data/coop-schedules.json",headers=c.headers).json() # Get API data about Salmon Run
    except Exception as e: # If we couldn't connect
        print(p.fail + "Couldn't connect to splatoon2.ink's API! Check your internet and try again later.") # Inform the user of the error
        al("ERR","Couldn't connect to splatoon2.ink: " + str(e)) # Output the exception to the log for troubleshooting
        return
    if int(schedule["details"][0]["end_time"]) < int(time.time()) or int(schedule["details"][0]["start_time"] > int(time.time())): # If Salmon Run is closed
        print(p.warn + "Salmon Run isn't open right now! Try again later.") # Warn the user
        al("INF","Salmon Run isn't open right now! Try again later.") # Output error to log
        return # Return to the main menu
    else: # If Salmon Run is open
        stagename = schedule["details"][0]["stage"]["name"] # Get the stage name from the API
        stagekey = stagename.lower().replace("'","").replace(" ","") # Define the key as the stage name with no spaces, no apostraphes and all lowercase
        setStatus(0,stagekey,"grizzco",stagename,"Grizzco","Salmon Run",stagename) # Set the status

def multiplayer():
    try:
        schedule = requests.get("https://splatoon2.ink/data/schedules.json",headers=c.headers).json() # Get API data about Salmon Run
        print(p.success + "Refreshed the splatoon2.ink schedule. Select your gamemode and map below.")
        check_time = schedule["regular"][0]["end_time"]
    except Exception as e: # If we couldn't connect
        print(p.fail + "Couldn't connect to splatoon2.ink's API! Check your internet and try again later.") # Inform the user of the error
        al("ERR","Couldn't connect to splatoon2.ink: " + str(e)) # Output the exception to the log for troubleshooting
        return
    try:
        while True:
            if check_time < int(time.time()):
                print(p.warn + "Multiplayer maps and modes have been updated!")
                setStatus(1,"square",None,"Inkopolis Square",None,"In Menus","Inkopolis Square")
                return
            else: # Repeating spaces method used below thanks to @Eli Courtwright on StackOverflow: https://stackoverflow.com/a/1424016
                choice = {"map":'',"mapkey":'',"type":'',"mode":'',"iconkey":'',"stext":''} # type: Regular,Ranked,League | mode: Turf War,Rainmaker,Splat Zones,Clam Blitz
                print(p.info + "Regular Battle        (Turf War) | 1. " + schedule["regular"][0]["stage_a"]["name"] + " "*(22-len(schedule["regular"][0]["stage_a"]["name"])) + "| 2. " + schedule["regular"][0]["stage_b"]["name"]) # Print Turf War stages

                print(p.info + "Ranked Battle" + " "*(32-13-2-len(schedule["gachi"][0]["rule"]["name"])) + "(" + schedule["gachi"][0]["rule"]["name"] + ") | 3. " + schedule["gachi"][0]["stage_a"]["name"] + " "*(22-len(schedule["gachi"][0]["stage_a"]["name"])) + "| 4. " + schedule["gachi"][0]["stage_b"]["name"]) # Print Ranked stages

                print(p.info + "League Battle" + " "*(32-13-2-len(schedule["league"][0]["rule"]["name"])) + "(" + schedule["league"][0]["rule"]["name"] + ") | 5. " + schedule["league"][0]["stage_a"]["name"] + " "*(22-len(schedule["league"][0]["stage_a"]["name"])) + "| 6. " + schedule["league"][0]["stage_b"]["name"]) # Print League stages

                print(p.info + "Inkcord Options  (Configuration) | 7. Exit to Main Menu     | 8. Refresh Schedule") # Add exit option
                try:
                    userchoice = int(input(p.ask)) # Request user input
                except ValueError:
                    print(p.fail + "That's not a valid option! Try again.") # If it's not an integer, retry
                    continue
                if userchoice == 1:
                    choice["map"] = schedule["regular"][0]["stage_a"]["name"] # Set the map to Regular Battle Stage A
                elif userchoice == 2:
                    choice["map"] = schedule["regular"][0]["stage_b"]["name"] # Set the map to Regular Battle Stage B
                elif userchoice == 3:
                    choice["map"] = schedule["gachi"][0]["stage_a"]["name"] # Set the map to Ranked Battle Stage A
                elif userchoice == 4:
                    choice["map"] = schedule["gachi"][0]["stage_b"]["name"] # Set the map to Ranked Battle Stage B
                elif userchoice == 5:
                    choice["map"] = schedule["league"][0]["stage_a"]["name"] # Set the map to League Battle Stage A
                elif userchoice == 6:
                    choice["map"] = schedule["league"][0]["stage_b"]["name"] # Set the map to League Battle Stage B
                elif userchoice == 7:
                    setStatus(1,"square",None,"Inkopolis Square",None,"In Menus","Inkopolis Square") # Reset presence to default
                    print(p.success + "Returning to main menu.") # Return to main menu
                    return
                elif userchoice == 8:
                    multiplayer()
                    return
                else:
                    print(p.fail + "That's not a valid option! Try again.") # If it's not any of the valid options, retry
                    continue
                if userchoice == 1 or userchoice == 2:
                    choice["type"] = "Regular Battle" # Set the type to Regular
                    choice["mode"] = "Turf War" # Set the mode to Turf War
                elif userchoice == 3 or userchoice == 4:
                    choice["type"] = "Ranked Battle" # Set the type to Ranked
                    choice["mode"] = schedule["gachi"][0]["rule"]["name"] # Set the mode to current Ranked rotation
                elif userchoice == 5 or userchoice == 6:
                    choice["type"] = "League Battle" # Set the type to League
                    choice["mode"] = schedule["league"][0]["rule"]["name"] # Set the mode to current League rotation
                choice["mapkey"] = choice["map"].lower().replace("'","").replace(" ","").replace("-","") # Map key is map all lowercase no spaces or punctuation
                choice["iconkey"] = choice["mode"].lower().replace(" ","-") + "-" + choice["type"].lower().split(" ")[0] # Mode key is all lowercase with dashes instead of spaces
                choice["stext"] = choice["type"] + " - " + choice["mode"] # stext is the type and mode combined
                al("INF","Choice variable: " + str(choice)) # Output the choice variable to log, useful for debugging
                setStatus(0,choice["mapkey"],choice["iconkey"],choice["map"],choice["stext"],"Playing " + choice["mode"],choice["type"]) # Set status
                continue # Do next loop
    except KeyboardInterrupt:
        print() # ^C will be on the current line
        print(p.warn + "Returning to main menu.") # Returns to the main menu
        setStatus(1,"chill_zone","dev","Chilling","Dev","Nick Salt","nicksaltfoxu.ml")
        return

def menu():
    setStatus(1,"chill_zone","dev","Chilling","Dev","Nick Salt","nicksaltfoxu.ml") # Default presence
    while True:
        opt = input(p.cmd)
        if opt.startswith("salmon"):
            salmonRun()
        elif opt.startswith("random"):
            setStatus(0,"chill_zone","dev","Chilling","Dev","Nick Salt",randint(10, 9999))
        elif opt.startswith("normal"):
            setStatus(0,"chill_zone","dev","Chilling","Dev","Nick Salt","l0calSerVe4")
        elif opt.startswith("octo"):
            setStatus(0,"deepsea","cq","Deepsea Metro","Octo Expansion","Playing Octo Expansion","Deepsea Metro")
        elif opt.startswith("lobby"):
            multiplayer()
        elif opt.startswith("private"):
            print(p.fail + "Private Battles are currently not supported. They're coming soon!")
        elif opt.startswith("splatfest"):
            print(p.warn + "The last Splatfest is already over! Splatfests are not currently supported.")
        elif opt == "exit":
            print(p.success + "Exiting...")
            al("INF","Exited via command with status code 0")
            sys.exit(0)
        else:
            print(p.warn + "That's not a valid command! Try again.")
print(p.smile + "Welcome to Chill Zone v" + c.ver + "!")
gitver = str(requests.get("http://l0calserve4.ml/apps_versions/chzn").text[:5])
if c.ver != gitver:
    print(p.warn + "You're out of date! The current version on GitHub is " + gitver + ". Update at l0calserve4.ml/apps/" + gitver + "!")
else:
    print(p.success + "You're up-to-date. Thanks for using Chill Zone!")
print(p.info + "Thanks to splatoon2.ink for the schedule information used in this app!")
print(p.warn + "Questions, comments, rants? Head to discord.gg/Tx7ratd!")

try:
    menu()
except KeyboardInterrupt:
    print()
    print(p.warn + "Exiting...")
    al("ERR","Exited via keyboard interrupt with status code 1")
