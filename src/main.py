'''Main driver for the Quran Secrets application.'''

from src.file_reader import read_quran_text
from src.text_preprocessor import remove_diacritics, normalize_arabic_letters
from src.analyzer import analyze_text
from src.logger import log_secret_found

def main():
    '''Main entry point for the Quran Secrets analysis.'''
    file_path = "data/quran-uthmani-min.txt"
    try:
        text = read_quran_text(file_path)
    except Exception as e:
        print("Error reading file:", e)
        return

    text = remove_diacritics(text)
    text = normalize_arabic_letters(text)
    anomalies = analyze_text(text)
    for anomaly in anomalies:
        log_secret_found(anomaly)
    print("Quran Secrets Analysis Completed.")

if __name__ == '__main__':
    main()