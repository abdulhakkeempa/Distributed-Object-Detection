import torch
import cv2

model = torch.hub.load("ultralytics/yolov5", "custom","./best.pt")
video = cv2.VideoCapture('./footage.mp4')

try:
  while True:
    ret, frame = video.read()
    if not ret:
      break
    result = model(frame)
    results.print()

except Exception as e:
  print("Some error occured")
  print(e)

video.release()
