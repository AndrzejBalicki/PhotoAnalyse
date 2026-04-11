import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import sys
from pathlib import Path

# Dodaj folder src do sys.path
sys.path.append(str(Path(__file__).parent / "src"))

# Importy modułów
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

    metrics = {
        "sharpness": sharp,
        "exposure": expo,
        "noise": noise,
        "face": face
    }

    score = Scorer().compute(metrics)

    # ZWRACAMY dane zamiast zapisywać do listy globalnej
    return {
        "file": file,
        "sharpness": sharp,
        "exposure": expo,
        "noise": noise,
        "face": face,
        "score": score
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

    # EXIF
    exif = ExifReader()
    timestamps = [exif.get_timestamp(f) for f in files]

    # Grupowanie
    groups = BurstGrouper().group(files, timestamps)

    all_results = []

    for group in groups:

        print(f"\nSeria: {len(group)} zdjęć")

        with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:

            results_data = list(
                tqdm(
                    executor.map(process_image, group),
                    total=len(group)
                )
            )

        # -----------------------------
        # Normalizacja
        # -----------------------------
        scores = [r["score"] for r in results_data]

        norm_scores = normalize_scores(scores)

        best_idx = select_best(norm_scores)

        # -----------------------------
        # Zapis plików
        # -----------------------------
        for i, data in enumerate(results_data):

            handle_output(
                data["file"],
                norm_scores[i],
                i == best_idx
            )

        # dodajemy score po normalizacji
        for i in range(len(results_data)):

            results_data[i]["normalized_score"] = norm_scores[i]

        all_results.extend(results_data)

    # -----------------------------
    # Export CSV (raz na końcu)
    # -----------------------------
    CSVExporter().export(all_results)

    print("\nZapisano wyniki do:")
    print("output/results.csv")


if __name__ == "__main__":

    main("data")