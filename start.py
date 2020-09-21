#Import's START
from pypresence import Presence
import time
import pip
import os
import random
from random import randint
import urllib.request, json 
#Import's END

#lolz
with urllib.request.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=google") as url:
    data = json.loads(url.read().decode())
    print(data)
#lolz end

#Discord RPC START
Discord_Game_ID = '619183056636477466'
Discord_Game_name = ''
Discord_Game_number = '----'
RPC = Presence(Discord_Game_ID)  # Initialize the Presence class
RPC.connect()  # Start the handshake loop
#Discord RPC END



while True:
 RPC.update(details="Number:", state=str(randint(1, 9999)), large_image="chill_zone") #Set the presence, picking a random quote
 time.sleep(1)
