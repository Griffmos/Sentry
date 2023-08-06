import cv2
#using https://www.youtube.com/watch?v=FygLqV15TxQ&ab_channel=NicholasRenotte as reference

cap = cv2.VideoCapture(0)


#testing downscaling

# ret, frame = cap.read(0)



# def rescale_frame(frame, percent):
#     width = int(frame.shape[1] * percent/ 100)
#     height = int(frame.shape[0] * percent/ 100)
#     dim = (width, height)
#     return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


# frameD = rescale_frame(frame, 100)

# print(len(frameD))
# print(len(frameD[0]))

# cv2.imshow('im',frameD)


#shows video
while(True): 

    ret, frame = cap.read()



    cv2.imshow('frame', frame)

    # frame75 = rescale_frame(frame, percent=10)

    # cv2.imshow('frame75', frame75) 


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



