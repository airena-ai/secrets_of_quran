'''Main driver for the Quran Secrets application.'''

from src.file_reader import read_quran_text
from src.text_preprocessor import remove_diacritics, normalize_arabic_letters
from src.analyzer import analyze_text, analyze_word_frequency, analyze_root_words, analyze_bigrams, analyze_verse_repetitions, analyze_palindromes, analyze_abjad_numerals, analyze_semantic_symmetry, analyze_lemmas, analyze_surah_verse_counts
from src.logger import log_secret_found, log_result, log_bigram_frequencies

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
    
    # Perform bigram frequency analysis.
    tokenized_text = text.split()
    bigram_frequencies = analyze_bigrams(tokenized_text)
    log_bigram_frequencies(bigram_frequencies, top_n=20)
    
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
        
    # Perform verse repetition analysis.
    verse_repetitions = analyze_verse_repetitions(text)
    log_result("Verse Repetition Analysis:")
    for item in verse_repetitions.get("within_surah", []):
        log_result("Within Surah - Surah {}: Verse '{}' repeated {} times at Ayahs {}".format(
            item["surah"], item["verse"], item["repetition"], item["ayah_numbers"]))
    for item in verse_repetitions.get("across_quran", []):
        log_result("Across Quran - Verse '{}' repeated {} times at locations: {}".format(
            item["verse"], item["repetition"], item["occurrences"]))
        surahs = {occ["surah"] for occ in item["occurrences"]}
        if len(surahs) > 1:
            log_secret_found("Verse '{}' is repeated across multiple Surahs: {}".format(item["verse"], list(surahs)))
    
    # Advanced pattern analyses
    analyze_palindromes(text)
    analyze_abjad_numerals(text)
    analyze_semantic_symmetry(text)
    
    # New analysis functions for lemma analysis and surah verse counts
    analyze_lemmas(text)
    analyze_surah_verse_counts(text)
    
    print("Quran Secrets Analysis Completed.")

if __name__ == '__main__':
    main()