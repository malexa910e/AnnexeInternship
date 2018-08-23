''' Record presence and identification in building'''

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

end = 0
present = 0 # to show nb of people in the building
person = []
stranger = 0
X = np.array([0]) #use to show with matplot, number of people
Y = np.array([0.]) #use to show with matplot, time
subjects = open("home/Names/Casting.txt").read().splitlines()
length = len(subjects)

# --- file with info to save --- #
today = datetime.now()
nameFile = "home/ActivityFile/" + str(today.strftime('%d%B%Y'))+".txt"

# --- Callback function --- #

def on_message(client, userdata, message):
    global present
    global person
    global stranger
    global nameFile
    global today
    global end
    global X
    global Y

    moment = datetime.now()
    change = 0 # to print only when change
    l = message.topic
    m = message.payload.decode("utf-8")

    #Map labels and names
    if (int(m) == length):
        name = "A stranger"
    else:
        name = subjects[int(m)]

        #to end Information
    if (l == "End"):
        end = 1

    elif (l[9:] == "Present"):
        if (name == "A stranger"):
            stranger += 1
            present += 1
            change = 1
        else:
            if (name not in person):
                person.append(name)
                present += 1
                change = 1

    elif (l[9:] == "Leaving"):
        if (name == "A stranger") and (stranger != 0):
            stranger -= 1
            present -= 1
            change = 1
        else:
            if (name in person):
                person.remove(name)
                present -= 1
                change = 1

    if change:
        X = np.insert(X,len(X),present)
        t = moment - today
        Y = np.insert(Y,len(Y), t.seconds)
        plt.plot(Y,X)
        plt.xlabel("times in seconds")
        plt.ylabel("number of person")
        plt.savefig('home/ActivityFile/' + str(today.strftime('%d%B%Y.%H:%M'))+ '.png')

        # print who is in the building and put it into activity files
        with open (nameFile,'a+') as f:
            f.write("At " + str(moment.strftime("%H:%M:%S")))
            f.write (", there are " + str(present) +" person(s) in the building:\n")
            for i in person:
                f.write(i + ",")
            f.write("and " + str(stranger) + " stranger(s) are here\n\n")

def main():
    global nameFile
    global end

    #--------Client constructor----------
    client = mqtt.Client("Schedule")

    #----------Connect to Broker---------
    Broker1 = "iot.eclipse.org"
    Broker2 = "test.mosquitto.org"
    try:
        client.connect(Broker1) # Brocker #
    except ConnectionRefusedError:
        client.connect(Broker2)

    #---------Subscribe-----------
    client.subscribe("Schedule/#")
    client.subscribe("End")

    while True :
        client.on_message = on_message #callback
        client.loop_start() # Callbacks depends on client loop
        time.sleep(0.5) #time to process the callback
        if (end):
            break

if __name__ == "__main__":
    main()
