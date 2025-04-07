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

def analyze_surah_word_ngrams(data, n=2):
    '''
    Analyze word n-gram frequency at the Surah level.

    This function groups the Quran data by Surah and computes the frequency of word n-grams for each Surah.
    For each Surah, it:
      1. Consolidates tokens from the preprocessed text of all ayahs.
      2. Generates n-grams using a sliding window approach.
      3. Logs the top 20 most frequent n-grams and the total unique n-grams count.

    :param data: List of dictionaries representing Quran data, where each dictionary contains keys
                 such as 'surah', 'ayah', 'verse_text', and optionally 'processed_text'.
    :param n: The size of the n-gram. Default is 2 for bigrams.
    :return: A dictionary mapping each Surah to a Counter object mapping n-gram tuples to their frequency count.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Surah-level word n-gram analysis.")
    from collections import defaultdict
    surah_ngram_counts = {}
    surah_tokens = defaultdict(list)
    for item in data:
        surah = item.get("surah", "Unknown")
        text = item.get("processed_text") or item.get("verse_text", "")
        tokens = text.split() if text else []
        surah_tokens[surah].extend(tokens)
    
    for surah, tokens in surah_tokens.items():
        counter = Counter()
        if len(tokens) < n:
            surah_ngram_counts[surah] = counter
            logger.info("Surah %s has insufficient tokens for n-gram analysis.", surah)
            continue
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            counter[ngram] += 1
        top_20 = counter.most_common(20)
        logger.info("Surah-level Word N-gram Analysis - Surah %s Top 20 n-grams: %s", surah, top_20)
        logger.info("Surah %s - Total unique n-grams found: %d", surah, len(counter))
        surah_ngram_counts[surah] = counter
    logger.info("Completed Surah-level word n-gram analysis.")
    return surah_ngram_counts

def analyze_ayah_word_ngrams(data, n=2):
    '''
    Analyze word n-gram frequency at the Ayah level.

    For each Ayah in the Quran data, this function:
      1. Tokenizes the verse text using 'processed_text' if available, otherwise 'verse_text'.
      2. Generates word n-grams using a sliding window approach.
      3. Logs the top 20 most frequent n-grams along with the total unique n-grams count for that Ayah.

    Logs are in the format:
    "Ayah-level N-gram Analysis - Ayah: [Surah|Ayah] Top 20 n-grams: <list>, Total unique n-grams: <count>"

    :param data: List of dictionaries representing Quran data.
    :param n: The size of the n-gram. Default is 2 for bigrams.
    :return: A dictionary mapping each Ayah identifier (formatted as 'Surah|Ayah') to a Counter object of n-grams.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Ayah-level word n-gram analysis.")
    from collections import Counter
    ayah_ngram_counts = {}
    for item in data:
        surah = item.get("surah", "Unknown")
        ayah = item.get("ayah", "Unknown")
        ayah_id = f"{surah}|{ayah}"
        text = item.get("processed_text") or item.get("verse_text", "")
        tokens = text.split() if text else []
        counter = Counter()
        if len(tokens) < n:
            ayah_ngram_counts[ayah_id] = counter
            logger.info("Ayah %s has insufficient tokens for n-gram analysis.", ayah_id)
            continue
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            counter[ngram] += 1
        top_20 = counter.most_common(20)
        logger.info("Ayah-level N-gram Analysis - Ayah: %s Top 20 n-grams: %s", ayah_id, top_20)
        logger.info("Ayah %s - Total unique n-grams found: %d", ayah_id, len(counter))
        ayah_ngram_counts[ayah_id] = counter
    logger.info("Completed Ayah-level word n-gram analysis.")
    return ayah_ngram_counts