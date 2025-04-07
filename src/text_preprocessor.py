import re
import logging

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
        
        1. Remove Arabic diacritics (Tashkeel): َ ً ُ ٌ ِ ٍ ْ ّ ٰ.
        2. Normalize letters: Replace 'ى' with 'ي' and 'ة' with 'ه'.

        :param text: The input Arabic text.
        :return: The preprocessed Arabic text.
        """
        # Remove Arabic diacritics using regex
        diacritics_pattern = re.compile(r"[ًٌٍَُِّْٰ]")
        processed_text = diacritics_pattern.sub("", text)
        # Normalize letters: replace 'ى' with 'ي' and 'ة' with 'ه'
        processed_text = processed_text.replace("ى", "ي").replace("ة", "ه")
        return processed_text