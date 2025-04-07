import io
import logging
import unittest
from src.gematria_analyzer import get_default_gematria_mapping, analyze_surah_gematria_distribution, analyze_ayah_gematria_distribution, analyze_first_word_gematria_ayah, analyze_last_word_gematria_ayah

class TestGematriaAnalyzer(unittest.TestCase):
    '''
    Unit tests for the Gematria analyzer functions at various levels.
    '''
    def test_analyze_surah_gematria_distribution(self):
        self.maxDiff = None
        # Prepare sample Quran data with surah and processed_text fields
        sample_data = [
            {"surah": "1", "ayah": "1", "processed_text": "اب"},
            {"surah": "1", "ayah": "2", "processed_text": "أب"},
            {"surah": "2", "ayah": "1", "processed_text": "ج"}
        ]
        gematria_mapping = get_default_gematria_mapping()
        # Redirect logging output to capture logs
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger = logging.getLogger("quran_analysis")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        result = analyze_surah_gematria_distribution(sample_data, gematria_mapping)
        logger.removeHandler(handler)
        
        expected = {
            "1": {
                "frequency": {3: 2},
                "summary": {"mean": 3, "median": 3, "mode": 3, "stdev": 0}
            },
            "2": {
                "frequency": {3: 1},
                "summary": {"mean": 3, "median": 3, "mode": 3, "stdev": 0}
            }
        }
        self.assertEqual(result, expected)
        logs = log_stream.getvalue()
        self.assertIn("Surah 1: Gematria Distribution: {3: 2}", logs)
        self.assertIn("Surah 2: Gematria Distribution: {3: 1}", logs)

    def test_analyze_ayah_gematria_distribution(self):
        self.maxDiff = None
        sample_data = [
            {"surah": "1", "ayah": "1", "processed_text": "اب"},
            {"surah": "1", "ayah": "2", "processed_text": "أب"},
            {"surah": "2", "ayah": "1", "processed_text": "ج"}
        ]
        gematria_mapping = get_default_gematria_mapping()
        
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger = logging.getLogger("quran_analysis")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        result = analyze_ayah_gematria_distribution(sample_data, gematria_mapping)
        logger.removeHandler(handler)
        
        expected = {
            "1|1": {
                "frequency": {3: 1},
                "summary": {"mean": 3, "median": 3, "mode": 3, "stdev": 0}
            },
            "1|2": {
                "frequency": {3: 1},
                "summary": {"mean": 3, "median": 3, "mode": 3, "stdev": 0}
            },
            "2|1": {
                "frequency": {3: 1},
                "summary": {"mean": 3, "median": 3, "mode": 3, "stdev": 0}
            }
        }
        self.assertEqual(result, expected)
        logs = log_stream.getvalue()
        self.assertIn("Ayah 1|1: Gematria Distribution: {3: 1}", logs)
        self.assertIn("Ayah 1|2: Gematria Distribution: {3: 1}", logs)
        self.assertIn("Ayah 2|1: Gematria Distribution: {3: 1}", logs)

    def test_analyze_first_word_gematria_ayah(self):
        self.maxDiff = None
        # Sample data for first word analysis
        sample_data = [
            {"surah": "1", "ayah": "1", "processed_text": "اب"},
            {"surah": "1", "ayah": "2", "processed_text": "أب"},
            {"surah": "2", "ayah": "1", "processed_text": "ج د"}
        ]
        gematria_mapping = get_default_gematria_mapping()
        
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger = logging.getLogger("quran_analysis")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        result = analyze_first_word_gematria_ayah(sample_data, gematria_mapping)
        logger.removeHandler(handler)
        
        # "اب" -> 1+2 = 3, "أب" -> 1+2 = 3, "ج" -> 3
        expected = {3: 3}
        self.assertEqual(result, expected)
        logs = log_stream.getvalue()
        self.assertIn("Top 10 most frequent Gematria values for first words:", logs)

    def test_analyze_last_word_gematria_ayah(self):
        self.maxDiff = None
        # Sample data for last word analysis
        sample_data = [
            {"surah": "1", "ayah": "1", "processed_text": "اب كلمة"},
            {"surah": "1", "ayah": "2", "processed_text": "أب كلمة"},
            {"surah": "2", "ayah": "1", "processed_text": "ج كلمة"}
        ]
        gematria_mapping = get_default_gematria_mapping()
        
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger = logging.getLogger("quran_analysis")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        result = analyze_last_word_gematria_ayah(sample_data, gematria_mapping)
        logger.removeHandler(handler)
        
        # "كلمة" -> ك=20, ل=30, م=40, ة=5; total = 95 for each entry.
        expected = {95: 3}
        self.assertEqual(result, expected)
        logs = log_stream.getvalue()
        self.assertIn("Top 10 most frequent Gematria values for last words:", logs)

if __name__ == "__main__":
    unittest.main()