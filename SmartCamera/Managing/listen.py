import paho.mqtt.client as mqtt
import time

debut = 1 #allowed to quit when all video are finished
nbrVideo = 0

# --- Callback function --- #
def on_message(client, userdata, message):
	global nbrVideo
	global debut
	l = message.topic
	m = message.payload.decode("utf-8")
	if (m == "Movie sending..."):
		nbrVideo += 1
		debut = 0
	elif (m == "Recording completed"):
		nbrVideo -= 1
	print ("from "+ l[14:] +" :  " + m)


def main():
	global nbrVideo
	global debut
	#--------Client constructor----------
	client = mqtt.Client("Listen")

	#----------Connect to Broker---------
	Broker1 = "iot.eclipse.org"
	Broker2 = "test.mosquitto.org"
	try:
		client.connect(Broker1) # Brocker #
	except ConnectionRefusedError:
		client.connect(Broker2)
#---------Subscribe-----------
	client.subscribe("FaceReco/Info/#") #12

	while True :
		client.on_message = on_message #callback
		client.loop_start() # Callbacks depends on client loop
		time.sleep(0.5) #time to process the callback
		if (not debut and not nbrVideo):
			client.publish("End","Record Completed")
			time.sleep(0.5)
			break

if __name__ == "__main__":
	main()
