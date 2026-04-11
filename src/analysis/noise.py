import cv2
import numpy as np

class NoiseAnalyzer:
    def compute(self, img):

        if img is None:
            return 0

        blur = cv2.GaussianBlur(img, (3,3), 0)
        return np.mean((img - blur) ** 2)