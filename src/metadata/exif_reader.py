from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


class ExifReader:

    def get_timestamp(self, path):

        try:
            img = Image.open(path)
            exif = img._getexif()

            if exif:
                for tag, value in exif.items():
                    if TAGS.get(tag) == "DateTimeOriginal":
                        return datetime.strptime(
                            value,
                            "%Y:%m:%d %H:%M:%S"
                        )

        except Exception:
            pass

        return datetime.now()