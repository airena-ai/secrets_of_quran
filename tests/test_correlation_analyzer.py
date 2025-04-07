import unittest
import numpy as np
from src.correlation_analyzer import analyze_sentence_length_gematria_correlation

class TestCorrelationAnalyzer(unittest.TestCase):
    '''
    Unit tests for the Sentence Length vs Gematria Correlation Analysis.
    '''
    def test_analyze_sentence_length_gematria_correlation(self):
        '''
        Test the analyze_sentence_length_gematria_correlation function with sample data.
        '''
        self.maxDiff = None
        sample_data = [
            {"surah": 1, "ayah": 1, "processed_text": "سلام"},
            {"surah": 1, "ayah": 2, "processed_text": "سلام عليكم"},
            {"surah": 1, "ayah": 3, "processed_text": "الله"}
        ]
        # Expected calculations:
        # Ayah 1: "سلام" -> tokens: ["سلام"], gematria = 131, average = 131, sentence length = 1.
        # Ayah 2: "سلام عليكم" -> tokens: ["سلام", "عليكم"], gematria: "سلام"=131, "عليكم"=170, average = (131+170)/2 = 150.5, sentence length = 2.
        # Ayah 3: "الله" -> tokens: ["الله"], gematria = 66, average = 66, sentence length = 1.
        # Group averages:
        # For sentence length 1: (131 + 66)/2 = 98.5 (count = 2)
        # For sentence length 2: 150.5 (count = 1)
        result = analyze_sentence_length_gematria_correlation(sample_data)
        expected_group_averages = {
            1: {"average_gematria": 98.5, "count": 2},
            2: {"average_gematria": 150.5, "count": 1}
        }
        self.assertEqual(result["group_averages"], expected_group_averages)
        # Validate correlation coefficient using numpy's calculation
        raw_lengths = [1, 2, 1]
        raw_avgs = [131, 150.5, 66]
        expected_corr = np.corrcoef(raw_lengths, raw_avgs)[0, 1]
        self.assertAlmostEqual(result["correlation_coefficient"], expected_corr, places=4)

if __name__ == "__main__":
    unittest.main()