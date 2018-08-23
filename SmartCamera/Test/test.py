
import cv2
import socket

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 30.0, (640,480))

while True:
    s = socket.socket()
    try:
        s.connect(("", 60000))
    except ConnectionRefusedError:
        break

    fp = 'file.jpg'

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
    frame = cv2.imread(fp)
    out.write(frame)

    cv2.imshow('frame',frame)

    cv2.waitKey(1)

    s.close()

s.close()
cap.release()
out.release()
cv2.destroyAllWindows()
