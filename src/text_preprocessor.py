import unicodedata

class TextPreprocessor:
    '''
    A class for preprocessing text including normalization and tokenization.
    '''
    def preprocess_text(self, text):
        '''
        Preprocess the input text by normalizing, removing diacritical marks,
        and replacing certain letters with their normalized forms.
        
        :param text: The original text string.
        :return: The normalized text string.
        '''
        # Normalize text and remove diacritics
        normalized = unicodedata.normalize('NFKD', text)
        filtered = ''.join([c for c in normalized if not unicodedata.combining(c)])
        # Normalize specific letters: replace 'ى' with 'ي' and 'ة' with 'ه'
        filtered = filtered.replace("ى", "ي").replace("ة", "ه")
        return filtered.lower().strip()
