import cv2
import numpy
import time
import concurrent.futures


def isDifferent(currPixel, lastPixel, DELTA):
   diff=abs(int(currPixel)-int(lastPixel))

   if (diff>DELTA):
       return True
   else:
    return False

def showFrame(frame):
    cv2.imshow('Feed', frame)


DELTA = 50

SHOWFEED = True

SHOWFPS =True

def readRow(gRow, lRow, r):
        avgTarget=[[0,0],0]
        for c in range(len(gRow)):
            
                if (isDifferent(gRow[c], lRow[c], DELTA)):
                    lRow[c]=gRow[c]
                    if (SHOWFEED):
                        gRow[c]=0
                    avgTarget=[[avgTarget[0][0]+r, avgTarget[0][1]+c], avgTarget[1]+1]
                else:
                    lRow[c]=gRow[c]
        return (avgTarget, lRow)


if __name__ == '__main__':
    print("code initiated")

    cap = cv2.VideoCapture(0)




    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 64)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,48)

    ret, lf = cap.read()
    lastFrame=cv2.cvtColor(lf, cv2.COLOR_BGR2GRAY)

    print(len(lastFrame))
    print(len(lastFrame[0]))



    #shows video

    targetPoint: list

    isTarget=False

    numFrames=0

    lastTime = time.time()


    avgTarget: list


    

    while(True): 

        totalAvgTarget = [[0,0],0]

        ret, frame = cap.read()

        gFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(readRow, gFrame[range(len(gFrame))], lastFrame[range(len(lastFrame))], range(len(gFrame)))

            row=0
            for res in results:

                lastFrame[row]=res[1]
                row+=1
                totalAvgTarget[0][0]+=res[0][0][0]
                totalAvgTarget[0][1]+=res[0][0][1]
                totalAvgTarget[1]+=res[0][1]


            

        if (totalAvgTarget[1]>100):
            isTarget=True
            targetPoint=[totalAvgTarget[0][0]/totalAvgTarget[1],totalAvgTarget[0][1]/totalAvgTarget[1]]
        if (isTarget):
            if (SHOWFEED):
                for r in range(int(targetPoint[0])-5, int(targetPoint[0])+5):
                    for c in range(int(targetPoint[1]-5), int(targetPoint[1]+5)):
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
