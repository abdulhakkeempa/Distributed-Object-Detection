import cv2

class ObjectSimilarity:
    def __init__(self, 
                 image_path, 
                 good_match_ratio=50, 
                 ):
        self.sift = cv2.SIFT_create()
        self.target_image = self.load_image(image_path)
        self.good_match_ratio = int(good_match_ratio)
        self.good_matches = []

    def create_flann_searcher(self, algorithm=0, trees=5, checks=50):
        index_params = dict(algorithm=algorithm, trees=trees)
        search_params = dict(checks=checks)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

    def load_image(self, image_path):
        target_image = cv2.imread(image_path)
        return target_image
    
    def process_target_image(self):
        keypoint, self.descriptor = self.compute_descriptor(self.target_image)
        del keypoint

    def compute_descriptor(self, image):
        keypoint, descriptor = self.sift.detectAndCompute(image, None)
        return keypoint, descriptor

    def find_match(self, compare_image, k=2):
        kp, des = self.compute_descriptor(compare_image)
        self.matches = self.flann.knnMatch(self.descriptor, des, k=k)
        del kp, des

    def lowes_ratio_test(self):
        self.good_matches = []
        for m, n in self.matches:
            if m.distance < 0.75 * n.distance:
                self.good_matches.append(m)

    def is_images_similar(self, ratio_test = False):
        if ratio_test:
            return True if len(self.good_matches) > self.good_match_ratio else False
        return True if len(self.matches) > self.no_of_matches else False