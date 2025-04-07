''' 
Module for advanced readability analysis for Arabic text.

This module implements two readability metrics:
1. The Dale-Chall Readability Score (adapted for Arabic).
   - Difficult words are defined as those not present in a common Arabic word list.
   - If a standard list is unavailable, a fixed set of common words is used.
   - Formula: 0.1579 * (percentage of difficult words) + 0.0496 * (average sentence length) + 3.6365

2. The SMOG Index.
   - Polysyllabic words are approximated as words with more than 5 characters.
   - Formula: 1.0430 * sqrt(polysyllabic_word_count * (30/number_of_sentences)) + 3.1291

Additionally, this module provides analysis functions that compute these metrics at three levels:
- Entire Quran text
- Per Surah
- Per Ayah
'''

import os
import math
import logging
from src.data_loader import QuranDataLoader
from src.text_preprocessor import TextPreprocessor

def load_common_arabic_words():
    '''
    Load a comprehensive set of common Arabic words from a file if available.
    
    Checks the environment variable 'COMMON_WORDS_FILE'. If the file exists, loads words from it.
    Otherwise, returns a default set of common words.
    
    :return: Set of common Arabic words.
    '''
    file_path = os.getenv("COMMON_WORDS_FILE")
    if file_path and os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            words = f.read().splitlines()
            return set(word.strip() for word in words if word.strip())
    return {
        "في", "من", "على", "إلى", "و", "ما", "كان", "الله", "عن", "لا", "كل", "مع", "هذا", "ذلك", "هو", "هي"
    }

COMMON_ARABIC_WORDS = load_common_arabic_words()

def split_sentences(text, delimiter="\n"):
    '''
    Split the given text into sentences based on the specified delimiter.
    
    :param text: The text to split.
    :param delimiter: The delimiter to use for splitting (default is newline).
    :return: List of non-empty sentences.
    '''
    return [sentence for sentence in text.split(delimiter) if sentence.strip()]

def is_polysyllabic(word, threshold=4):
    '''
    Determine if a word is polysyllabic based on its length.
    
    :param word: The word to check.
    :param threshold: The character length threshold above which a word is considered polysyllabic.
    :return: True if word length is greater than threshold, False otherwise.
    '''
    return len(word) > threshold

def calculate_dale_chall_readability(text):
    '''
    Calculate the Dale-Chall Readability Score for the given preprocessed Arabic text.
    
    The function tokenizes the text into words, counts the number of difficult words 
    (words not in the common Arabic word list), computes the percentage of difficult words,
    and calculates the average sentence length assuming each ayah is a sentence.
    
    The formula used is:
      Score = 0.1579 * (percentage_difficult_words) + 0.0496 * (average_sentence_length) + 3.6365
    
    :param text: Preprocessed Arabic text as a string.
    :return: The Dale-Chall Readability Score as a float.
    '''
    words = text.split()
    total_words = len(words)
    if total_words == 0:
        percentage_difficult = 0
    else:
        difficult_word_count = sum(1 for word in words if word not in COMMON_ARABIC_WORDS)
        percentage_difficult = (difficult_word_count / total_words) * 100

    sentences = split_sentences(text)
    sentence_count = len(sentences) if sentences else 1
    average_sentence_length = total_words / sentence_count if sentence_count > 0 else total_words

    score = 0.1579 * percentage_difficult + 0.0496 * average_sentence_length + 3.6365
    return score

def calculate_smog_index(text):
    '''
    Calculate the SMOG Index for the given preprocessed Arabic text.
    
    For this approximation, words with more than 4 characters are considered polysyllabic.
    The number of sentences is determined by splitting on newline characters.
    
    The formula used is:
      SMOG Index = 1.0430 * sqrt(polysyllabic_word_count * (30 / number_of_sentences)) + 3.1291
    
    :param text: Preprocessed Arabic text as a string.
    :return: The SMOG Index as a float.
    '''
    words = text.split()
    total_words = len(words)
    polysyllabic_word_count = sum(1 for word in words if is_polysyllabic(word, threshold=4))
    sentences = split_sentences(text)
    sentence_count = len(sentences) if sentences else 1
    smog_index = 1.0430 * ((polysyllabic_word_count * (30 / sentence_count)) ** 0.5) + 3.1291
    return smog_index

def analyze_quran_dale_chall_readability():
    '''
    Analyze the Dale-Chall Readability Score for the entire Quran text.
    
    Loads the Quran data using QuranDataLoader, preprocesses the text using TextPreprocessor,
    concatenates all verses into a single string, computes the Dale-Chall score, logs the result,
    and returns the score.
    
    :return: The Dale-Chall Readability Score for the entire Quran as a float.
    '''
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    all_text = "\n".join(processor.preprocess_text(item.get("verse_text", "")) for item in data)
    score = calculate_dale_chall_readability(all_text)
    logger.info("Quran Dale-Chall Readability Score: %f", score)
    return score

def analyze_surah_dale_chall_readability():
    '''
    Analyze the Dale-Chall Readability Score for each Surah.
    
    Loads the Quran data, groups the verses by Surah, concatenates the preprocessed text for each Surah,
    computes the Dale-Chall score for each group, logs the results, and returns a dictionary mapping
    each Surah to its Dale-Chall score.
    
    :return: Dictionary mapping Surah identifiers to their Dale-Chall Readability Scores.
    '''
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    surah_groups = {}
    for item in data:
        surah = str(item.get("surah", "Unknown"))
        processed_text = processor.preprocess_text(item.get("verse_text", ""))
        surah_groups.setdefault(surah, []).append(processed_text)
    surah_scores = {}
    for surah, texts in surah_groups.items():
        full_text = "\n".join(texts)
        score = calculate_dale_chall_readability(full_text)
        logger.info("Surah %s Dale-Chall Readability Score: %f", surah, score)
        surah_scores[surah] = score
    return surah_scores

def analyze_ayah_dale_chall_readability():
    '''
    Analyze the Dale-Chall Readability Score for each Ayah.
    
    Loads the Quran data and for each Ayah, preprocesses the verse text,
    computes the Dale-Chall score, logs the result with the Ayah identifier,
    and returns a dictionary mapping each Ayah (formatted as "surah|ayah") to its score.
    
    :return: Dictionary mapping each Ayah identifier to its Dale-Chall Readability Score.
    '''
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    ayah_scores = {}
    for item in data:
        surah = str(item.get("surah", "Unknown"))
        ayah = str(item.get("ayah", "Unknown"))
        text = processor.preprocess_text(item.get("verse_text", ""))
        score = calculate_dale_chall_readability(text)
        identifier = f"{surah}|{ayah}"
        logger.info("Ayah %s Dale-Chall Readability Score: %f", identifier, score)
        ayah_scores[identifier] = score
    return ayah_scores

def analyze_quran_smog_index():
    '''
    Analyze the SMOG Index for the entire Quran text.
    
    Loads the Quran data using QuranDataLoader, preprocesses the text using TextPreprocessor,
    concatenates all verses into a single string, computes the SMOG Index, logs the result,
    and returns the SMOG Index.
    
    :return: The SMOG Index for the entire Quran as a float.
    '''
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    all_text = "\n".join(processor.preprocess_text(item.get("verse_text", "")) for item in data)
    index = calculate_smog_index(all_text)
    logger.info("Quran SMOG Index: %f", index)
    return index

def analyze_surah_smog_index():
    '''
    Analyze the SMOG Index for each Surah.
    
    Loads the Quran data, groups the verses by Surah, concatenates the preprocessed text for each Surah,
    computes the SMOG Index for each group, logs the results, and returns a dictionary mapping
    each Surah to its SMOG Index.
    
    :return: Dictionary mapping Surah identifiers to their SMOG Index.
    '''
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    surah_groups = {}
    for item in data:
        surah = str(item.get("surah", "Unknown"))
        processed_text = processor.preprocess_text(item.get("verse_text", ""))
        surah_groups.setdefault(surah, []).append(processed_text)
    surah_indices = {}
    for surah, texts in surah_groups.items():
        full_text = "\n".join(texts)
        index = calculate_smog_index(full_text)
        logger.info("Surah %s SMOG Index: %f", surah, index)
        surah_indices[surah] = index
    return surah_indices

def analyze_ayah_smog_index():
    '''
    Analyze the SMOG Index for each Ayah.
    
    Loads the Quran data and for each Ayah, preprocesses the verse text,
    computes the SMOG Index, logs the result with the Ayah identifier,
    and returns a dictionary mapping each Ayah (formatted as "surah|ayah") to its SMOG Index.
    
    :return: Dictionary mapping each Ayah identifier to its SMOG Index.
    '''
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    ayah_indices = {}
    for item in data:
        surah = str(item.get("surah", "Unknown"))
        ayah = str(item.get("ayah", "Unknown"))
        text = processor.preprocess_text(item.get("verse_text", ""))
        index = calculate_smog_index(text)
        identifier = f"{surah}|{ayah}"
        logger.info("Ayah %s SMOG Index: %f", identifier, index)
        ayah_indices[identifier] = index
    return ayah_indices