import logging
import statistics
from collections import Counter, defaultdict

def count_word_frequencies(tokenized_text):
    '''
    Count the frequency of each word in the tokenized text.
    
    :param tokenized_text: List of lists, where each inner list contains words from a verse.
    :return: Dictionary mapping words to their frequency count.
    '''
    freq = {}
    for tokens in tokenized_text:
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
    return freq

def analyze_word_length_distribution(tokenized_text):
    '''
    Analyze the distribution of word lengths in the tokenized text.
    
    Logs:
    - Total words analyzed.
    - Average word length.
    - Most frequent word length(s).
    
    :param tokenized_text: List of lists containing tokenized words.
    :return: Dictionary mapping word lengths to their frequency.
    '''
    logger = logging.getLogger("quran_analysis")
    total_words = sum(len(tokens) for tokens in tokenized_text)
    lengths = []
    for tokens in tokenized_text:
        lengths.extend(len(token) for token in tokens)
    avg_length = statistics.mean(lengths) if lengths else 0
    length_freq = {}
    for l in lengths:
        length_freq[l] = length_freq.get(l, 0) + 1
    most_frequent = [length for length, count in sorted(length_freq.items(), key=lambda x: x[1], reverse=True)]
    logger.info("Word Length Distribution Analysis:")
    logger.info("Total words analyzed: %d", total_words)
    logger.info("Average word length: %.2f", avg_length)
    logger.info("Most frequent word length(s): %s", most_frequent)
    return length_freq

def analyze_surah_word_frequency(data):
    '''
    Analyze word frequencies at the Surah level.
    
    For each Surah, logs the top 10 most frequent words in the format:
    "Surah-level Frequency Analysis - [Surah Name] Top 10 Words: [(word, count), ...]"
    
    :param data: List of dictionaries containing Quran data.
    :return: Dictionary mapping Surah names to their word frequency Counter.
    '''
    logger = logging.getLogger("quran_analysis")
    surah_freqs = defaultdict(Counter)
    for item in data:
        surah = item.get("surah", "Unknown")
        text = item.get("processed_text") or item.get("verse_text", "")
        tokens = text.split() if text else []
        surah_freqs[surah].update(tokens)
    for surah, counter in surah_freqs.items():
        top_10 = counter.most_common(10)
        logger.info("Surah-level Frequency Analysis - Surah %s Top 10 Words: %s", surah, top_10)
    return surah_freqs

def analyze_ayah_word_frequency(data):
    '''
    Analyze word frequencies at the Ayah level.
    
    For each Ayah, logs the top 5 most frequent words in the format:
    "Ayah-level Frequency Analysis - [Surah Name], Ayah [Ayah Number] Top 5 Words: [(word, count), ...]"
    
    :param data: List of dictionaries containing Quran data.
    :return: Dictionary mapping (Surah Name, Ayah) to their word frequency Counter.
    '''
    logger = logging.getLogger("quran_analysis")
    ayah_freqs = defaultdict(Counter)
    for item in data:
        surah = item.get("surah", "Unknown")
        ayah = item.get("ayah", "Unknown")
        text = item.get("processed_text") or item.get("verse_text", "")
        tokens = text.split() if text else []
        key = (surah, ayah)
        ayah_freqs[key].update(tokens)
    for (surah, ayah) in ayah_freqs:
        top_5 = ayah_freqs[(surah, ayah)].most_common(5)
        logger.info("Ayah-level Frequency Analysis - Surah %s, Ayah %s Top 5 Words: %s", surah, ayah, top_5)
    return ayah_freqs

def analyze_root_word_frequency(data):
    '''
    Analyze the frequency of root words across the Quran data.
    
    Logs:
    - A header indicating the start of root word frequency analysis.
    - Total unique root words found.
    - The top 1000 most frequent root words.
    
    :param data: List of dictionaries containing Quran data with 'roots' key.
    :return: Counter object mapping root words to their frequency count.
    '''
    logger = logging.getLogger("quran_analysis")
    root_counts = Counter()
    for item in data:
        roots = item.get("roots", [])
        root_counts.update(roots)
    logger.info("Starting root word frequency analysis.")
    logger.info("Total unique root words found: %d", len(root_counts))
    top_1000 = root_counts.most_common(1000)
    logger.info("Top 1000 most frequent root words: %s", top_1000)
    return root_counts

def analyze_lemma_word_frequency(data):
    '''
    Analyze the frequency of lemma words across the Quran data.
    
    Logs:
    - A header indicating the start of lemma word frequency analysis.
    - Total unique lemma words found.
    - The top 1000 most frequent lemma words.
    
    :param data: List of dictionaries containing Quran data with 'lemmas' key.
    :return: Counter object mapping lemma words to their frequency count.
    '''
    logger = logging.getLogger("quran_analysis")
    lemma_counts = Counter()
    for item in data:
        lemmas = item.get("lemmas", [])
        lemma_counts.update(lemmas)
    logger.info("Starting lemma word frequency analysis.")
    logger.info("Total unique lemma words found: %d", len(lemma_counts))
    top_1000 = lemma_counts.most_common(1000)
    logger.info("Top 1000 most frequent lemma words: %s", top_1000)
    return lemma_counts

def analyze_surah_root_word_frequency(data):
    '''
    Analyze the frequency of root words at the Surah level.
    
    For each Surah in the Quran data:
    - Preprocess each verse's original text using TextPreprocessor.preprocess_text to extract root words.
    - Count the frequency of each root word using collections.Counter.
    - Log the top 10 most frequent root words and the total unique root words count.
    
    :param data: List of dictionaries containing Quran data.
    :return: Dictionary mapping Surah identifiers to a Counter of root word frequencies.
    '''
    import logging
    from collections import Counter, defaultdict
    from src.text_preprocessor import TextPreprocessor
    logger = logging.getLogger("quran_analysis")
    surah_root_freq = defaultdict(Counter)
    processor = TextPreprocessor()
    for item in data:
        surah = item.get("surah", "Unknown")
        original_text = item.get("verse_text", "")
        if not original_text:
            continue
        processed_text = processor.preprocess_text(original_text)
        tokens = processed_text.split()
        surah_root_freq[surah].update(tokens)
    for surah, counter in surah_root_freq.items():
        top_10 = counter.most_common(10)
        unique_count = len(counter)
        logger.info("Surah-level Root Word Frequency Analysis - Surah %s Top 10 Root Words: %s, Unique Root Words Count: %d", surah, top_10, unique_count)
    return surah_root_freq

def analyze_ayah_root_word_frequency(data):
    '''
    Analyze the frequency of root words at the Ayah level.
    
    For each Ayah:
      - Tokenize the ayah text using the existing tokenization logic.
      - For each token, extract the root word using the existing root word extraction logic.
      - Count the frequency of each root word within that ayah.
      - Log the results in a structured format including:
          Ayah identifier (Surah|Ayah), top 5 most frequent root words, and total unique root word count.
    
    :param data: List of dictionaries containing Quran data.
    :return: Dictionary mapping ayah identifier (Surah|Ayah) to a dictionary of root word frequencies.
    '''
    import logging
    from collections import Counter
    from src.tokenizer import tokenize_text
    from src.root_extractor import extract_root
    logger = logging.getLogger("quran_analysis")
    ayah_root_freqs = {}
    for item in data:
        surah = item.get("surah", "Unknown")
        ayah = item.get("ayah", "Unknown")
        ayah_id = f"{surah}|{ayah}"
        text = item.get("processed_text") or item.get("verse_text", "")
        if not text:
            continue
        tokens = tokenize_text(text)
        roots = [extract_root(token) for token in tokens]
        counter = Counter(roots)
        ayah_root_freqs[ayah_id] = dict(counter)
        top_5 = counter.most_common(5)
        logger.info("Ayah Root Word Frequency Analysis - Ayah: %s", ayah_id)
        logger.info("Top 5 Root Words: %s", dict(top_5))
        logger.info("Total Unique Root Words: %d", len(counter))
    return ayah_root_freqs

def analyze_character_frequency(tokenized_text):
    '''
    Analyze the frequency of each character in the preprocessed Quran text.
    
    This function iterates over each ayah and each word, counting the occurrences 
    of each character. It then sorts the characters by frequency in descending order 
    and logs the top 20 most frequent characters along with the total count of unique 
    characters.
    
    :param tokenized_text: List of ayahs, where each ayah is a list of words.
    :return: Dictionary mapping each character to its frequency count.
    '''
    logger = logging.getLogger("quran_analysis")
    char_freq = {}
    logger.info("Starting Character Frequency Analysis...")
    for ayah in tokenized_text:
        for word in ayah:
            for char in word:
                char_freq[char] = char_freq.get(char, 0) + 1
    sorted_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)
    logger.info("Top 20 most frequent characters:")
    for char, count in sorted_chars[:20]:
        logger.info("Character: %s, Count: %d", char, count)
    logger.info("Total unique characters: %d", len(char_freq))
    logger.info("Finished Character Frequency Analysis.")
    return char_freq