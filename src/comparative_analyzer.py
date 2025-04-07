"""Module for comparative analysis between Makki and Madani Surahs.

This module provides functions to compare text complexity metrics,
word frequency distributions, and Gematria value distributions between
Makki and Madani Surahs. It leverages existing analysis modules and
includes helper functions to compute approximate Dale-Chall and SMOG scores.
"""

import logging
import math
import os
from collections import Counter

from src.data_loader import QuranDataLoader
from src.text_preprocessor import TextPreprocessor
from src.text_complexity_analyzer import calculate_flesch_reading_ease, calculate_flesch_kincaid_grade_level
from src.frequency_analyzer import count_word_frequencies
from src.gematria_analyzer import calculate_gematria_value


def compute_dale_chall(text):
    """
    Compute an approximate Dale-Chall Readability Score for the given text.
    
    This is a rudimentary implementation using the formula:
      score = 0.1579 * (percent_difficult_words) + 0.0496 * (average_sentence_length) + 3.6365
    Here, difficult words are approximated as words with length greater than 4.
    
    :param text: Preprocessed text as a string.
    :return: Dale-Chall score as a float.
    """
    sentences = [s for s in text.splitlines() if s.strip()]
    if not sentences:
        sentences = [text]
    words = text.split()
    total_words = len(words)
    if total_words == 0:
        return 0.0
    difficult_words = [word for word in words if len(word) > 4]
    percent_difficult = (len(difficult_words) / total_words) * 100
    avg_sentence_length = total_words / len(sentences)
    score = 0.1579 * percent_difficult + 0.0496 * avg_sentence_length + 3.6365
    return score


def compute_smog(text):
    """
    Compute an approximate SMOG Index for the given text.
    
    This implementation approximates polysyllabic words as words with length >= 3.
    Uses the formula:
      SMOG = 1.0430 * sqrt(polysyllabic_word_count * (30 / number_of_sentences)) + 3.1291
      
    :param text: Preprocessed text as a string.
    :return: SMOG index as a float.
    """
    sentences = [s for s in text.splitlines() if s.strip()]
    if not sentences:
        sentences = [text]
    words = text.split()
    if len(sentences) == 0 or len(words) == 0:
        return 0.0
    poly_count = sum(1 for word in words if len(word) >= 3)
    smog = 1.0430 * math.sqrt(poly_count * (30 / len(sentences))) + 3.1291
    return smog


def compare_makki_madani_text_complexity(makki_surahs, madani_surahs):
    """
    Compare text complexity metrics between Makki and Madani Surahs.
    
    For each metric (Flesch Reading Ease, Flesch-Kincaid Grade Level, Dale-Chall, SMOG Index),
    this function loads the Quran data, filters verses by surah using the provided lists,
    concatenates the preprocessed text, computes the metrics, logs the comparative results,
    and returns a dictionary with metrics for 'Makki' and 'Madani' groups.
    
    :param makki_surahs: List of surah numbers (int) classified as Makki.
    :param madani_surahs: List of surah numbers (int) classified as Madani.
    :return: Dictionary with keys 'Makki' and 'Madani' mapping to their respective metrics.
    """
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if not file_path:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    
    makki_texts = []
    madani_texts = []
    for item in data:
        surah = item.get("surah")
        text = processor.preprocess_text(item.get("verse_text", ""))
        if surah in makki_surahs:
            makki_texts.append(text)
        elif surah in madani_surahs:
            madani_texts.append(text)
    
    makki_text = "\n".join(makki_texts)
    madani_text = "\n".join(madani_texts)
    
    makki_metrics = {}
    madani_metrics = {}
    
    # Flesch Reading Ease
    makki_flesch = calculate_flesch_reading_ease(makki_text)
    madani_flesch = calculate_flesch_reading_ease(madani_text)
    makki_metrics["Flesch_Reading_Ease"] = makki_flesch
    madani_metrics["Flesch_Reading_Ease"] = madani_flesch
    
    # Flesch-Kincaid Grade Level
    makki_fk = calculate_flesch_kincaid_grade_level(makki_text)
    madani_fk = calculate_flesch_kincaid_grade_level(madani_text)
    makki_metrics["Flesch_Kincaid_Grade_Level"] = makki_fk
    madani_metrics["Flesch_Kincaid_Grade_Level"] = madani_fk
    
    # Dale-Chall Readability Score (approximate)
    makki_dc = compute_dale_chall(makki_text)
    madani_dc = compute_dale_chall(madani_text)
    makki_metrics["Dale_Chall"] = makki_dc
    madani_metrics["Dale_Chall"] = madani_dc
    
    # SMOG Index (approximate)
    makki_smog = compute_smog(makki_text)
    madani_smog = compute_smog(madani_text)
    makki_metrics["SMOG_Index"] = makki_smog
    madani_metrics["SMOG_Index"] = madani_smog
    
    logger.info("Comparative Text Complexity Analysis:")
    logger.info("Makki Metrics: %s", makki_metrics)
    logger.info("Madani Metrics: %s", madani_metrics)
    
    return {"Makki": makki_metrics, "Madani": madani_metrics}


def compare_makki_madani_word_frequency_distribution(makki_surahs, madani_surahs, top_n=20):
    """
    Compare word frequency distributions between Makki and Madani Surahs.
    
    The function aggregates processed text from each group, tokenizes the words,
    computes the frequency distribution, identifies the top 'n' words,
    logs the results, and returns a dictionary mapping each group to its top frequency list.
    
    :param makki_surahs: List of surah numbers (int) classified as Makki.
    :param madani_surahs: List of surah numbers (int) classified as Madani.
    :param top_n: Number of top frequent words to return (default is 20).
    :return: Dictionary with keys 'Makki' and 'Madani' mapping to lists of (word, frequency) tuples.
    """
    logger = logging.getLogger("quran_analysis")
    loader = QuranDataLoader()
    data = loader.load_data()
    processor = TextPreprocessor()
    
    makki_tokens = []
    madani_tokens = []
    for item in data:
        surah = item.get("surah")
        text = processor.preprocess_text(item.get("verse_text", ""))
        tokens = text.split()
        if surah in makki_surahs:
            makki_tokens.extend(tokens)
        elif surah in madani_surahs:
            madani_tokens.extend(tokens)
    
    makki_freq = count_word_frequencies([makki_tokens])
    madani_freq = count_word_frequencies([madani_tokens])
    
    top_makki = sorted(makki_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_madani = sorted(madani_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    logger.info("Comparative Word Frequency Distribution Analysis:")
    logger.info("Makki Top %d Words: %s", top_n, top_makki)
    logger.info("Madani Top %d Words: %s", top_n, top_madani)
    
    return {"Makki": top_makki, "Madani": top_madani}


def compare_makki_madani_gematria_distribution(makki_surahs, madani_surahs, top_n=20):
    """
    Compare Gematria value distributions between Makki and Madani Surahs.
    
    The function aggregates processed text from each group, tokenizes the words,
    computes the Gematria value for each word, counts the frequency distribution,
    identifies the top 'n' frequent Gematria values, logs the outcomes,
    and returns a dictionary with the results.
    
    :param makki_surahs: List of surah numbers (int) classified as Makki.
    :param madani_surahs: List of surah numbers (int) classified as Madani.
    :param top_n: Number of top Gematria values to return (default is 20).
    :return: Dictionary with keys 'Makki' and 'Madani' mapping to lists of (gematria value, frequency) tuples.
    """
    logger = logging.getLogger("quran_analysis")
    loader = QuranDataLoader()
    data = loader.load_data()
    processor = TextPreprocessor()
    
    makki_values = []
    madani_values = []
    
    for item in data:
        surah = item.get("surah")
        text = processor.preprocess_text(item.get("verse_text", ""))
        tokens = text.split()
        if surah in makki_surahs:
            for token in tokens:
                value = calculate_gematria_value(token)
                makki_values.append(value)
        elif surah in madani_surahs:
            for token in tokens:
                value = calculate_gematria_value(token)
                madani_values.append(value)
    
    makki_distribution = Counter(makki_values)
    madani_distribution = Counter(madani_values)
    
    top_makki = sorted(makki_distribution.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_madani = sorted(madani_distribution.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    logger.info("Comparative Gematria Distribution Analysis:")
    logger.info("Makki Top %d Gematria Values: %s", top_n, top_makki)
    logger.info("Madani Top %d Gematria Values: %s", top_n, top_madani)
    
    return {"Makki": top_makki, "Madani": top_madani}