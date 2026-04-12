1. PhotoAnalyse to aplikacja napisana w języku Python, której zadaniem jest automatyczna analiza i selekcja zdjęć.
Program ocenia jakość techniczną zdjęć, przypisuje im punkty, wybiera najlepsze ujęcia z każdej serii oraz zapisuje wyniki do pliku CSV.

Celem programu jest przyspieszenie pracy fotografa poprzez automatyczne odrzucenie słabszych zdjęć i wskazanie najlepszych.

---

2. Główne zadania programu

---

Program wykonuje następujące operacje:

1. Wczytuje zdjęcia z folderu
2. Odczytuje datę wykonania zdjęcia (EXIF)
3. Grupuje zdjęcia w serie
4. Analizuje jakość każdego zdjęcia
5. Oblicza punktację
6. Normalizuje wyniki w zakresie 0–100
7. Wybiera najlepsze zdjęcie z serii
8. Zmienia nazwę pliku lub kopiuje go do odpowiedniego folderu
9. Zapisuje szczegółowe wyniki do pliku results.csv

---

3. Na czym polega analiza zdjęć

---

Każde zdjęcie jest analizowane pod kątem czterech podstawowych parametrów jakości:

1. Ostrość (sharpness)
2. Ekspozycja (exposure)
3. Szum (noise)
4. Detekcja twarzy / obiektu (face)

Każdy parametr jest liczony osobno, a następnie łączony w jedną końcową ocenę.

---

4. Wzory i metody obliczeń

---

4.1 Ostrość (Sharpness)

Biblioteka:
OpenCV (cv2)

Metoda:
Wariancja Laplacianu (Laplacian variance)

Wzór:

sharpness = Var( Laplacian(image) )

Opis:
Im większa wartość, tym zdjęcie jest ostrzejsze.
Niskie wartości oznaczają rozmycie lub brak ostrości.

---

4.2 Ekspozycja (Exposure)

Biblioteki:
NumPy
OpenCV

Metoda:
Analiza histogramu jasności.

Wzór:

exposure = 1 - ( (pixels_dark + pixels_bright) / total_pixels )

Gdzie:

pixels_dark  — liczba bardzo ciemnych pikseli
pixels_bright — liczba bardzo jasnych pikseli
total_pixels — liczba wszystkich pikseli

Zakres:

0.0 — bardzo zła ekspozycja
1.0 — poprawna ekspozycja

---

4.3 Szum (Noise)

Biblioteki:
NumPy
OpenCV

Metoda:
Porównanie obrazu z jego rozmytą wersją.

Wzór:

noise = mean( (image - blur(image))² )

Opis:

Im większa wartość:

→ więcej szumu
→ gorsza jakość techniczna

---

4.4 Detekcja twarzy / obiektu (Face)

Biblioteka:

OpenCV Haar Cascade

Metoda:

faces = detectMultiScale(image)

Wartość:

face_score = liczba wykrytych obiektów

Opis:

Im więcej wykrytych twarzy / obiektów, tym wyższy wynik.

---

5. Obliczanie końcowej punktacji

---

Każdy parametr ma przypisaną wagę.

Przykładowe wagi:

sharpness — 0.5
exposure — 0.3
noise — 0.1
face — 0.1

Wzór:

score =
0.5 × sharpness +
0.3 × exposure +
0.1 × noise +
0.1 × face

---

6. Normalizacja wyniku

---

Ponieważ wartości score mogą być bardzo różne, program przelicza je do skali:

0 – 100

Wzór:

normalized_score =
(score - min_score)
/
(max_score - min_score)
× 100

Opis:

0 — najgorsze zdjęcie w serii
100 — najlepsze zdjęcie w serii

Normalizacja wykonywana jest osobno dla każdej serii zdjęć.

---

7. Wykorzystane biblioteki

---

Program wykorzystuje następujące biblioteki Python:

opencv-python

przetwarzanie obrazu
analiza ostrości
detekcja twarzy

rawpy

obsługa plików RAW (.ARW)

numpy

obliczenia matematyczne
operacje na macierzach

pillow / exifread

odczyt danych EXIF

tqdm

pasek postępu

concurrent.futures

przetwarzanie równoległe

csv

zapis wyników

os / shutil

operacje na plikach

---

8. Struktura projektu

---

PhotoAnalyse/

src/
loader/
metadata/
grouping/
analysis/
scoring/
selection/
output/

data/

main.py
config.py
requirements.txt
venv/

---

9. Jak uruchomić program

---

Krok 1 — aktywuj środowisko:

Windows:

venv\Scripts\activate

Krok 2 — uruchom program:

python main.py

---

10. Jak używać programu

---

1. Umieść zdjęcia w folderze:

data/

np.

data/
DSC0001.ARW
DSC0002.ARW
DSC0003.JPG

2. Uruchom program:

python main.py

3. Program:

* przeanalizuje zdjęcia
* pogrupuje je w serie
* policzy punkty
* wybierze najlepsze zdjęcie
* zapisze wyniki

---

11. Wyniki działania programu

---

Program tworzy:

output/results.csv

Plik zawiera:

file — nazwa pliku
sharpness — ostrość
exposure — ekspozycja
noise — poziom szumu
face — liczba wykrytych obiektów
score — surowa punktacja
normalized_score — wynik 0–100

Przykład:

file, sharpness, exposure, noise, face, score, normalized_score

DSA00405.jpg, 377.9, 0.80, 11.2, 2, 236.27, 61

---

Autor projektu: Andrzej Balicki
