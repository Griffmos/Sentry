import cv2
import numpy
#using https://www.youtube.com/watch?v=FygLqV15TxQ&ab_channel=NicholasRenotte as reference

cap = cv2.VideoCapture(0)

DELTA = 50

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 64)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,48)

ret, lastFrame = cap.read()

print(len(lastFrame))
print(len(lastFrame[0]))

def isDifferent(currPixel, lastPixel, DELTA):
   diffR = abs(int(currPixel[0])-int(lastPixel[0]))
   diffG = abs(int(currPixel[1])-int(lastPixel[1]))
   diffB = abs(int(currPixel[2])-int(lastPixel[2]))

   if (diffR+diffG+diffB>DELTA):
       return True
   else:
    return False


#shows video

targetPoint: list

isTarget=False

while(True): 

    avgTarget = [[0,0],0]

    ret, frame = cap.read()

    for r in range(len(frame)):
        for c in range(len(frame[0])):
            # if (frame[r][c][0]!=origFrame[r][c][0] or  frame[r][c][1]!=origFrame[r][c][1] or frame[r][c][2]!=origFrame[r][c][2]):
            #     frame[r][c]=[0,0,0] 
            if (isDifferent(frame[r][c], lastFrame[r][c], DELTA)):
                lastFrame[r][c]=frame[r][c]
                frame[r][c]=[0,0,0]
                avgTarget=[[avgTarget[0][0]+r, avgTarget[0][1]+c], avgTarget[1]+1]
            else:
                lastFrame[r][c]=frame[r][c]
    if (avgTarget[1]>100):
        isTarget=True
        targetPoint=[avgTarget[0][0]/avgTarget[1],avgTarget[0][1]/avgTarget[1]]
    if (isTarget):
        for r in range(int(targetPoint[0])-5, int(targetPoint[0])+5):
            for c in range(int(targetPoint[1]-5), int(targetPoint[1]+5)):
                frame[r][c]=[255,0,0]
    


    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
