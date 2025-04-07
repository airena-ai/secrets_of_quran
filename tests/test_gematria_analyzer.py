import unittest
from collections import Counter
from src.gematria_analyzer import analyze_gematria_cooccurrence_ayah

class TestGematriaCooccurrenceAnalysis(unittest.TestCase):
    '''
    Unit tests for the analyze_gematria_cooccurrence_ayah function.
    '''
    def test_empty_text(self):
        self.maxDiff = None
        data = [{"processed_text": ""}]
        result = analyze_gematria_cooccurrence_ayah(data)
        self.assertEqual(result, Counter())

    def test_single_word(self):
        self.maxDiff = None
        # Single word should yield no pairs.
        data = [{"processed_text": "ا"}]
        result = analyze_gematria_cooccurrence_ayah(data)
        self.assertEqual(result, Counter())

    def test_unique_values(self):
        self.maxDiff = None
        # "ا ب ج" -> Gematria values: 1, 2, 3. Expect pairs: (1,2), (1,3), (2,3) each once.
        data = [{"processed_text": "ا ب ج"}]
        result = analyze_gematria_cooccurrence_ayah(data)
        expected = Counter({(1, 2): 1, (1, 3): 1, (2, 3): 1})
        self.assertEqual(result, expected)

    def test_repeated_values(self):
        self.maxDiff = None
        # "ا ا ب" -> Gematria values: 1, 1, 2. Combinations: (1,1) once and (1,2) twice.
        data = [{"processed_text": "ا ا ب"}]
        result = analyze_gematria_cooccurrence_ayah(data)
        expected = Counter({(1, 1): 1, (1, 2): 2})
        self.assertEqual(result, expected)

    def test_multiple_ayahs(self):
        self.maxDiff = None
        # Two ayahs: first with "ا ب" and second with "ب ج"
        # First yields: (1,2): 1 ; second yields: (2,3): 1
        data = [{"processed_text": "ا ب"}, {"processed_text": "ب ج"}]
        result = analyze_gematria_cooccurrence_ayah(data)
        expected = Counter({(1, 2): 1, (2, 3): 1})
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()