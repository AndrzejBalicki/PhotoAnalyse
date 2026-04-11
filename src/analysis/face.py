import cv2

class FaceAnalyzer:
    def __init__(self):
        self.model = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def compute(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.model.detectMultiScale(gray, 1.1, 4)

        return len(faces) * 10  # im więcej twarzy tym lepiej