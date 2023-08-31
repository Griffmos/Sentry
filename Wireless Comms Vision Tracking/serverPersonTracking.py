import cv2 
import numpy;
from ultralytics import YOLO
import socket
import struct
import time

FRAME_BYTE_SIZE=921600

MODEL= YOLO('yolov8n.pt')

def recvFrame(s:socket.socket):
    startRecv=time.perf_counter()
    data:bytes = []

    while len(data) < 921600:
        data+=s.recv(921600-len(data))

    # print(bP)
    frame = numpy.asarray(data,numpy.uint8)
    frame = numpy.reshape(frame, [480, 640, 3])

    print(f"recv frame time: {time.perf_counter()-startRecv}")

    return frame

def sendTarget(s:socket.socket, target):
    startSend=time.perf_counter()
    print(target)
    if (type(target) is not list):
        s.sendall(bytearray([0,0,0,0,0,0,0,0,0,0,0]))
    else:
        xcoord = struct.pack('>H', int(target[0][0]))
        ycoord = struct.pack('>H', int(target[0][1]))

        llx = struct.pack('>H', int(target[1][0]))
        lly = struct.pack('>H', int(target[1][1]))

        urx = struct.pack('>H', int(target[1][2]))
        ury = struct.pack('>H', int(target[1][3]))
    
        s.sendall(xcoord+ycoord+llx+lly+urx+ury)
    print(f"send target time: {time.perf_counter()-startSend}")


def runServer():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',8888))
    s.listen(1)
    print("server running")
    print(s.getsockname())


    conn,address = s.accept()
    print(f"Connection from {address} worked!")

    while True:
        startTime=time.perf_counter()
        try:
            frame = recvFrame(conn)
        except Exception as error:
            print("error on recv, restaring")
            print(f"error: {error}")

            return -1
        recvTime=time.perf_counter()
        
        results = MODEL.track(frame, persist=True, classes=0)

        target=-1
        if (len(results)>0):
            boxes = getattr(results[0],'boxes')

            boxPos=getattr(boxes, 'xyxy')


            if (len(boxPos)>0):
                x=(boxPos[0][0].item()+boxPos[0][2].item())/2
                y=(boxPos[0][1].item()+boxPos[0][3].item())/2
                target=[[x,y], boxPos[0].tolist()]
        sendTime=time.perf_counter()
        try:
            sendTarget(conn, target)
        except Exception as error:
            print(f"error on send, restaring")
            print(f"error: {error}")
            return -1
        
        print(f"process time: {sendTime-recvTime}")
        print(f"total time: {time.perf_counter()-startTime}")
        
            


def main():
    while True:
        runServer()


main()

    


