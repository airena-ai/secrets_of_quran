'''Main driver for the Quran Secrets application.'''

from src.file_reader import read_quran_text
from src.text_preprocessor import remove_diacritics, normalize_arabic_letters
from src.analyzer import analyze_text, analyze_word_frequency, analyze_root_words, analyze_bigrams, analyze_verse_repetitions, analyze_verse_lengths_distribution, analyze_palindromes, analyze_abjad_numerals, analyze_semantic_symmetry, analyze_verse_length_symmetry, analyze_enhanced_semantic_symmetry, analyze_lemmas, analyze_surah_verse_counts, analyze_muqattaat, analyze_muqattaat_positions, analyze_muqattaat_sequences, analyze_muqattaat_numerical_values, analyze_correlations
from src.logger import log_secret_found, log_result, log_bigram_frequencies

def main():
    '''Main entry point for the Quran Secrets analysis.'''
    file_path = "data/quran-uthmani-min-only-fatiha-with-bism.txt"
    try:
        text = read_quran_text(file_path)
    except Exception as e:
        print("Error reading file:", e)
        return

    text = remove_diacritics(text)
    text = normalize_arabic_letters(text)
    
    # Perform verse length analysis and distribution.
    verse_lengths = analyze_verse_lengths_distribution(text)
    
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
    abjad_anomalies = analyze_abjad_numerals(text)
    analyze_semantic_symmetry(text)
    
    # New analysis for verse arrangement rhythm & balance
    analyze_verse_length_symmetry(text)
    enhanced_symmetry = analyze_enhanced_semantic_symmetry(text)
    
    # New analysis functions for lemma analysis and surah verse counts
    analyze_lemmas(text)
    analyze_surah_verse_counts(text)
    
    # New analysis for Muqatta'at
    muqattaat_data, _ = analyze_muqattaat(text)
    muqattaat_positions_summary = analyze_muqattaat_positions(text)
    numerical_summary = analyze_muqattaat_numerical_values(text)
    
    # New analysis for Muqatta'at sequences
    muqattaat_seq_freq = analyze_muqattaat_sequences(text)
    log_result("Muqatta'at Sequences Frequency Analysis:")
    for seq, freq in muqattaat_seq_freq.items():
        log_result("Sequence '{}' occurred {} times".format(seq, freq))
        if freq > 1:
            log_secret_found("Sequence '{}' appears unusually often ({} times)".format(seq, freq))
    
    # Perform correlation analysis across various analytical dimensions.
    correlation_secrets = analyze_correlations(
        text,
        verse_lengths=verse_lengths,
        muqattaat_data=muqattaat_data,
        word_frequency_result=(freq_summary, freq_flagged),
        flagged_words=freq_flagged,
        verse_repetitions_data=verse_repetitions,
        enhanced_symmetry_data=enhanced_symmetry,
        abjad_anomalies=abjad_anomalies
    )
    
    # Generate enhanced final report.
    final_report_lines = []
    final_report_lines.append("FINAL REPORT: QURAN SECRETS ANALYSIS")
    final_report_lines.append("--------------------------------------------------")
    final_report_lines.append("Word Frequency Analysis Summary:")
    final_report_lines.append(freq_summary)
    final_report_lines.append("")
    final_report_lines.append("Arabic Root Word Analysis Summary:")
    final_report_lines.append(root_summary)
    final_report_lines.append("")
    final_report_lines.append("Bigram Frequency Analysis:")
    sorted_bigrams = sorted(bigram_frequencies.items(), key=lambda x: x[1], reverse=True)
    top_n = 20
    bigram_lines = ["Top {} Bigrams:".format(top_n)]
    for idx, (bigram, count) in enumerate(sorted_bigrams[:top_n], start=1):
        bigram_lines.append("{}. {}: {}".format(idx, ' '.join(bigram), count))
    final_report_lines.extend(bigram_lines)
    final_report_lines.append("")
    final_report_lines.append("Verse Repetition Analysis:")
    for item in verse_repetitions.get("within_surah", []):
        final_report_lines.append("Within Surah - Surah {}: Verse '{}' repeated {} times at Ayahs {}".format(
            item["surah"], item["verse"], item["repetition"], item["ayah_numbers"]))
    for item in verse_repetitions.get("across_quran", []):
        final_report_lines.append("Across Quran - Verse '{}' repeated {} times at locations: {}".format(
            item["verse"], item["repetition"], item["occurrences"]))
    final_report_lines.append("")
    final_report_lines.append("Muqatta'at Insights:")
    surahs_with_muq = sorted(muqattaat_data.keys(), key=lambda x: int(x))
    final_report_lines.append("Surahs with Muqatta'at: " + ", ".join(surahs_with_muq))
    for surah in surahs_with_muq:
        final_report_lines.append("Surah {}: Muqatta'at Letters: {}".format(surah, muqattaat_data[surah]))
    final_report_lines.append("")
    final_report_lines.append("Muqatta'at Positional Distribution:")
    final_report_lines.append(muqattaat_positions_summary)
    final_report_lines.append("")
    final_report_lines.append("Muqatta'at Numerical Analysis:")
    final_report_lines.append(numerical_summary)
    final_report_lines.append("")
    final_report_lines.append("Muqatta'at Sequences Frequency Analysis:")
    for seq, freq in muqattaat_seq_freq.items():
        final_report_lines.append("Sequence '{}' occurred {} times".format(seq, freq))
    final_report_lines.append("")
    final_report_lines.append("Correlation Analysis:")
    if correlation_secrets:
        for msg in correlation_secrets:
            final_report_lines.append(msg)
    else:
        final_report_lines.append("No significant correlations detected.")
    final_report = "\n".join(final_report_lines)
    
    # Use the already imported log_result function instead of re-importing it
    log_result(final_report)
    try:
        with open("quran_secrets_report.txt", "w", encoding="utf-8") as rep_file:
            rep_file.write(final_report)
    except Exception as e:
        log_result("Error writing human-readable report: " + str(e))
    
    print("Quran Secrets Analysis Completed.")

if __name__ == '__main__':
    main()