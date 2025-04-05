'''Main driver for the Quran Secrets application.'''

from src.file_reader import read_quran_text
from src.text_preprocessor import remove_diacritics, normalize_arabic_letters
from src.analyzer import analyze_text, analyze_word_frequency, analyze_root_words
from src.logger import log_secret_found, log_result

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
    
    # Execute both numerical pattern analysis and word frequency analysis.
    anomalies = analyze_text(text)
    freq_summary, freq_flagged = analyze_word_frequency(text)
    
    # Execute Arabic root word frequency analysis.
    root_summary, root_freq, top_roots = analyze_root_words(text)
    
    # Log the word frequency analysis summary with a timestamp.
    log_result(freq_summary)
    
    # Log the Arabic root word analysis summary.
    log_result(root_summary)
    
    # Log flagged words from frequency analysis as potential secrets.
    for flag in freq_flagged:
        log_secret_found(flag)
    
    # Log other anomalies detected in the text.
    for anomaly in anomalies:
        log_secret_found(anomaly)
        
    print("Quran Secrets Analysis Completed.")

if __name__ == '__main__':
    main()