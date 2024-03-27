import torch
import cv2
import pathlib
import matplotlib.pyplot as plt
import sys
from identify import ObjectSimilarity

if sys.platform == "win32":
  temp = pathlib.PosixPath
  pathlib.PosixPath = pathlib.WindowsPath
  del temp

model = torch.hub.load("ultralytics/yolov5", "custom","./best.pt")
video = cv2.VideoCapture('./footage.mp4')

params = {
    "image_path" : "./cars/car_1221.jpg",
    "good_match_ratio" : 50
}

flann_param = {
    "trees": 5,
    "checks": 150
}

checker = ObjectSimilarity(**params)
checker.process_target_image()
checker.create_flann_searcher(**flann_param)

def detect_cars(model, video):
  """
    Detects cars in a given video as display each frame.

    Args:
      model: Torch object containing Yolo model
      video: Input video for detecting cars

    Returns:
      None
  """
  frame_count = 0
  try:
    while True:
      ret, frame = video.read()
      if not ret:
        break

      # Skip every 3 frames
      frame_count += 1
      if frame_count % 3 != 0:
        continue

      results = model(frame)

      for result in results.xyxy[0]: 
        x1, y1, x2, y2 = map(int, result[:4])  
        print(f"Found a car, checking similarity")
        # frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)  
        car = frame[y1:y2, x1:x2]
        checker.find_match(car)
        checker.lowes_ratio_test()
        print(checker.is_images_similar(ratio_test=True))
        print(len(checker.good_matches))

      cv2.imshow("Vehicle Footage", frame) 
      cv2.waitKey(5)

  except Exception as e:
    print("Some error occured")
    print(e)


detect_cars(model, video)

cv2.destroyAllWindows() 
plt.show()
video.release()
