import torch
import cv2
from similarity import ObjectSimilarity
from const import MODEL_PATH, VIDEO_PATH, IMAGE_PATH
import sys
import pathlib
from iot.publish import MqttClient
import random 

if sys.platform == "win32":
  temp = pathlib.PosixPath
  pathlib.PosixPath = pathlib.WindowsPath
  del temp

class CarDetection:
    def __init__(self, model_path, video_path, image_path, good_match_ratio=50, mqtt_client):
        self.model = torch.hub.load("ultralytics/yolov5", "custom", model_path)
        self.video = cv2.VideoCapture(video_path)
        self.params = {
            "image_path": image_path,
            "good_match_ratio": good_match_ratio
        }
        self.flann_param = {
            "trees": 5,
            "checks": 150
        }
        self.checker = ObjectSimilarity(**self.params)
        self.checker.process_target_image()
        self.checker.create_flann_searcher(**self.flann_param)
        self.mqtt = mqtt_client

    def detect_cars(self):
        """
        Detects cars in a given video and displays each frame.

        Args:
            None

        Returns:
            None
        """
        frame_count = 0
        try:
            while True:
                ret, frame = self.video.read()
                if not ret:
                    break

                # Skip every 3 frames
                frame_count += 1
                if frame_count % 3 != 0:
                    continue

                results = self.model(frame)

                for result in results.xyxy[0]:
                    x1, y1, x2, y2 = map(int, result[:4])
                    print(f"Found a car, checking similarity")
                    car = frame[y1:y2, x1:x2]
                    self.checker.find_match(car)
                    self.checker.lowes_ratio_test()
                    print(self.checker.is_images_similar(ratio_test=True))
                    print(len(self.checker.good_matches))

                    if self.checker.is_images_similar(ratio_test=True):
                        self.mqtt.publish("Random Location")
                        

        except Exception as e:
            print("Some error occurred")
            print(e)

    def cleanup(self):
        self.video.release()

    def run(self):
        self.detect_cars()
        self.cleanup()


broker = 'broker.emqx.io'
port = 1883
topic = "python/dob-iot"
client_id = f'publish-{random.randint(0, 100)}'


mqtt = MqttClient(broker, port, topic, client_id)
app = CarDetection(MODEL_PATH, VIDEO_PATH, IMAGE_PATH, good_match_ratio=50, mqtt_client=mqtt)
