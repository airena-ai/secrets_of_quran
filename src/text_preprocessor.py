import logging
from src.arabic_normalization import normalize_text
from src.tokenizer import tokenize_text

class TextPreprocessor:
    """
    A class for preprocessing Arabic text.
    """

    def __init__(self):
        """
        Initialize the TextPreprocessor.
        """
        self.logger = logging.getLogger(__name__)

    def preprocess_text(self, text):
        """
        Preprocess the Arabic text by performing the following steps:

        1. Comprehensive normalization:
           - Removes invisible Unicode artifacts.
           - Removes Arabic diacritics.
           - Normalizes various Arabic letter forms (e.g., 'أ', 'إ', 'آ' to 'ا', 'ة' to 'ه', etc.)
        2. Tokenization:
           - Splits the normalized text into individual tokens based on whitespace and punctuation.
           - Logs the number of tokens generated and a sample of tokens for verification.

        :param text: The input Arabic text.
        :return: A string containing the processed tokens joined by a space.
        """
        normalized_text = normalize_text(text)
        tokens = tokenize_text(normalized_text)
        self.logger.info("Normalization complete. Normalized text: %s", normalized_text)
        self.logger.info("Tokenization complete: %d tokens generated. Sample tokens: %s", len(tokens), tokens[:5])
        return " ".join(tokens)