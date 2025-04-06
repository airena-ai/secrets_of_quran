'''Main driver for the Quran Secrets application.'''

from src.file_reader import read_quran_text
from src.text_preprocessor import remove_diacritics, normalize_arabic_letters
from src.analyzer import analyze_text, analyze_word_frequency, analyze_root_words, analyze_bigrams, analyze_verse_repetitions, analyze_verse_lengths_distribution, analyze_palindromes, analyze_abjad_numerals, analyze_semantic_symmetry, analyze_verse_length_symmetry, analyze_enhanced_semantic_symmetry, analyze_lemmas, analyze_surah_verse_counts, analyze_muqattaat, analyze_muqattaat_positions, analyze_muqattaat_sequences, analyze_muqattaat_numerical_values, analyze_muqattaat_preceding_context, analyze_muqattaat_themes, analyze_muqattaat_context, analyze_correlations, compare_surahs_muqattaat_vs_non_muqattaat, analyze_muqattaat_distribution_meccan_medinan, surah_classification, categorize_surahs_by_muqattaat, analyze_grouped_root_frequencies, analyze_grouped_lemma_frequencies, analyze_muqattaat_length, generate_muqattaat_report, review_muqattaat_report, synthesize_muqattaat_analyses, analyze_muqattaat_semantic_similarity

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
    from src.logger import log_bigram_frequencies
    log_bigram_frequencies(bigram_frequencies, top_n=20)
    
    # Log the word frequency analysis summary with a timestamp.
    from src.logger import log_result, log_secret_found
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
        logResultMsg = "Across Quran - Verse '{}' repeated {} times at locations: {}".format(
            item["verse"], item["repetition"], item["occurrences"])
        log_result(logResultMsg)
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
    # NEW: Distribution Analysis of Muqatta'at: Meccan vs. Medinan
    from src.analyzer import surah_classification
    analyze_muqattaat_distribution_meccan_medinan(text, surah_classification)
    # New: Thematic Analysis for Muqatta'at
    analyze_muqattaat_themes()
    
    # New analysis for Muqatta'at sequences
    muqattaat_seq_freq = analyze_muqattaat_sequences(text)
    log_result("Muqatta'at Sequences Frequency Analysis:")
    for seq, freq in muqattaat_seq_freq.items():
        log_result("Sequence '{}' occurred {} times".format(seq, freq))
        if freq > 1:
            log_secret_found("Sequence '{}' appears unusually often ({} times)".format(seq, freq))
    
    # New: Muqatta'at Sequence Length Analysis
    analyze_muqattaat_length(text)
    
    # New: Contextual Analysis of Verses Following Muqatta'at
    analyze_muqattaat_context(text)
    
    # NEW: Preceding Context Analysis of Verses Before Muqatta'at
    analyze_muqattaat_preceding_context(text)
    
    # New: Comparative Analysis for Surahs with and without Muqatta'at
    from src.analyzer import categorize_surahs_by_muqattaat, analyze_grouped_root_frequencies, analyze_grouped_lemma_frequencies
    muq_surahs, non_muq_surahs = categorize_surahs_by_muqattaat(text)
    root_freq_muq = analyze_grouped_root_frequencies(text, muq_surahs)
    root_freq_non_muq = analyze_grouped_root_frequencies(text, non_muq_surahs)
    lemma_freq_muq = analyze_grouped_lemma_frequencies(text, muq_surahs)
    lemma_freq_non_muq = analyze_grouped_lemma_frequencies(text, non_muq_surahs)
    
    top_n = 20
    log_result("----- Comparative Analysis: Root Word Frequencies -----")
    sorted_roots_muq = sorted(root_freq_muq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    log_result("Top {} Root Words for Muqatta'at Surahs:".format(top_n))
    for idx, (root, freq) in enumerate(sorted_roots_muq, start=1):
         log_result("{}. '{}' : {}".format(idx, root, freq))
    
    sorted_roots_non_muq = sorted(root_freq_non_muq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    log_result("Top {} Root Words for Non-Muqatta'at Surahs:".format(top_n))
    for idx, (root, freq) in enumerate(sorted_roots_non_muq, start=1):
         log_result("{}. '{}' : {}".format(idx, root, freq))
    
    common_roots = set(dict(sorted_roots_muq).keys()).intersection(set(dict(sorted_roots_non_muq).keys()))
    if len(common_roots) < (0.5 * top_n):
         log_secret_found("POTENTIAL SECRET FOUND: Significant difference in top root words between Muqatta'at and Non-Muqatta'at Surahs.")
    
    logResultLemma = "----- Comparative Analysis: Lemma Frequencies -----"
    log_result(logResultLemma)
    sorted_lemmas_muq = sorted(lemma_freq_muq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    log_result("Top {} Lemmas for Muqatta'at Surahs:".format(top_n))
    for idx, (lemma, freq) in enumerate(sorted_lemmas_muq, start=1):
         log_result("{}. '{}' : {}".format(idx, lemma, freq))
    
    sorted_lemmas_non_muq = sorted(lemma_freq_non_muq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    log_result("Top {} Lemmas for Non-Muqatta'at Surahs:".format(top_n))
    for idx, (lemma, freq) in enumerate(sorted_lemmas_non_muq, start=1):
         log_result("{}. '{}' : {}".format(idx, lemma, freq))
    
    common_lemmas = set(dict(sorted_lemmas_muq).keys()).intersection(set(dict(sorted_lemmas_non_muq).keys()))
    if len(common_lemmas) < (0.5 * top_n):
         log_secret_found("POTENTIAL SECRET FOUND: Significant difference in top lemmas between Muqatta'at and Non-Muqatta'at Surahs.")
    
    # New: Comparison between Surahs with and without Muqatta'at
    compare_surahs_muqattaat_vs_non_muqattaat(text)
    
    # NEW: Analysis of Muqatta'at Root Co-occurrence with Frequent Root Words
    from src.analyzer import analyze_muqattaat_root_cooccurrence
    analyze_muqattaat_root_cooccurrence(text)
    
    # NEW: Synthesize Muqatta'at Analyses Cross-Analysis
    from src.analyzer import synthesize_muqattaat_analyses
    synthesize_muqattaat_analyses(text)
    
    # NEW: Semantic Similarity Analysis of Surahs with Same Muqatta'at
    log_result("Starting semantic similarity analysis for Muqatta'at...")
    analyze_muqattaat_semantic_similarity(text, muqattaat_data)
    
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
    final_report_lines.append("Correlation Analysis Summary:")
    if correlation_secrets:
        for msg in correlation_secrets:
            final_report_lines.append(msg)
    else:
        final_report_lines.append("No significant correlations detected.")
    final_report = "\n".join(final_report_lines)
    
    log_result(final_report)
    try:
        with open("quran_secrets_report.txt", "w", encoding="utf-8") as rep_file:
            rep_file.write(final_report)
    except Exception as e:
        log_result("Error writing human-readable report: " + str(e))
    
    # NEW: Generate final Muqatta'at report
    generate_muqattaat_report(text)
    # NEW: Append final conclusions based on Muqatta'at analysis review
    try:
        with open("results.log", "r", encoding="utf-8") as rep_file:
            report_content = rep_file.read()
    except Exception as e:
        log_result("Error reading results.log: " + str(e))
        report_content = ""
    final_conclusion = review_muqattaat_report(report_content)
    log_result(final_conclusion)
    
    # NEW: Compare scholarly interpretations with analysis findings.
    from src.data_loader import load_muqattaat_interpretations
    from src.analyzer import compare_interpretations_with_analysis
    interpretations = load_muqattaat_interpretations()
    compare_interpretations_with_analysis(interpretations)
    
    print("Quran Secrets Analysis Completed.")

if __name__ == '__main__':
    main()