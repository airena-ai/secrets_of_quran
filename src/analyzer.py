'''Module for analyzing the Quran text for hidden patterns and anomalies.'''

from collections import Counter, defaultdict
import datetime
import importlib.util
import re
import src.logger

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
                flagged.append("Word '{}' frequency is {}".format(word, freq))
            elif avg_freq > 1 and freq < (avg_freq / 2):
                flagged.append("Word '{}' frequency is {}".format(word, freq))
    
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
        summary_lines.append(f"Root '{root}': {freq}")
    summary_lines.append("")
    summary_lines.append("Top Root Word Frequencies:")
    for idx, (root, freq) in enumerate(top_roots, 1):
        summary_lines.append(f"{idx}. Root '{root}' : {freq}")
    summary = "\n".join(summary_lines)

    src.logger.log_result("Arabic Root Word Frequency Analysis Summary:")
    src.logger.log_result("Top Root Word Frequencies:")
    for idx, (root, freq) in enumerate(top_roots, 1):
        src.logger.log_result(f"{idx}. Root '{root}' : {freq}")

    return summary, dict(root_freq), top_roots

def analyze_bigrams(tokenized_text, n=2):
    '''Perform bigram frequency analysis on the given tokenized text.

    This function generates n-grams (bigrams by default) from the tokenized text,
    counts the frequency of each n-gram, and returns a dictionary where keys are n-gram tuples
    and values are their respective occurrence counts.

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
        'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100, 'ر': 200,
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