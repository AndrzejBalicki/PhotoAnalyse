import csv
import os


class CSVExporter:

    def export(self, results):

        os.makedirs("output", exist_ok=True)

        with open("output/results.csv", "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                "file",
                "sharpness",
                "exposure",
                "noise",
                "face",
                "score",
                "normalized_score"
            ])

            for r in results:

                writer.writerow([
                    r["file"],
                    r["sharpness"],
                    r["exposure"],
                    r["noise"],
                    r["face"],
                    r["score"],
                    r.get("normalized_score", "")
                ])