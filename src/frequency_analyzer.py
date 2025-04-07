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

def analyze_word_length_distribution(tokenized_text):
    '''
    Analyze the distribution of word lengths within the tokenized Quran text.
    
    For each word in the tokenized text, calculate its length and count the occurrences
    of each word length. Also, compute summary statistics such as total number of words,
    average word length, and the most frequent word length(s).
    
    :param tokenized_text: List of lists of words, where each inner list represents an ayah.
    :return: Dictionary mapping word lengths (int) to their frequency counts (int).
    '''
    logger = logging.getLogger(__name__)
    counter = Counter()
    total_words = 0
    total_length = 0
    for ayah in tokenized_text:
        for word in ayah:
            word_length = len(word)
            counter[word_length] += 1
            total_words += 1
            total_length += word_length
    avg_word_length = total_length / total_words if total_words > 0 else 0
    max_freq = max(counter.values()) if counter else 0
    most_frequent_word_lengths = [length for length, count in counter.items() if count == max_freq]
    logger.info("Word Length Distribution Analysis:")
    logger.info("Total words analyzed: %d", total_words)
    logger.info("Word Length Distribution: %s", dict(counter))
    logger.info("Average word length: %.2f", avg_word_length)
    logger.info("Most frequent word length(s): %s (Count: %d)", most_frequent_word_lengths, max_freq)
    return dict(counter)

def analyze_root_word_frequency(tokenized_text):
    '''
    Analyze the frequency distribution of root words across the tokenized Quran text.
    
    This function iterates through each verse and counts the occurrences of each unique root word.
    It logs the top 20 most frequent root words along with their counts, as well as the total number
    of unique root words found in the Quran.
    
    :param tokenized_text: List of lists of root word tokens, where each inner list represents an ayah.
    :return: Dictionary with unique root words as keys and their frequency counts as values.
    '''
    logger = logging.getLogger(__name__)
    logger.info("Root Word Frequency Analysis started.")
    counter = Counter()
    if tokenized_text and isinstance(tokenized_text[0], list):
        for verse_tokens in tokenized_text:
            counter.update(verse_tokens)
    else:
        counter.update(tokenized_text)
    unique_count = len(counter)
    top_20 = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:20]
    logger.info("Total unique root words found: %d", unique_count)
    logger.info("Top 20 most frequent root words:")
    for root, count in top_20:
        logger.info("Root: %s, Count: %d", root, count)
    logger.info("Root Word Frequency Analysis completed.")
    return dict(counter)