import cv2 
import threading
from ultralytics import YOLO


class tracker:

    

    def __init__(self, showFeed:bool):
        print("inited")
        self.model = YOLO('yolov8n.pt')
        self.cap = cv2.VideoCapture(0)
        self.currFrame=None
        self.showFeed=showFeed

        self.currTarget=[]

        self.startFeed()



    def runFeed(self):

        while self.cap.isOpened():


            success, frame = self.cap.read()

            self.currFrame=frame

            if ((len(self.currTarget))>0):
                 
                 target=self.currTarget
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
        while True:


            


            if (self.currFrame is not None):



                results = self.model.track(self.currFrame, persist=True, classes=0)
                if (len(results)>0):


                    boxes = getattr(results[0],'boxes')

                    boxPos=getattr(boxes, 'xyxy')

                    #print(boxPos)

                    if (len(boxPos)>0):
                        x=(boxPos[0][0].item()+boxPos[0][2].item())/2
                        y=(boxPos[0][1].item()+boxPos[0][3].item())/2
                        self.currTarget=[x,y]
                        #print(target)

                        

                    
                    self.currFrame = results[0].plot()
                else:
                    self.currTarget=[]

                    
                
                    
            if (len(self.currTarget)>0):
                return self.currTarget
                
        

    def terminateTracker(self):
        self.cap.release()
        cv2.destroyAllWindows()



    


