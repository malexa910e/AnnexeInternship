''' Open door and record passage in restricted room'''

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import numpy as np

end = 0
permitted = open("home/Names/Allowed.txt").read().splitlines()
subjects = open("home/Names/Casting.txt").read().splitlines()
length = len(subjects)

# --- file with info to save --- #
today = datetime.now()
nameFile = "home/ActivityFile/" + str(today.strftime('%d%B%Y'))+".txt"

# --- Callback function --- #

def on_message(client, userdata, message):
    global nameFile
    global today
    global end

    moment = datetime.now()

    l = message.topic
    m = message.payload.decode("utf-8")

    #Map labels and names
    if (int(m) == length):
        name = "A stranger"
    else:
        name = subjects[int(m)]

    #to end it
    if (l == "End"):
        end = 1
    elif (l == "Access"):
        with open (nameFile,'a+') as f:
            f.write("At " + str(moment.strftime("%H:%M:%S") + ", "))
            if (name == "A stranger"):
                print("Warning, a stranger tried to enter a restricted area \n")
                f.write ("a stranger tried to enter the restricted area \n")
            else:
                if (name not in permitted):
                    print("Warning, " + name + " tried to enter a restricted area\n")
                    f.write (name + " tried to enter the restricted area \n")
                else :
                    print("Door opening, " + name + " is authorized to enter \n")
                    f.write (name + " enters the restricted area \n")



def main():
    global end

    #--------Client constructor----------
    client = mqtt.Client("Access")

    #----------Connect to Broker---------
    Broker1 = "iot.eclipse.org"
    Broker2 = "test.mosquitto.org"
    try:
        client.connect(Broker1) # Brocker #
    except ConnectionRefusedError:
        client.connect(Broker2)

    #---------Subscribe-----------
    client.subscribe("Access")
    client.subscribe("End")

    print("Access control message: ")
    while True :
        client.on_message = on_message #callback
        client.loop_start() # Callbacks depends on client loop
        time.sleep(0.5) #time to process the callback
        if (end):
            break

if __name__ == "__main__":
    main()
