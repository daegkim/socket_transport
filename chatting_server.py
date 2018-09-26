import socket
import threading
import numpy
import cv2
HOST = ''
PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

def recv_all(sock, count):
    buf = b''
    while count:
        newbuf = conn.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def gettingVideo():
    while True:
        data = conn.recv(921600)
        byte_to_numpy = numpy.frombuffer(data, numpy.uint8).reshape(480,640,3)
        cv2.imshow('hi',byte_to_numpy)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    s.close()

#String형 주고 받는 채팅
def sendingMsg():
    while True:
        data = input()
        data = data.encode()
        conn.send(data)
    conn.close()

def gettingMsg():
    while True:
        data = conn.recv(1024)
        print(f'client : {data.decode()}')
    conn.close()

threading._start_new_thread(gettingVideo,())
threading._start_new_thread(sendingMsg,())
#threading._start_new_thread(gettingMsg,())

while True:
    pass
