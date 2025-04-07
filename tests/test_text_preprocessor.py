import unittest
from src.text_preprocessor import TextPreprocessor
from src.arabic_normalization import normalize_text
from src.tokenizer import tokenize_text

class TestTextPreprocessor(unittest.TestCase):
    '''
    Unit tests for the TextPreprocessor class and its components.
    '''

    def test_preprocess_text_removes_diacritics_and_normalizes(self):
        self.maxDiff = None
        processor = TextPreprocessor()
        input_text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ ىة"
        # Expected output after removal of diacritics and normalization:
        # 'بِسْمِ' becomes 'بسم', 'اللَّهِ' becomes 'الله', and the final letters are normalized.
        expected_output = "بسم الله الرحمن الرحيم يه"
        output = processor.preprocess_text(input_text)
        self.assertEqual(output, expected_output)

    def test_preprocess_text_no_modification(self):
        self.maxDiff = None
        processor = TextPreprocessor()
        input_text = "الكلم"
        # 'الكلمة' is already normalized and should remain unchanged.
        expected_output = "الكلم"
        output = processor.preprocess_text(input_text)
        self.assertEqual(output, expected_output)

    def test_arabic_normalization_removes_invisible_and_normalizes(self):
        self.maxDiff = None
        # Input with an invisible character and a diacritic on 'أ'
        input_text = "أختِبار\u200c"
        # Expected: 'أ' -> 'ا', diacritic removed, invisible character removed
        expected = "اختبار"
        output = normalize_text(input_text)
        self.assertEqual(output, expected)

    def test_tokenizer_splits_on_punctuation_and_whitespace(self):
        self.maxDiff = None
        input_text = "هذا، نص تجريبي! اختبار."
        expected = ["هذا", "نص", "تجريبي", "اختبار"]
        output = tokenize_text(input_text)
        self.assertEqual(output, expected)

if __name__ == "__main__":
    unittest.main()