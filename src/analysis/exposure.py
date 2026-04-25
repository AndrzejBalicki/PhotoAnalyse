import cv2
import numpy as np


class ExposureAnalyzer:

    def compute(self, img):

        if img is None:
            return 0.0

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        # ---------------------------------
        # 1. exposure_raw (0–1)
        # ---------------------------------

        mean = np.mean(gray)

        exposure_raw = mean / 255.0

        # ---------------------------------
        # 2. jakość względem optimum 0.5
        # ---------------------------------

        brightness_quality = 1 - 2 * abs(
            exposure_raw - 0.5
        )

        if brightness_quality < 0:
            brightness_quality = 0.0

        # ---------------------------------
        # 3. clipping penalty
        # ---------------------------------

        overexposed = np.sum(gray >= 250)
        underexposed = np.sum(gray <= 5)

        total = gray.size

        clipping_ratio = (
            overexposed + underexposed
        ) / total

        clipping_penalty = 1 - clipping_ratio

        # ---------------------------------
        # 4. final score
        # ---------------------------------

        score = (
            0.7 * brightness_quality
            + 0.3 * clipping_penalty
        )

        score = max(0.0, min(1.0, score))

        return float(score)