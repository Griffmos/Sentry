import cv2
import numpy
import time

cap = cv2.VideoCapture(0)

DELTA = 25

#step amount
rSTEP=4
cSTEP=4

SHOWFEED = True
SHOWFPS =True

FRAME_WIDTH=120
FRAME_HEIGHT=160

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)

ret, lf = cap.read()
lastFrame=cv2.cvtColor(lf, cv2.COLOR_BGR2GRAY)
gFrame:list



def isDifferent(currPixel, lastPixel, DELTA):
   diff=abs(int(currPixel)-int(lastPixel))

   if (diff>DELTA):
       return True
   else:
    return False
   
def checkAround(row:int, col:int):
    avgTarget=[[0,0],0]
    for r in range(max(row-rSTEP+1,0),min(row+rSTEP,FRAME_HEIGHT)):
            for c in range(max(col-cSTEP+1,0), min(col+cSTEP, FRAME_WIDTH)):
                if (isDifferent(gFrame[r][c], lastFrame[r][c], DELTA)):
                    lastFrame[r][c]=gFrame[r][c]
                    if (SHOWFEED):
                        gFrame[r][c]=0
                    avgTarget=[[avgTarget[0][0]+r, avgTarget[0][1]+c], avgTarget[1]+1]
                else:
                    lastFrame[r][c]=gFrame[r][c]
    return avgTarget


def showFrame(frame):
    cv2.imshow('Feed', frame)

#shows video
if (__name__=='__main__'):
    targetPoint: list

    isTarget=False

    numFrames=0

    lastTime = time.time()

    while(True): 

        avgTarget = [[0,0],0]

        ret, frame = cap.read()

        gFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        for r in range(0,len(gFrame),rSTEP):
            for c in range(0, len(gFrame[0]), cSTEP):

                if (isDifferent(gFrame[r][c], lastFrame[r][c], DELTA)):
                    lastFrame[r][c]=gFrame[r][c]
                    aroundTarget = checkAround(r,c)
                    if (SHOWFEED):
                        gFrame[r][c]=0
                    avgTarget=[[avgTarget[0][0]+r+aroundTarget[0][0], avgTarget[0][1]+c+aroundTarget[0][1]], avgTarget[1]+1+aroundTarget[1]]
                    c+=2*cSTEP

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
