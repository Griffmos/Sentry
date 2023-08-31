#code from spsand branch

import socket
import numpy
import cv2
import struct

def recvFrame(s:socket.socket):
    data:bytes = []

    while len(data) < 921600:
        data+=s.recv(921600)

    # print(bP)
    arr = numpy.asarray(data,numpy.uint8)
    arr = numpy.reshape(arr, [480, 640, 3])

    return arr

def sendMessage(s:socket.socket):
    xcoord = struct.pack('>H', 400)
    ycoord = struct.pack('>H', 200)

    llx = struct.pack('>H', 100)
    lly = struct.pack('>H', 100)

    urx = struct.pack('>H', 800)
    ury = struct.pack('>H', 800)

    s.send(xcoord+ycoord+llx+lly+urx+ury)
    #s.send(xcoord)








def main():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',8888))
    s.listen(1)
    print("server runnig")
    print(s.getsockname())

    conn,address = s.accept()
    print(f"Connection from {address} worked!")

    
    count=0

    while True:
        arr=recvFrame(conn)
        print(arr.shape)
        #cv2.imwrite(f'frame{count}.jpg',arr)
        cv2.imshow(winname='frame',mat=arr)
        
        sendMessage(conn)





main()