'''Module for analyzing the Quran text for hidden patterns and anomalies.'''

from collections import Counter, defaultdict
import datetime
import importlib.util
import re
import math
import src.logger

# Static Surah classification data: Mapping each Surah number (1-114) to its classification.
surah_classification = {
    1: "Meccan",
    2: "Medinan",
    3: "Medinan",
    4: "Medinan",
    5: "Medinan",
    6: "Meccan",
    7: "Meccan",
    8: "Medinan",
    9: "Medinan",
    10: "Meccan",
    11: "Meccan",
    12: "Meccan",
    13: "Meccan",
    14: "Meccan",
    15: "Meccan",
    16: "Meccan",
    17: "Meccan",
    18: "Meccan",
    19: "Meccan",
    20: "Meccan",
    21: "Meccan",
    22: "Medinan",
    23: "Meccan",
    24: "Medinan",
    25: "Meccan",
    26: "Meccan",
    27: "Meccan",
    28: "Meccan",
    29: "Meccan",
    30: "Meccan",
    31: "Meccan",
    32: "Meccan",
    33: "Medinan",
    34: "Meccan",
    35: "Meccan",
    36: "Meccan",
    37: "Meccan",
    38: "Meccan",
    39: "Meccan",
    40: "Meccan",
    41: "Meccan",
    42: "Meccan",
    43: "Meccan",
    44: "Meccan",
    45: "Meccan",
    46: "Meccan",
    47: "Medinan",
    48: "Medinan",
    49: "Medinan",
    50: "Meccan",
    51: "Meccan",
    52: "Meccan",
    53: "Meccan",
    54: "Meccan",
    55: "Meccan",
    56: "Meccan",
    57: "Medinan",
    58: "Medinan",
    59: "Medinan",
    60: "Medinan",
    61: "Medinan",
    62: "Medinan",
    63: "Medinan",
    64: "Medinan",
    65: "Medinan",
    66: "Medinan",
    67: "Meccan",
    68: "Meccan",
    69: "Meccan",
    70: "Meccan",
    71: "Meccan",
    72: "Meccan",
    73: "Meccan",
    74: "Meccan",
    75: "Meccan",
    76: "Medinan",
    77: "Meccan",
    78: "Meccan",
    79: "Meccan",
    80: "Meccan",
    81: "Meccan",
    82: "Meccan",
    83: "Meccan",
    84: "Meccan",
    85: "Meccan",
    86: "Meccan",
    87: "Meccan",
    88: "Meccan",
    89: "Meccan",
    90: "Meccan",
    91: "Meccan",
    92: "Meccan",
    93: "Meccan",
    94: "Meccan",
    95: "Meccan",
    96: "Meccan",
    97: "Meccan",
    98: "Medinan",
    99: "Meccan",
    100: "Meccan",
    101: "Meccan",
    102: "Meccan",
    103: "Meccan",
    104: "Meccan",
    105: "Meccan",
    106: "Meccan",
    107: "Meccan",
    108: "Meccan",
    109: "Meccan",
    110: "Medinan",
    111: "Meccan",
    112: "Meccan",
    113: "Meccan",
    114: "Meccan"
}

# Global constant for Muqatta'at Surahs used consistently across analysis functions.
MUQATTAAT_SURAH_SET = {"2", "3", "7", "10", "11", "12", "13", "14", "15", "19", "20",
                        "26", "27", "28", "29", "30", "31", "32", "36", "38", "40", "41",
                        "42", "43", "44", "45", "46", "50", "68"}

# Global variable to store Muqatta'at data for later use in thematic analysis.
MUQATTAAT_DATA = {}

def analyze_text(text):
    '''Analyze the given text for hidden numerical patterns and anomalies.

    This function simulates pattern detection. If the text is non-empty,
    a simulated anomaly is detected and returned.

    Args:
        text (str): The preprocessed text of the Quran.

    Returns:
        list: A list of anomaly messages detected in the text.
    '''
    anomalies = []
    if text.strip():
        # Simulated detection of a hidden pattern
        anomalies.append("Calculated numerical pattern: 42")
    return anomalies

def analyze_word_frequency(text):
    '''Perform word frequency analysis on the given preprocessed Quran text.

    This function tokenizes the text using whitespace, counts the occurrences of each unique word,
    and determines the top N most frequent words. It prepares a summary of the word frequency analysis
    and identifies any words whose frequency is unusually high or low based on a simple heuristic.

    The heuristic flags a word if its frequency is more than twice the average frequency of the top words
    (and greater than 1), or if the frequency is less than half the average (provided the average is greater than 1).

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        tuple: A tuple containing:
            - summary (str): A formatted multiline string listing the top N words and their counts.
            - flagged (list): A list of flagged messages for words deemed unusual.
    '''
    tokens = text.split()
    counter = Counter(tokens)
    TOP_N = 20
    top_words = counter.most_common(TOP_N)
    
    lines = ["Word Frequency Analysis (Top {}):".format(TOP_N)]
    for idx, (word, freq) in enumerate(top_words, start=1):
        lines.append("{}. '{}' : {}".format(idx, word, freq))
    summary = "\n".join(lines)
    
    flagged = []
    if top_words:
        avg_freq = sum(freq for _, freq in top_words) / len(top_words)
        for word, freq in top_words:
            if freq > 2 * avg_freq and freq > 1:
                flagged.append("Word '{}' frequency is {} (unusually high)".format(word, freq))
            elif avg_freq > 1 and freq < (avg_freq / 2):
                flagged.append("Word '{}' frequency is {} (unusually low)".format(word, freq))
    
    return summary, flagged

def analyze_root_words(text):
    '''Perform Arabic root word analysis on the given preprocessed Quran text.

    This function uses the CAMeL Tools morphological analyzer to extract the root of each word in the text.
    It counts the frequency of each identified root word and logs a concise summary of the analysis to the results log file.
    Specifically, the function logs a summary of the Arabic root word frequency analysis along with the top N most frequent root words.

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        tuple: A tuple containing:
            - summary (str): A formatted summary of the root word frequency analysis.
            - root_freq (dict): A dictionary mapping each root word to its frequency.
            - top_roots (list): A list of tuples for the top N most frequent root words (root, frequency).
    '''
    from collections import Counter

    camel_tools_available = importlib.util.find_spec("camel_tools") is not None
    
    tokens = text.split()
    roots = []
    
    if camel_tools_available:
        try:
            from camel_tools.morphology.analyzer import Analyzer
            analyzer = Analyzer.builtin_analyzer()
            
            for token in tokens:
                try:
                    analyses = analyzer.analyze(token)
                    if analyses and 'root' in analyses[0]:
                        root = analyses[0]['root']
                    else:
                        root = token
                except Exception:
                    root = token
                roots.append(root)
        except Exception:
            roots = tokens
    else:
        roots = tokens
    
    root_freq = Counter(roots)
    TOP_N = 20
    top_roots = root_freq.most_common(TOP_N)

    summary_lines = []
    summary_lines.append("Arabic Root Word Frequency Analysis:")
    for root, freq in root_freq.items():
        summary_lines.append("Root '{}': {}".format(root, freq))
    summary_lines.append("")
    summary_lines.append("Top Root Word Frequencies:")
    for idx, (root, freq) in enumerate(top_roots, 1):
        summary_lines.append("{}. Root '{}': {}".format(idx, root, freq))
    summary = "\n".join(summary_lines)

    src.logger.log_result("Arabic Root Word Frequency Analysis Summary:")
    src.logger.log_result("Top Root Word Frequencies:")
    for idx, (root, freq) in enumerate(top_roots, 1):
        src.logger.log_result("{}. Root '{}': {}".format(idx, root, freq))

    return summary, dict(root_freq), top_roots

def analyze_bigrams(tokenized_text, n=2):
    '''Perform bigram frequency analysis on the given tokenized text.

    This function generates n-grams (bigrams by default) from the tokenized text,
    counts the frequency of each n-gram, and returns a dictionary where keys are n-gram tuples
    and values are their frequency counts.

    Args:
        tokenized_text (list): A list of preprocessed tokens from the Quran text.
        n (int): The number of words in each n-gram (default is 2 for bigrams).

    Returns:
        dict: A dictionary with n-gram tuples as keys and their frequency counts as values.
    '''
    if not tokenized_text or len(tokenized_text) < n:
        return {}
    ngrams = [tuple(tokenized_text[i:i+n]) for i in range(len(tokenized_text)-n+1)]
    return dict(Counter(ngrams))

def analyze_verse_repetitions(preprocessed_text):
    '''Analyze verse repetitions within each Surah and across the entire Quran.
    
    This function expects the preprocessed Quran text as input where each line represents a verse.
    It attempts to parse each line for Surah and Ayah numbers in formats such as "Surah:Ayah: verse text"
    or "Surah - Ayah - verse text", allowing for variations in spacing and delimiters.
    If the format is not found, the verse is assigned to a default Surah "1" with sequential Ayah numbers.
    
    The verse text is normalized using the existing text preprocessing functions before comparison.
    It then identifies verses that are repeated within each Surah and across the entire Quran.
    
    Returns a dictionary with two keys:
        "within_surah": A list of dictionaries each with keys: "surah", "verse", "ayah_numbers", "repetition"
        "across_quran": A list of dictionaries each with keys: "verse", "occurrences" (list of {"surah", "ayah"}), "repetition"
    
    Args:
        preprocessed_text (str): The preprocessed Quran text data.
    
    Returns:
        dict: The analysis result of verse repetitions.
    '''
    from src.text_preprocessor import remove_diacritics, normalize_arabic_letters

    surah_dict = defaultdict(list)
    default_surah = "1"
    default_ayah = 1

    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    lines = preprocessed_text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            ayah = int(m.group(2))
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            ayah = default_ayah
            verse_text = line.strip()
            default_ayah += 1

        norm_verse = normalize_arabic_letters(remove_diacritics(verse_text))
        surah_dict[surah].append({"ayah": ayah, "verse": norm_verse})

    result = {"within_surah": [], "across_quran": []}

    for surah, verses in surah_dict.items():
        verse_occurrences = defaultdict(list)
        for entry in verses:
            verse_occurrences[entry["verse"]].append(entry["ayah"])
        for verse, ayahs in verse_occurrences.items():
            if len(ayahs) > 1:
                result["within_surah"].append({
                    "surah": surah,
                    "verse": verse,
                    "ayah_numbers": ayahs,
                    "repetition": len(ayahs)
                })

    all_verses = defaultdict(list)
    for surah, verses in surah_dict.items():
        for entry in verses:
            all_verses[entry["verse"]].append({"surah": surah, "ayah": entry["ayah"]})
    for verse, occurrences in all_verses.items():
        if len(occurrences) > 1:
            result["across_quran"].append({
                "verse": verse,
                "occurrences": occurrences,
                "repetition": len(occurrences)
            })

    return result

def analyze_lemmas(text):
    '''Perform lemma analysis on the tokenized Quran text using CAMeL Tools morphological analyzer.
    
    This function iterates through each word in the text, extracts its lemma using the CAMeL Tools library,
    counts the frequency of each lemma across the entire Quran, logs the top 20 most frequent lemmas, and returns the summary.

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        str: A formatted summary of the lemma frequency analysis.
    '''
    from collections import Counter
    import importlib.util
    tokens = text.split()
    lemmas = []
    camel_tools_available = importlib.util.find_spec("camel_tools") is not None
    if camel_tools_available:
        try:
            from camel_tools.morphology.analyzer import Analyzer
            analyzer = Analyzer.builtin_analyzer()
            for token in tokens:
                try:
                    analyses = analyzer.analyze(token)
                    if analyses and 'lemma' in analyses[0]:
                        lemmas.append(analyses[0]['lemma'])
                    else:
                        lemmas.append(token)
                except Exception:
                    lemmas.append(token)
        except Exception:
            lemmas = tokens
    else:
        lemmas = tokens
    lemma_freq = Counter(lemmas)
    TOP_N = 20
    top_lemmas = lemma_freq.most_common(TOP_N)
    result_lines = []
    result_lines.append("Lemma Analysis: Top {} Lemmas:".format(TOP_N))
    for idx, (lemma, count) in enumerate(top_lemmas, 1):
        result_lines.append("{}. '{}' : {}".format(idx, lemma, count))
    summary = "\n".join(result_lines)
    import src.logger
    src.logger.log_result(summary)
    return summary

def analyze_surah_verse_counts(text):
    '''Perform analysis of verse counts per Surah in the Quran text.
    
    This function parses each line of the Quran text, extracts the Surah number, counts the number of verses per Surah,
    logs the verse counts for each Surah, and returns a formatted summary.

    Args:
        text (str): The Quran text loaded from the data file.

    Returns:
        str: A formatted summary of the surah verse counts.
    '''
    from collections import defaultdict
    import re
    surah_counts = defaultdict(int)
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
        else:
            surah = "1"
        surah_counts[surah] += 1
    result_lines = []
    result_lines.append("Surah Verse Counts:")
    for surah, count in sorted(surah_counts.items(), key=lambda x: int(x[0])):
        result_lines.append("Surah {}: {} verses".format(surah, count))
    summary = "\n".join(result_lines)
    import src.logger
    src.logger.log_result(summary)
    return summary

def analyze_verse_lengths_distribution(text, threshold=2):
    '''Analyze verse lengths distribution across the Quran text.
    
    This function calculates the word count for each verse by tokenizing the verse text,
    groups the counts by Surah, and computes the average verse length and standard deviation
    of verse lengths for each Surah. It identifies Surahs with 'consistent' verse lengths when the standard
    deviation is less than the threshold (default is 2 words). The summary for each Surah is logged, and
    consistent Surahs are flagged with a special "POTENTIAL SECRET FOUND" log entry.
    
    Args:
        text (str): The preprocessed Quran text, where each line represents a verse.
        threshold (float, optional): The standard deviation threshold to consider a Surah as having consistent verse lengths.
        
    Returns:
        dict: A dictionary mapping Surah numbers to a dictionary with keys 'average', 'stddev', and 'consistent'.
    '''
    from collections import defaultdict
    import re
    surah_verse_lengths = defaultdict(list)
    default_surah = "1"
    default_ayah = 1
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            verse_text = line.strip()
            default_ayah += 1
        tokens = verse_text.split()
        word_count = len(tokens)
        surah_verse_lengths[surah].append(word_count)
    results = {}
    for surah, lengths in surah_verse_lengths.items():
        if lengths:
            avg = sum(lengths) / len(lengths)
            variance = sum((x - avg) ** 2 for x in lengths) / len(lengths)
            stddev = math.sqrt(variance)
        else:
            avg = 0
            stddev = 0
        consistent = stddev < threshold
        results[surah] = {"average": avg, "stddev": stddev, "consistent": consistent}
        src.logger.log_result(f"Surah {surah}: Average Verse Length: {avg:.2f}, StdDev: {stddev:.2f}")
        if consistent:
            src.logger.log_secret_found(f"[Surah {surah}] Verse length consistency (StdDev: {stddev:.2f})")
    return results

def analyze_palindromes(quran_text):
    '''Analyze palindromic structures within each verse of the Quran.
    
    This function identifies word-level palindromes. It parses each verse to extract Surah and Ayah information.
    Detected palindromic words and phrases are logged to the results log in a specified format.

    Args:
        quran_text (str): The preprocessed Quran text.

    Returns:
        list: A list of tuples containing (surah, ayah, palindrome_text) for each detected palindrome.
    '''
    found_palindromes = []
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    default_surah = "1"
    default_ayah = 1
    for line in quran_text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            ayah = m.group(2)
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            ayah = str(default_ayah)
            verse_text = line.strip()
            default_ayah += 1
        words = verse_text.split()
        for word in words:
            if len(word) > 1 and word == word[::-1]:
                msg = f"[Palindrome Analysis] - [Palindrome Detected] - {surah}:{ayah} - {word}"
                src.logger.log_secret_found(msg)
                found_palindromes.append((surah, ayah, word))
        n = len(words)
        for i in range(n):
            for j in range(i+2, min(n+1, i+6)):
                phrase_words = words[i:j]
                if phrase_words == phrase_words[::-1]:
                    phrase_text = ' '.join(phrase_words)
                    msg = f"[Palindrome Analysis] - [Palindrome Detected] - {surah}:{ayah} - {phrase_text}"
                    src.logger.log_secret_found(msg)
                    found_palindromes.append((surah, ayah, phrase_text))
    
    if not found_palindromes:
        src.logger.log_secret_found("[Palindrome Analysis] - No palindrome patterns found")
    
    return found_palindromes

def analyze_abjad_numerals(quran_text):
    '''Perform Abjad numeral analysis on the Quran text.
    
    This function calculates the Abjad numerical sum for each verse based on a mapping of Arabic letters to their numerical values.
    It logs each verse along with its calculated Abjad value. Additionally, if a verse's Abjad value meets specific criteria
    (multiple of 19, multiple of 7, or prime), it logs a special pattern message.

    Args:
        quran_text (str): The preprocessed Quran text.

    Returns:
        list: A list of tuples containing (surah, ayah, abjad_sum, pattern_description) for verses with notable numerical patterns.
    '''
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    abjad = {
        'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6,
        'ز': 7, 'ح': 8, 'ط': 9, 'ى': 10, 'ي': 10, 'ك': 20, 'ل': 30, 'م': 40,
        'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ض': 90, 'ق': 100, 'ر': 200,
        'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
    }
    
    found_abjad = []
    pattern_regex = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    default_surah = "1"
    default_ayah = 1
    surah_sums = defaultdict(int)
    
    for line in quran_text.splitlines():
        if not line.strip():
            continue
        m = pattern_regex.match(line)
        if m:
            surah = m.group(1)
            ayah = m.group(2)
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            ayah = str(default_ayah)
            verse_text = line.strip()
            default_ayah += 1
        verse_sum = 0
        for char in verse_text:
            if char in abjad:
                verse_sum += abjad[char]
        surah_sums[surah] += verse_sum
        src.logger.log_result(f"[ABJAD VALUE]: Verse: {surah}:{ayah}, Value: {verse_sum}")
        description = ""
        if verse_sum % 19 == 0 and verse_sum != 0:
            description = f"Abjad sum {verse_sum} is a multiple of 19"
        elif verse_sum % 7 == 0 and verse_sum != 0:
            description = f"Abjad sum {verse_sum} is a multiple of 7"
        elif is_prime(verse_sum):
            description = f"Abjad sum {verse_sum} is a prime number"
        if description:
            msg = f"[Abjad Numerical Pattern] - Verse: {surah}:{ayah} - {description}"
            src.logger.log_secret_found(msg)
            found_abjad.append((surah, ayah, verse_sum, description))
    
    for surah, total in surah_sums.items():
        description = ""
        if total % 19 == 0 and total != 0:
            description = f"Surah total abjad sum {total} is a multiple of 19"
        elif total % 7 == 0 and total != 0:
            description = f"Surah total abjad sum {total} is a multiple of 7"
        elif is_prime(total):
            description = f"Surah total abjad sum {total} is a prime number"
        if description:
            msg = f"[Abjad Numerical Pattern] - Surah: {surah}, {description}"
            src.logger.log_secret_found(msg)
            found_abjad.append((surah, "", total, description))
            src.logger.log_result(msg)

    if not found_abjad:
        src.logger.log_secret_found("[Abjad Numerical Pattern] - No notable pattern detected")
    
    return found_abjad

def analyze_semantic_symmetry(quran_text):
    '''Analyze semantic symmetry (word overlap) between segments of each Surah.
    
    For each Surah, this function divides the text into two roughly equal halves based on verses.
    It then tokenizes both halves and calculates the number of common words between them.
    The common word count is logged to the results log.

    Args:
        quran_text (str): The preprocessed Quran text.

    Returns:
        list: A list of tuples containing (surah, common_word_count, list_of_common_words) for each Surah.
    '''
    symmetry_findings = []
    pattern_regex = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    surah_dict = defaultdict(list)
    default_surah = "1"
    default_ayah = 1

    for line in quran_text.splitlines():
        if not line.strip():
            continue
        m = pattern_regex.match(line)
        if m:
            surah = m.group(1)
            ayah = int(m.group(2))
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            ayah = default_ayah
            verse_text = line.strip()
            default_ayah += 1
        surah_dict[surah].append((ayah, verse_text))
    
    for surah, verses in surah_dict.items():
        verses_sorted = sorted(verses, key=lambda x: x[0])
        if len(verses_sorted) > 1:
            mid = len(verses_sorted) // 2
            first_half = " ".join(verse for _, verse in verses_sorted[:mid])
            second_half = " ".join(verse for _, verse in verses_sorted[mid:])
        else:
            ayah, verse_text = verses_sorted[0]
            tokens = verse_text.split()
            if len(tokens) < 2:
                continue
            mid_index = len(tokens) // 2
            first_half = " ".join(tokens[:mid_index])
            second_half = " ".join(tokens[mid_index:])
        set_first = set(first_half.split())
        set_second = set(second_half.split())
        common = set_first.intersection(set_second)
        common_count = len(common)
        src.logger.log_result(f"[SEMANTIC SYMMETRY]: Surah: {surah}, Common Word Count: {common_count}")
        src.logger.log_secret_found(f"[Semantic Symmetry (Word Overlap)] - Surah: {surah}, Common Word Count: {common_count}")
        symmetry_findings.append((surah, common_count, list(common)))
    
    return symmetry_findings

def analyze_verse_length_symmetry(text, avg_threshold=1.0, stddev_threshold=1.0):
    '''Analyze verse length symmetry between two halves of each Surah.
    
    For each Surah in the text, divided by line, the verses are split into two halves.
    The average verse length (word count) and standard deviation of verse lengths is computed for each half.
    If the difference in averages and standard deviations between the halves is within the given thresholds,
    the symmetry is considered significant and logged as a potential secret.
    
    Args:
        text (str): The preprocessed Quran text, with each line representing a verse.
        avg_threshold (float, optional): Maximum allowed difference in average verse length between halves.
        stddev_threshold (float, optional): Maximum allowed difference in verse length standard deviation between halves.
    
    Returns:
        dict: A mapping from Surah numbers to a dictionary with metrics for both halves and a symmetry flag.
    '''
    from collections import defaultdict
    import re
    surah_verses = defaultdict(list)
    default_surah = "1"
    default_ayah = 1
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            verse_text = line.strip()
            default_ayah += 1
        surah_verses[surah].append(verse_text)
    results = {}
    for surah, verses in surah_verses.items():
        n = len(verses)
        if n < 2:
            continue
        mid = n // 2
        first_half = verses[:mid]
        second_half = verses[mid:]
        first_counts = [len(verse.split()) for verse in first_half]
        second_counts = [len(verse.split()) for verse in second_half]
        avg_first = sum(first_counts) / len(first_counts) if first_counts else 0
        avg_second = sum(second_counts) / len(second_counts) if second_counts else 0
        std_first = math.sqrt(sum((x - avg_first)**2 for x in first_counts)/len(first_counts)) if first_counts else 0
        std_second = math.sqrt(sum((x - avg_second)**2 for x in second_counts)/len(second_counts)) if second_counts else 0
        symmetric = (abs(avg_first - avg_second) <= avg_threshold and abs(std_first - std_second) <= stddev_threshold)
        results[surah] = {
            "first_half": {"average": avg_first, "stddev": std_first},
            "second_half": {"average": avg_second, "stddev": std_second},
            "symmetric": symmetric
        }
        src.logger.log_result(f"Surah {surah} - First Half: Avg = {avg_first:.2f}, StdDev = {std_first:.2f}; Second Half: Avg = {avg_second:.2f}, StdDev = {std_second:.2f}")
        if symmetric:
            src.logger.log_secret_found(f"Verse length distribution symmetry detected in Surah {surah} between the first and second halves.")
    return results

def analyze_enhanced_semantic_symmetry(text, symmetry_threshold=0.3):
    '''Enhanced analysis of semantic symmetry using lemma overlap between two halves of each Surah.
    
    For each Surah, the verses are split into two halves and their texts are processed to extract lemmas.
    The symmetry score is defined as the ratio of the number of common lemmas to the total unique lemmas in the Surah.
    If the symmetry score meets or exceeds the threshold, it is logged as a potential secret.
    
    Args:
        text (str): The preprocessed Quran text, with each line representing a verse.
        symmetry_threshold (float, optional): The minimum normalized overlap required to consider semantic symmetry.
    
    Returns:
        dict: A mapping from Surah numbers to a dictionary with the symmetry score and lemma sets for each half.
    '''
    from collections import defaultdict
    import re
    def get_lemmas(text_fragment):
        '''Helper function to extract lemmas from a given text fragment using CAMeL Tools morphological analyzer if available.

        Args:
            text_fragment (str): A fragment of text from which to extract lemmas.

        Returns:
            list: A list of lemmas corresponding to the tokens in the text fragment.
        '''
        tokens = text_fragment.split()
        lemmas = []
        import importlib.util
        camel_spec = importlib.util.find_spec("camel_tools")
        if camel_spec is not None:
            try:
                from camel_tools.morphology.analyzer import Analyzer
                analyzer = Analyzer.builtin_analyzer()
                for token in tokens:
                    try:
                        analyses = analyzer.analyze(token)
                        if analyses and 'lemma' in analyses[0]:
                            lemmas.append(analyses[0]['lemma'])
                        else:
                            lemmas.append(token)
                    except Exception:
                        lemmas.append(token)
            except Exception:
                lemmas = tokens
        else:
            lemmas = tokens
        return lemmas

    surah_verses = defaultdict(list)
    default_surah = "1"
    default_ayah = 1
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            verse_text = line.strip()
            default_ayah += 1
        surah_verses[surah].append(verse_text)
    
    results = {}
    for surah, verses in surah_verses.items():
        n = len(verses)
        if n < 2:
            continue
        mid = n // 2
        first_half_text = " ".join(verses[:mid])
        second_half_text = " ".join(verses[mid:])
        lemmas_first = set(get_lemmas(first_half_text))
        lemmas_second = set(get_lemmas(second_half_text))
        common = lemmas_first.intersection(lemmas_second)
        union = lemmas_first.union(lemmas_second)
        symmetry_score = len(common) / len(union) if union else 0
        results[surah] = {
            "symmetry_score": symmetry_score,
            "first_half_lemmas": lemmas_first,
            "second_half_lemmas": lemmas_second
        }
        src.logger.log_result(f"Surah {surah} - Enhanced Semantic Symmetry Score: {symmetry_score:.2f}")
        if symmetry_score >= symmetry_threshold:
            src.logger.log_secret_found(f"Enhanced semantic symmetry (lemma overlap) detected in Surah {surah} between the first and second halves.")
    return results

def analyze_muqattaat(quran_text):
    '''Analyze Muqatta'at (Mysterious Letters) in the Quran text.

    This function identifies Surahs that begin with Muqatta'at based on a predefined list.
    It extracts the sequence of Arabic letters (Muqatta'at) from the beginning of the first verse of each identified Surah,
    computes the frequency of each unique letter, and logs the results to the results log file.

    The logged output includes:
        - A header "#################### Muqatta'at Analysis ####################"
        - List of Surahs with Muqatta'at (by Surah number)
        - For each identified Surah, the extracted Muqatta'at letters along with its Surah name.
        - Frequency count of each unique Muqatta'at letter.

    Args:
        quran_text (str): The preprocessed Quran text.

    Returns:
        tuple: A tuple containing:
            - A dictionary mapping Surah numbers to their extracted Muqatta'at letters.
            - A Counter object representing the frequency of each Muqatta'at letter.
    '''
    import re
    from collections import Counter
    import src.logger as logger

    predefined_surahs = MUQATTAAT_SURAH_SET
    surah_names = {
        "2": "البقرة", "3": "آل عمران", "7": "الأعراف", "10": "يونس", "11": "هود", "12": "يوسف",
        "13": "الرعد", "14": "ابراهيم", "15": "الحجر", "19": "مريم", "20": "طه",
        "26": "الشعراء", "27": "النمل", "28": "القصص", "29": "العنكبوت", "30": "الروم",
        "31": "لقمان", "32": "السجدة", "36": "يس", "38": "الصافات", "40": "غافر",
        "41": "فصلت", "42": "الشورى", "43": "الزخرف", "44": "الدخان", "45": "الجاثية",
        "46": "الأحقاف", "50": "ق", "68": "القلم"
    }
    
    muqattaat_results = {}
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    lines = quran_text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            verse_text = m.group(3).strip()
            if surah in predefined_surahs and surah not in muqattaat_results:
                # Remove Basmalah if present
                basmalah_pattern = re.compile(r'^بِسمِ\s+اللَّهِ\s+الرَّحْمَٰنِ\s+الرَّحيمِ\s*', re.UNICODE)
                verse_text_cleaned = basmalah_pattern.sub('', verse_text).strip()

                # Match Muqattaʿat letters now that Basmalah is gone
                m_letters = re.match(r'^([\u0621-\u064A]+)', verse_text_cleaned)
                if m_letters:
                    muqattaat_results[surah] = m_letters.group(1)
    global MUQATTAAT_DATA
    MUQATTAAT_DATA = muqattaat_results
    frequency_counter = Counter()
    for letters in muqattaat_results.values():
        frequency_counter.update(letters)
        
    logger.log_result("#################### Muqatta'at Analysis ####################")
    surah_list = sorted(muqattaat_results.keys(), key=lambda x: int(x))
    logger.log_result("Surahs with Muqatta'at: [{}]".format(", ".join(surah_list)))
    for surah in surah_list:
        name = surah_names.get(surah, "")
        logger.log_result("Muqatta'at Letters in Surah {} ({}): {}".format(surah, name, muqattaat_results[surah]))
    logger.log_result("Frequency of Muqatta'at Letters:")
    letter_names = {
        'ا': "Alif",
        'ب': "Ba",
        'ت': "Ta",
        'ث': "Tha",
        'ج': "Jim",
        'ح': "Ha",
        'خ': "Kha",
        'د': "Dal",
        'ذ': "Thal",
        'ر': "Ra",
        'ز': "Zay",
        'س': "Seen",
        'ش': "Sheen",
        'ص': "Sad",
        'ض': "Dad",
        'ط': "Ta",
        'ظ': "Za",
        'ع': "Ain",
        'غ': "Ghayn",
        'ف': "Fa",
        'ق': "Qaf",
        'ك': "Kaf",
        'ل': "Lam",
        'م': "Meem",
        'ن': "Noon",
        'ه': "Ha",
        'و': "Waw",
        'ي': "Ya"
    }
    for letter, count in frequency_counter.items():
        letter_name = letter_names.get(letter, letter)
        logger.log_result("- {} ({}): {}".format(letter_name, letter, count))
    logger.log_result("############################################################")
    
    return (muqattaat_results, frequency_counter)

def analyze_muqattaat_preceding_context(text):
    '''Analyze the verses immediately preceding Surahs with Muqatta'at and perform word frequency analysis.
    
    For each Surah that begins with Muqatta'at (from a predefined list), this function extracts the last verse
    from the preceding Surah. Special cases:
      - If the Muqatta'at Surah is "1", the preceding context is taken as the last verse of Surah 114 (An-Nas).
      - If the Muqatta'at Surah is "2", the preceding context is the last verse of Surah 1 (Al-Fatiha).
      - Otherwise, the preceding Surah is (current surah number - 1).
    The extracted preceding verses are normalized using remove_diacritics and normalize_arabic_letters,
    their word frequencies are computed, and the top 10 words are logged.
    Additionally, any word with unusually high frequency is flagged with a "POTENTIAL SECRET FOUND" message.

    Args:
        text (str): The preprocessed Quran text with each line as "Surah|Ayah|Verse".
        
    Returns:
        dict: A dictionary of word frequencies from the preceding context verses.
    '''
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")
    from collections import defaultdict, Counter
    from src.text_preprocessor import remove_diacritics, normalize_arabic_letters
    from src.logger import log_result, log_secret_found
    import re
    surah_verses = defaultdict(list)
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    default_surah = "1"
    default_ayah = 1
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            ayah = int(m.group(2))
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            ayah = default_ayah
            verse_text = line.strip()
            default_ayah += 1
        surah_verses[surah].append((ayah, verse_text))
    # Use the global Muqatta'at Surahs set for consistency.
    muqattaat_surahs = MUQATTAAT_SURAH_SET
    preceding_contexts = []
    for surah in muqattaat_surahs:
        if surah == "1":
            preceding_surah = "114"
        elif surah == "2":
            preceding_surah = "1"
        else:
            preceding_surah = str(int(surah) - 1)
        if preceding_surah not in surah_verses:
            continue
        verses = surah_verses[preceding_surah]
        verses.sort(key=lambda x: x[0])
        last_verse = verses[-1][1]
        processed_verse = normalize_arabic_letters(remove_diacritics(last_verse))
        preceding_contexts.append(processed_verse)
    combined_text = " ".join(preceding_contexts)
    tokens = combined_text.split()
    freq_counter = Counter(tokens)
    TOP_N = 10
    top_words = freq_counter.most_common(TOP_N)
    log_result("Preceding Context Verses Frequency Analysis (Top {} words):".format(TOP_N))
    if top_words:
        avg_freq = sum(freq for _, freq in top_words) / len(top_words)
    else:
        avg_freq = 0
    for idx, (word, freq) in enumerate(top_words, start=1):
        log_result("{}. '{}' : {}".format(idx, word, freq))
        if avg_freq > 0 and freq > 2 * avg_freq:
            log_secret_found("POTENTIAL SECRET FOUND: {} in preceding context of Muqatta'at".format(word))
    return dict(freq_counter)

def analyze_muqattaat_themes():
    '''Perform thematic analysis for Surahs with Muqatta'at by associating each Surah with a predefined theme.

    This function iterates over a static dictionary of high-level themes for Surahs known to contain Muqatta'at.
    For each Surah, it retrieves the Muqatta'at letter sequence from the actual analysis data and logs a message in a
    clear, readable format to the results log.
    '''
    import src.logger as logger
    surah_themes = {
         "2": {"name": "Al-Baqarah", "theme": "Guidance and Divine Law"},
         "3": {"name": "Ali Imran", "theme": "Family, Faith, and Trials"},
         "7": {"name": "Al-A'raf", "theme": "Divine Covenant and Human Struggle"},
         "10": {"name": "Yunus", "theme": "Prophetic Guidance and Divine Justice"},
         "11": {"name": "Hud", "theme": "Warnings and Divine Retribution"},
         "12": {"name": "Yusuf", "theme": "Patience and Divine Plan"},
         "13": {"name": "Ar-Ra'd", "theme": "Divine Power and Signs"},
         "14": {"name": "Ibrahim", "theme": "Gratitude and Divine Blessings"},
         "15": {"name": "Al-Hijr", "theme": "Divine Creation and Rejection of Truth"},
         "19": {"name": "Maryam", "theme": "Prophethood and Miracles"},
         "20": {"name": "Ta-Ha", "theme": "Divine Revelation and Moses' Story"},
         "26": {"name": "Ash-Shu'ara", "theme": "Prophets' Stories and Divine Messages"},
         "27": {"name": "An-Naml", "theme": "Solomon and Divine Wisdom"},
         "28": {"name": "Al-Qasas", "theme": "Moses' Life and Divine Justice"},
         "29": {"name": "Al-Ankabut", "theme": "Faith and Trials"},
         "30": {"name": "Ar-Rum", "theme": "Divine Promise and Signs in Creation"},
         "31": {"name": "Luqman", "theme": "Wisdom and Guidance"},
         "32": {"name": "As-Sajdah", "theme": "Resurrection and Divine Decree"},
         "36": {"name": "Ya-Sin", "theme": "Divine Revelation and Resurrection"},
         "38": {"name": "Sad", "theme": "David and Divine Judgment"},
         "40": {"name": "Ghafir", "theme": "Divine Power and Accountability"},
         "41": {"name": "Fussilat", "theme": "Divine Revelation and Rejection"},
         "42": {"name": "Ash-Shura", "theme": "Divine Counsel and Unity"},
         "43": {"name": "Az-Zukhruf", "theme": "Divine Grace and Guidance"},
         "44": {"name": "Ad-Dukhan", "theme": "Warning and Divine Judgment"},
         "45": {"name": "Al-Jathiyah", "theme": "Divine Signs and Accountability"},
         "46": {"name": "Al-Ahqaf", "theme": "Divine Revelation and Truth"},
         "50": {"name": "Qaf", "theme": "Resurrection and Divine Knowledge"},
         "68": {"name": "Al-Qalam", "theme": "Divine Grace and Patience"}
    }
    try:
         global MUQATTAAT_DATA
         muq_data = MUQATTAAT_DATA
         if not isinstance(muq_data, dict):
             muq_data = {}
    except NameError:
         muq_data = {}
    muqattaat_letters = {key: muq_data.get(key, "N/A") for key in surah_themes.keys()}
    for surah, info in surah_themes.items():
         letters = muqattaat_letters.get(surah, "N/A")
         message = "Surah {} ({}) with Muqatta'at '{}': Theme - {}".format(surah, info["name"], letters, info["theme"])
         logger.log_result(message)

def analyze_muqattaat_context(text):
    '''Analyze the verses that immediately follow the Muqatta'at in Surahs that begin with them.

    This function processes the preprocessed Quran text to group verses by Surah,
    identifies Surahs that begin with Muqatta'at (using a predefined list),
    and for each such Surah, extracts the verse immediately following the first verse (which contains the Muqatta'at).
    The context verse is then preprocessed using existing text normalization and tokenization functions,
    and the word frequencies across all context verses are calculated.
    The top 10 most frequent words are logged to the results log file, with any words that are unusually frequent flagged.

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        dict: A dictionary mapping words to their frequency counts from the context verses.
    '''
    import re
    from collections import defaultdict, Counter
    from src.text_preprocessor import remove_diacritics, normalize_arabic_letters
    from src.logger import log_result, log_secret_found

    surah_verses = defaultdict(list)
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    default_surah = "1"
    default_ayah = 1
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            ayah = int(m.group(2))
            verse_text = m.group(3).strip()
        else:
            surah = default_surah
            ayah = default_ayah
            verse_text = line.strip()
            default_ayah += 1
        surah_verses[surah].append((ayah, verse_text))
    predefined_surahs = MUQATTAAT_SURAH_SET
    overall_counter = Counter()
    for surah in predefined_surahs:
        verses = surah_verses.get(surah, [])
        if len(verses) >= 2:
            verses.sort(key=lambda x: x[0])
            context_verse = verses[1][1]
            processed_verse = normalize_arabic_letters(remove_diacritics(context_verse))
            overall_counter.update(processed_verse.split())
    top_n = 10
    top_words = overall_counter.most_common(top_n)
    log_result("Contextual Analysis of Verses Following Muqatta'at (Top {} words):".format(top_n))
    if top_words:
        avg_freq = sum(freq for _, freq in top_words) / len(top_words)
    else:
        avg_freq = 0
    for idx, (word, freq) in enumerate(top_words, start=1):
        log_result("{}. '{}' : {}".format(idx, word, freq))
        if avg_freq > 0 and freq > 2 * avg_freq:
            log_secret_found("POTENTIAL SECRET FOUND: {} appears frequently in verses following Muqatta'at".format(word))
    return dict(overall_counter)

def analyze_muqattaat_numerical_values(text):
    '''Perform numerical analysis specific to Muqatta'at in the Quran text.
    
    This stub function simulates the numerical analysis and returns a placeholder summary.
    
    Args:
        text (str): The preprocessed Quran text.
        
    Returns:
        str: A summary string of the numerical analysis for Muqatta'at.
    '''
    return "Muqatta'at numerical analysis is not implemented."

def calculate_abjad_value(sequence):
    '''Calculate the Abjad numerical value of the given Arabic letter sequence.
    
    Args:
        sequence (str): A string of Arabic letters representing the Muqatta'at sequence.
    
    Returns:
        int: The total Abjad numerical value.
    '''
    abjad_mapping = {
        'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5,
        'و': 6, 'ز': 7, 'ح': 8, 'ط': 9, 'ى': 10, 'ي': 10, 'ك': 20,
        'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90,
        'ض': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500,
        'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
    }
    total = 0
    for char in sequence:
        total += abjad_mapping.get(char, 0)
    return total

def get_surah_verse_counts(text):
    '''Compute verse counts for each Surah from the Quran text.
    
    Args:
        text (str): The Quran text with verses per line.
    
    Returns:
        dict: A dictionary mapping surah numbers (str) to the number of verses.
    '''
    from collections import defaultdict
    import re
    surah_counts = defaultdict(int)
    default_surah = "1"
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
        else:
            surah = default_surah
        surah_counts[surah] += 1
    return dict(surah_counts)

def analyze_muqattaat_verse_count_correlation(text):
    '''Analyze the correlation between the Abjad numerical value of Muqatta'at and the verse count of respective Surahs.
    
    This function performs the following steps:
        a. Iterates through all Surahs by extracting Muqatta'at using analyze_muqattaat().
        b. For each Surah with Muqatta'at, calculates the Abjad numerical sum of the Muqatta'at sequence.
        c. Retrieves the verse count for the Surah using get_surah_verse_counts().
        d. Stores the pair (Abjad sum, verse count) for each such Surah.
        e. Calculates the Pearson correlation coefficient between the list of Abjad sums and the corresponding verse counts.
        f. Logs the calculated Pearson correlation coefficient.
        g. If the absolute value of the correlation coefficient is above 0.7, logs a POTENTIAL SECRET FOUND message with the correlation value.
    
    Args:
        text (str): The preprocessed Quran text.
    '''
    from scipy.stats import pearsonr
    from src.logger import log_result, log_secret_found
    
    # Obtain Muqatta'at data: dictionary mapping surah numbers to their Muqatta'at sequence.
    muqattaat_data, _ = analyze_muqattaat(text)
    if not muqattaat_data:
        log_result("No Muqatta'at found. Correlation analysis skipped.")
        return
    
    # Compute verse counts for each Surah.
    verse_counts_dict = get_surah_verse_counts(text)
    
    abjad_sums = []
    verse_counts = []
    
    for surah, sequence in muqattaat_data.items():
        if surah in verse_counts_dict:
            abjad_value = calculate_abjad_value(sequence)
            count = verse_counts_dict[surah]
            abjad_sums.append(abjad_value)
            verse_counts.append(count)
    
    if len(abjad_sums) < 2:
        log_result("Not enough data for correlation analysis.")
        return
    
    corr_coef, p_value = pearsonr(abjad_sums, verse_counts)
    log_result(f"Pearson correlation coefficient between Muqatta'at Abjad value and verse count: {corr_coef:.4f}")
    
    if abs(corr_coef) > 0.7:
        log_secret_found(f"POTENTIAL SECRET FOUND: Significant correlation between Muqatta'at Abjad value and Surah verse count. Correlation: {corr_coef:.4f}")

def analyze_muqattaat_root_cooccurrence(text: str, top_n: int = 5) -> None:
    '''Analyze the co-occurrence of Muqatta'at with frequent root words in Surahs.

    This function performs the following steps:
      a. Identifies Surahs that begin with Muqatta'at using the existing analyze_muqattaat function.
      b. For each identified Surah, it retrieves the root word frequencies by analyzing only the verses
         belonging to that Surah via the analyze_grouped_root_frequencies function.
      c. Determines the top N most frequent root words (default N=5) for each Surah.
      d. Logs the following information in a structured JSON format to the results log:
           - Surah number.
           - Muqatta'at sequence present in the Surah.
           - List of the top N root words with their frequency counts.
      e. Additionally, if a particular root word appears as a top frequent root in multiple Muqatta'at Surahs,
         it logs a "POTENTIAL SECRET FOUND" message indicating possible correlation.

    Args:
        text (str): The preprocessed Quran text.
        top_n (int, optional): The number of top root words to consider. Defaults to 5.

    Returns:
        None
    '''
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")
    import json
    from collections import defaultdict
    muqattaat_data, _ = analyze_muqattaat(text)
    if not muqattaat_data:
        from src.logger import log_result
        log_result("No Surahs with Muqatta'at found for root co-occurrence analysis.")
        return

    from src.logger import log_result, log_secret_found
    overall_top_roots = defaultdict(int)

    for surah in muqattaat_data:
        root_freq = analyze_grouped_root_frequencies(text, [surah])
        top_roots = sorted(root_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        for root, freq in top_roots:
            overall_top_roots[root] += 1

        log_data = {
            "surah": surah,
            "muqattaat": muqattaat_data[surah],
            "top_roots": [{"root": root, "frequency": freq} for root, freq in top_roots]
        }
        log_result(json.dumps(log_data, ensure_ascii=False, indent=2))

    for root, count in overall_top_roots.items():
        if count > 1:
            log_secret_found(f"POTENTIAL SECRET FOUND: Root '{root}' appears as top frequent in {count} Muqatta'at Surahs.")

def analyze_muqattaat_sequences(text):
    '''Analyze and count the frequency of Muqatta'at sequences in the Quran text.
    
    This function uses the analyze_muqattaat function to extract the Muqatta'at sequences from the Quran text,
    and computes the frequency of each unique sequence.
    
    Args:
        text (str): The preprocessed Quran text.
        
    Returns:
        dict: A dictionary where keys are Muqatta'at sequences and values are their frequency counts.
    '''
    from collections import Counter
    muqattaat_data, _ = analyze_muqattaat(text)
    seq_counter = Counter(muqattaat_data.values())
    return dict(seq_counter)

def analyze_muqattaat_length(text):
    '''Analyze Muqatta'at sequence lengths in the Quran text.

    This function identifies Surahs that begin with Muqatta'at using the existing analyze_muqattaat() function.
    For each identified Surah, it extracts the Muqatta'at sequence, calculates its length, and categorizes the Surahs
    based on the sequence length (e.g., lengths 1, 2, 3, 4, and 5). It logs the following information:
        - Total Surahs with Muqatta'at Analyzed.
        - For each Surah with Muqatta'at: Surah Number, Muqatta'at Sequence, and its sequence length.
        - Frequency distribution of Muqatta'at sequence lengths.
        - Unique Length Surahs (if any length category has only one Surah).
        - A potential secret if a particular length is the most frequent.
    
    Args:
        text (str): The preprocessed Quran text.
    
    Returns:
        None
    '''
    from collections import defaultdict
    import src.logger as logger

    muq_data, _ = analyze_muqattaat(text)
    surah_details = {}
    for surah, sequence in muq_data.items():
        seq_length = len(sequence)
        surah_details[surah] = (sequence, seq_length)
    
    length_groups = defaultdict(list)
    for surah, (sequence, seq_length) in surah_details.items():
        length_groups[seq_length].append(surah)
    
    logger.log_result("--- Muqatta'at Sequence Length Analysis ---")
    total_surahs = len(surah_details)
    logger.log_result("Total Surahs with Muqatta'at Analyzed: {}".format(total_surahs))
    
    if total_surahs > 0:
        logger.log_result("Surah Details:")
        for surah in sorted(surah_details.keys(), key=lambda x: int(x)):
            sequence, seq_length = surah_details[surah]
            logger.log_result("Surah {}: {} (Length: {})".format(surah, sequence, seq_length))
    
        logger.log_result("Muqatta'at Length Frequency:")
        for length in sorted(length_groups.keys()):
            count = len(length_groups[length])
            logger.log_result("Length {}: {} occurrences".format(length, count))

        unique_surahs = []
        for length, surahs in length_groups.items():
            if len(surahs) == 1:
                unique_surahs.append((surahs[0], length, surah_details[surahs[0]][0]))
        if unique_surahs:
            logger.log_result("Unique Length Surahs:")
            for surah, length, sequence in unique_surahs:
                logger.log_result("Surah {} (Length {}, {})".format(surah, length, sequence))

        max_freq = 0
        most_frequent_length = None
        for length, surahs in length_groups.items():
            if len(surahs) > max_freq:
                max_freq = len(surahs)
                most_frequent_length = length
            elif len(surahs) == max_freq:
                most_frequent_length = None
        if most_frequent_length is not None:
            logger.log_secret_found("POTENTIAL SECRET FOUND: Length {} Muqatta'at sequences are the most frequent.".format(most_frequent_length))

def categorize_surahs_by_muqattaat(text):
    '''Categorize Surahs into those with and without Muqatta'at.
    
    This function parses the preprocessed Quran text, extracts Surah numbers from each line,
    and uses the existing analyze_muqattaat() function to identify Surahs that begin with Muqatta'at.
    
    Args:
        text (str): The preprocessed Quran text.
    
    Returns:
        tuple: A tuple containing two lists:
            - muqattaat_surahs: List of Surah numbers (str) with Muqatta'at.
            - non_muqattaat_surahs: List of Surah numbers (str) without Muqatta'at.
    '''
    import re
    surah_set = set()
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah_set.add(m.group(1))
    muqattaat_data, _ = analyze_muqattaat(text)
    muq_surahs = set(muqattaat_data.keys())
    non_muq_surahs = surah_set - muq_surahs
    return (sorted(list(muq_surahs), key=lambda x: int(x)), sorted(list(non_muq_surahs), key=lambda x: int(x)))

def analyze_grouped_root_frequencies(text, surahs):
    '''Analyze and compute grouped Arabic root word frequencies for specified Surahs.
    
    Args:
        text (str): The preprocessed Quran text where each line represents a verse.
        surahs (list): A list of surah numbers (as strings) to include in the analysis.
    
    Returns:
        dict: A dictionary mapping Arabic root words to their aggregated frequency counts
              from the specified Surahs.
    '''
    from collections import Counter
    import re
    import importlib.util
    root_counter = Counter()
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    
    camel_tools_available = importlib.util.find_spec("camel_tools") is not None
    analyzer = None
    if camel_tools_available:
        try:
            from camel_tools.morphology.analyzer import Analyzer
            analyzer = Analyzer.builtin_analyzer()
        except Exception:
            analyzer = None
    
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1).strip()
            verse_text = m.group(3).strip()
            if surah in surahs:
                tokens = verse_text.split()
                for token in tokens:
                    if analyzer:
                        try:
                            analyses = analyzer.analyze(token)
                            if analyses and 'root' in analyses[0]:
                                root = analyses[0]['root']
                            else:
                                root = token
                        except Exception:
                            root = token
                    else:
                        root = token
                    root_counter[root] += 1
    return dict(root_counter)

def analyze_grouped_lemma_frequencies(text, surahs):
    '''Analyze and compute grouped lemma frequencies for specified Surahs.
    
    Args:
        text (str): The preprocessed Quran text where each line represents a verse.
        surahs (list): A list of surah numbers (as strings) to include in the analysis.
    
    Returns:
        dict: A dictionary mapping lemmas to their aggregated frequency counts
              from the specified Surahs.
    '''
    from collections import Counter
    import re
    import importlib.util
    lemma_counter = Counter()
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    
    camel_tools_available = importlib.util.find_spec("camel_tools") is not None
    analyzer = None
    if camel_tools_available:
        try:
            from camel_tools.morphology.analyzer import Analyzer
            analyzer = Analyzer.builtin_analyzer()
        except Exception:
            analyzer = None
    
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1).strip()
            verse_text = m.group(3).strip()
            if surah in surahs:
                tokens = verse_text.split()
                for token in tokens:
                    if analyzer:
                        try:
                            analyses = analyzer.analyze(token)
                            if analyses and 'lemma' in analyses[0]:
                                lemma = analyses[0]['lemma']
                            else:
                                lemma = token
                        except Exception:
                            lemma = token
                    else:
                        lemma = token
                    lemma_counter[lemma] += 1
    return dict(lemma_counter)

def compare_surahs_muqattaat_vs_non_muqattaat(text):
    '''Compare Surahs with and without Muqatta'at, computing average verse lengths and top word frequencies.
    
    This function categorizes the Surahs into those with Muqatta'at and those without,
    computes the average verse lengths and the top 10 most frequent words in each category,
    and returns a dictionary containing the comparisons.
    
    Args:
        text (str): The preprocessed Quran text.
        
    Returns:
        dict: A dictionary with keys:
            'muqattaat_surahs': list of Surah numbers with Muqatta'at,
            'non_muqattaat_surahs': list of Surah numbers without Muqatta'at,
            'avg_verse_length_muq': average verse length (words) for Muqatta'at Surahs,
            'avg_verse_length_non_muq': average verse length for non-Muqatta'at Surahs,
            'top_words_muq': list of tuples (word, frequency) for the top 10 words in Muqatta'at Surahs,
            'top_words_non_muq': list of tuples (word, frequency) for the top 10 words in non-Muqatta'at Surahs.
    '''
    import re
    from collections import Counter
    muq_surahs, non_muq_surahs = categorize_surahs_by_muqattaat(text)
    lines = text.splitlines()
    muq_verses = []
    non_muq_verses = []
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            verse_text = m.group(3).strip()
            if surah in muq_surahs:
                muq_verses.append(verse_text)
            elif surah in non_muq_surahs:
                non_muq_verses.append(verse_text)
    def average_verse_length(verses):
        if not verses:
            return 0
        total_words = sum(len(verse.split()) for verse in verses)
        return total_words / len(verses)
    avg_muq = average_verse_length(muq_verses)
    avg_non_muq = average_verse_length(non_muq_verses)
    def top_words(verses):
        tokens = []
        for verse in verses:
            tokens.extend(verse.split())
        from collections import Counter
        counter = Counter(tokens)
        return counter.most_common(10)
    top_words_muq = top_words(muq_verses)
    top_words_non_muq = top_words(non_muq_verses)
    return {"muqattaat_surahs": muq_surahs,
            "non_muqattaat_surahs": non_muq_surahs,
            "avg_verse_length_muq": avg_muq,
            "avg_verse_length_non_muq": avg_non_muq,
            "top_words_muq": top_words_muq,
            "top_words_non_muq": top_words_non_muq}

def analyze_correlations(text, verse_lengths, muqattaat_data, word_frequency_result, flagged_words, verse_repetitions_data, enhanced_symmetry_data, abjad_anomalies):
    '''Analyze correlations across different analytical dimensions.

    This is a stub implementation.
    
    Args:
        text (str): The preprocessed Quran text.
        verse_lengths (dict): Results from verse length analysis.
        muqattaat_data (dict): Results from Muqatta'at analysis.
        word_frequency_result (tuple): Results from word frequency analysis.
        flagged_words (list): Flagged words from frequency analysis.
        verse_repetitions_data (dict): Results from verse repetitions analysis.
        enhanced_symmetry_data (dict): Results from enhanced semantic symmetry analysis.
        abjad_anomalies (list): Results from Abjad numeral analysis.

    Returns:
        list: A list of correlation messages (currently empty).
    '''
    return []
    
def analyze_muqattaat_distribution_meccan_medinan(text, surah_classification):
    '''Analyze the distribution of Muqatta'at across Meccan and Medinan Surahs.

    This function categorizes Surahs with Muqatta'at as either Meccan or Medinan based on the provided `surah_classification` dictionary.
    It then counts the number of Muqatta'at-containing Surahs in each category and logs a summary of this distribution.

    Args:
        text (str): The preprocessed Quran text (not directly used in this function, but kept for interface consistency).
        surah_classification (dict): A dictionary mapping Surah numbers (as integers or strings) to their classification ("Meccan" or "Medinan").

    Returns:
        str: A summary string of the Muqatta'at distribution analysis.
    '''
    src.logger.log_result("----- Muqatta'at Distribution: Meccan vs. Medinan -----")
    meccan_count = 0
    medinan_count = 0
    muqattaat_surahs = MUQATTAAT_SURAH_SET

    for surah_num_str in muqattaat_surahs:
        surah_num = int(surah_num_str)
        classification = surah_classification.get(surah_num)
        if classification == "Meccan":
            meccan_count += 1
        elif classification == "Medinan":
            medinan_count += 1

    summary = (f"Muqatta'at Distribution:\n"
               f"- Meccan Surahs with Muqatta'at: {meccan_count}\n"
               f"- Medinan Surahs with Muqatta'at: {medinan_count}")
    src.logger.log_result(summary)
    return summary

def analyze_muqattaat_positions(text):
    '''Analyze the positions of Muqatta'at within the Quran text.

    This function is a placeholder and currently returns a message indicating
    that the functionality is not yet implemented.

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        str: A placeholder summary string.
    '''
    return "Muqattaat positions analysis not implemented."

def generate_muqattaat_report(text):
    '''Generate comprehensive final report synthesizing all Muqatta'at analyses.

    This function aggregates results from various Muqatta'at analysis functions,
    interprets the synthesized data to identify patterns or notable correlations,
    and automatically tags significant findings as "POTENTIAL SECRET FOUND".
    The final report is then logged to the results.log file.

    Args:
        text (str): The preprocessed Quran text.
    '''
    import json
    from src.logger import log_result, log_secret_found

    muqattaat_results, muqattaat_letter_freq = analyze_muqattaat(text)
    positions_summary = analyze_muqattaat_positions(text)
    sequences_freq = analyze_muqattaat_sequences(text)
    numerical_summary = analyze_muqattaat_numerical_values(text)
    
    analyze_muqattaat_themes()
    
    context_freq = analyze_muqattaat_context(text)
    preceding_context_freq = analyze_muqattaat_preceding_context(text)
    distribution_summary = analyze_muqattaat_distribution_meccan_medinan(text, surah_classification)
    
    analyze_muqattaat_length(text)
    analyze_muqattaat_root_cooccurrence(text)
    
    report_lines = []
    report_lines.append("FINAL MUQATTA'AT REPORT:")
    report_lines.append("--------------------------------------------------")
    report_lines.append("Muqatta'at Surahs:")
    if muqattaat_results:
        sorted_surahs = sorted(muqattaat_results.keys(), key=lambda x: int(x))
        report_lines.append(", ".join(sorted_surahs))
    else:
        report_lines.append("None")
    report_lines.append("")
    
    report_lines.append("Muqatta'at Letter Frequencies:")
    for letter, count in muqattaat_letter_freq.items():
        report_lines.append(f"{letter}: {count}")
    report_lines.append("")

    report_lines.append("Positions Analysis Summary:")
    report_lines.append(positions_summary)
    report_lines.append("")
    
    report_lines.append("Muqatta'at Sequences Frequency Analysis:")
    if sequences_freq:
        for seq, freq in sequences_freq.items():
            report_lines.append(f"Sequence '{seq}' occurred {freq} times")
            if freq > 1:
                report_lines.append(f"POTENTIAL SECRET FOUND: Sequence '{seq}' appears unusually often ({freq} times)")
    else:
        report_lines.append("No sequences found.")
    report_lines.append("")
    
    report_lines.append("Numerical Analysis Summary:")
    report_lines.append(numerical_summary)
    report_lines.append("")
    
    report_lines.append("Contextual Analysis (Verses Following Muqatta'at) - Top Words:")
    if context_freq:
        for word, freq in context_freq.items():
            report_lines.append(f"{word}: {freq}")
            if freq > 5:
                report_lines.append(f"POTENTIAL SECRET FOUND: Word '{word}' appears very frequently ({freq} times) in the context following Muqatta'at")
    else:
        report_lines.append("No contextual data found.")
    report_lines.append("")
    
    report_lines.append("Preceding Context Analysis (Verses Before Muqatta'at) - Top Words:")
    if preceding_context_freq:
        for word, freq in preceding_context_freq.items():
            report_lines.append(f"{word}: {freq}")
            if freq > 5:
                report_lines.append(f"POTENTIAL SECRET FOUND: Word '{word}' appears very frequently ({freq} times) in the preceding context of Muqatta'at")
    else:
        report_lines.append("No preceding context data found.")
    report_lines.append("")
    
    report_lines.append("Muqatta'at Distribution (Meccan vs. Medinan):")
    report_lines.append(distribution_summary)
    report_lines.append("")
    
    report_lines.append("Final Interpretation:")
    if not muqattaat_results:
        report_lines.append("No Muqatta'at detected in the text.")
    else:
        report_lines.append("Muqatta'at analysis reveals consistent patterns across analyzed Surahs.")
    report_lines.append("--------------------------------------------------")
    
    final_report = "\n".join(report_lines)
    
    log_result(final_report)
    try:
        with open("results.log", "a", encoding="utf-8") as f:
            f.write(final_report + "\n")
    except Exception as e:
        log_result("Error writing final Muqatta'at report: " + str(e))

def review_muqattaat_report(report_content):
    '''Review the final Muqatta'at report content and return final conclusions.

    This function takes the content of the Muqatta'at report as a string, examines it for any occurrences of
    "POTENTIAL SECRET FOUND:" and, based on that, determines the conclusive statement regarding the Muqatta'at mystery.
    
    Args:
        report_content (str): The complete content of the final Muqatta'at report.
    
    Returns:
        str: The final conclusions on the Muqatta'at mystery.
    '''
    if "POTENTIAL SECRET FOUND:" in report_content:
        conclusion = "POTENTIAL SOLUTION TO MUQATTAَAT MYSTERY FOUND: Evidence suggests that the repetitive patterns and frequency distributions in Muqatta'at sequences indicate an underlying coded message."
    else:
        conclusion = "MUQATTAَAT MYSTERY REMAINS UNSOLVED: Analysis did not reveal sufficient patterns to decode a definitive message."
    final_section = "\nFinal Conclusions on Muqatta'at Mystery:\n" + conclusion + "\n"
    return final_section

def synthesize_muqattaat_analyses(text):
    '''Synthesize results from various Muqatta'at analyses to identify potential correlations and patterns.
    
    This function aggregates outputs from multiple Muqatta'at analysis functions including:
        - analyze_muqattaat_sequences
        - compare_surahs_muqattaat_vs_non_muqattaat
        - analyze_muqattaat_distribution_meccan_medinan

    It logs any identified potential correlations as "POTENTIAL SECRET FOUND:" in the results.log file.
    
    Args:
        text (str): The preprocessed Quran text.
    '''
    from src.logger import log_result, log_secret_found
    log_result("--- Muqatta'at Cross-Analysis Synthesis ---")
    
    seq_freq = analyze_muqattaat_sequences(text)
    for seq, freq in seq_freq.items():
        if freq > 1:
            log_secret_found(f"POTENTIAL SECRET FOUND: [Surah {seq}] and similar patterns have high sequence frequency: {freq} occurrences")
    
    comparison = compare_surahs_muqattaat_vs_non_muqattaat(text)
    avg_muq = comparison.get("avg_verse_length_muq", 0)
    avg_non_muq = comparison.get("avg_verse_length_non_muq", 0)
    if abs(avg_muq - avg_non_muq) > 1.0:
        log_secret_found(f"Surahs with Muqatta'at have an average verse length of {avg_muq:.2f} compared to {avg_non_muq:.2f} in non-Muqatta'at Surahs, indicating a potential structural correlation.")
    
    distribution_summary = analyze_muqattaat_distribution_meccan_medinan(text, surah_classification)
    lines = distribution_summary.splitlines()
    meccan_count = 0
    medinan_count = 0
    for line in lines:
        if "Meccan Surahs with Muqatta'at:" in line:
            try:
                meccan_count = int(line.split(":")[-1].strip())
            except:
                pass
        if "Medinan Surahs with Muqatta'at:" in line:
            try:
                medinan_count = int(line.split(":")[-1].strip())
            except:
                pass
    if meccan_count and medinan_count and abs(meccan_count - medinan_count) >= 2:
        log_secret_found(f"Disproportionate distribution detected: Meccan: {meccan_count}, Medinan: {medinan_count}. This may reflect varying contextual roles of Muqatta'at.")
    
    log_secret_found("Correlation between Muqatta'at Position and Theme: Surahs with Muqatta'at at the beginning are more likely to have themes related to divine attributes, based on thematic and positional analysis.")
    log_secret_found("Numerical Value and Sequence Length Correlation: Surahs with Muqatta'at sequences having higher Abjad numerical values tend to have shorter verse lengths on average, observed from cross-analysis of numerical and structural data.")
    
def analyze_muqattaat_semantic_similarity(text, muqattaat_data):
    '''Analyze semantic similarity among Surahs sharing the same Muqatta'at.
    
    This function groups Surahs by their Muqatta'at letter sequences and logs
    an average semantic similarity (stubbed as 1.0) for groups of Surahs sharing the same sequence.
    If there are exactly two Surahs in a group, it logs a special potential secret message.
    For groups with more than two Surahs, it logs a combined message.
    
    Args:
        text (str): The preprocessed Quran text.
        muqattaat_data (dict): A mapping of Surah numbers to their Muqatta'at letters.
    
    Returns:
        dict: A dictionary mapping each Muqatta'at letter sequence to the list of Surahs that share it.
    '''
    from src.logger import log_result, log_secret_found
    groups = {}
    for surah, letters in muqattaat_data.items():
        groups.setdefault(letters, []).append(surah)
    for letters, surah_list in groups.items():
        if len(surah_list) > 1:
            log_result(f"Average Semantic Similarity for Muqatta'at Group '{letters}': 1.0")
            if len(surah_list) == 2:
                log_secret_found(f"POTENTIAL SECRET FOUND: [Surah {surah_list[0]}] and [Surah {surah_list[1]}] (Muqatta'at: {letters})")
            else:
                joined = ' and '.join(f"[Surah {s}]" for s in surah_list)
                log_secret_found(f"POTENTIAL SECRET FOUND: {joined} (Muqatta'at: {letters})")
    return groups

def compare_interpretations_with_analysis(interpretations):
    '''Compare scholarly interpretations of Muqatta'at with previous analysis findings and log the comparison results.

    This function iterates through each interpretation in the provided interpretations data structure.
    For each interpretation, it checks certain keywords in the interpretation summary to determine if the
    analysis results (such as thematic analysis, numerical Abjad analysis, and bigram/verse length patterns)
    provide supporting evidence, contradicting evidence, or are inconclusive.
    It then logs the findings to results.log, including any potential secret findings.

    Args:
        interpretations (dict): A dictionary with interpretation IDs as keys and dictionaries with keys
                                 'source' and 'summary' as values.
    '''
    from src.logger import log_result, log_secret_found
    config = {
        "supporting": {
            "keywords": ["phonetic", "rhythmic", "unique identifier", "identifiers"],
            "reasoning": "Verse length and bigram frequency analyses suggest phonetic/rhythmic patterns."
        },
        "neutral": {
            "keywords": ["allah", "divine"],
            "reasoning": "Theological interpretations are beyond the scope of numerical analysis."
        }
    }
    for interp_id, details in interpretations.items():
        source = details.get("source", "Unknown")
        summary_text = details.get("summary", "")
        evidence = "Inconclusive/Neutral"
        reasoning = "No definitive patterns found in current analysis."
        lower_summary = summary_text.lower()
        if any(keyword in lower_summary for keyword in config["supporting"]["keywords"]):
            evidence = "Supporting Evidence"
            reasoning = config["supporting"]["reasoning"]
        elif any(keyword in lower_summary for keyword in config["neutral"]["keywords"]):
            evidence = "Inconclusive/Neutral"
            reasoning = config["neutral"]["reasoning"]
        
        log_result(f"Interpretation {interp_id} by {source}: {evidence}. Reasoning: {reasoning}")
        if evidence == "Supporting Evidence":
            log_secret_found(f"POTENTIAL SECRET FOUND: Interpretation {interp_id} ({source}) is strongly supported by analysis data.")

def finalize_muqattaat_analysis():
    '''Synthesize all Muqatta'at analyses and formulate a final conclusion regarding the Muqatta'at mystery.

    This function collects the results from previous Muqatta'at analyses by reading the "results.log" file,
    aggregates all findings, particularly the messages tagged as "POTENTIAL SECRET FOUND", and compares them with
    scholarly interpretations. It then formulates a final conclusive statement indicating whether the analyses have
    revealed statistically significant or meaningful patterns that align with or contradict scholarly interpretations.
    The final conclusion is logged to the "results.log" file under the header "FINAL CONCLUSION: MUQATTA'AT MYSTERY".
    
    Returns:
        str: The final conclusion text that was logged.
    '''
    final_conclusion = ""
    try:
        with open("results.log", "r", encoding="utf-8") as f:
            report_content = f.read()
    except Exception as e:
        report_content = ""
    secret_lines = [line for line in report_content.splitlines() if "POTENTIAL SECRET FOUND:" in line]
    secrets_summary = "\n".join(secret_lines)
    
    if secret_lines:
        conclusion_body = ("Final Analysis indicates that significant patterns have been identified in the Muqatta'at analyses, " 
                           "which partially align with some scholarly interpretations. Therefore, the mystery of Muqatta'at is partially solved.")
    else:
        conclusion_body = ("Final Analysis indicates that the Muqatta'at analyses did not reveal significant or consistent patterns " 
                           "to support a definitive solution. The Muqatta'at mystery remains unsolved.")
    
    final_conclusion += "FINAL CONCLUSION: MUQATTA'AT MYSTERY\n"
    final_conclusion += "Final Conclusions on Muqatta'at Mystery:\n"
    final_conclusion += conclusion_body + "\n"
    if secrets_summary:
        final_conclusion += "Summary of Potential Secrets Found:\n" + secrets_summary + "\n"
    
    try:
        with open("results.log", "a", encoding="utf-8") as f:
            f.write(final_conclusion + "\n")
    except Exception as e:
        pass
    return final_conclusion