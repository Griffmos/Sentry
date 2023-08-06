import cv2
import numpy
#using https://www.youtube.com/watch?v=FygLqV15TxQ&ab_channel=NicholasRenotte as reference

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 64)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,48)

ret, origFrame = cap.read()

print(len(origFrame))
print(len(origFrame[0]))

orig = numpy.zeros((len(origFrame), len(origFrame[0])),dtype=int)

print(len(orig))
print(len(orig[0]))

count =0

for r in range(len(orig)):
    for c in range(len(orig[0])):
            red:int
            if (origFrame[r][c][0]==0):
                red=1
            else:
                red= origFrame[r][c][0]

            green:int
            if (origFrame[r][c][1]==0):
                green=1
            else:
                green= origFrame[r][c][1]

            blue:int
            if (origFrame[r][c][2]==0):
                blue=1

            else:
                blue= origFrame[r][c][2]


            # if ((int(red)*int(green)*int(blue))==0):
            #     print(red," ",green," ",blue)

            orig[r][c]=int(red)*int(green)*int(blue)

            # orig[r][c]=origFrame[r][c][0]*origFrame[r][c][1]*origFrame[r][c][2]

            count+=1
print(orig)
print(count)

def isDifferent(currPixel, r, c):
   currPixelVal:int
   currPixelVal = int(currPixel[0])*int(currPixel[1])*int(currPixel[2])

   

   if (abs(currPixelVal-orig[r][c]>2000000)):
       return True
   else:
        return False


#shows video
while(True): 


    ret, frame = cap.read()

    for r in range(len(frame)):
        for c in range(len(frame[0])):
            # if (frame[r][c][0]!=origFrame[r][c][0] or  frame[r][c][1]!=origFrame[r][c][1] or frame[r][c][2]!=origFrame[r][c][2]):
            #     frame[r][c]=[0,0,0] 
            if (isDifferent(frame[r][c],r,c)):
                frame[r][c]=[0,0,0]



    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
