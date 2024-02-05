import os
import cv2
from pytube import YouTube
from config import URLS

count = 0

def download_video(url, filename):
    yt = YouTube(url)
    yt.streams.first().download(filename=filename)

def save_frames(filename, output_folder):
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    global count
    while success:
        if (count % 10 == 0):
            cv2.imwrite(os.path.join(output_folder, f"frame{count}.jpg"), image)
        success, image = vidcap.read()
        count += 1

output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)
for i, url in enumerate(URLS):
    filename = f"video{i}.mp4"
    download_video(url, filename)
    save_frames(filename, output_folder)
    os.remove(filename)
