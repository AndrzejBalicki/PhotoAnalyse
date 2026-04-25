import rawpy
import cv2


class RawProcessor:

    def process(self, path):

        try:

            with rawpy.imread(path) as raw:

                rgb = raw.postprocess(

                    use_auto_wb=False,
                    use_camera_wb=True,

                    no_auto_bright=True,
                    auto_bright_thr=0.0,

                    gamma=(1, 1),

                    output_bps=8

                )

                img = cv2.cvtColor(
                    rgb,
                    cv2.COLOR_RGB2BGR
                )

                return img

        except Exception as e:

            print("RAW error:", path)
            print(e)

            return None