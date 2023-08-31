import cv2 
import threading
import numpy;
from ultralytics import YOLO
import socket
from time import sleep

MAX_AMT_POINTS=10
maxPointLoops=30



class tracker:


    def __init__(self, showFeed:bool, IP, PORT):
        print("inited")
        self.cap = cv2.VideoCapture(0)
        self.currFrame=None
        self.showFeed=showFeed

       

        self.points:list=[]

        self.currTarget=[]



        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((IP,PORT))
        print("connected")


        self.startFeed()
    
    def displayPoint(self, x, y):

        self.points.append([x,y, 0])

        if (len(self.points)>MAX_AMT_POINTS):
            self.points.pop(0)

    


    def runFeed(self):

        while self.cap.isOpened():



            success, frame = self.cap.read()

            self.currFrame=frame

            
            for i in range(len(self.points)):
                if (len(self.points)>i):
                    currPoint = self.points[i]
                    if (currPoint[2]<maxPointLoops):
                        currPoint[2]+=1
                        x=currPoint[0]
                        y=currPoint[1]
                        for r in range(int(max(0,y-5)), int(min(len(self.currFrame),y+5))):
                            for c in range(int(max(0,x-5)), int(min(len(self.currFrame),x+5))):
                                self.currFrame[r][c]=[0,255,0]
                    else:
                        self.points.pop(i)

            if ((len(self.currTarget))>0):
                 
                targetPoint=self.currTarget[0]
        
                for r in range(int(max(0,targetPoint[1]-5)), int(min(len(self.currFrame),targetPoint[1]+5))):
                    for c in range(int(max(0,targetPoint[0]-5)), int(min(len(self.currFrame),targetPoint[0]+5))):
                        self.currFrame[r][c]=[255,0,0]

                

            if (self.currFrame is not None and self.showFeed==True):
                cv2.imshow('currFrame', self.currFrame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.terminateTracker()


    def startFeed(self):
        print("called startfeed")
        feed = threading.Thread(target=self.runFeed)

        print("started feed")
        feed.start()




    def sendFrame(self):
        self.socket.sendall(bytearray(self.currFrame))
    
    def recieveTarget(self):
        bytes_in : bytes = []

        while len(bytes_in)<12:
            bytes_in += self.socket.recv(12-len(bytes_in))
        

        isNone:bool=True

        for byte in bytes_in:
            if (numpy.int8(byte)!=0):
                isNone=False
                break
        
        if (isNone):
            self.currTarget=None
        else:
            x = numpy.uint16(bytes_in[1]) + 256*numpy.uint16(bytes_in[0])
            y = numpy.uint16(bytes_in[3]) + 256*numpy.uint16(bytes_in[2])

            llx = numpy.uint16(bytes_in[5]) + 256*numpy.uint16(bytes_in[4])
            lly = numpy.uint16(bytes_in[7]) + 256*numpy.uint16(bytes_in[6])
            urx = numpy.uint16(bytes_in[9]) + 256*numpy.uint16(bytes_in[8])
            ury = numpy.uint16(bytes_in[11]) + 256*numpy.uint16(bytes_in[10])

            self.currTarget= [[x,y],[llx,lly,urx,ury]]

    def findTarget(self):
        if (self.currFrame is not None):
            self.sendFrame()

            self.recieveTarget()
            return True
        else:
            return False


    def terminateTracker(self):
        self.cap.release()
        cv2.destroyAllWindows()


