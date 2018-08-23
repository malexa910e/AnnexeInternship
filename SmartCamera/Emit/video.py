''' Send movie '''

import socket                   # Import socket module
import threading
import cv2
import os
import paho.mqtt.client as mqtt
import time
import sys
import iperf3

connection = 0
display = 0
Compute = 0

def on_message(client, userdata, message):
    '''callback function, receive host and port throught mqtt'''
    # --- Variable --- #
    global connection
    global display
    global compute
    option = os.getenv('option') #to differentiate between alarm, presence and leaving
    m = message.payload.decode("utf-8")
    t = message.topic

    if (m == "Display"):
        display = 1
        connection += 1

    elif (m == "Compute"):
        compute = 1
        connection += 1

# --- Main function --- #

def main():
        # --- Variables --- #
    global connection
    global display
    global compute
    movie = os.getenv('movie')

    '''videoType = 0 #indicator of webcam or file to delete ?
    # --- Choose between movie and webcam --- #
    if os.getenv('movie') == "0":  # Webcam #
        movie = 0
    else:                   # Movie #
        movie = os.getenv('movie')
        videoType = 1'''

    option = os.getenv('option') #to differientiate between alarme presence leaving

    # --- Mqtt connection --- #
    client = mqtt.Client("Emit" + option) # Client creation #
    Broker1 = "iot.eclipse.org"
    Broker2 = "test.mosquitto.org"
    try:
    	client.connect(Broker1) # Brocker #
    except ConnectionRefusedError:
    	client.connect(Broker2)

    client.subscribe("FaceReco/Connection/" + option)
    client.publish("FaceReco/Info/Emit/" + option, "Connection to Broker") # send info to Managing

    # Socket connection through Compute #
    sCompute = socket.socket()                 # Create a socket object
    hostCompute = socket.gethostname()         # Get hostname
    sCompute.bind((hostCompute, 0))                   # Bind to first port available
    hostCompute,portCompute = sCompute.getsockname()         # Get local machine name and port0
    sCompute.listen(5)                         # Now wait for client connection.

    # Socket connection through Display #
    sDisplay = socket.socket()                 # Create a socket object
    hostDisplay = socket.gethostname()         # Get hostname
    sDisplay.bind((hostDisplay, 0))                   # Bind to first port available
    hostDisplay,portDisplay = sDisplay.getsockname()         # Get local machine name and port0
    sDisplay.listen(5)                         # Now wait for client connection.

    while (connection != 2) :
        client.publish("FaceReco/Display/"+ option , str(hostDisplay) +' '+ str(portDisplay))
        client.publish("FaceReco/Compute/"+ option, str(hostCompute) +' '+ str(portCompute))
        client.on_message = on_message #callback
        client.loop_start() # Callbacks depends on client loop
        time.sleep(0.5) #time to process the callback

    # --- Send Movie --- #
    video_capture = cv2.VideoCapture(movie)
    fps =  video_capture.get(cv2.CAP_PROP_FPS)

    while (True):
        ret, frame = video_capture.read()
        # Quit when the input video file ends
        if not ret:
            break

        #Connection with both compute and display
        connC, addrC = sCompute.accept()
        connD, addrD = sDisplay.accept()

        #Send from to both compute and display
        test = cv2.imwrite('test.jpg',frame)
        f = open('test.jpg','rb')
        l = f.read(1024)
        while (l):
            if (compute == 1):
                connC.send(l)
            else:
                pass
            if (display == 1):
                connD.send(l)
            else:
                pass
            l = f.read(1024)
        f.close()

        #Close when over
        if (compute == 1):
            connC.close()
        else:
            pass
        if (display == 1):
            connD.close()
        else:
            pass
    video_capture.release()


if __name__ == "__main__":
	main()
