import socket
import struct         
import cv2                
from time import sleep
import numpy


def send_frame(arr:numpy.ndarray, s:socket.socket):
    s.sendall(bytearray(arr))

def recieve_uint16(s:socket.socket):
    bytes_in : bytes = []

    while len(bytes_in)<12:
        bytes_in += s.recv(12)
    
    x = numpy.uint16(bytes_in[1]) + 256*numpy.uint16(bytes_in[0])
    y = numpy.uint16(bytes_in[3]) + 256*numpy.uint16(bytes_in[2])

    llx = numpy.uint16(bytes_in[5]) + 256*numpy.uint16(bytes_in[4])
    lly = numpy.uint16(bytes_in[7]) + 256*numpy.uint16(bytes_in[6])
    urx = numpy.uint16(bytes_in[9]) + 256*numpy.uint16(bytes_in[8])
    ury = numpy.uint16(bytes_in[11]) + 256*numpy.uint16(bytes_in[10])

    return [x,y,llx,lly,urx,ury]

def main():


    cap = cv2.VideoCapture(0)


    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    s.connect(('192.168.1.96',8888))
    print("connected")


    while True:
        ret, frame =cap.read()

        send_frame(frame,s)

        ping_back = recieve_uint16(s)
        print(ping_back)

main()

