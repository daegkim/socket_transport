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

#buffer에 나눠서 담기는 것들을 전부 하나로 모아서 가져오도록 한다.
def recv_all(count):
    buf = b''
    while count:
        #버퍼 하나의 사이즈는 반드시 count/(2^n)인 값이 와야 한다.
        #물론 버퍼 하나의 사이즈가 count 자체이면 제일 빠르고 좋다.
        newbuf = conn.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

#영상의 shape과 size를 반환
def get_shape_and_size(s):
    shape = ()
    start=1
    end=0
    for i in s:
        if i==',' or i==')':
            tmp_tup = (int(s[start:end]),)
            shape+=tmp_tup
            start=end+2
        end+=1
    size = 1
    for i in shape:
        size*=i
    return shape, size

#영상을 받는 함수
def gettingVideo():
    data = conn.recv(1024)
    data = data.decode()
    shape, size = get_shape_and_size(data)
    while True:
        data = recv_all(size) #921600 = 480*640*3
        byte_to_numpy = numpy.frombuffer(data, numpy.uint8).reshape(shape)
        cv2.imshow('client to server',byte_to_numpy)
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
