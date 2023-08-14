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

SHOWFEED = False

SHOWFPS =True

NUM_CORES =4

# def readRow(gRow, lRow, r):
#         avgTarget=[[0,0],0]
#         for c in range(len(gRow)):
            
#                 if (isDifferent(gRow[c], lRow[c], DELTA)):
#                     lRow[c]=gRow[c]
#                     if (SHOWFEED):
#                         gRow[c]=0
#                     avgTarget=[[avgTarget[0][0]+r, avgTarget[0][1]+c], avgTarget[1]+1]
#                 else:
#                     lRow[c]=gRow[c]
#         return (avgTarget, lRow)

def readRows(gFrame, lFrame):
    rT=0
    cT=0
    total=0
    for r in range(len(gFrame)):
        for c in range(len(gFrame[0])):
            if (isDifferent(gFrame[r][c], lFrame[r][c], DELTA)):
                lFrame[r][c]=gFrame[r][c]
                if (SHOWFEED):
                    gFrame[r][c]=0
                rT+=r
                cT+=c
                total+=1
            else:
                lFrame[r][c]=gFrame[r][c]
    return [[rT, cT], total, lFrame, gFrame]

if __name__ == '__main__':
    print("code initiated")

    cap = cv2.VideoCapture(0)




    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 64)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,48)

    ret, lf = cap.read()
    lastFrame=cv2.cvtColor(lf, cv2.COLOR_BGR2GRAY)
    lastFrame = numpy.array_split(lastFrame,4)
    #print(lastFrame)
    # print(lastFrame[0])
    # print(lastFrame[1])

    print(len(lastFrame))
    rows=len(lastFrame)
    cols=len(lastFrame[0])
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

        gFrame=numpy.array_split(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),NUM_CORES)


        with concurrent.futures.ProcessPoolExecutor() as executor:
            #hard coded for 4 cores

            results = executor.map(readRows, gFrame, lastFrame) 

            f=0
            for res in results:

                totalAvgTarget[0][0]+=res[0][0]
                totalAvgTarget[0][1]+=res[0][1]
                totalAvgTarget[1]+=res[1]
                lastFrame[f]=res[2]
                gFrame[f]=res[3]
                f+=1

        totalAvgTarget[0][0]+=rows*1.5
        totalAvgTarget[0][1]+=cols*1.5



 

        if (totalAvgTarget[1]>100):
            isTarget=True
            targetPoint=[totalAvgTarget[0][0]/totalAvgTarget[1],totalAvgTarget[0][1]/totalAvgTarget[1]]
        if (isTarget):
            if (SHOWFEED):
                sFrame=numpy.append(numpy.append(gFrame[0], gFrame[1]),numpy.append(gFrame[2],gFrame[3]))
                for r in range(max(int(targetPoint[0])-5,0), min(int(targetPoint[0])+5, len(gFrame))):
                    for c in range(max(int(targetPoint[1])-5,0), min(int(targetPoint[1]+5),len(gFrame[0]))):
                        sFrame[r][c]=255
                showFrame(sFrame)
            if(SHOWFPS):
                numFrames+=1
                if (time.time()-lastTime>=1):
                    print(numFrames)
                    lastTime=time.time()
                    numFrames=0


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
