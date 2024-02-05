import cv2
import os
import time

image_folder = 'frames'

image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

cv2.namedWindow('Object Detection Dataset', cv2.WINDOW_NORMAL)

for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    frame = cv2.imread(image_path)

    if frame is not None:
        cv2.imshow('Image Viewer', frame)
        cv2.waitKey(500)  
    else:
        print(f"Error loading image: {image_file}")

cv2.destroyAllWindows()
