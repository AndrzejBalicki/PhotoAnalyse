import cv2
import os
from .raw_processor import RawProcessor


class ImageLoader:

    def __init__(self):
        self.raw_processor = RawProcessor()

    def load(self, path):

        ext = os.path.splitext(path)[1].lower()

        if ext == ".arw":
            img = self.raw_processor.process(path)

        else:
            img = cv2.imread(path)

        if img is None:
            print(f"❌ Nie udało się wczytać obrazu: {path}")

        return img