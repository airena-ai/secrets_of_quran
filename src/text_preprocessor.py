import logging
from src.arabic_normalization import normalize_text
from src.tokenizer import tokenize_text
from src.lemmatizer import lemmatize_token
from src.root_extractor import extract_root

class TextPreprocessor:
    '''
    A class for preprocessing Arabic text.
    '''

    def __init__(self):
        '''
        Initialize the TextPreprocessor.
        '''
        self.logger = logging.getLogger(__name__)

    def preprocess_text(self, text):
        '''
        Preprocess the Arabic text by performing the following steps:
        
        1. Comprehensive normalization:
           - Removes invisible Unicode artifacts.
           - Removes Arabic diacritics.
           - Normalizes various Arabic letter forms (e.g., 'أ', 'إ', 'آ' to 'ا', 'ة' to 'ه', etc.)
        2. Tokenization:
           - Splits the normalized text into individual tokens based on whitespace and punctuation.
           - Logs the number of tokens generated and a sample of tokens for verification.
        3. Lemmatization:
           - Applies Arabic lemmatization to each token.
           - Logs the original token, normalized token, and its lemmatized form.
        4. Root Word Extraction:
           - Extracts the root form of each lemmatized token.
           - Logs the original token, normalized token, lemmatized token, and extracted root word.
        
        :param text: The input Arabic text.
        :return: A string containing the processed tokens (root forms) joined by a space.
        '''
        normalized_text = normalize_text(text)
        tokens = tokenize_text(normalized_text)
        self.logger.info("Normalization complete. Normalized text: %s", normalized_text)
        self.logger.info("Tokenization complete: %d tokens generated. Sample tokens: %s", len(tokens), tokens[:5])
        
        # Obtain original tokens from the raw text for logging purposes using robust tokenization.
        original_tokens = tokenize_text(text)
        processed_tokens = []
        for i, token in enumerate(tokens):
            original_token = original_tokens[i] if i < len(original_tokens) else token
            lemma = lemmatize_token(token)
            root = extract_root(lemma)
            self.logger.info("Token processed - Original: %s, Normalized: %s, Lemma: %s, Root: %s", original_token, token, lemma, root)
            processed_tokens.append(root)
        return " ".join(processed_tokens)