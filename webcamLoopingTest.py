


import cv2
#using https://www.youtube.com/watch?v=FygLqV15TxQ&ab_channel=NicholasRenotte as reference

cap = cv2.VideoCapture(0)

ret, origFrame = cap.read()
print(origFrame)


#shows video
while(True): 

    ret, frame = cap.read()

    frame[0][0]=[0,0,0]

    for r in range(len(frame)):
        for c in range(10):
            frame[r][c]=[0,0,0]       



    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
