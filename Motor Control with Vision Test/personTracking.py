import cv2 
import threading
import numpy;
from ultralytics import YOLO

MAX_AMT_POINTS=10
maxPointLoops=30



class tracker:


    def __init__(self, showFeed:bool):
        print("inited")
        self.model = YOLO('yolov8n.pt')
        self.cap = cv2.VideoCapture(0)
        self.currFrame=None
        self.showFeed=showFeed


        self.points:list=[]

        self.currTarget=[]

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
                 
                target=self.currTarget[0]
        
                for r in range(int(max(0,target[1]-5)), int(min(len(self.currFrame),target[1]+5))):
                    for c in range(int(max(0,target[0]-5)), int(min(len(self.currFrame),target[0]+5))):
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

    

    def startSearch(self):


            
            if (self.currFrame is not None):


                results = self.model.track(self.currFrame, persist=True, classes=0)
                if (len(results)>0):


                    boxes = getattr(results[0],'boxes')

                    boxPos=getattr(boxes, 'xyxy')

                    #print(boxPos)

                    if (len(boxPos)>0):
                        x=(boxPos[0][0].item()+boxPos[0][2].item())/2
                        y=(boxPos[0][1].item()+boxPos[0][3].item())/2
                        self.currTarget=[[x,y], boxPos[0].tolist()]
                        print(self.currTarget)
                    else:
                        self.currTarget=[[len(self.currFrame)/2, len(self.currFrame[0])/2],[0,0,0,0]]

                    self.currFrame = results[0].plot()
                else:
                    self.currTarget=[[len(self.currFrame)/2, len(self.currFrame[0])/2],[0,0,0,0]]
                

                    
                
                    
                    
            else:
                self.currTarget=[[len(self.currFrame)/2, len(self.currFrame[0])/2], [0,0,0,0]]

            return self.currTarget  

    def terminateTracker(self):
        self.cap.release()
        cv2.destroyAllWindows()



    


