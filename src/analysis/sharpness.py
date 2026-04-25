import cv2
import numpy as np


class SharpnessAnalyzer:

    def compute(self, img):

        if img is None:
            return 0.0

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        # gradient

        gx = cv2.Sobel(
            gray,
            cv2.CV_64F,
            1,
            0,
            ksize=3
        )

        gy = cv2.Sobel(
            gray,
            cv2.CV_64F,
            0,
            1,
            ksize=3
        )

        gradient_energy = np.mean(
            gx**2 + gy**2
        )

        # ---------------------------------
        # clipping penalty
        # ---------------------------------

        clipped = np.sum(gray >= 250)

        clipping_ratio = clipped / gray.size

        penalty = 1 - clipping_ratio

        sharpness = gradient_energy * penalty

        sharpness = np.log1p(sharpness)

        return float(sharpness)