import logging
from collections import Counter

def analyze_word_ngrams(quran_data, n=2):
    '''
    Analyze word n-gram frequency for the Quran data.

    This function iterates over each ayah in quran_data, tokenizes the ayah if necessary,
    generates word n-grams using a sliding window approach, counts the occurrence of each n-gram,
    and logs the top 20 most frequent n-grams along with the total unique n-grams count.

    :param quran_data: List of ayahs where each ayah is either a string (pre-tokenized) or a list of tokens.
    :param n: The size of the n-gram. Default is 2 for bigrams.
    :return: A Counter object mapping n-grams (as tuples) to their frequency count.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Word N-gram (Bigram) Frequency Analysis (Quran Level)...")

    ngram_counts = Counter()
    for ayah in quran_data:
        # Determine if the ayah is already tokenized (list) or a string needing splitting.
        if isinstance(ayah, list):
            tokens = ayah
        elif isinstance(ayah, str):
            tokens = ayah.split()
        else:
            tokens = []

        if len(tokens) < n:
            continue

        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngram_counts[ngram] += 1

    top_20 = ngram_counts.most_common(20)
    logger.info("Top 20 most frequent word bigrams:")
    for idx, (ngram, count) in enumerate(top_20, start=1):
        logger.info("%d.  %s: %d", idx, ngram, count)
    logger.info("Total unique word bigrams found: %d", len(ngram_counts))
    logger.info("Completed Word N-gram (Bigram) Frequency Analysis (Quran Level).")
    return ngram_counts