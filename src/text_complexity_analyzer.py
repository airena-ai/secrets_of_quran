import logging
from src.logger_config import configure_logger

def analyze_text_complexity(text):
    '''
    Analyze text complexity metrics for a preprocessed Arabic text.
    
    This function tokenizes the input text into words, calculates the average word length
    (total number of characters in words divided by the number of words), and computes the
    average sentence length (total words divided by the number of sentences, where each sentence
    is assumed to be separated by a newline character). The calculated metrics are logged and
    returned as a dictionary.
    
    :param text: Preprocessed Arabic text as a string.
    :return: Dictionary with keys "average_word_length" and "average_sentence_length".
    '''
    if not text:
        return {"average_word_length": 0, "average_sentence_length": 0}
    
    words = text.split()
    total_words = len(words)
    avg_word_length = (sum(len(word) for word in words) / total_words) if total_words > 0 else 0
    
    if "\n" in text:
        sentences = [line.strip() for line in text.splitlines() if line.strip()]
        num_sentences = len(sentences) if sentences else 1
        avg_sentence_length = total_words / num_sentences
    else:
        avg_sentence_length = total_words  # if no newline, consider entire text as one sentence
    
    logger = logging.getLogger("quran_analysis")
    logger.info("Text Complexity Analysis: Average Word Length = %.2f, Average Sentence Length = %.2f", 
                avg_word_length, avg_sentence_length)
    return {"average_word_length": avg_word_length, "average_sentence_length": avg_sentence_length}

def calculate_flesch_reading_ease(text):
    '''
    Calculate the Flesch Reading Ease score for the given preprocessed text.
    
    This function uses the formula:
      206.835 - 1.015*(total words/total sentences) - 84.6*(total syllables/total words)
    
    Syllables are approximated as the count of vowels in each word. Vowels considered include both
    English vowels (a, e, i, o, u) and Arabic vowels ('ا', 'و', 'ي').
    
    :param text: Preprocessed text as a string.
    :return: Flesch Reading Ease score as a float.
    '''
    vowels = set("aeiouAEIOUاوي")
    words = text.split()
    sentences = [s for s in text.splitlines() if s.strip()]
    if not sentences:
        sentences = [text]
    total_words = len(words)
    if total_words == 0:
        return 0.0
    total_sentences = len(sentences)
    total_syllables = 0
    for word in words:
        syllable_count = sum(1 for c in word if c in vowels)
        total_syllables += syllable_count
    avg_words_per_sentence = total_words / total_sentences if total_sentences > 0 else total_words
    avg_syllables_per_word = total_syllables / total_words
    score = 206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word
    return score

def calculate_flesch_kincaid_grade_level(text):
    '''
    Calculate the Flesch-Kincaid Grade Level for the given preprocessed text.
    
    This function uses the formula:
      0.39*(total words/total sentences) + 11.8*(total syllables/total words) - 14.59
    
    Syllables are approximated as the count of vowels in each word. Vowels considered include both
    English vowels (a, e, i, o, u) and Arabic vowels ('ا', 'و', 'ي').
    
    :param text: Preprocessed text as a string.
    :return: Flesch-Kincaid Grade Level score as a float.
    '''
    vowels = set("aeiouAEIOUاوي")
    words = text.split()
    sentences = [s for s in text.splitlines() if s.strip()]
    if not sentences:
        sentences = [text]
    total_words = len(words)
    if total_words == 0:
        return 0.0
    total_sentences = len(sentences)
    total_syllables = sum(sum(1 for c in word if c in vowels) for word in words)
    avg_words_per_sentence = total_words / total_sentences if total_sentences > 0 else total_words
    avg_syllables_per_word = total_syllables / total_words
    grade = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 14.59
    return grade

def analyze_quran_flesch_reading_ease():
    '''
    Analyze and log the Flesch Reading Ease score for the entire Quran.
    
    Loads the Quran data, concatenates the preprocessed text from all verses,
    computes the Flesch Reading Ease score, logs the result, and returns the score.
    
    :return: Flesch Reading Ease score for the entire Quran as a float.
    '''
    import os
    from src.data_loader import QuranDataLoader
    from src.text_preprocessor import TextPreprocessor
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    all_text = "\n".join(processor.preprocess_text(item.get("verse_text", "")) for item in data)
    score = calculate_flesch_reading_ease(all_text)
    logger.info("Quran Flesch Reading Ease Score: %.2f", score)
    return score

def analyze_quran_flesch_kincaid_grade_level():
    '''
    Analyze and log the Flesch-Kincaid Grade Level for the entire Quran.
    
    Loads the Quran data, concatenates the preprocessed text from all verses,
    computes the Flesch-Kincaid Grade Level, logs the result, and returns the grade level.
    
    :return: Flesch-Kincaid Grade Level for the entire Quran as a float.
    '''
    import os
    from src.data_loader import QuranDataLoader
    from src.text_preprocessor import TextPreprocessor
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    all_text = "\n".join(processor.preprocess_text(item.get("verse_text", "")) for item in data)
    grade = calculate_flesch_kincaid_grade_level(all_text)
    logger.info("Quran Flesch-Kincaid Grade Level: %.2f", grade)
    return grade

def analyze_surah_flesch_reading_ease():
    '''
    Analyze and log the Flesch Reading Ease score for each Surah.
    
    Groups the Quran data by Surah, concatenates the preprocessed text for each Surah,
    computes the Flesch Reading Ease score, logs the result for each Surah, and returns a dictionary
    mapping each Surah to its score.
    
    :return: Dictionary mapping Surah identifiers to Flesch Reading Ease scores.
    '''
    import os
    from src.data_loader import QuranDataLoader
    from src.text_preprocessor import TextPreprocessor
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    surah_scores = {}
    surah_groups = {}
    for item in data:
        surah = str(item.get("surah", "Unknown"))
        text = processor.preprocess_text(item.get("verse_text", ""))
        surah_groups.setdefault(surah, []).append(text)
    for surah, texts in surah_groups.items():
        full_text = "\n".join(texts)
        score = calculate_flesch_reading_ease(full_text)
        logger.info("Surah %s Flesch Reading Ease Score: %.2f", surah, score)
        surah_scores[surah] = score
    return surah_scores

def analyze_surah_flesch_kincaid_grade_level():
    '''
    Analyze and log the Flesch-Kincaid Grade Level for each Surah.
    
    Groups the Quran data by Surah, concatenates the preprocessed text for each Surah,
    computes the Flesch-Kincaid Grade Level, logs the result for each Surah, and returns a dictionary
    mapping each Surah to its grade level.
    
    :return: Dictionary mapping Surah identifiers to Flesch-Kincaid Grade Level scores.
    '''
    import os
    from src.data_loader import QuranDataLoader
    from src.text_preprocessor import TextPreprocessor
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    surah_grades = {}
    surah_groups = {}
    for item in data:
        surah = str(item.get("surah", "Unknown"))
        text = processor.preprocess_text(item.get("verse_text", ""))
        surah_groups.setdefault(surah, []).append(text)
    for surah, texts in surah_groups.items():
        full_text = "\n".join(texts)
        grade = calculate_flesch_kincaid_grade_level(full_text)
        logger.info("Surah %s Flesch-Kincaid Grade Level: %.2f", surah, grade)
        surah_grades[surah] = grade
    return surah_grades

def analyze_ayah_flesch_reading_ease():
    '''
    Analyze and log the Flesch Reading Ease score for each Ayah.
    
    Processes each Ayah individually, computes the Flesch Reading Ease score,
    logs the result with its Surah and Ayah identifiers, and returns a dictionary
    mapping each Ayah (formatted as "surah|ayah") to its score.
    
    :return: Dictionary mapping Ayah identifiers to Flesch Reading Ease scores.
    '''
    import os
    from src.data_loader import QuranDataLoader
    from src.text_preprocessor import TextPreprocessor
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    ayah_scores = {}
    for item in data:
        surah = str(item.get("surah", "Unknown"))
        ayah = str(item.get("ayah", "Unknown"))
        text = processor.preprocess_text(item.get("verse_text", ""))
        score = calculate_flesch_reading_ease(text)
        logger.info("Surah %s, Ayah %s Flesch Reading Ease Score: %.2f", surah, ayah, score)
        ayah_scores[f"{surah}|{ayah}"] = score
    return ayah_scores

def analyze_ayah_flesch_kincaid_grade_level():
    '''
    Analyze and log the Flesch-Kincaid Grade Level for each Ayah.
    
    Processes each Ayah individually, computes the Flesch-Kincaid Grade Level,
    logs the result with its Surah and Ayah identifiers, and returns a dictionary
    mapping each Ayah (formatted as "surah|ayah") to its grade level.
    
    :return: Dictionary mapping Ayah identifiers to Flesch-Kincaid Grade Level scores.
    '''
    import os
    from src.data_loader import QuranDataLoader
    from src.text_preprocessor import TextPreprocessor
    logger = logging.getLogger("quran_analysis")
    file_path = os.getenv("DATA_FILE")
    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    processor = TextPreprocessor()
    ayah_grades = {}
    for item in data:
        surah = str(item.get("surah", "Unknown"))
        ayah = str(item.get("ayah", "Unknown"))
        text = processor.preprocess_text(item.get("verse_text", ""))
        grade = calculate_flesch_kincaid_grade_level(text)
        logger.info("Surah %s, Ayah %s Flesch-Kincaid Grade Level: %.2f", surah, ayah, grade)
        ayah_grades[f"{surah}|{ayah}"] = grade
    return ayah_grades