import logging
from collections import Counter

def count_word_frequencies(tokenized_text):
    '''
    Calculate the frequency of each unique word across the tokenized Quran text.

    The input may be a list of lists of words (each inner list represents a verse)
    or a flat list of words.
    The output is a dictionary with unique words as keys and their frequency counts as values.

    :param tokenized_text: List of lists of word tokens or a flat list of tokens.
    :return: Dictionary of word frequencies.
    '''
    counter = Counter()
    if tokenized_text and isinstance(tokenized_text[0], list):
        for verse_tokens in tokenized_text:
            counter.update(verse_tokens)
    else:
        counter.update(tokenized_text)
    return dict(counter)

def analyze_surah_word_frequency(quran_data):
    '''
    Analyze word frequencies aggregated at the Surah level.

    For each Surah, aggregate the preprocessed text from all Ayahs and calculate the frequency of each word.
    Returns a dictionary mapping surah number to a dictionary of word frequencies.
    Logs the top 10 most frequent words for each Surah.

    :param quran_data: List of dictionaries, each containing 'surah', 'ayah', and 'processed_text'.
    :return: Dictionary where keys are surah numbers and values are frequency dictionaries.
    '''
    logger = logging.getLogger(__name__)
    # Mapping for Surah names for selected surahs
    surah_names = {1: "Al-Fatiha", 2: "Al-Baqarah"}
    surah_tokens = {}
    for item in quran_data:
        surah = item.get("surah")
        processed_text = item.get("processed_text", "")
        tokens = processed_text.split()
        if surah in surah_tokens:
            surah_tokens[surah].extend(tokens)
        else:
            surah_tokens[surah] = tokens.copy()
    surah_frequencies = {}
    # Use count_word_frequencies for each Surah (pass flat list of tokens)
    for surah, tokens in surah_tokens.items():
        freq = count_word_frequencies(tokens)
        surah_frequencies[surah] = freq
        # Compute top 10 words
        top_10 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
        surah_name = surah_names.get(surah, f"Surah {surah}")
        logger.info("Surah-level Frequency Analysis - Surah %d (%s) Top 10 Words:", surah, surah_name)
        for word, count in top_10:
            logger.info("Word: %s, Count: %d", word, count)
    return surah_frequencies

def analyze_ayah_word_frequency(quran_data):
    '''
    Analyze word frequencies at the Ayah level.

    For each Ayah, read the preprocessed text and calculate the frequency of each word.
    Stores the results in a nested dictionary keyed by surah and ayah numbers.
    For selected surahs (e.g., Surah Al-Fatiha and Surah Al-Baqarah), logs the top 5 most frequent words for each Ayah.

    :param quran_data: List of dictionaries containing 'surah', 'ayah' and 'processed_text'.
    :return: Nested dictionary where keys are surah numbers and values are dictionaries mapping ayah numbers to frequency dictionaries.
    '''
    logger = logging.getLogger(__name__)
    # Selected surahs for detailed logging
    selected_surahs = {1: "Al-Fatiha", 2: "Al-Baqarah"}
    
    ayah_frequencies = {}
    for item in quran_data:
        surah = item.get("surah")
        ayah = item.get("ayah")
        processed_text = item.get("processed_text", "")
        tokens = processed_text.split()
        counter = {}
        for token in tokens:
            counter[token] = counter.get(token, 0) + 1
        if surah not in ayah_frequencies:
            ayah_frequencies[surah] = {}
        ayah_frequencies[surah][ayah] = counter

        if surah in selected_surahs:
            top_5 = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:5]
            surah_name = selected_surahs[surah]
            logger.info("Ayah-level Frequency Analysis - Surah %d (%s), Ayah %d Top 5 Words:", surah, surah_name, ayah)
            for word, count in top_5:
                logger.info("Word: %s, Count: %d", word, count)
    return ayah_frequencies