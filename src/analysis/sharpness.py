import cv2


class SharpnessAnalyzer:

    def compute(self, img):

        if img is None:
            return 0

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return cv2.Laplacian(gray, cv2.CV_64F).var()