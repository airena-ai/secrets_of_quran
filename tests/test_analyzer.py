'''Unit tests for the analyzer module.'''

import unittest
from unittest.mock import MagicMock
from src.analyzer import analyze_text, analyze_word_frequency, analyze_root_words, analyze_bigrams, analyze_palindromes, analyze_abjad_numerals, analyze_semantic_symmetry, analyze_verse_repetitions
import importlib.util
import src.logger

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_analyze_non_empty(self):
        '''Test that a non-empty text returns a simulated anomaly.'''
        text = "Some sample Quran text"
        anomalies = analyze_text(text)
        self.assertIsInstance(anomalies, list)
        self.assertGreater(len(anomalies), 0)
        self.assertIn("Calculated numerical pattern: 42", anomalies)

    def test_analyze_empty(self):
        '''Test that an empty text returns no anomalies.'''
        text = "   "
        anomalies = analyze_text(text)
        self.assertEqual(anomalies, [])
        
    def test_analyze_word_frequency_summary(self):
        '''Test that the word frequency analysis returns a proper summary and flagged list.'''
        text = "apple apple banana banana banana cherry"
        summary, flagged = analyze_word_frequency(text)
        self.assertIn("Word Frequency Analysis (Top 20):", summary)
        self.assertIn("1.", summary)
        self.assertIsInstance(flagged, list)
        
    def test_analyze_word_frequency_with_flags(self):
        '''Test that the word frequency analysis flags unusual word frequencies.'''
        text = ("wow " * 10) + ("meh " * 2)
        summary, flagged = analyze_word_frequency(text)
        self.assertIn("wow", summary)
        self.assertTrue(any("meh" in flag for flag in flagged))
        for flag in flagged:
            self.assertIn("frequency is", flag)
            
    def test_analyze_root_words_empty(self):
        '''Test Arabic root word analysis on empty text.'''
        from unittest.mock import patch
        with patch('importlib.util.find_spec', return_value=None):
            summary, root_freq, top_roots = analyze_root_words("")
            self.assertIn("Arabic Root Word Frequency Analysis:", summary)
            self.assertEqual(root_freq, {})
            self.assertEqual(top_roots, [])
        
    def test_analyze_root_words_sample(self):
        '''Test Arabic root word analysis on sample text with mocked CAMeL Tools analyzer.'''
        from unittest.mock import patch, MagicMock
        mock_spec = MagicMock()
        mock_analyzer = MagicMock()
        mock_analyzer.analyze.side_effect = lambda token: [{'root': 'كتب'}] if token == "كتاب" else [{'root': 'درس'}] if token == "مدرسة" else [{'root': token}]
        mock_analyzer_class = MagicMock()
        mock_analyzer_class.builtin_analyzer.return_value = mock_analyzer
        with patch('importlib.util.find_spec', return_value=mock_spec), \
             patch.dict('sys.modules', {'camel_tools': MagicMock(), 
                                          'camel_tools.morphology': MagicMock(),
                                          'camel_tools.morphology.analyzer': MagicMock()}), \
             patch('camel_tools.morphology.analyzer.Analyzer', mock_analyzer_class):
            sample_text = "كتاب مدرسة كتاب"
            summary, root_freq, top_roots = analyze_root_words(sample_text)
            self.assertEqual(root_freq.get('كتب'), 2)
            self.assertEqual(root_freq.get('درس'), 1)
            self.assertIn("Root 'كتب': 2", summary)
            self.assertIn("Root 'درس': 1", summary)
            self.assertEqual(top_roots[0], ('كتب', 2))
            
    def test_analyze_bigrams_empty(self):
        '''Test that analyze_bigrams returns an empty dictionary when provided an empty tokenized text or insufficient tokens.'''
        self.assertEqual(analyze_bigrams([]), {})
        self.assertEqual(analyze_bigrams(["word"]), {})
        
    def test_analyze_bigrams_sample(self):
        '''Test analyze_bigrams with a sample tokenized text for correct bigram generation and frequency counting.'''
        tokens = ['a', 'b', 'a', 'b']
        result = analyze_bigrams(tokens)
        expected = {('a', 'b'): 2, ('b', 'a'): 1}
        self.assertEqual(result, expected)

    def test_analyze_palindromes_detects_palindrome(self):
        '''Test that analyze_palindromes detects palindromic words and phrases.'''
        original_log = src.logger.log_secret_found
        captured = []
        src.logger.log_secret_found = lambda msg: captured.append(msg)
        sample_text = "1:1: باب\n1:2: نور نور"
        results = analyze_palindromes(sample_text)
        src.logger.log_secret_found = original_log
        palindrome_detected = any("[Palindrome Detected] - 1:1 - باب" in msg for msg in captured)
        self.assertTrue(palindrome_detected)
        word_level_detected = any("[Palindrome Detected] - 1:2 - نور نور" in msg for msg in captured)
        self.assertTrue(word_level_detected)
        self.assertGreaterEqual(len(results), 2)

    def test_analyze_abjad_numerals_detects_patterns(self):
        '''Test that analyze_abjad_numerals detects notable numerical patterns.'''
        original_log = src.logger.log_secret_found
        captured = []
        src.logger.log_secret_found = lambda msg: captured.append(msg)
        sample_text = "1|1| ب\n1|2| ز"
        results = analyze_abjad_numerals(sample_text)
        src.logger.log_secret_found = original_log
        pattern_detected = any("[Abjad Numerical Pattern]" in msg for msg in captured)
        self.assertTrue(pattern_detected)
        self.assertTrue(any(r[2] == 2 for r in results))
        self.assertTrue(any(r[2] == 7 for r in results))

    def test_analyze_semantic_symmetry_detects_symmetry(self):
        '''Test that analyze_semantic_symmetry detects significant word overlap.'''
        original_log_secret = src.logger.log_secret_found
        original_log_result = src.logger.log_result
        captured_secret = []
        captured_result = []
        src.logger.log_secret_found = lambda msg: captured_secret.append(msg)
        src.logger.log_result = lambda msg: captured_result.append(msg)
        sample_text = "1|1| كلمة كلمة كلمة كلمة"
        results = analyze_semantic_symmetry(sample_text)
        src.logger.log_secret_found = original_log_secret
        src.logger.log_result = original_log_result
        symmetry_detected = any("[Semantic Symmetry (Word Overlap)]" in msg for msg in captured_secret)
        self.assertTrue(symmetry_detected)
        self.assertGreaterEqual(len(results), 1)
        
    def test_analyze_verse_repetitions(self):
        '''Test that analyze_verse_repetitions correctly identifies repetitions both intra-surah and across the Quran.'''
        sample_text = "1|1|VerseA\n1|2|VerseB\n1|3|VerseA\n2|1|VerseA\n2|2|VerseC"
        result = analyze_verse_repetitions(sample_text)
        self.assertEqual(len(result["within_surah"]), 1)
        within = result["within_surah"][0]
        self.assertEqual(within["surah"], "1")
        self.assertEqual(within["verse"], "VerseA")
        self.assertEqual(within["ayah_numbers"], [1, 3])
        self.assertEqual(within["repetition"], 2)
        self.assertEqual(len(result["across_quran"]), 1)
        across = result["across_quran"][0]
        self.assertEqual(across["verse"], "VerseA")
        self.assertEqual(across["occurrences"], [{'surah': '1', 'ayah': 1}, {'surah': '1', 'ayah': 3}, {'surah': '2', 'ayah': 1}])
        self.assertEqual(across["repetition"], 3)
        
    def test_analyze_verse_lengths_distribution(self):
        '''Test that analyze_verse_lengths_distribution correctly calculates average verse length,
        standard deviation, and identifies consistent surahs, logging the appropriate messages.'''
        from src.analyzer import analyze_verse_lengths_distribution
        import src.logger
        sample_text = ("1|1| This is test\n"
                       "1|2| That is a trial\n"
                       "2|1| Short\n"
                       "2|2| This is a much longer verse than others")
        log_results = []
        log_secrets = []
        original_log_result = src.logger.log_result
        original_log_secret = src.logger.log_secret_found
        src.logger.log_result = lambda msg: log_results.append(msg)
        src.logger.log_secret_found = lambda msg: log_secrets.append(msg)
        
        results = analyze_verse_lengths_distribution(sample_text)
        
        # For Surah 1: "This is test" (3 words) and "That is a trial" (4 words) -> avg = 3.5, stddev = 0.5, consistent True.
        self.assertAlmostEqual(results["1"]["average"], 3.5)
        self.assertAlmostEqual(results["1"]["stddev"], 0.5)
        self.assertTrue(results["1"]["consistent"])
        
        # For Surah 2: "Short" (1 word) and "This is a much longer verse than others" (8 words) -> avg = 4.5, stddev = 3.5, not consistent.
        self.assertAlmostEqual(results["2"]["average"], 4.5)
        self.assertAlmostEqual(results["2"]["stddev"], 3.5)
        self.assertFalse(results["2"]["consistent"])
        
        found_secret = any("Verse length consistency" in msg and "[Surah 1]" in msg for msg in log_secrets)
        self.assertTrue(found_secret)
        
        found_surah1_log = any("Surah 1:" in msg and "Average Verse Length: 3.50" in msg for msg in log_results)
        self.assertTrue(found_surah1_log)
        
        found_surah2_log = any("Surah 2:" in msg and "Average Verse Length: 4.50" in msg for msg in log_results)
        self.assertTrue(found_surah2_log)
        
        src.logger.log_result = original_log_result
        src.logger.log_secret_found = original_log_secret

if __name__ == '__main__':
    unittest.main()