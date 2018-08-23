import socket
import cv2

# --- Socket connection --- #
s = socket.socket()                 # Create a socket object
s.bind(("", 60000))                   # Bind to first port available
s.listen(5)                         # Now wait for client connection.

# --- Send Movie --- #
cap = cv2.VideoCapture("Video/Alarme.mp4")
while (cap.isOpened()):
    ret, frame = cap.read()
    # Quit when the input video file ends
    if not ret:
        break
    conn, addr = s.accept()
    test = cv2.imwrite('test.jpg',frame)
    f = open('test.jpg','rb')
    l = f.read(1024)
    while (l):
        conn.send(l)
        l = f.read(1024)
    f.close()
    conn.close()
cap.release()
os.system("rm *.jpg")
