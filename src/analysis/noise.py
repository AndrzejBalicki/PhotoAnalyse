import cv2
import numpy as np


class NoiseAnalyzer:

    def compute(self, img):

        if img is None:
            return 0.0

        # ---------------------------------
        # 1. konwersja do przestrzeni LAB
        # ---------------------------------

        lab = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2LAB
        )

        L, A, B = cv2.split(lab)

        # ---------------------------------
        # 2. wykrycie płaskich obszarów
        # (tam mierzymy szum)
        # ---------------------------------

        gx = cv2.Sobel(
            L,
            cv2.CV_64F,
            1,
            0,
            ksize=3
        )

        gy = cv2.Sobel(
            L,
            cv2.CV_64F,
            0,
            1,
            ksize=3
        )

        gradient = np.sqrt(
            gx**2 + gy**2
        )

        flat_mask = gradient < 10

        # jeśli brak płaskich obszarów
        if np.sum(flat_mask) < 100:
            return 0.5

        # ---------------------------------
        # 3. luminance noise
        # ---------------------------------

        blur_L = cv2.GaussianBlur(
            L,
            (7, 7),
            0
        )

        lum_noise = L - blur_L

        lum_std = np.std(
            lum_noise[flat_mask]
        )

        # ---------------------------------
        # 4. chroma noise (kolorowy szum)
        # ---------------------------------

        blur_A = cv2.GaussianBlur(
            A,
            (7, 7),
            0
        )

        blur_B = cv2.GaussianBlur(
            B,
            (7, 7),
            0
        )

        chroma_noise = (
            (A - blur_A) ** 2 +
            (B - blur_B) ** 2
        )

        chroma_std = np.sqrt(
            np.mean(
                chroma_noise[flat_mask]
            )
        )

        # ---------------------------------
        # 5. połączenie metryk
        # ---------------------------------

        noise_value = (
            0.6 * lum_std +
            0.4 * chroma_std
        )

        # ---------------------------------
        # 6. kara za clipping
        # (kluczowe dla prześwietleń)
        # ---------------------------------

        overexposed = np.sum(L >= 250)
        underexposed = np.sum(L <= 5)

        clipping_ratio = (
            overexposed + underexposed
        ) / L.size

        # wzmacniamy wpływ clippingu

        noise_value = noise_value * (
            1 + 3 * clipping_ratio
        )

        # ---------------------------------
        # 7. stabilizacja zakresu
        # ---------------------------------

        noise_value = np.log1p(
            noise_value
        )

        # ---------------------------------
        # 8. konwersja na score jakości
        # ---------------------------------

        score = 1 / (
            1 + noise_value
        )

        return float(score)