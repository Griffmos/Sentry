import cv2 
from ultralytics import YOLO


class tracker:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.cap = cv2.VideoCapture(0)
        self.currFrame=None

    

        

    def startSearch(self):
        while self.cap.isOpened():

            success, frame = self.cap.read()

            self.currFrame=frame

            target=None

            if success:


                results = self.model.track(frame, persist=True, classes=0)
                if (len(results)>0):


                    boxes = getattr(results[0],'boxes')

                    boxPos=getattr(boxes, 'xyxy')

                    #print(boxPos)

                    if (len(boxPos)>0):
                        x=(boxPos[0][0].item()+boxPos[0][2].item())/2
                        y=(boxPos[0][1].item()+boxPos[0][3].item())/2
                        target=[x,y]
                        #print(target)

                        for r in range(int(max(0,y-5)), int(min(len(frame),y+5))):
                            for c in range(int(max(0,x-5)), int(min(len(frame),x+5))):
                                frame[r][c]=[255,0,0]

                    
                    self.currFrame = results[0].plot()

                    
                

                if (self.currFrame is not None):
                    cv2.imshow('currFrame', self.currFrame)
                    
            if (target is not None):
                return target
                
        

    def terminateTracker(self):
        self.cap.release()



    


