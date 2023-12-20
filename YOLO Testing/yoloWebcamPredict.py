#from https://docs.ultralytics.com/modes/predict/#streaming-source-for-loop

import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')


# Open the video file
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)

    print(len(bytearray(frame)))

    if success:
        # Run YOLOv8 inference on the frame
        results = model.predict(source=frame, conf=0.70)

        #print(results)

        target=[0,0]

        if (len(results)>0):

            boxes = getattr(results[0],'boxes')

            boxPos=getattr(boxes, 'xyxy')

            print(boxPos)

            if (len(boxPos)>0):
                x=(boxPos[0][0].item()+boxPos[0][2].item())/2
                y=(boxPos[0][1].item()+boxPos[0][3].item())/2
                target=[x,y]
                print(target)

                for r in range(int(max(0,y-5)), int(min(len(frame),y+5))):
                    for c in range(int(max(0,x-5)), int(min(len(frame),x+5))):
                        frame[r][c]=[255,0,0]




            
            

            



        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
