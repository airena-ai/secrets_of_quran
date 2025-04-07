import io
import logging
import math
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

    def test_calculate_dale_chall_readability_empty(self):
        self.maxDiff = None
        from src.readability_analyzer import calculate_dale_chall_readability
        score = calculate_dale_chall_readability("")
        # With no words, total_words=0 so percentage difficult =0, assume one sentence => score = 3.6365
        self.assertAlmostEqual(score, 3.6365, places=4)

    def test_calculate_dale_chall_readability_non_empty(self):
        self.maxDiff = None
        from src.readability_analyzer import calculate_dale_chall_readability
        # Using a text where both words are common (assuming "على" and "الله" are in COMMON_ARABIC_WORDS)
        score = calculate_dale_chall_readability("على الله")
        # total_words = 2, difficult words = 0, average sentence length = 2
        expected = 3.6365 + 0.0496 * 2  # 3.6365 + 0.0992 = 3.7357 approximately
        self.assertAlmostEqual(score, expected, places=4)

    def test_calculate_smog_index_empty(self):
        self.maxDiff = None
        from src.readability_analyzer import calculate_smog_index
        score = calculate_smog_index("")
        # With no words, polysyllabic count =0, sentence count assumed 1, so score = 1.0430*sqrt(0) + 3.1291 = 3.1291
        self.assertAlmostEqual(score, 3.1291, places=4)

    def test_calculate_smog_index_non_empty(self):
        self.maxDiff = None
        from src.readability_analyzer import calculate_smog_index
        # Testing with text "كلمة طويلة": "كلمة" has 5 letters, "طويلة" has 6 letters -> one polysyllabic word.
        expected = 1.0430 * math.sqrt(1 * (30 / 1)) + 3.1291
        score = calculate_smog_index("كلمة طويلة")
        self.assertAlmostEqual(score, expected, places=4)

    def test_calculate_dale_chall_readability_multiple_sentences(self):
        self.maxDiff = None
        from src.readability_analyzer import calculate_dale_chall_readability
        # Text with two sentences: first with common words, second with difficult words.
        text = "على الله\nكلمة اختبار"
        # Total words = 4, difficult words = 2 (in second sentence), percentage = 50,
        # average sentence length = 4/2 = 2
        # Expected score = 0.1579*50 + 0.0496*2 + 3.6365
        expected = 0.1579 * 50 + 0.0496 * 2 + 3.6365
        score = calculate_dale_chall_readability(text)
        self.assertAlmostEqual(score, expected, places=4)

    def test_calculate_smog_index_multiple_sentences(self):
        self.maxDiff = None
        from src.readability_analyzer import calculate_smog_index
        # Sentence 1: "كلمة طويلة جدا" -> "كلمة" (5 letters, not polysyllabic), "طويلة" (6 letters, polysyllabic), "جدا" (3 letters)
        # Sentence 2: "صغير" (assumed 5 letters, not polysyllabic)
        # Thus, polysyllabic count = 1, sentence count = 2
        # Expected SMOG = 1.0430 * sqrt(1*(30/2)) + 3.1291
        expected = 1.0430 * math.sqrt(30/2) + 3.1291
        text = "كلمة طويلة جدا\nصغير"
        score = calculate_smog_index(text)
        self.assertAlmostEqual(score, expected, places=4)

if __name__ == "__main__":
    unittest.main()