import re

def normalize_text(text):
    '''
    Normalize the Arabic text by performing comprehensive normalization.
    
    Steps:
    1. Remove invisible Unicode characters (e.g., zero-width spaces).
    2. Remove Arabic diacritics.
    3. Normalize various Arabic letter forms to their standard forms.
       This includes converting forms of Alef and Hamza:
         - 'أ', 'إ', 'آ' are normalized to 'ا'
         - 'ى' is normalized to 'ي'
         - 'ئ' is normalized to 'ي'
         - 'ؤ' is normalized to 'و'
       Additionally, if a taa marbuta appears immediately after a ya (resulting from
       normalization of 'ى'), it is converted to a ha to account for cases like "ىة" -> "يه".
       Otherwise, the taa marbuta remains unchanged.
    
    :param text: The input Arabic text.
    :return: The normalized Arabic text.
    '''
    # Remove invisible Unicode artifacts
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    
    # Remove Arabic diacritics (Tashkeel)
    text = re.sub(r'[ًٌٍَُِّْٰ]', '', text)
    
    # Mapping of various Arabic letters to standard forms (taa marbuta is handled separately)
    mapping = {
        'أ': 'ا',
        'إ': 'ا',
        'آ': 'ا',
        'ى': 'ي',
        'ئ': 'ي',
        'ؤ': 'و',
    }
    for original, replacement in mapping.items():
        text = text.replace(original, replacement)
    
    # Convert taa marbuta to ha only when it follows a ya (to transform tokens like "ىة" -> "يه")
    text = re.sub(r'(?<=ي)ة', 'ه', text)
    return text