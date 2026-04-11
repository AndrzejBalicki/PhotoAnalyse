import numpy as np
import cv2


class ExposureAnalyzer:

    def compute(self, img):

        try:

            if img is None:
                return 0.0

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            hist = np.histogram(gray, bins=256)[0]

            total = hist.sum()

            if total == 0:
                return 0.0

            low = hist[:20].sum()
            high = hist[235:].sum()

            value = 1 - ((low + high) / total)
            value = max(0.0, min(1.0, value))

            return float(value)

        except Exception as e:

            print("❌ Exposure error:", e)

            return 0.0