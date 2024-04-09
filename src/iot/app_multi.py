import torch
import cv2
from similarity import ObjectSimilarity
from const import MODEL_PATH, VIDEO_PATH, IMAGE_PATH
import sys
import pathlib
import threading
from publish import MqttClient
import random
import os

if not os.getenv("DEVICE"):
  raise Exception("DEVICE value not set which is essential for sending data to MQTT Client, run `export DEVICE=<with_your_device_id>`")

if sys.platform == "win32":
  temp = pathlib.PosixPath
  pathlib.PosixPath = pathlib.WindowsPath
  del temp

class CarDetection:
    def __init__(self, model_path, video_path, image_path, mqtt_client, good_match_ratio=50, batch_size=5):
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

        self.batch_size = batch_size
        self.frame_buffer = []  # Buffer to hold frames for batch processing
        self.lock = threading.Lock()  # Lock for thread safety

        self.mqtt = mqtt_client

    def process_frame_batch(self, frame_batch):
        # Process a batch of frames using the car detection model
        results = self.model(frame_batch)
        car_boxes = []
        for result in results.xyxy[0]:
            x1, y1, x2, y2 = map(int, result[:4])
            car_boxes.append((x1, y1, x2, y2))
        return car_boxes

    def process_frames(self):
        while True:
            with self.lock:
                if len(self.frame_buffer) >= self.batch_size:
                    frame_batch = self.frame_buffer[:self.batch_size]
                    del self.frame_buffer[:self.batch_size]
                else:
                    frame_batch = self.frame_buffer[:]

            if frame_batch:
                car_boxes = self.process_frame_batch(frame_batch)
                for car_box in car_boxes:
                    x1, y1, x2, y2 = car_box
                    car = frame_batch[0][y1:y2, x1:x2]
                    self.checker.find_match(car)
                    self.checker.lowes_ratio_test()
                    print(f"Similarity: {self.checker.is_images_similar(ratio_test=True)}")
                    print(f"Good Matches: {len(self.checker.good_matches)}")

                    if self.checker.is_images_similar(ratio_test=True):
                        print(f"Sending Data")
                        self.mqtt.send_data(os.getenv("DEVICE"))


    def capture_frames(self):
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

                with self.lock:
                    self.frame_buffer.append(frame)

        except Exception as e:
            print("Some error occurred")
            print(e)

    def start_threads(self):
        capture_thread = threading.Thread(target=self.capture_frames)
        process_thread = threading.Thread(target=self.process_frames)

        capture_thread.start()
        process_thread.start()

        capture_thread.join()
        process_thread.join()


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

        except Exception as e:
            print("Some error occurred")
            print(e)

    def cleanup(self):
        self.video.release()

    def run(self):
        self.start_threads()
        self.cleanup()

mqtt = MqttClient('broker.emqx.io', 1883, 'python/dob-iot', f'publish-{random.randint(0, 100)}')
app = CarDetection(MODEL_PATH, VIDEO_PATH, IMAGE_PATH, good_match_ratio=20, mqtt_client=mqtt)
