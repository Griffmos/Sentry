#!/usr/bin/python3

from time import sleep
from ultralytics import YOLO

from numpysocket import NumpySocket
import cv2
import numpy

model = YOLO('yolov8n.pt')


with NumpySocket() as s:
    s.bind(('', 9999))

    s.listen(1)


    conn, addr = s.accept()
    with conn:
        print(f"connected: {addr}")

        while True:
            target=numpy.array([0,0,-1])
            frame = conn.recv()

            print("recieved data")

            if len(frame)==0:break
                
            results = model.predict(frame)

            if (len(results)>0):

                annotated_frame = results[0].plot()

                cv2.imshow('Frame', annotated_frame)

                
                boxes = getattr(results[0],'boxes')
                boxPos=getattr(boxes, 'xyxy')
                if (len(boxPos)>0):

                    x=(boxPos[0][0].item()+boxPos[0][2].item())/2
                    y=(boxPos[0][1].item()+boxPos[0][3].item())/2
                    target = [int(x),int(y),-1]

                    

                    


            print("data processed")

            # print(target)
            # encodedTarget=bytes(target)
            # print(encodedTarget)
            # print(len(encodedTarget))
                    
            # print (list(encodedTarget))

            sleep(0.1)

            target = numpy.array(target)
            
            frame[0][0]=target
            
            print(conn.sendall(frame))

            
            print("sent target")
                
            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                exit(1)
       