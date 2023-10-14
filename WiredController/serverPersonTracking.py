import threading
import cv2 
import numpy;
from ultralytics import YOLO
import socket
import struct
import time
from time import sleep
import keyboard

#FRAME_BYTE_SIZE=57600

#TIME_OUT=5 #time out time in seconds

INIT_WAIT=15 #amount of time the server waits until first recieving data

MODEL= YOLO('yolov8n.pt')

MAX_AMT_POINTS=10

MAX_POINTS_LOOPS=30




run=True
connection=None
cap = None
showFeed = None
points = None

currTarget = None
currFrame=None

def quit():    

    print("tried to quit")
    global run
    run = False




def init(sF:bool):
    print("inited tracker")

    keyboard.add_hotkey("q",quit)


    global cap
    cap = cv2.VideoCapture(0)

    global currFrame
    currFrame=None

    global showFeed
    showFeed=sF

       
    global points
    points:list=[]

    global currTarget

    currTarget=[]



    startTracking()


def findTarget(frame):

    results = MODEL.track(frame, persist=True, classes=0, conf=0.70 )

    target=-1
    if (len(results)>0):
        boxes = getattr(results[0],'boxes')

        boxPos=getattr(boxes, 'xyxy')


        if (len(boxPos)>0):
            x=(boxPos[0][0].item()+boxPos[0][2].item())/2
            y=(boxPos[0][1].item()+boxPos[0][3].item())/2
            target=[x,y]

    return target


def runTracker():
        
        global MAX_POINTS_LOOPS

        
        global cap
        global currFrame
        global points
        global showFeed
        global currTarget
        

        while cap.isOpened():



            success, frame = cap.read()
            if success:

                frame = cv2.resize(frame, (160,120), interpolation=cv2.INTER_AREA)

                currFrame=frame

                currTarget = findTarget(currFrame)

                
                for i in range(len(points)):
                    if (len(points)>i):
                        currPoint = points[i]
                        if (currPoint[2]<MAX_POINTS_LOOPS):
                            currPoint[2]+=1
                            x=currPoint[0]
                            y=currPoint[1]
                            for r in range(int(max(0,y-5)), int(min(len(currFrame),y+5))):
                                for c in range(int(max(0,x-5)), int(min(len(currFrame),x+5))):
                                    currFrame[r][c]=[0,255,0]
                        else:
                            points.pop(i)

                if (currTarget is not None and (len(currTarget))>0):
                     
                    targetPoint=currTarget
            
                    for r in range(int(max(0,targetPoint[1]-5)), int(min(len(currFrame),targetPoint[1]+5))):
                        for c in range(int(max(0,targetPoint[0]-5)), int(min(len(currFrame),targetPoint[0]+5))):
                            currFrame[r][c]=[255,0,0]

                    

                if (currFrame is not None and showFeed==True):
                    cv2.imshow('currFrame', currFrame)



def startTracking(self):
        print("called startfeed")
        feed = threading.Thread(target=runTracker)

        print("started feed")
        feed.start()




def sendTarget(s:socket.socket, target):
    startSend=time.perf_counter()
    print(target)
    if (type(target) is not list):
        s.sendall(bytearray([0,0]))
    else:
        xcoord = struct.pack('>H', int(target[0][0]))
        ycoord = struct.pack('>H', int(target[0][1]))

        s.sendall(xcoord+ycoord)
    print(f"send target time: {time.perf_counter()-startSend}")


def parseTargetRequest(s:socket.socket):
    startRecv=time.perf_counter()
    data:bytes = []

    while len(data) == 0:
        data+=s.recv(4096)
    return True


def runServer():

    global run
    global currTarget
    
    print()
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',8888))
    s.listen(1)
    print("server running")
    print(s.getsockname())


    conn,address = s.accept()
    print(f"Connection from {address} worked!")
    run = True

    sleep(INIT_WAIT)
    print("wait over")

    while run:
        
        parseTargetRequest()

        sendTime=time.perf_counter()


        try:
            sendTarget(conn,currTarget)
        except Exception as error:
            print(f"error on send, restaring")
            print(f"error: {error}")
            return -1
        
        
    print("shutdown from server, restarting")
    conn.sendall(bytearray([1,1,1,1,1,1,1,1,1,1,1,1]))
    return -1


def main():
    init()
    while True:
        runServer()


main()

    


