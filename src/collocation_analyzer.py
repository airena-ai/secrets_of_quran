''' 
Module for analyzing word collocations in Quran text.
'''
import logging
from collections import Counter
from src.text_preprocessor import TextPreprocessor

def analyze_word_collocation(quran_data, window_size=3):
    '''
    Analyze word collocations in the given Quran data using a sliding window.
    
    For each ayah in quran_data, the function preprocesses the verse text 
    (using the existing TextPreprocessor if the processed text is not already present)
    and tokenizes the text into words. For each word, it considers a window of adjacent 
    words (window_size to the left and window_size to the right, excluding the target word)
    and counts each collocation pair. The collocation pairs are stored in alphabetical order 
    to ensure consistency.
    
    Parameters:
        quran_data (list): A list of dictionaries representing ayahs. Each dictionary 
                           should contain at least a 'verse_text' key, and may contain a 
                           'processed_text' key.
        window_size (int): The number of words to consider to the left and right of a target word.
                           Default is 3.
    
    Returns:
        Counter: A Counter object mapping each collocation pair (tuple) to its occurrence count.
    
    Logs:
        - The window size used for analysis.
        - The top 20 most frequent collocation pairs and their counts.
        - The total number of unique word collocation pairs found.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.propagate = True
    collocation_counter = Counter()
    processor = TextPreprocessor()

    for ayah in quran_data:
        text = ayah.get("processed_text")
        if not text:
            text = processor.preprocess_text(ayah.get("verse_text", ""))
        tokens = text.split()
        n = len(tokens)
        for i in range(n):
            target = tokens[i]
            start = max(0, i - window_size)
            end = min(n, i + window_size + 1)
            for j in range(start, end):
                if j == i:
                    continue
                neighbor = tokens[j]
                pair = tuple(sorted([target, neighbor]))
                collocation_counter[pair] += 1

    logger.info("Word Collocation Analysis: Window size used: %d", window_size)
    top_20 = collocation_counter.most_common(20)
    logger.info("Top 20 most frequent word collocation pairs:")
    for pair, count in top_20:
        logger.info("Pair: %s, Count: %d", pair, count)
    logger.info("Total unique word collocation pairs found: %d", len(collocation_counter))
    return collocation_counter