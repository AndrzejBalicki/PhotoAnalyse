import csv
import os


class CSVExporter:

    def export(self, results):

        os.makedirs("output", exist_ok=True)

        with open(
            "output/results.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "file",

                "sharpness_raw",
                "sharpness_norm",

                "exposure_raw",
                "exposure_norm",

                "noise_raw",
                "noise_norm",

                "face_raw",
                "face_norm",

                "score",
                "normalized_score"
            ])

            for r in results:

                writer.writerow([

                    r["file"],

                    r.get("sharpness"),
                    r.get("sharpness_norm"),

                    r.get("exposure"),
                    r.get("exposure_norm"),

                    r.get("noise"),
                    r.get("noise_norm"),

                    r.get("face"),
                    r.get("face_norm"),

                    r.get("score"),
                    r.get("normalized_score")

                ])