'''Unit tests for the text_preprocessor module.'''

import unittest
from src.text_preprocessor import remove_diacritics, normalize_arabic_letters

class TestTextPreprocessor(unittest.TestCase):
    def test_remove_diacritics(self):
        '''Test removal of Arabic diacritics from text.'''
        # Example Arabic text with diacritics: "مُحَمَّدٌ" should become "محمد"
        text_with_diacritics = "مُحَمَّدٌ"
        expected_text = "محمد"
        result = remove_diacritics(text_with_diacritics)
        self.assertEqual(result, expected_text)

    def test_normalize_arabic_letters(self):
        '''Test normalization of specific Arabic letters in text.'''
        # \u0649 (ى) should be replaced with \u064A (ي)
        # \u0629 (ة) should be replaced with \u0647 (ه)
        text_to_normalize = "منى \u0649 مدرسة\u0629"
        expected_text = "منى ي مدرسه"
        result = normalize_arabic_letters(text_to_normalize)
        self.assertEqual(result, expected_text)

if __name__ == '__main__':
    unittest.main()