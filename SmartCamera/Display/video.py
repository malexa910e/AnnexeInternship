''' Receive movie '''
import socket                   # Import socket module
import cv2						# Import OpenCV
import sys
import paho.mqtt.client as mqtt
import time
import os
import numpy as np

firstPassage = False
host = 0
port = 0
closed = 0

    #--------Callback function---------#
def on_message(client, userdata, message):
        # --- Variable --- #
    global host
    global port
    global firstPassage
    option = os.getenv('option') #to differ between alarm, present and leaving
    m = message.payload.decode("utf-8")
    t = message.topic
    sockname = m.split(' ')
    host = str(sockname[0])
    port = int(sockname[1])
    firstPassage = True

def main():
    global firstPassage
    global host
    global port
    global closed
    option = os.getenv('option') #to differ between alarm, present and leaving
    
    # --- Mqtt connection --- #
    client = mqtt.Client("Display" + option)
    Broker1 = "iot.eclipse.org"
    Broker2 = "test.mosquitto.org"
    try:
    	client.connect(Broker1) # Brocker #
    except ConnectionRefusedError:
    	client.connect(Broker2)

    client.publish("FaceReco/Info/Display/" + option, "Connection to Broker")
    client.subscribe("FaceReco/Display/"+option)


    # --- Wait until get Host and Port --- #
    while (not firstPassage):
        client.on_message = on_message #callback
        client.loop_start() # Callbacks depends on client loop
        time.sleep(0.5) #time to process the callback

    client.publish("FaceReco/Connection/" + option,"Display")


    while True:
        #Connect to a server
        s = socket.socket()
        try:
        	s.connect((host, port))
        except ConnectionRefusedError:
        	break

        fp = option + 'file.jpg'

        with open(fp, 'wb') as f:
        	while True:
        		try:
        			data = s.recv(1024)
        		except ConnectionResetError:
        			break
        		if not data:
        			break
        		f.write(data)

        f.close()
        img = cv2.imread(fp)
        cv2.namedWindow(option, cv2.WINDOW_NORMAL)
        if (option[0]=='P'):
            cv2.resizeWindow(option,640,360)
            cv2.moveWindow(option,800,0)
        elif (option[0]=='L'):
            cv2.resizeWindow(option, 640, 360)
            cv2.moveWindow(option,400,600)
        else:
            cv2.resizeWindow(option,640,480)
        try:
        	cv2.imshow(option, img)
        except cv2.error:
        	break
        cv2.waitKey(1)

        s.close()

    s.close()
    #----------Publish---------------
    client.publish("FaceReco/Info/Display/" + option, "Recording completed")
    client.loop_start() # Callbacks depends on client loop
    time.sleep(0.5) #time to process the callback
    cv2.destroyAllWindows()
    os.system("rm *.jpg")

if __name__ == "__main__":
	main()
