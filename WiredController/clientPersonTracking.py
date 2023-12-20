import cv2 
import threading
import numpy;
import socket
from time import sleep
import time

IPT = str

PRTT = int


class Tracker:


    def __init__(self, showFeed:bool, IP: IPT, PORT: PRTT):
        print("inited tracker")

        self.currTarget=[]

        self.isRunning=True






        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((IP,PORT))
        print("connected")   


    def requestTarget(self):
        self.socket.sendall("r".encode("utf-8"))

    def recieveTarget(self):
        # ~ startRecv=time.perf_counter()
        bytes_in : bytes = []

        while len(bytes_in)<4:
            try:
                bytes_in += self.socket.recv(4-len(bytes_in))
            except:
                return False
        

        isNone:bool=True
        stopReq:bool=True

        for byte in bytes_in:
            if (numpy.int8(byte)!=0):
                isNone=False
            if (numpy.int8(byte)!=1):
                stopReq=False
            if (not isNone and not stopReq):
                break
        
        
        if (stopReq):
            print("recieved a stop request")
            return False
        if (isNone):
            self.currTarget=None
        else:
            x = numpy.uint16(bytes_in[1]) + 256*numpy.uint16(bytes_in[0])
            y = numpy.uint16(bytes_in[3]) + 256*numpy.uint16(bytes_in[2])


            self.currTarget= [x,y]
        # ~ print(f"recv target time: {time.perf_counter()-startRecv}")
        return True

    def findTarget(self):
        try:
            self.requestTarget()
        except:
            print("Issue sending")
            return False

            
        return self.recieveTarget()
    
    def terminateTracker(self):
        self.currTarget=None
        self.isRunning=False
        cv2.destroyAllWindows()


