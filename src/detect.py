import torch
import cv2
import pathlib
import matplotlib.pyplot as plt
import sys

if sys.platform == "win32":
  temp = pathlib.PosixPath
  pathlib.PosixPath = pathlib.WindowsPath
  del temp

model = torch.hub.load("ultralytics/yolov5", "custom","./best.pt", force_reload = True)
video = cv2.VideoCapture('./footage.mp4')

frame_count = 0
try:
  while True:
    ret, frame = video.read()
    if not ret:
      break

    # Skip every 10 frames
    frame_count += 1
    if frame_count % 3 != 0:
      continue

    results = model(frame)

    for result in results.xyxy[0]: 
      x1, y1, x2, y2 = map(int, result[:4])  
      frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)  

    cv2.imshow("Vehicle Footage", frame) 
    cv2.waitKey(5)

except Exception as e:
  print("Some error occured")
  print(e)

cv2.destroyAllWindows() 
plt.show()
video.release()
