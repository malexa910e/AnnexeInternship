# AnnexeInternship
Smart security camera in a smart building:
This app is the code of my first use case developping during my internshp with Ryax Technologies

## Presentation
This app, which enables to work with docker, allows to identify people appearing in front of different cameras and to send different messages such as:

* Identification of people entering the building thanks to a camera recording the entrance
* Identification of people leaving the building thanks to a camera recording the exit
* Number of people in the building
* Opening of the door when an authorized person attempts to enter a specific place.
* Warning when an unauthorized person attempts to enter a specific place.

## Source

* [Facial Recognition](https://github.com/ageitgey/face_recognition)
* [Dockerisation OpenCv](https://github.com/janza/docker-python3-opencv)
* [Dockerisation face_recognition](https://hub.docker.com/r/kkdai/docker-python3-opencv-face_recognition/) based on OpenCv

## Step

Assure to lauch this different commande into different terminal

'''
make managing
'''
'''
make security
'''
'''
make access
'''
make schedule
'''
make alarm
make present
make leaving
'''
* Warning *

For this to work, make sure you allow the GUI application to run with docker, we have chosen to add a local user to xhost while the application is running

'''
xhost local:root
'''
