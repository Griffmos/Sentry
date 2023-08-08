import cv2
import numpy
import time


#dont think I did anything with this


















cap = cv2.VideoCapture(0)

DELTA = 25

SHOWFEED = True
SHOWFPS =False

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 64)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,48)

ret, lf = cap.read()
lastFrame=cv2.cvtColor(lf, cv2.COLOR_BGR2GRAY)

print(len(lastFrame))
print(len(lastFrame[0]))

def isDifferent(currPixel, lastPixel, DELTA):
   diff=abs(int(currPixel)-int(lastPixel))

   if (diff>DELTA):
       return True
   else:
    return False

def showFrame(frame):
    cv2.imshow('Feed', frame)

#shows video

targetPoint: list

isTarget=False

numFrames=0

lastTime = time.time()

while(True): 

    avgTarget = [[0,0],0]

    ret, frame = cap.read()

    gFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    for r in range(len(gFrame)):
        for c in range(len(gFrame[0])):
            #
            if (isDifferent(gFrame[r][c], lastFrame[r][c], DELTA)):
                lastFrame[r][c]=gFrame[r][c]
                if (SHOWFEED):
                    gFrame[r][c]=0
                avgTarget=[[avgTarget[0][0]+r, avgTarget[0][1]+c], avgTarget[1]+1]
            else:
                lastFrame[r][c]=gFrame[r][c]
    if (avgTarget[1]>25):
        isTarget=True
        targetPoint=[avgTarget[0][0]/avgTarget[1],avgTarget[0][1]/avgTarget[1]]
    if (isTarget):
        if (SHOWFEED):
            for r in range(max(int(targetPoint[0])-5,0), min(int(targetPoint[0])+5, len(gFrame))):
                for c in range(max(int(targetPoint[1])-5,0), min(int(targetPoint[1]+5),len(gFrame[0]))):
                    gFrame[r][c]=255
            showFrame(gFrame)
        if(SHOWFPS):
            numFrames+=1
            if (time.time()-lastTime>=1):
                print(numFrames)
                lastTime=time.time()
                numFrames=0


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
