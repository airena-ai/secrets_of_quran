import logging

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