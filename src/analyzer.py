'''Module for analyzing the Quran text for hidden patterns and anomalies.'''

from collections import Counter, defaultdict
import datetime
import importlib.util
import re
import math
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

def analyze_muqattaat(text):
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
        text (str): The preprocessed Quran text.

    Returns:
        tuple: A tuple containing:
            - A dictionary mapping Surah numbers to their extracted Muqatta'at letters.
            - A Counter object representing the frequency of each Muqatta'at letter.
    '''
    import re
    from collections import Counter
    import src.logger as logger

    predefined_surahs = {"2", "3", "7", "10", "11", "12", "13", "14", "15",
                           "19", "20", "26", "27", "28", "29", "30", "31", "32", "36",
                           "38", "40", "41", "42", "43", "44", "45", "46", "50", "68"}
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
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            verse_text = m.group(3).strip()
            if surah in predefined_surahs and surah not in muqattaat_results:
                # Remove Basmalah if present
                basmalah_pattern = re.compile(r'^بِسمِ\s+اللَّهِ\s+الرَّحمٰنِ\s+الرَّحيمِ\s*', re.UNICODE)
                verse_text_cleaned = basmalah_pattern.sub('', verse_text).strip()

                # Match Muqattaʿat letters now that Basmalah is gone
                m_letters = re.match(r'^([\u0621-\u064A]+)', verse_text_cleaned)
                if m_letters:
                    muqattaat_results[surah] = m_letters.group(1)
    
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

def analyze_muqattaat_positions(text):
    '''Analyze the positional distribution of Muqatta'at within Surahs.

    This function processes the preprocessed Quran text (with each line representing a verse in the format "Surah|Ayah|Verse")
    to identify the occurrence positions of Muqatta'at within each Surah (only for predefined Surahs).
    It determines in which category (Beginning, Middle, End, or Throughout) the Muqatta'at appear,
    based on the index of the verses in the Surah where they are found. The results,
    including a summary count for each category, are logged to results.log.

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        str: A summary report of the Muqatta'at positional analysis.
    '''
    import re
    from math import ceil, floor
    summary_lines = []
    # Group verses by Surah
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    surahs = {}
    default_surah = "1"
    default_ayah = 1
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah_no = m.group(1)
            verse_text = m.group(3).strip()
        else:
            surah_no = default_surah
            verse_text = line.strip()
            default_ayah += 1
        if surah_no not in surahs:
            surahs[surah_no] = []
        surahs[surah_no].append(verse_text)
    # Predefined Surahs that may contain Muqatta'at based on established logic
    predefined_surahs = {"2", "3", "7", "10", "11", "12", "13", "14", "15", "16",
                           "19", "20", "26", "27", "28", "29", "30", "31", "32", "36",
                           "38", "40", "41", "42", "43", "44", "45", "46", "50", "68"}
    position_results = {}
    for surah_no, verses in surahs.items():
        if surah_no not in predefined_surahs:
            continue
        verse_indices = []
        letters_list = []
        for idx, verse in enumerate(verses, start=1):
            m_letters = re.match(r'^([\u0621-\u064A]+)', verse)
            if m_letters:
                verse_indices.append(idx)
                letters_list.append(m_letters.group(1))
        if not verse_indices:
            continue
        total_verses = len(verses)
        begin_threshold = ceil(0.2 * total_verses)
        end_start = total_verses - floor(0.2 * total_verses) + 1
        categories = set()
        for index in verse_indices:
            if index <= begin_threshold:
                categories.add("Beginning")
            elif index >= end_start:
                categories.add("End")
            else:
                categories.add("Middle")
        if len(categories) > 1:
            position_category = "Throughout"
        else:
            position_category = list(categories)[0]
        representative_letters = letters_list[0] if letters_list else ""
        position_results[surah_no] = {
            "letters": representative_letters,
            "indices": verse_indices,
            "category": position_category
        }
    import src.logger as logger
    logger.log_result("MUQATTA'AT POSITION ANALYSIS:")
    logger.log_result("---------------------------")
    summary_lines.append("MUQATTA'AT POSITION ANALYSIS:")
    summary_lines.append("---------------------------")
    for surah_no in sorted(position_results.keys(), key=lambda x: int(x)):
        res = position_results[surah_no]
        line = "Surah {} - Muqatta'at: {} - Position: {}".format(surah_no, res["letters"], res["category"])
        logger.log_result(line)
        summary_lines.append(line)
    summary_counts = {"Beginning": 0, "Middle": 0, "End": 0, "Throughout": 0}
    for res in position_results.values():
        summary_counts[res["category"]] += 1
    logger.log_result("")
    summary_lines.append("")
    logger.log_result("Summary of Muqatta'at Positions:")
    summary_lines.append("Summary of Muqatta'at Positions:")
    logger.log_result("Beginning: {} Surahs".format(summary_counts["Beginning"]))
    summary_lines.append("Beginning: {} Surahs".format(summary_counts["Beginning"]))
    logger.log_result("Middle: {} Surahs".format(summary_counts["Middle"]))
    summary_lines.append("Middle: {} Surahs".format(summary_counts["Middle"]))
    logger.log_result("End: {} Surahs".format(summary_counts["End"]))
    summary_lines.append("End: {} Surahs".format(summary_counts["End"]))
    logger.log_result("Throughout: {} Surahs".format(summary_counts["Throughout"]))
    summary_lines.append("Throughout: {} Surahs".format(summary_counts["Throughout"]))
    return "\n".join(summary_lines)

def analyze_muqattaat_sequences(text):
    '''Analyze Muqatta'at sequences in the Quran text.

    This function identifies Surahs recognized to contain Muqatta'at by checking if the Surah number is in a predefined list.
    For each such Surah, it extracts the sequence of Muqatta'at letters from the beginning of the first verse.
    It then counts the frequency of each unique sequence across all Surahs and returns the result.

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        dict: A dictionary mapping each unique Muqatta'at sequence (str) to its frequency (int).
    '''
    import re
    from collections import Counter
    predefined_surahs = {"2", "3", "7", "10", "11", "12", "13", "14", "15", "16",
                           "19", "20", "26", "27", "28", "29", "30", "31", "32", "36",
                           "38", "40", "41", "42", "43", "44", "45", "46", "50", "68"}
    sequence_by_surah = {}
    pattern = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pattern.match(line)
        if m:
            surah = m.group(1)
            verse_text = m.group(3).strip()
            if surah in predefined_surahs and surah not in sequence_by_surah:
                m_seq = re.match(r'^([\u0621-\u064A]+)', verse_text)
                if m_seq:
                    sequence_by_surah[surah] = m_seq.group(1)
    freq_counter = Counter(sequence_by_surah.values())
    return dict(freq_counter)

def analyze_muqattaat_numerical_values(text):
    '''Perform numerical analysis of Muqatta'at using Abjad values.

    This function identifies Surahs with Muqatta'at (extracted from the beginning of the first verse)
    and calculates the numerical sum of the Abjad values for each letter in the Muqatta'at.
    The result is logged in a structured format including:
        - Surah Number
        - Muqatta'at Letters (as a string)
        - Individual Abjad values for each letter
        - Total Abjad Sum

    If the total Abjad sum is a prime number, a multiple of 19, or a multiple of 7, the result is flagged
    as a potential secret.
    
    Args:
        text (str): The preprocessed Quran text.

    Returns:
        str: A summary report of the Muqatta'at numerical analysis.
    '''
    import re
    from src import logger
    summary_lines = []
    # Define Abjad mapping - Comprehensive mapping
    abjad = {
        'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ؤ': 6, 'ز': 7, 'ح': 8, 'ط': 9,
        'ي': 10, 'ى': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100,
        'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
        'ء': 1, 'ئ': 1, 'ة': 5, 'ۀ': 5, 'ی': 10, 'ے': 10, 'ە': 5, 'ھ': 5, 'ہ': 5, 'ۃ': 5,
        'ٱ': 1, 'ٲ': 1, 'ٳ': 1, 'ٴ': 1, 'ٵ': 1, 'ٶ': 6, 'ٷ': 6, 'ں': 50, 'ڻ': 50, 'ټ': 400
    }
    # Predefined Surahs with Muqatta'at - Surah 1 removed
    predefined_surahs = {"2", "3", "7", "10", "11", "12", "13", "14", "15", "16",
                           "19", "20", "26", "27", "28", "29", "30", "31", "32", "36",
                           "38", "40", "41", "42", "43", "44", "45", "46", "50", "68"}
    muqattaat_numerical = {}
    pattern_line = re.compile(r'^\s*(\d+)\s*[|\-]\s*(\d+)\s*[|\-]\s*(.+)$')
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        m = pattern_line.match(line)
        if m:
            surah = m.group(1)
            verse_text = m.group(3).strip()
            if surah not in muqattaat_numerical:
                m_letters = re.match(r'^([\u0621-\u064A]+)', verse_text)
                if m_letters:
                    muqattaat_numerical[surah] = m_letters.group(1)
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0:
                return False
        return True

    logger.log_result("#################### Muqatta'at Numerical Analysis ####################")
    summary_lines.append("#################### Muqatta'at Numerical Analysis ####################")
    for surah, letters in sorted(muqattaat_numerical.items(), key=lambda x: int(x[0])):
        letters_list = list(letters)
        letter_values = {letter: abjad.get(letter, 0) for letter in letters_list}
        total_sum = sum(letter_values.values())
        line1 = f"Surah {surah} - Muqatta'at: {letters}"
        line2 = f"  Letters: {letters_list}"
        line3 = f"  Abjad Values: {letter_values}"
        line4 = f"  Total Abjad Sum: {total_sum}"
        logger.log_result(line1)
        logger.log_result(line2)
        logger.log_result(line3)
        logger.log_result(line4)
        summary_lines.extend([line1, line2, line3, line4])
        if total_sum != 0:
            if total_sum % 19 == 0:
                secret_msg = f"Abjad sum {total_sum} is a multiple of 19"
                logger.log_secret_found(secret_msg)
                summary_lines.append("  SECRET: " + secret_msg)
            elif total_sum % 7 == 0:
                secret_msg = f"Abjad sum {total_sum} is a multiple of 7"
                logger.log_secret_found(secret_msg)
                summary_lines.append("  SECRET: " + secret_msg)
            elif is_prime(total_sum):
                secret_msg = f"Abjad sum {total_sum} is a prime number"
                logger.log_secret_found(secret_msg)
                summary_lines.append("  SECRET: " + secret_msg)
    return "\n".join(summary_lines)

def analyze_muqattaat_themes():
    '''Perform thematic analysis for Surahs with Muqatta'at by associating each Surah with a predefined theme.

    This function iterates over a static dictionary of high-level themes for Surahs known to contain Muqatta'at.
    For each Surah, it retrieves a hardcoded Muqatta'at letter sequence (assumed to be "الم") and logs a message in a
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
    # For this step, hardcode Muqatta'at letters as 'الم' for all specified Surahs
    muqattaat_letters = { key: "الم" for key in surah_themes.keys() }
    for surah, info in surah_themes.items():
         letters = muqattaat_letters.get(surah, "N/A")
         message = "Surah {} ({}) with Muqatta'at '{}': Theme - {}".format(surah, info["name"], letters, info["theme"])
         logger.log_result(message)

def analyze_correlations(text, verse_lengths=None, muqattaat_data=None, word_frequency_result=None, flagged_words=None, verse_repetitions_data=None, enhanced_symmetry_data=None, abjad_anomalies=None, verse_length_diff_threshold=2, semantic_symmetry_diff_threshold=0.1):
    '''Perform correlation analysis across multiple analytical dimensions.
    
    This function integrates the results from various analysis functions including:
    verse length distribution, word frequency, verse repetition, semantic symmetry,
    and Muqatta'at analyses. It attempts to identify significant correlations such as:
    
    - Correlation between Muqatta'at presence/sequences/Abjad values and verse length distributions in Surahs.
    - Correlation between Muqatta'at presence/sequences/Abjad values and semantic symmetry scores of Surahs.
    - Relationship between unusual word frequencies and verse repetition patterns.
    - Association between Abjad numeral anomalies and flagged word frequencies.
    
    The thresholds for determining significance can be configured via parameters.
    
    Args:
        text (str): The preprocessed Quran text.
        verse_lengths (dict, optional): Precomputed verse length analysis.
        muqattaat_data (dict, optional): Precomputed Muqatta'at analysis data.
        word_frequency_result (tuple, optional): Output from word frequency analysis.
        flagged_words (list, optional): List of flagged words from frequency analysis.
        verse_repetitions_data (dict, optional): Precomputed verse repetition analysis.
        enhanced_symmetry_data (dict, optional): Precomputed enhanced semantic symmetry analysis.
        abjad_anomalies (list, optional): Precomputed Abjad numeral anomalies.
        verse_length_diff_threshold (float, optional): Threshold for average verse length difference.
        semantic_symmetry_diff_threshold (float, optional): Threshold for semantic symmetry score difference.
    
    Returns:
        list: A list of strings each representing a potential secret found.
    '''
    secrets = []
    from src.logger import log_secret_found
    if verse_lengths is None:
        verse_lengths = analyze_verse_lengths_distribution(text)
    if muqattaat_data is None:
        muqattaat_data, _ = analyze_muqattaat(text)
    if word_frequency_result is None:
        word_frequency_result = analyze_word_frequency(text)
    if flagged_words is None:
        flagged_words = word_frequency_result[1]
    if verse_repetitions_data is None:
        verse_repetitions_data = analyze_verse_repetitions(text)
    if enhanced_symmetry_data is None:
        enhanced_symmetry_data = analyze_enhanced_semantic_symmetry(text)
    if abjad_anomalies is None:
        abjad_anomalies = analyze_abjad_numerals(text)
    
    # Correlation 1: Muqatta'at vs Verse Length
    muq_surahs = set(muqattaat_data.keys())
    lengths_with_muq = []
    lengths_without_muq = []
    for surah, stats in verse_lengths.items():
        if surah in muq_surahs:
            lengths_with_muq.append(stats.get("average", 0))
        else:
            lengths_without_muq.append(stats.get("average", 0))
    if lengths_with_muq and lengths_without_muq:
        avg_with = sum(lengths_with_muq) / len(lengths_with_muq)
        avg_without = sum(lengths_without_muq) / len(lengths_without_muq)
        diff = avg_with - avg_without
        if abs(diff) >= verse_length_diff_threshold:
            direction = "higher" if diff > 0 else "lower"
            message = ("POTENTIAL SECRET FOUND: Surahs with Muqatta'at have an average verse length of {:.2f} words compared to "
                       "{:.2f} words in Surahs without Muqatta'at (difference: {:.2f}, {} correlation)").format(avg_with, avg_without, abs(diff), direction)
            log_secret_found(message)
            secrets.append(message)
    
    # Correlation 2: Muqatta'at vs Enhanced Semantic Symmetry
    symmetry_with_muq = []
    symmetry_without_muq = []
    for surah, data in enhanced_symmetry_data.items():
        score = data.get("symmetry_score", 0)
        if surah in muq_surahs:
            symmetry_with_muq.append(score)
        else:
            symmetry_without_muq.append(score)
    if symmetry_with_muq and symmetry_without_muq:
        avg_sym_with = sum(symmetry_with_muq) / len(symmetry_with_muq)
        avg_sym_without = sum(symmetry_without_muq) / len(symmetry_without_muq)
        diff_sym = avg_sym_with - avg_sym_without
        if abs(diff_sym) >= semantic_symmetry_diff_threshold:
            direction = "higher" if diff_sym > 0 else "lower"
            message = ("POTENTIAL SECRET FOUND: Surahs with Muqatta'at have a semantic symmetry score of {:.2f} compared to "
                       "{:.2f} in Surahs without (difference: {:.2f}, {} correlation)").format(avg_sym_with, avg_sym_without, abs(diff_sym), direction)
            log_secret_found(message)
            secrets.append(message)
    
    # Correlation 3: Word Frequency Flags vs Verse Repetition
    repetition_count = len(verse_repetitions_data.get("across_quran", []))
    flagged_count = len(flagged_words)
    if flagged_count > 0 and repetition_count > 0:
        ratio = flagged_count / repetition_count
        message = ("POTENTIAL SECRET FOUND: Detected {} flagged word frequency anomalies correlating with {} instances of verse repetitions "
                   "(ratio: {:.2f}) across the Quran. [Note: Further statistical analysis is recommended]").format(flagged_count, repetition_count, ratio)
        log_secret_found(message)
        secrets.append(message)
    
    # Correlation 4: Abjad Anomalies vs Word Frequency Flags
    if len(abjad_anomalies) > 0 and flagged_count > 0:
        ratio_abjad = len(abjad_anomalies) / flagged_count
        message = ("POTENTIAL SECRET FOUND: Detected {} abjad numeral anomalies alongside {} flagged word frequency anomalies "
                   "(ratio: {:.2f}), suggesting a potential interplay between numerical values and word usage.").format(len(abjad_anomalies), flagged_count, ratio_abjad)
        log_secret_found(message)
        secrets.append(message)
    
    return secrets