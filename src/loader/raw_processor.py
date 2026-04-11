import rawpy
import cv2


class RawProcessor:

    def process(self, path):

        try:
            with rawpy.imread(path) as raw:

                rgb = raw.postprocess()

                img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

                return img

        except Exception as e:

            print("❌ Błąd RAW:", path)
            print(e)

            return None