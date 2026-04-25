import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from src.loader.image_loader import ImageLoader
from src.metadata.exif_reader import ExifReader
from src.grouping.burst_grouper import BurstGrouper

from src.analysis.sharpness import SharpnessAnalyzer
from src.analysis.exposure import ExposureAnalyzer
from src.analysis.noise import NoiseAnalyzer
from src.analysis.face import FaceAnalyzer

from src.scoring.scorer import Scorer
from src.scoring.normalizer import normalize_scores

from src.selection.selector import select_best
from src.output.file_manager import handle_output
from src.output.exporter import CSVExporter

from src.utils.normalization import min_max_normalize
from src.utils.exposure import exposure_quality

import config


# -----------------------------
# Worker dla jednego zdjęcia
# -----------------------------
def process_image(file):

    loader = ImageLoader()
    img = loader.load(file)

    sharp = SharpnessAnalyzer().compute(img)
    expo = ExposureAnalyzer().compute(img)
    noise = NoiseAnalyzer().compute(img)
    face = FaceAnalyzer().compute(img)

    return {
        "file": file,
        "sharpness": sharp,
        "exposure": expo,
        "noise": noise,
        "face": face
    }


# -----------------------------
# Główna funkcja
# -----------------------------
def main(folder):

    valid_ext = (".jpg", ".jpeg", ".png", ".arw")

    files = sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(valid_ext)
    ])

    if not files:
        print("Brak plików w folderze.")
        return

    exif = ExifReader()
    timestamps = [exif.get_timestamp(f) for f in files]

    groups = BurstGrouper().group(files, timestamps)

    all_results = []

    scorer = Scorer()

    for group in groups:

        print(f"\nSeria: {len(group)} zdjęć")

        with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:

            results_data = list(
                tqdm(
                    executor.map(process_image, group),
                    total=len(group)
                )
            )

        # ------------------------------------
        # NORMALIZACJA METRYK (kluczowa zmiana)
        # ------------------------------------

        sharp_vals = [r["sharpness"] for r in results_data]
        expo_vals = [r["exposure"] for r in results_data]
        noise_vals = [r["noise"] for r in results_data]
        face_vals = [r["face"] for r in results_data]

        # odwrócenie logiki noise (mniej szumu = lepiej)

        noise_vals = [
            1 / (1 + v)
            for v in noise_vals
        ]

        sharp_norm = min_max_normalize(sharp_vals)
        expo_norm = [
            exposure_quality(v)
            for v in expo_vals
        ]
        noise_norm = min_max_normalize(noise_vals)
        face_norm = min_max_normalize(face_vals)

        # ------------------------------------
        # LICZENIE SCORE Z NORMALIZOWANYCH DANYCH
        # ------------------------------------

        scores = []

        for i in range(len(results_data)):

            norm_metrics = {
                "sharpness": sharp_norm[i],
                "exposure": expo_norm[i],
                "noise": noise_norm[i],
                "face": face_norm[i]
            }

            score = scorer.compute(norm_metrics)

            results_data[i]["sharpness_norm"] = sharp_norm[i]
            results_data[i]["exposure_norm"] = expo_norm[i]
            results_data[i]["noise_norm"] = noise_norm[i]
            results_data[i]["face_norm"] = face_norm[i]
            results_data[i]["score"] = score

            scores.append(score)

        # ------------------------------------
        # NORMALIZACJA KOŃCOWA (ranking w serii)
        # ------------------------------------

        norm_scores = normalize_scores(scores)

        best_idx = select_best(norm_scores)

        # ------------------------------------
        # ZAPIS PLIKÓW
        # ------------------------------------

        for i, data in enumerate(results_data):

            handle_output(
                data["file"],
                norm_scores[i],
                i == best_idx
            )

        for i in range(len(results_data)):

            results_data[i]["normalized_score"] = norm_scores[i]

        all_results.extend(results_data)

    # ------------------------------------
    # EXPORT CSV
    # ------------------------------------

    CSVExporter().export(all_results)

    print("\nZapisano wyniki do:")
    print("output/results.csv")


if __name__ == "__main__":

    main("data")