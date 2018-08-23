''' Send security message with number of people'''

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

end = 0
present = 0 # to show nb of people in the building
X = np.array([0]) #use to show with matplot, number of people
Y = np.array([0.]) #use to show with matplot, time
today = datetime.now()
# --- Callback function --- #

def on_message(client, userdata, message):
    global present
    global end
    global X
    global Y
    global today

    l = message.topic
    m = message.payload.decode("utf-8")
    moment = datetime.now()
    change = 0 # to print only when change

    #to end it
    if (l == "End"):
        end = 1
    elif (l == "Security"):
        if (m == "1"):
            present += 1
            change = 1
        else :
            if (present > 0):
                present -= 1
                change = 1

    if change:
        print("At this moment, there are " + str(present) + " persons in the building")
        print()

        X = np.insert(X,len(X),present)
        t = moment - today
        Y = np.insert(Y,len(Y), t.seconds)
        plt.plot(Y,X)
        plt.xlabel("times in seconds")
        plt.ylabel("number of person")
        plt.savefig('home/ActivityFile/' + str(today.strftime('%d%B%Y.%H:%M'))+ '.png')


def main():
    global end

    #--------Client constructor----------
    client = mqtt.Client("Security")

    #----------Connect to Broker---------
    Broker1 = "iot.eclipse.org"
    Broker2 = "test.mosquitto.org"
    try:
        client.connect(Broker1) # Brocker #
    except ConnectionRefusedError:
        client.connect(Broker2)

    #---------Subscribe-----------
    client.subscribe("Security")
    client.subscribe("End")

    print("Security message: ")
    while True :
        client.on_message = on_message #callback
        client.loop_start() # Callbacks depends on client loop
        time.sleep(0.5) #time to process the callback
        if (end):
            break

if __name__ == "__main__":
    main()
