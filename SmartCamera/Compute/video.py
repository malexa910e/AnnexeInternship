''' Take movie and send back movie + face recognition '''


import socket                   # Import socket module
import cv2						# Import OpenCV
import os
import face_recognition
import paho.mqtt.client as mqtt #import the client class
import time
import sys
import numpy as np


# --- Globals variables --- #
firstPassage = False # To wait until reception of host and port
# Host and port receive throught mqtt and use to receive video throught socket #
host = 0
port = 0

# --- Functions --- #
def prepare_training_data(data_folder_path):
    '''prepare data which allow to recognise faces''' # source : https://github.com/informramiz/opencv-face-recognition-python
    # --- Variables --- #
    dirs = os.listdir(data_folder_path) # list to all directories
    faces = [] #list to hold all subject faces
    labels = []  #list to hold labels for all subjects
    length = (len(dirs))

        # --- Pass in each directories to read images --- #
    for dir_name in dirs:
        #ignore any non-relevant directories
        if not dir_name.startswith("s"):
            continue;
            # --- Variables --- #
        label = int(dir_name.replace("s", "")) # name of directorie #
        subject_dir_path = data_folder_path + "/" + dir_name # path to dir. #
        subject_images_names = os.listdir(subject_dir_path) # list of images #
        # --- for every image ---#'''
        for image_name in subject_images_names:
                # --- Variables --- #
            image_path = subject_dir_path + "/" + image_name #path to images

                # --- Steps --- #
            image = face_recognition.load_image_file(image_path) #load images#
            try:
                locate = face_recognition.face_locations(image, number_of_times_to_upsample=2) #Locate faces#
                face = face_recognition.face_encodings(image,locate)[0] #Encoding faces#
            except IndexError:
                continue;
            if face is not None:        #ignore faces that are not detected
                faces.append(face)      #add face to list of faces
                labels.append(label)    #add label for this face
    return faces, labels, length


def on_message(client, userdata, message):
    '''callback function, receive host and port throught mqtt'''
    # --- Variable --- #
    global firstPassage
    global host
    global port
    option = os.getenv('option') #to differentiate between alarm, presence and leaving
    m = message.payload.decode("utf-8")
    t = message.topic

    # Receive host and port to connect throught socket and receive video send by Emit
    sockname = m.split(' ')
    host = str(sockname[0])
    port = int(sockname[1])
    firstPassage = True

# --- Main fonction --- #
def main():
    global firstPassage
    global host
    global port
    option = os.getenv('option') #to differentiate between alarm, presence and leaving

    person = []


    # --- Mqtt connection --- #
    client = mqtt.Client("Compute" + option)
    Broker1 = "iot.eclipse.org"
    Broker2 = "test.mosquitto.org"
    try:
    	client.connect(Broker1) # Brocker #
    except ConnectionRefusedError:
    	client.connect(Broker2)

    client.subscribe("FaceReco/Compute/" + option)
    client.publish("FaceReco/Info/Compute/" + option, "Connection to Broker") # send info to Managing



    # --- Steps --- #
        # --- Prepare Data --- #
    client.publish("FaceReco/Info/Compute/" + option, "Preparing Data ...") #send info to Managing
    DBFolder = "Casting"
    faces,labels, length = prepare_training_data(DBFolder) # Load faces and labels
    unknown_faces = [] # Hold unknown faces
    presence = [] # np.array to show presence
    presence2 = [] # np.array to show presence of stranger
    verif = [0]*length #to verif a presence and avoir error
    verif2 = [] #to avoid error for unknown person

    client.publish("FaceReco/Info/Compute/" + option, "Data prepared ...") #send info to Managing

        # --- Receive Host and Port --- #
    while (not firstPassage):
        client.on_message = on_message #callback
        client.loop_start() # Callbacks depends on client loop
        time.sleep(0.5) #time to process the callback

    client.publish("FaceReco/Connection/" + option,"Compute")

    #start = time.time()
        # --- Socket connection --- #
    while True:
        #pause = time.time()
        s = socket.socket()
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            break

            # --- Receive movie --- #
        fp = option+'file.jpg'

        with open(fp, 'wb') as f:
            while True:
                try:
                    data = s.recv(1024)
                except ConnectionResetError:
                    break
                if not data:
                    break
                f.write(data)


        img = cv2.imread(fp) # Load the frame
        #out.write(img)
            # --- Change image for better process ---#
        #if (pause-start >= 0.25 ):
            #start = time.time()
        try: # Resize frame of video to 1/4 size for faster face recognition processing
            smallImg = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        except cv2.error:
            break
        rgbImg = smallImg[:, :, ::-1] # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)

            # --- Get faces location and encodage --- #
        test_loca = face_recognition.face_locations(rgbImg) # Find all the faces in the current frame of video
        test_enco = face_recognition.face_encodings(rgbImg, test_loca) # Find all the faces encoding in the current frame of video
        face_names = [] # Hold face names
            # --- Recognise face and send names --- #
        for each_face in test_enco:
                results = face_recognition.compare_faces(faces, each_face) # Compare faces find in img and faces in data bases

                try:     # If recognised faces
                    id = labels[results.index(True)]
                    verif[id-1] += 1 # names add to verif

                except ValueError: #else stranger
                    if (not (unknown_faces)): # for the first stranger
                        unknown_faces.append(each_face) # Add his face
                        verif2.append(1) # add to verif
                    else :
                        # Compare face with strangers faces already known
                        results2 = face_recognition.compare_faces(unknown_faces, each_face)
                        if (True not in results2): #if first apparition of stranger
                            unknown_faces.append(each_face) # Add his face
                            verif2.append(1) #add to verif
                        else: # Face already seen
                            id2 = results2.index(True)
                            verif2[id2] += 1 # add to verif

                # to avoid false positive for strangers, if faces recognised at least 5 time
                for i in range (len(verif2)):
                    if (verif2[i] > 4) & (i not in presence2) :
                        presence2.append(i) # Info send just once
                        if (option == "Present"):
                            client.publish("Security","1")
                            client.publish("Schedule/Present", length)
                        elif (option == "Leaving"):
                            client.publish("Security","-1")
                            client.publish("Schedule/Leaving", length)
                        elif (option == "Alarm"):
                            client.publish("Access", length)

                # to avoid false positive for known people, if faces recognised at least 5 time
                for i in range (len(verif)):
                    if (verif[i] > 4) & (i not in presence) :
                        presence.append(i) # Info send just once
                        if (option == "Present"):
                            client.publish("Security","1")
                            client.publish("Schedule/Present", i)
                        elif (option == "Leaving"):
                            client.publish("Security","-1")
                            client.publish("Schedule/Leaving", i)
                        elif (option == "Alarm"):
                            client.publish("Access", i)

        #else:
        #    pass

        s.close()

    s.close()
    #out.release()

if __name__ == "__main__":
    main()
