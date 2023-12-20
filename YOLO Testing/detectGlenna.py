from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("yolov8m.pt")


# from ndarray
im2 = cv2.imread("C:\\Users\\griff\\OneDrive\\Documents\\Coding\\Sentry\\Images\\Glenna.jpg")
results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# from list of PIL/ndarray
#results = model.predict(source=[im1, im2])

# results would be a list of Results object including all the predictions by default
# but be careful as it could occupy a lot memory when there're many images,
# especially the task is segmentation.
# 1. return as a list

print(results)

for result in results:
    # Detection
    result.boxes.xyxy   # box with xyxy format, (N, 4)
    result.boxes.xywh   # box with xywh format, (N, 4)
    result.boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
    result.boxes.xywhn  # box with xywh format but normalized, (N, 4)
    result.boxes.conf   # confidence score, (N, 1)
    result.boxes.cls    # cls, (N, 1)


# Each result is composed of torch.Tensor by default,
# in which you can easily use following functionality:
result = result.numpy()

print(result)

