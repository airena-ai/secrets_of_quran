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