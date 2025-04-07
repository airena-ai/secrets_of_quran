import logging
import statistics

def calculate_gematria_value(word):
    '''
    Calculate the Gematria value of the given Arabic word.
    
    Uses a predefined mapping of Arabic letters to their Gematria values. Each letter's 
    numeric value is summed to provide the total Gematria value for the word.
    
    :param word: Arabic word string.
    :return: Total Gematria value as an integer.
    '''
    gematria_map = {
        'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
        'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90,
        'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
        'ء': 1, 'أ': 1, 'ؤ': 1, 'إ': 1, 'ئ': 1, 'ى': 10, 'ة': 5
    }
    total = 0
    logger = logging.getLogger("quran_analysis")
    for char in word:
        value = gematria_map.get(char, 0)
        if value == 0:
            logger.warning("Character '%s' not found in Gematria mapping. Treated as 0.", char)
        total += value
    return total

def analyze_gematria_value_distribution(tokenized_text):
    '''
    Analyze the frequency distribution of Gematria values across all words in the Quran text.
    
    Iterates over the tokenized text (list of lists of words), calculates the Gematria value for each word,
    and updates a count dictionary. Logs the distribution of Gematria values including the top 10 most frequent values.
    
    :param tokenized_text: List of lists of Arabic words.
    :return: Dictionary mapping Gematria values (integers) to their frequency count.
    '''
    logger = logging.getLogger("quran_analysis")
    gematria_value_counts = {}
    
    for tokens in tokenized_text:
        for word in tokens:
            value = calculate_gematria_value(word)
            gematria_value_counts[value] = gematria_value_counts.get(value, 0) + 1
            
    logger.info("Gematria Value Distribution Analysis:")
    logger.info("Complete Gematria Distribution: %s", gematria_value_counts)
    sorted_distribution = sorted(gematria_value_counts.items(), key=lambda item: item[1], reverse=True)
    top_10 = sorted_distribution[:10]
    logger.info("Top 10 most frequent Gematria values:")
    for value, count in top_10:
        logger.info("Gematria Value: %d, Count: %d", value, count)
        
    return gematria_value_counts

def get_default_gematria_mapping():
    '''
    Return the default Gematria mapping of Arabic letters to their numerical values.
    
    :return: Dictionary mapping Arabic letters to Gematria values.
    '''
    return {
        'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
        'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90,
        'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
        'ء': 1, 'أ': 1, 'ؤ': 1, 'إ': 1, 'ئ': 1, 'ى': 10, 'ة': 5
    }

def calculate_gematria_value_with_mapping(word, gematria_mapping):
    '''
    Calculate the Gematria value of the given word using the provided Gematria mapping.
    
    :param word: Arabic word string.
    :param gematria_mapping: Dictionary mapping Arabic letters to numerical values.
    :return: Total Gematria value as an integer.
    '''
    logger = logging.getLogger("quran_analysis")
    total = 0
    for char in word:
        value = gematria_mapping.get(char, 0)
        if value == 0:
            logger.warning("Character '%s' not found in provided Gematria mapping. Treated as 0.", char)
        total += value
    return total

def analyze_surah_gematria_distribution(quran_data, gematria_mapping):
    '''
    Analyze the Gematria value distribution at the Surah level.
    
    For each Surah in quran_data, calculates the frequency distribution and summary statistics (mean, median, mode, stdev)
    of the Gematria values of all words within that Surah. Logs the distribution and summary for each Surah.
    
    :param quran_data: List of dictionaries representing Quran data. Each dictionary should contain "surah" and a text field.
    :param gematria_mapping: Dictionary mapping Arabic letters to Gematria values.
    :return: Dictionary mapping surah identifiers to a dictionary with keys "frequency" and "summary".
    '''
    logger = logging.getLogger("quran_analysis")
    surah_results = {}
    surah_groups = {}
    for item in quran_data:
        surah_id = item.get("surah", "Unknown")
        text = item.get("processed_text") or item.get("verse_text", "")
        words = text.split()
        surah_groups.setdefault(surah_id, []).extend(words)
    
    for surah_id, words in surah_groups.items():
        values = []
        frequency = {}
        for word in words:
            val = calculate_gematria_value_with_mapping(word, gematria_mapping)
            values.append(val)
            frequency[val] = frequency.get(val, 0) + 1
        if values:
            mean_val = statistics.mean(values)
            median_val = statistics.median(values)
            try:
                mode_val = statistics.mode(values)
            except statistics.StatisticsError:
                mode_val = "No unique mode"
            stdev_val = statistics.stdev(values) if len(values) > 1 else 0
        else:
            mean_val = median_val = mode_val = stdev_val = 0
        summary = {"mean": mean_val, "median": median_val, "mode": mode_val, "stdev": stdev_val}
        surah_results[surah_id] = {"frequency": frequency, "summary": summary}
        logger.info("Surah %s: Gematria Distribution: %s", surah_id, frequency)
        logger.info("Surah %s: Summary Stats: Mean=%.2f, Median=%.2f, Mode=%s, Stdev=%.2f", surah_id, mean_val, median_val, mode_val, stdev_val)
    return surah_results

def analyze_ayah_gematria_distribution(quran_data, gematria_mapping):
    '''
    Analyze the Gematria value distribution at the Ayah level.
    
    For each Ayah in quran_data, calculates the frequency distribution and summary statistics (mean, median, mode, stdev)
    of the Gematria values of all words within that Ayah. Logs the distribution and summary for each Ayah.
    
    :param quran_data: List of dictionaries representing Quran data. Each dictionary should contain "surah", "ayah", and a text field.
    :param gematria_mapping: Dictionary mapping Arabic letters to Gematria values.
    :return: Dictionary mapping ayah identifiers (formatted as "surah|ayah") to a dictionary with keys "frequency" and "summary".
    '''
    logger = logging.getLogger("quran_analysis")
    ayah_results = {}
    for item in quran_data:
        surah_id = item.get("surah", "Unknown")
        ayah_id = item.get("ayah", "Unknown")
        identifier = f"{surah_id}|{ayah_id}"
        text = item.get("processed_text") or item.get("verse_text", "")
        words = text.split()
        values = []
        frequency = {}
        for word in words:
            val = calculate_gematria_value_with_mapping(word, gematria_mapping)
            values.append(val)
            frequency[val] = frequency.get(val, 0) + 1
        if values:
            mean_val = statistics.mean(values)
            median_val = statistics.median(values)
            try:
                mode_val = statistics.mode(values)
            except statistics.StatisticsError:
                mode_val = "No unique mode"
            stdev_val = statistics.stdev(values) if len(values) > 1 else 0
        else:
            mean_val = median_val = mode_val = stdev_val = 0
        summary = {"mean": mean_val, "median": median_val, "mode": mode_val, "stdev": stdev_val}
        ayah_results[identifier] = {"frequency": frequency, "summary": summary}
        logger.info("Ayah %s: Gematria Distribution: %s", identifier, frequency)
        logger.info("Ayah %s: Summary Stats: Mean=%.2f, Median=%.2f, Mode=%s, Stdev=%.2f", identifier, mean_val, median_val, mode_val, stdev_val)
    return ayah_results