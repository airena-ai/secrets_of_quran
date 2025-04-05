"""
Module for searching words in the loaded Quran data.
"""

import logging

logger = logging.getLogger(__name__)

ABJAD_VALUES = {
    'ا': 1,
    'ب': 2,
    'ج': 3,
    'د': 4,
    'ه': 5,
    'و': 6,
    'ز': 7,
    'ح': 8,
    'ط': 9,
    'ي': 10,
    'ك': 20,
    'ل': 30,
    'م': 40,
    'ن': 50,
    'س': 60,
    'ع': 70,
    'ف': 80,
    'ص': 90,
    'ق': 100,
    'ر': 200,
    'ش': 300,
    'ت': 400,
    'ث': 500,
    'خ': 600,
    'ذ': 700,
    'ض': 800,
    'ظ': 900,
    'غ': 1000
}

def search_word_in_quran(quran_data, search_word, case_sensitive=False):
    """
    Search for a word in the Quran verses.

    This function iterates over the provided Quran data and checks if the search word is present
    in the verse text. The search can be performed in a case-sensitive or case-insensitive manner.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        search_word (str): The word to search for in the verse text.
        case_sensitive (bool): If True, performs case-sensitive search; otherwise, performs case-insensitive search.
                               Defaults to False.

    Returns:
        list: A list of dictionaries for verses containing the search word.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if search_word in verse_text:
                results.append(verse)
        else:
            if search_word.lower() in verse_text.lower():
                results.append(verse)
    return results

def search_word_group(quran_data, word_group, case_sensitive=False):
    """
    Search for a specific word group (phrase) in the Quran verses.

    This function iterates over the provided Quran data and checks if the given word group, treated
    as an exact phrase, is present in the verse text. The search can be performed in a case-sensitive
    or case-insensitive manner while maintaining the word order.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (exact phrase) to search for in the verse text.
        case_sensitive (bool): If True, performs case-sensitive search; otherwise, performs case-insensitive search.
                               Defaults to False.

    Returns:
        list: A list of dictionaries representing verses that contain the specified word group.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if word_group in verse_text:
                results.append(verse)
        else:
            if word_group.lower() in verse_text.lower():
                results.append(verse)
    return results

def search_word_in_surah(word, surah_number, quran_data):
    """
    Searches for a word within a specific Surah in the Quran data.

    Args:
        word (str): The word to search for (case-insensitive).
        surah_number (int): The Surah number to search within.
        quran_data (list[dict]): The loaded Quran data.

    Returns:
        list[dict]: A list of verses (dictionaries) where the word is found in the specified Surah.
    """
    results = []
    for verse in quran_data:
        try:
            verse_surah_number = int(verse.get('surah_number'))
        except (ValueError, TypeError):
            continue
        if verse_surah_number == surah_number:
            verse_text = verse.get('verse_text', '')
            if word.lower() in verse_text.lower():
                results.append(verse)
    return results

def search_word_group_in_surah(quran_data, word_group, surah_number, case_sensitive=False):
    """
    Search for a specific word group (phrase) within a given Surah of the Quran data.

    This function iterates over the provided Quran data, filtering verses to those that belong
    to the specified Surah (identified by surah_number). It then checks if the given word group,
    treated as an exact phrase, is present in the verse text using either case-sensitive or
    case-insensitive comparison based on the case_sensitive flag.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (exact phrase) to search for in the verse text.
        surah_number (int): The Surah number to filter verses.
        case_sensitive (bool): If True, performs case-sensitive search; otherwise, performs case-insensitive search.
                               Defaults to False.

    Returns:
        list: A list of dictionaries for verses that contain the specified word group within the given Surah.
    """
    results = []
    for verse in quran_data:
        try:
            verse_surah_number = int(verse.get('surah_number'))
        except (ValueError, TypeError):
            continue
        if verse_surah_number == surah_number:
            verse_text = verse.get('verse_text', '')
            if case_sensitive:
                if word_group in verse_text:
                    results.append(verse)
            else:
                if word_group.lower() in verse_text.lower():
                    results.append(verse)
    return results

def count_word_occurrences(quran_data, word):
    """
    Count the total number of occurrences of a word in the entire Quran text data.

    The search is performed in a case-insensitive manner by default, counting all occurrences
    of the specified word as a substring within each verse.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word (str): The word whose occurrences need to be counted.

    Returns:
        int: The total number of occurrences of the word in the Quran data.
    """
    if not word:
        return 0
    word_lower = word.lower()
    total_count = 0
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        total_count += verse_text.lower().count(word_lower)
    return total_count

def count_word_occurrences_in_surah(quran_data, word, surah_number):
    """
    Count the total number of occurrences of a specific word within the specified Surah in the Quran data.

    This function filters the Quran data for verses belonging to the specified Surah (by surah_number)
    and counts all occurrences of the given word as a substring in a case-insensitive manner.
    If the word is an empty string, it returns 0.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word (str): The word to count occurrences for.
        surah_number (int): The Surah number to filter verses.

    Returns:
        int: The total number of occurrences of the word within the specified Surah.
    """
    if not word:
        return 0
    word_lower = word.lower()
    total_count = 0
    for verse in quran_data:
        try:
            verse_surah_num = int(verse.get('surah_number'))
        except (ValueError, TypeError):
            continue
        if verse_surah_num == surah_number:
            verse_text = verse.get('verse_text', '')
            total_count += verse_text.lower().count(word_lower)
    return total_count

def count_word_group_occurrences_in_surah(quran_data, word_group, surah_number):
    """
    Count the total number of occurrences of a specific word group (phrase) within the specified Surah in the Quran data.
    
    This function filters the Quran data for verses belonging to the specified Surah (identified by surah_number)
    and counts all non-overlapping occurrences of the given word group as a substring in a case-insensitive manner.
    If the word group is an empty string, it returns 0.
    
    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (phrase) to count occurrences for.
        surah_number (int): The Surah number to filter verses.
    
    Returns:
        int: The total number of occurrences of the word group within the specified Surah.
    """
    if not word_group:
        return 0
    word_group_lower = word_group.lower()
    total_count = 0
    for verse in quran_data:
        try:
            verse_surah_num = int(verse.get('surah_number'))
        except (ValueError, TypeError):
            continue
        if verse_surah_num == surah_number:
            verse_text = verse.get('verse_text', '')
            total_count += verse_text.lower().count(word_group_lower)
    return total_count

def count_word_group_occurrences(quran_data, word_group):
    """
    Count the total number of occurrences of a word group (phrase) in the entire Quran text data.

    This function iterates over each verse in the provided Quran data and counts all non-overlapping
    occurrences of the specified word group, performing a case-insensitive search by default.
    If the word_group is an empty string, the function returns 0.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (phrase) to count occurrences of.

    Returns:
        int: The total number of occurrences of the word group in the Quran data.
    """
    if not word_group:
        return 0
    word_group_lower = word_group.lower()
    total_count = 0
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        total_count += verse_text.lower().count(word_group_lower)
    return total_count

def search_word_in_verse_range(quran_data, word: str, start_verse: tuple[int, int], end_verse: tuple[int, int], case_sensitive: bool = False) -> list[dict]:
    """
    Searches for a word within a specified verse range in the Quran.

    This function searches the provided quran_data list for verses within the given range
    (inclusive) that contain the specified word. The search is performed in a case-sensitive or
    case-insensitive manner based on the case_sensitive flag.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word (str): The word to search for.
        start_verse (tuple[int, int]): The starting verse of the range as (surah_number, ayah_number).
        end_verse (tuple[int, int]): The ending verse of the range as (surah_number, ayah_number).
        case_sensitive (bool, optional): Whether the search is case-sensitive. Defaults to False.

    Returns:
        list[dict]: A list of dictionaries, each containing verse details where the word is found within the specified range.
    """
    results = []
    for verse in quran_data:
        try:
            surah_num = int(verse.get('surah_number'))
            ayah_num = int(verse.get('ayah_number'))
        except (ValueError, TypeError):
            continue
        current_verse = (surah_num, ayah_num)
        if current_verse < start_verse or current_verse > end_verse:
            continue
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if word in verse_text:
                results.append(verse)
        else:
            if word.lower() in verse_text.lower():
                results.append(verse)
    return results

def search_word_group_in_verse_range(quran_data, word_group: str, start_verse: tuple[int, int], end_verse: tuple[int, int], case_sensitive: bool = False) -> list[dict]:
    """
    Searches for a word group within a specified verse range in the Quran.

    This function searches the provided quran_data for verses within the given range
    (inclusive) that contain the specified word group. The search is performed in a case-sensitive or
    case-insensitive manner based on the case_sensitive flag.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (phrase) to search for.
        start_verse (tuple[int, int]): The starting verse of the range as (surah_number, ayah_number).
        end_verse (tuple[int, int]): The ending verse of the range as (surah_number, ayah_number).
        case_sensitive (bool, optional): Whether the search is case-sensitive. Defaults to False.

    Returns:
        list[dict]: A list of dictionaries, each containing verse details where the word group is found within the specified range.
    """
    results = []
    for verse in quran_data:
        try:
            surah_num = int(verse.get('surah_number'))
            ayah_num = int(verse.get('ayah_number'))
        except (ValueError, TypeError):
            continue
        current_verse = (surah_num, ayah_num)
        if current_verse < start_verse or current_verse > end_verse:
            continue
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if word_group in verse_text:
                results.append(verse)
        else:
            if word_group.lower() in verse_text.lower():
                results.append(verse)
    return results

def count_word_occurrences_in_verse_range(quran_data, word: str, start_verse: tuple[int, int], end_verse: tuple[int, int], case_sensitive: bool = False) -> int:
    """
    Count the total occurrences of a specific word within a defined verse range in the Quran data.
    
    This function iterates over the provided Quran data and selects verses whose (surah_number, ayah_number)
    falls within the inclusive range defined by start_verse and end_verse. It then counts all non-overlapping
    occurrences of the specified word in each verse, using either case-sensitive or case-insensitive matching.
    
    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word (str): The word to be counted.
        start_verse (tuple[int, int]): The starting verse as a tuple (surah_number, ayah_number).
        end_verse (tuple[int, int]): The ending verse as a tuple (surah_number, ayah_number).
        case_sensitive (bool, optional): Whether the count operation should be case-sensitive. Defaults to False.
    
    Returns:
        int: The cumulative count of the word in the verses within the specified range.
    """
    if not word:
        return 0
    total_count = 0
    for verse in quran_data:
        try:
            surah_num = int(verse.get('surah_number'))
            ayah_num = int(verse.get('ayah_number'))
        except (ValueError, TypeError):
            continue
        current_verse = (surah_num, ayah_num)
        if current_verse < start_verse or current_verse > end_verse:
            continue
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            total_count += verse_text.count(word)
        else:
            total_count += verse_text.lower().count(word.lower())
    return total_count

def search_verses_by_word_count(quran_data, word_count):
    """
    Search Quran verses that contain exactly the specified number of words.

    Iterates over the provided quran_data, splitting each verse's verse_text into words, and collects
    verses where the number of words is exactly equal to word_count.

    Args:
        quran_data (list): List of dictionaries representing Quran verses.
        word_count (int): The desired number of words in a verse.

    Returns:
        list: A list of dictionaries, each containing a verse with exactly word_count words.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        words = verse_text.split()
        if len(words) == word_count:
            results.append(verse)
    return results

def search_verses_by_word_count_multiple(quran_data, multiple_of):
    """
    Search for Quran verses where the number of words is a multiple of a specified number.

    Iterates over the provided quran_data, splitting each verse's verse_text into words, 
    and collects verses where the number of words is an exact multiple of multiple_of.

    Args:
        quran_data (list): List of dictionaries representing Quran verses.
        multiple_of (int): The integer multiple to check against. Must be a non-zero integer.

    Returns:
        list: A list of dictionaries, each containing a verse where the word count is a multiple of multiple_of.

    Raises:
        ValueError: If multiple_of is zero.
    """
    if multiple_of == 0:
        raise ValueError("multiple_of must be non-zero")
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        words = verse_text.split()
        if len(words) % multiple_of == 0:
            results.append(verse)
    return results

def calculate_gematrical_value(text: str) -> int:
    """
    Calculate the gematrical (Abjad) value of a given Arabic word or phrase.

    This function computes the sum of the numerical values of the Arabic letters in the input
    text based on the standard Abjad numeral mapping. Characters not present in the mapping are ignored.

    Args:
        text (str): An Arabic word or phrase.

    Returns:
        int: The gematrical value calculated by summing the Abjad numeral values of characters in the text.
    """
    total = 0
    for char in text:
        total += ABJAD_VALUES.get(char, 0)
    return total

def search_words_by_gematrical_value(quran_data, target_value: int) -> list:
    """
    Search for words in the Quran that have the specified gematrical value.

    This function iterates over each verse in the provided Quran data. It splits the verse text into individual words,
    calculates the gematrical value of each word using the calculate_gematrical_value function,
    and returns a list of dictionaries for words that match the specified target gematrical value.
    Each dictionary contains the matching word and its location (surah and ayah numbers).

    Args:
        quran_data (list): List of dictionaries representing Quran verses.
        target_value (int): The target gematrical value to match.

    Returns:
        list: A list of dictionaries. Each dictionary has the keys 'word', 'surah_number', and 'ayah_number' for each matching word.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        words = verse_text.split()
        for word in words:
            if calculate_gematrical_value(word) == target_value:
                results.append({
                    'word': word,
                    'surah_number': verse.get('surah_number'),
                    'ayah_number': verse.get('ayah_number')
                })
    return results

def search_word_groups_by_gematrical_value(quran_data, word_group, target_value, case_sensitive=False):
    """
    Search for word groups in the Quran that have a specific gematrical value.

    This function iterates over the provided Quran data. For each verse, it performs a case-(in)sensitive search for the 
    specified word group (phrase). If the word group is found in the verse, its gematrical value is calculated using 
    calculate_gematrical_value. If the calculated gematrical value matches the target value, the verse is added to the results.

    Args:
        quran_data (list): List of dictionaries representing Quran verses.
        word_group (str): The word group (phrase) to search for.
        target_value (int): The target gematrical value to match for the word group.
        case_sensitive (bool, optional): If True, performs a case-sensitive search; otherwise, performs case-insensitive search.
                                         Defaults to False.

    Returns:
        list: A list of dictionaries representing verses where the word group is found and its gematrical value matches target_value.
    """
    logger.info("Searching for word group '%s' with target gematrical value %d", word_group, target_value)
    computed_value = calculate_gematrical_value(word_group)
    if computed_value != target_value:
        logger.info("Computed gematrical value %d does not match target %d", computed_value, target_value)
        return []
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if word_group in verse_text:
                results.append(verse)
        else:
            if word_group.lower() in verse_text.lower():
                results.append(verse)
    logger.info("Found %d verses containing word group '%s'", len(results), word_group)
    return results

def calculate_surah_gematrical_value(quran_data, surah_number: int) -> int:
    """
    Calculate the total gematrical value of all words within a specified Surah.
    
    This function filters the Quran data for verses that belong to the given Surah number,
    then splits each verse's text into individual words. The gematrical value of each word is computed
    using the calculate_gematrical_value function, and these values are summed to obtain the total value for the Surah.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        surah_number (int): The Surah number to calculate the gematrical value for.

    Returns:
        int: The total gematrical value of all words in the specified Surah.
    """
    logger.info("Calculating gematrical value for Surah %d", surah_number)
    total_value = 0
    for verse in quran_data:
        try:
            current_surah = int(verse.get('surah_number'))
        except (ValueError, TypeError):
            continue
        if current_surah != surah_number:
            continue
        verse_text = verse.get('verse_text', '')
        # Split the verse text into words based on whitespace.
        words = verse_text.split()
        for word in words:
            total_value += calculate_gematrical_value(word)
    return total_value

def calculate_verse_range_gematrical_value(quran_data, start_verse_num: int, end_verse_num: int) -> int:
    """
    Calculate the total gematrical value for verses in the specified overall verse number range.

    This function iterates over the Quran data, considering each verse's overall position (starting at 1).
    For every verse whose overall verse number falls within the range [start_verse_num, end_verse_num] (inclusive),
    it computes the gematrical value using calculate_gematrical_value and accumulates the total.

    Args:
        quran_data (list): List of dictionaries representing Quran verses.
        start_verse_num (int): The starting overall verse number (inclusive).
        end_verse_num (int): The ending overall verse number (inclusive).

    Returns:
        int: The total gematrical value of all verses within the specified range.
    """
    total = 0
    for idx, verse in enumerate(quran_data, start=1):
        if start_verse_num <= idx <= end_verse_num:
            verse_text = verse.get('verse_text', '')
            total += calculate_gematrical_value(verse_text)
    return total

def calculate_quran_gematrical_value(quran_data) -> int:
    """
    Calculate the total gematrical value of the entire Quran.
    
    This function iterates through each verse in the provided Quran data, splits the verse text into individual words,
    calculates the gematrical value of each word using the calculate_gematrical_value function, and sums these values
    to produce the total gematrical value for the entire Quran.

    Args:
        quran_data (list): List of dictionaries representing Quran verses. Each dictionary should have a 'verse_text' key.

    Returns:
        int: The total gematrical value computed for all verses.
    """
    total_value = 0
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        words = verse_text.split()
        for word in words:
            total_value += calculate_gematrical_value(word)
    return total_value

def search_word_at_position(quran_data, word, position):
    """
    Search for verses where the specified word appears at the given position within the verse.

    The search is performed in a case-insensitive manner, and the position parameter is 1-indexed.
    If the specified position is greater than the number of words in a verse, that verse is skipped.

    Args:
        quran_data (list): A list of dictionaries representing Quran verses.
        word (str): The word to search for.
        position (int): The 1-indexed position to look for the word in each verse.

    Returns:
        list: A list of verses (dictionaries) where the word is found at the specified position.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        words = verse_text.split()
        if position <= len(words) and words[position - 1].lower() == word.lower():
            results.append(verse)
    return results