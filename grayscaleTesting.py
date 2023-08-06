import cv2


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 64)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,48)

ret, frame = cap.read()

grayFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


# print(grayFrame)
while(True):

    ret, frame = cap.read()

    grayFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('gray', grayFrame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
