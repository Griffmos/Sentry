
# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import rollingAvg


rollingCenters=20 #number of centers in rolling avg

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



cap = cv2.VideoCapture(0)

def drawCenter(x:int, y:int, frame):
     for r in range(max(y-5,0), min(y+5, len(frame))):
                for c in range(max(x-5,0), min(x+5,len(frame[0]))):
                    frame[r][c]=[255,0,0]


#shows video

xRA=rollingAvg.rollingAvg(rollingCenters)
yRA=rollingAvg.rollingAvg(rollingCenters)


xARA=rollingAvg.rollingAvg(rollingCenters)
xBRA=rollingAvg.rollingAvg(rollingCenters)

yARA=rollingAvg.rollingAvg(rollingCenters)
yBRA=rollingAvg.rollingAvg(rollingCenters)




while(True): 

    ret, frame = cap.read()
    frame = imutils.resize(frame, height=480, width=640)

    (rects, weights) = hog.detectMultiScale(frame,hitThreshold=0.10 ,winStride=(4, 4), scale=1.05)
    print(weights)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    #currAvgCenter=[0,0] #avg center for the current frame

    for (xA, yA, xB, yB) in pick:
        # cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
       
        # print(f'xs:{xA} {xB}' )
        # print(f'maxs: {len(frame[0])} {len(frame)}')

        center=[min(int((xA+xB)/2), len(frame[0])), min(int((yA+yB)/2), len(frame))]
        xRA.addVal(center[0])
        yRA.addVal(center[1])


        xARA.addVal(xA)
        xBRA.addVal(xB)

        yARA.addVal(yA)
        yBRA.addVal(yB)

        # drawCenter(center[0], center[1],frame)

        #currAvgCenter= [currAvgCenter[0]+center[0], currAvgCenter[1]+center[1]]
    
    

    # if (len(pick)!=0):
    #     avgCenter=[int(avgCenter[0]/len(pick)), int(avgCenter[1]/len(pick))]


    #     #rolling centers down
        


    #     drawCenter(int(drawCX/rollingCenters), int(drawCY/rollingCenters), frame)

    drawCenter(xRA.avg,yRA.avg,frame)

    cv2.rectangle(frame, (xARA.avg, yARA.avg), (xBRA.avg, yBRA.avg), (0,255,0),2)



    #drawCenter(avgCenter[0], avgCenter[1],frame)


    cv2.imshow('frame', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



#code taken from https://pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/

# for imagePath in paths.list_images(args["images"]):
# 	# load the image and resize it to (1) reduce detection time
# 	# and (2) improve detection accuracy
# 	image = cv2.imread(imagePath)
# 	image = imutils.resize(image, width=min(400, image.shape[1]))
# 	orig = image.copy()
# 	# detect people in the image
# 	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
# 		padding=(8, 8), scale=1.05)
# 	# draw the original bounding boxes
# 	for (x, y, w, h) in rects:
# 		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
# 	# apply non-maxima suppression to the bounding boxes using a
# 	# fairly large overlap threshold to try to maintain overlapping
# 	# boxes that are still people
# 	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
# 	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
# 	# draw the final bounding boxes
# 	for (xA, yA, xB, yB) in pick:
# 		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
# 	# show some information on the number of bounding boxes
# 	filename = imagePath[imagePath.rfind("/") + 1:]
# 	print("[INFO] {}: {} original boxes, {} after suppression".format(
# 		filename, len(rects), len(pick)))
# 	# show the output images
# 	cv2.imshow("Before NMS", orig)
# 	cv2.imshow("After NMS", image)
# 	cv2.waitKey(0)