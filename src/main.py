"""
Main entry point for the Quran Secrets Analyzer.

This script performs a comprehensive analysis of the Quran text to uncover potential secrets.
The results are logged to analysis_results.log in the project root.
"""

import logging
import os
from src.quran_data_loader import load_quran_text, load_quran_data
from src.quran_search import (
    search_word_in_quran,
    search_word_group,
    search_words_by_gematrical_value,
    search_verses_by_word_count,
    search_word_at_position,
    search_word_group_at_position,
    search_verses_by_word_gematrical_value_equals_word_count,
    search_verses_by_word_group_gematrical_value_equals_verse_number,
    search_verses_by_word_gematrical_value_equals_surah_number,
    search_verses_by_verse_gematrical_value_equals,
    calculate_gematrical_value,
    calculate_quran_gematrical_value,
    search_word_in_verse_range,
    search_word_group_in_verse_range,
)

LOG_DETAILS_THRESHOLD = 5  # Threshold for logging verse details

def main():
    """
    Main function to perform a comprehensive analysis of the Quran.
    
    This function loads the Quran data and performs a series of analyses, including:
      - Keyword search
      - Word group search
      - Gematrical value analysis
      - Word count analysis
      - Positional search
      - Range search
      - Combinatorial search
      - Additional gematrical vs. structure analyses
      
    All results are logged to the analysis_results.log file.
    """
    # Configure logging to file and console
    log_file = os.path.join(os.getcwd(), "analysis_results.log")

    # Clear existing handlers to avoid interference with pytest logging
    # Note: Resetting root handlers might interfere with other parts of a larger application
    #       if they also configure logging. For a standalone script, this is acceptable.
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure logging with explicit handlers
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)
    logger.info("Starting comprehensive Quran analysis.")

    try:
        quran_file_path = os.path.join("data", "quran-uthmani-min.txt")
        quran_data = load_quran_data(quran_file_path)
        if not quran_data:
            logger.error("No Quran data loaded. Exiting analysis.")
            return

        # Keyword Searches
        keywords = ['Allah', 'Ar-Rahman', 'Ar-Rahim', 'day', 'night', 'sun', 'moon']
        for kw in keywords:
            results_kw = search_word_in_quran(quran_data, kw)
            logger.info("Keyword Search - '%s': Found %d verses.", kw, len(results_kw))
            if results_kw and len(results_kw) < LOG_DETAILS_THRESHOLD:
                details = "; ".join([f"Surah {v.get('surah_number')}, Ayah {v.get('ayah_number')}" for v in results_kw])
                logger.info("Details: %s", details)

        # Word Group Searches
        word_groups = ["بسم الله الرحمن الرحيم", "الله أكبر"]
        for wg in word_groups:
            results_wg = search_word_group(quran_data, wg)
            logger.info("Word Group Search - '%s': Found %d verses.", wg, len(results_wg))
            if results_wg and len(results_wg) < LOG_DETAILS_THRESHOLD:
                details = "; ".join([f"Surah {v.get('surah_number')}, Ayah {v.get('ayah_number')}" for v in results_wg])
                logger.info("Details: %s", details)

        # Gematrical Value Analysis: search for words with gematrical value 66 (e.g., for 'الله')
        gem_target = 66
        results_gem = search_words_by_gematrical_value(quran_data, gem_target)
        logger.info("Gematrical Value Analysis: Found %d words with gematrical value %d.", len(results_gem), gem_target)

        # Word Count Analysis: search for verses with exactly 19 words
        specific_word_count = 19
        results_word_count = search_verses_by_word_count(quran_data, specific_word_count)
        logger.info("Word Count Analysis: Found %d verses with exactly %d words.", len(results_word_count), specific_word_count)

        # Positional Searches
        results_pos = search_word_at_position(quran_data, "الله", 1)
        logger.info("Positional Search: Found %d verses where 'الله' is the first word.", len(results_pos))

        results_group_pos = search_word_group_at_position(quran_data, "بسم الله", 1)
        logger.info("Positional Word Group Search: Found %d verses where 'بسم الله' starts at position 1.", len(results_group_pos))

        # Range Searches
        results_range = search_word_in_verse_range(quran_data, "الله", (1, 1), (1, 5))
        logger.info("Verse Range Search: Found %d verses with 'الله' between verses (1,1) and (1,5).", len(results_range))

        results_group_range = search_word_group_in_verse_range(quran_data, "بسم الله", (1, 1), (1, 5))
        logger.info("Word Group Range Search: Found %d verses with 'بسم الله' between verses (1,1) and (1,5).", len(results_group_range))

        # Combinatorial Searches
        # Example: Search for verses where the gematrical value of "ب" equals the verse number and word count is a multiple of 19.
        results_combinatorial = []
        verses_with_b = search_word_in_quran(quran_data, "ب")
        for verse in verses_with_b:
            try:
                ayah_num = int(verse.get("ayah_number"))
                word_count = len(verse.get("verse_text", "").split())
            except (ValueError, TypeError) as e:
                logger.exception(f"Error processing verse for combinatorial search: Surah {verse.get('surah_number')}, Ayah {verse.get('ayah_number')}", exc_info=True)
                continue
            if calculate_gematrical_value("ب") == ayah_num and word_count % 19 == 0:
                results_combinatorial.append(verse)
        logger.info("Combinatorial Search: Found %d verses meeting combined criteria.", len(results_combinatorial))
        if results_combinatorial:
            for verse in results_combinatorial:
                logger.info("POTENTIAL SECRET FOUND: Surah %s, Ayah %s - %s", verse.get("surah_number"), verse.get("ayah_number"), verse.get("verse_text"))

        # Additional Gematrical vs. Structure Analyses
        results_gem_wc = search_verses_by_word_gematrical_value_equals_word_count(quran_data, "بسم الله")
        logger.info("Gematrical Value vs Word Count: Found %d verses where word count equals gematrical value of 'بسم الله'.", len(results_gem_wc))

        results_group_gem_verse = search_verses_by_word_group_gematrical_value_equals_verse_number(quran_data, "ب")
        logger.info("Gematrical Value vs Verse Number: Found %d verses where gematrical value of 'ب' equals verse number.", len(results_group_gem_verse))

        results_gem_surah = search_verses_by_word_gematrical_value_equals_surah_number(quran_data, "ب")
        logger.info("Gematrical Value vs Surah Number: Found %d verses where gematrical value of 'ب' equals surah number.", len(results_gem_surah))

        total_quran_gem = calculate_quran_gematrical_value(quran_data)
        logger.info("Total Gematrical Value of the Quran: %d", total_quran_gem)

        results_verse_gem = search_verses_by_verse_gematrical_value_equals(quran_data, 168)
        logger.info("Verses with total gematrical value equal to 168: Found %d verses.", len(results_verse_gem))

        logger.info("Quran analysis completed.")
    except Exception as e:
        logger.exception("An error occurred during Quran analysis: %s", str(e))
    finally:
        # Ensure all log messages are flushed to the file
        for handler in logging.getLogger().handlers:
            handler.flush()

if __name__ == "__main__":
    main()