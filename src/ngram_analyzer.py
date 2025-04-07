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
      3. Logs the top 10 most frequent n-grams and the total unique n-grams count in a structured format,
         indicating the Surah number and name.
         
    :param data: List of dictionaries representing Quran data, where each dictionary contains keys
                 such as 'surah', 'ayah', 'verse_text', and optionally 'processed_text' and 'surah_name'.
    :param n: The size of the n-gram. Default is 2 for bigrams.
    :return: A dictionary mapping each Surah to a Counter object mapping n-gram tuples to their frequency count.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Surah-level word n-gram analysis.")
    from collections import defaultdict, Counter
    surah_ngram_counts = {}
    surah_grouped = {}
    for item in data:
        surah = item.get("surah", "Unknown")
        surah_name = item.get("surah_name", "Unknown")
        if surah not in surah_grouped:
            surah_grouped[surah] = {"name": surah_name, "tokens": []}
        text = item.get("processed_text") or item.get("verse_text", "")
        tokens = text.split() if text else []
        surah_grouped[surah]["tokens"].extend(tokens)
    
    for surah, info in surah_grouped.items():
        tokens = info["tokens"]
        counter = Counter()
        if len(tokens) < n:
            surah_ngram_counts[surah] = counter
            logger.info("Surah %s (%s) has insufficient tokens for n-gram analysis.", surah, info["name"])
            continue
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            counter[ngram] += 1
        top_10 = counter.most_common(10)
        log_message = {
            "Surah": surah,
            "Surah Name": info["name"],
            "Top 10 N-grams": top_10,
            "Total Unique N-grams": len(counter)
        }
        logger.info("Surah Word N-gram Analysis: %s", log_message)
        surah_ngram_counts[surah] = counter
    logger.info("Completed Surah-level word n-gram analysis.")
    return surah_ngram_counts

def analyze_ayah_word_ngrams(data, n=2):
    '''
    Analyze word n-gram frequency at the Ayah level.

    For each Ayah in the Quran data, this function:
      1. Tokenizes the verse text using 'processed_text' if available, otherwise 'verse_text'.
      2. Generates word n-grams using a sliding window approach.
      3. Logs the top 5 most frequent n-grams and the total unique n-grams count in a structured format,
         clearly indicating the Surah and Ayah number.
         
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
        top_5 = counter.most_common(5)
        log_message = {
            "Ayah": ayah_id,
            "Top 5 N-grams": top_5,
            "Total Unique N-grams": len(counter)
        }
        logger.info("Ayah Word N-gram Analysis: %s", log_message)
        ayah_ngram_counts[ayah_id] = counter
    logger.info("Completed Ayah-level word n-gram analysis.")
    return ayah_ngram_counts

def analyze_character_ngrams(quran_data, n=2):
    '''
    Analyze character n-gram frequency for the entire Quran text.
    
    This function concatenates the preprocessed text of all ayahs to form a single string,
    generates character n-grams using a sliding window of length n, counts the frequency of each n-gram,
    and logs the top 10 most frequent n-grams and the total unique n-gram count.
    
    :param quran_data: List of dictionaries representing Quran data.
    :param n: The length of the n-gram (default is 2 for bigrams).
    :return: A Counter object mapping character n-grams to their frequency.
    '''
    import logging
    from collections import Counter
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Character N-gram Analysis at Quran level.")
    combined_text = ""
    for item in quran_data:
        text = item.get("processed_text") or item.get("text") or item.get("verse_text", "")
        combined_text += text
    ngram_counts = Counter()
    for i in range(len(combined_text) - n + 1):
        ngram = combined_text[i:i+n]
        ngram_counts[ngram] += 1
    top_10 = ngram_counts.most_common(10)
    logger.info("Quran-wide Character N-gram Analysis - Top 10 n-grams: %s", top_10)
    logger.info("Total unique character n-grams: %d", len(ngram_counts))
    logger.info("Completed Character N-gram Analysis at Quran level.")
    return ngram_counts

def analyze_surah_character_ngrams(quran_data, n=2):
    '''
    Analyze character n-grams at the Surah level.
    
    This function groups the Quran data by Surah, concatenates the preprocessed text of all ayahs within each Surah,
    generates character n-grams using a sliding window, counts their frequencies, and logs the top 10 most frequent n-grams
    and the total unique n-gram count for each Surah.
    
    :param quran_data: List of dictionaries representing Quran data.
    :param n: The length of the n-gram (default is 2 for bigrams).
    :return: A dictionary mapping each Surah to a Counter of character n-gram frequencies.
    '''
    import logging
    from collections import defaultdict, Counter
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Character N-gram Analysis at Surah level.")
    surah_texts = defaultdict(str)
    for item in quran_data:
        surah = item.get("surah_number") or item.get("surah", "Unknown")
        text = item.get("processed_text") or item.get("text") or item.get("verse_text", "")
        surah_texts[surah] += text
    surah_ngram_counts = {}
    for surah, text in surah_texts.items():
        counter = Counter()
        for i in range(len(text) - n + 1):
            ngram = text[i:i+n]
            counter[ngram] += 1
        top_10 = counter.most_common(10)
        logger.info("Surah-level Character N-gram Analysis - Surah: %s, Top 10 n-grams: %s", surah, top_10)
        logger.info("Surah %s - Total unique character n-grams: %d", surah, len(counter))
        surah_ngram_counts[surah] = counter
    logger.info("Completed Character N-gram Analysis at Surah level.")
    return surah_ngram_counts

def analyze_ayah_character_ngrams(quran_data, n=2):
    '''
    Analyze character n-grams at the Ayah level.
    
    For a sample of Ayahs (first 5 ayahs per Surah) in the Quran data, this function generates character n-grams from 
    the preprocessed text, counts their frequencies, and logs the top 5 most frequent n-grams along with the total unique 
    n-gram count, clearly indicating the Surah and Ayah number.
    
    :param quran_data: List of dictionaries representing Quran data.
    :param n: The length of the n-gram (default is 2 for bigrams).
    :return: A dictionary mapping each Ayah identifier (Surah|Ayah) to a Counter of character n-gram frequencies for the sampled ayahs.
    '''
    import logging
    from collections import defaultdict, Counter
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Character N-gram Analysis at Ayah level.")
    ayah_ngram_counts = {}
    surah_groups = defaultdict(list)
    for item in quran_data:
        surah = item.get("surah_number") or item.get("surah", "Unknown")
        surah_groups[surah].append(item)
    for surah, ayah_items in surah_groups.items():
        for item in ayah_items[:5]:
            ayah = item.get("ayah_number") or item.get("ayah", "Unknown")
            text = item.get("processed_text") or item.get("text") or item.get("verse_text", "")
            counter = Counter()
            for i in range(len(text) - n + 1):
                ngram = text[i:i+n]
                counter[ngram] += 1
            ayah_id = f"{surah}|{ayah}"
            top_5 = counter.most_common(5)
            logger.info("Ayah-level Character N-gram Analysis - Surah: %s, Ayah: %s, Top 5 n-grams: %s", surah, ayah, top_5)
            logger.info("Ayah %s - Total unique character n-grams: %d", ayah_id, len(counter))
            ayah_ngram_counts[ayah_id] = counter
    logger.info("Completed Character N-gram Analysis at Ayah level.")
    return ayah_ngram_counts