import socket
import threading
import numpy as np
import cv2
import pickle
import numpy
HOST = "127.0.0.1"
PORT = 8089
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def sendingVideo():
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        numpy_to_bytes = frame.tobytes()
        #s.send(str(len(stringData)).ljust(16).encode())
        s.send(numpy_to_bytes)
    s.close()

    capture.release()
    cv2.destroyAllWindows()

def sendingMsg():
    while True:
        data = input()
        s.send(data.encode())
    s.close()

def gettingMsg():
    while True:
        data = s.recv(1024)
        print(f'server : {data.decode()}')
    s.close()

threading._start_new_thread(sendingVideo,())
#threading._start_new_thread(sendingMsg,())
threading._start_new_thread(gettingMsg,())

while True:
    pass
