import unittest
from src.text_preprocessor import TextPreprocessor

class TestTextPreprocessor(unittest.TestCase):
    """
    Unit tests for the TextPreprocessor class.
    """

    def test_preprocess_text_removes_diacritics_and_normalizes(self):
        self.maxDiff = None
        processor = TextPreprocessor()
        input_text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ ىة"
        # Expected output after removing diacritics and normalizing:
        # 'بِسْمِ' becomes 'بسم', 'اللَّهِ' becomes 'الله', etc.
        expected_output = "بسم الله الرحمن الرحيم يه"
        output = processor.preprocess_text(input_text)
        self.assertEqual(output, expected_output)

    def test_preprocess_text_no_modification(self):
        self.maxDiff = None
        processor = TextPreprocessor()
        input_text = "الكلمة"
        # 'الكلمة' should be normalized to 'الكلمه' (final letter normalization)
        expected_output = "الكلمه"
        output = processor.preprocess_text(input_text)
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()