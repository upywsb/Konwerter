# Mazovia-to-Modern Converter v1.5

[PL] Profesjonalne narzędzie do konwersji plików w kodowaniu Mazovia (DOS) na współczesne standardy.
[EN] A professional utility for converting legacy Mazovia (DOS) encoded files to modern standards.

---

## 🇵🇱 Wersja Polska

### Opis
Niezawodne narzędzie GUI napisane w Pythonie, stworzone do konwersji starych plików tekstowych i zrzutów baz danych z kodowania **Mazovia** na standardy takie jak **Windows-1250**, **UTF-8** lub **ISO-8859-2**. Narzędzie przygotowane z myślą o inżynierach systemowych pracujących z archiwalnymi systemami bankowymi lub przemysłowymi.

### Główne Funkcje
*   **Wierne Mapowanie Mazovii:** Precyzyjna tabela 256 znaków zapewniająca poprawne dekodowanie polskich liter oraz znaków ramkowych DOS.
*   **Przetwarzanie Wsadowe:** Możliwość wyboru wielu plików jednocześnie (obsługa rozszerzeń `.x`, `.xx`, `.dat`, `.prn`, `.txt`).
*   **Wybór Kodowania Wynikowego:**
    *   **Windows-1250 (Domyślne):** Idealne do Excela i Notatnika.
    *   **UTF-8:** Standard dla baz danych, aplikacji webowych i systemów typu Splunk.
    *   **ISO-8859-2:** Dla starszych systemów Linux/Unix.
*   **Ochrona przed Nadpisywaniem:** Automatyczne wersjonowanie plików (np. `plik_cp1250_2026-05-13_1.txt`) zapobiega przypadkowej utracie danych.
*   **Obsługa Dużych Plików:** Optymalizacja pod kątem rzutów baz danych o wielkości do 100MB.

### Instrukcja Obsługi
1. Uruchom skrypt: `python mazovia_converter.py`
2. Wybierz żądany format wynikowy.
3. Kliknij **"WYBIERZ PLIKI I KONWERTUJ"**.
4. Wybierz pliki – przekonwertowane kopie pojawią się w tym samym folderze z datą w nazwie.

---

## 🇺🇸 English Version

### Description
A robust Python-based GUI utility designed to convert legacy **Mazovia (DOS)** encoded text files and database dumps into modern standards. Developed for engineers dealing with legacy infrastructure and banking systems.

### Key Features
*   **Authentic Mazovia Mapping:** Uses a precise 256-character table to ensure legacy Polish characters and DOS box-drawing symbols are preserved correctly.
*   **Batch Processing:** Select multiple files at once (supports `.x`, `.xx`, `.dat`, `.prn`, etc.).
*   **Dynamic Encoding Selection:**
    *   **Windows-1250 (Default):** Perfect for Excel and Windows-native apps.
    *   **UTF-8:** Ideal for web apps, modern databases, and logging systems.
    *   **ISO-8859-2:** For Linux/Unix environments.
*   **Anti-Overwrite Protection:** Automatically versions output files to prevent data loss.
*   **High Performance:** Efficiently handles large database dumps up to 100MB.

### How to Use
1. Run the script: `python mazovia_converter.py`
2. Select your desired output encoding.
3. Click **"WYBIERZ PLIKI I KONWERTUJ"**.
4. Select one or more files – the result will be saved in the source directory with a timestamped suffix.

---

## 🛠️ Requirements / Wymagania
*   Python 3.x
*   Libraries: `tkinter`, `os`, `datetime`

**Author:** Marek
