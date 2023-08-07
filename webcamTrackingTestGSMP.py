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
    cv2.imshow('Feed', )


DELTA = 50

SHOWFEED = True

SHOWFPS =True

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
            #   if (SHOWFEED):
            #       gFrame[r][c]=0
                rT+=r
                cT+=c
                total+=1
            else:
                lFrame[r][c]=gFrame[r][c]
    return [[rT, cT], total]

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

        gFrame=numpy.array_split(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),4)


        with concurrent.futures.ProcessPoolExecutor() as executor:
            #hard coded for 4 cores
            t = executor.submit(readRows, gFrame[0], lastFrame[0])
            m1= executor.submit(readRows, gFrame[1], lastFrame[1])
            m2= executor.submit(readRows, gFrame[2], lastFrame[3])
            b= executor.submit(readRows, gFrame[3], lastFrame[3])
            print('submits done')

            tRes = t.result()
            m1Res =m1.result()
            m2Res =m2.result()
            bRes = b.result()
            print('results in')

            totalAvgTarget[0][0]=tRes[0][0]+m1Res[0][0]+m2Res[0][0]+bRes[0][0]+(rows*1.5)
            totalAvgTarget[0][1]=tRes[0][1]+m1Res[0][1]+m2Res[0][1]+bRes[0][1]+(rows*1.5)
            totalAvgTarget[1]=tRes[1]+m1Res[1]+m2Res[1]+bRes[1]











            

        if (totalAvgTarget[1]>100):
            isTarget=True
            targetPoint=[totalAvgTarget[0][0]/totalAvgTarget[1],totalAvgTarget[0][1]/totalAvgTarget[1]]
        if (isTarget):
            # if (SHOWFEED):
            #     frame = numpy.concatenate(numpy.concatenate(gFrame[0],gFrame[1]),numpy.concatenate(gFrame[2],gFramerame[3]))
            #     for r in range(int(targetPoint[0])-5, int(targetPoint[0])+5):
            #         for c in range(int(targetPoint[1]-5), int(targetPoint[1]+5)):
            #             frame[r][c]=255
            #     showFrame(frame)
            if(SHOWFPS):
                numFrames+=1
                if (time.time()-lastTime>=1):
                    print(numFrames)
                    lastTime=time.time()
                    numFrames=0


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
