'''Unit tests for the analyzer module.'''

import unittest
import src
from src.analyzer import (analyze_text, analyze_word_frequency, analyze_root_words, analyze_bigrams,
                          analyze_palindromes, analyze_abjad_numerals, analyze_semantic_symmetry,
                          analyze_verse_repetitions, analyze_verse_lengths_distribution, analyze_verse_length_symmetry,
                          analyze_enhanced_semantic_symmetry, analyze_muqattaat_length, analyze_muqattaat,
                          analyze_muqattaat_semantic_similarity, compare_interpretations_with_analysis)

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
        with patch('importlib.util.find_spec', return_value=mock_spec), \
             patch.dict('sys.modules', {'camel_tools': MagicMock(), 
                                          'camel_tools.morphology': MagicMock(),
                                          'camel_tools.morphology.analyzer': MagicMock()}), \
            patch('src.analyzer.Analyzer', return_value=mock_analyzer):                                          

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
                       "2|1|Short\n"
                       "2|2|This is a much longer verse than others")
        log_results = []
        log_secrets = []
        original_log_result = src.logger.log_result
        original_log_secret = src.logger.log_secret_found
        src.logger.log_result = lambda msg: log_results.append(msg)
        src.logger.log_secret_found = lambda msg: log_secrets.append(msg)
        
        results = analyze_verse_lengths_distribution(sample_text)
        
        self.assertAlmostEqual(results["1"]["average"], 3.5)
        self.assertAlmostEqual(results["1"]["stddev"], 0.5)
        self.assertTrue(results["1"]["consistent"])
        
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

    def test_analyze_verse_length_symmetry_symmetry_detected(self):
        '''Test that analyze_verse_length_symmetry detects symmetry when halves have similar verse lengths.'''
        sample_text = ("1|1| word word\n"
                       "1|2| word word\n"
                       "1|3| word word\n"
                       "1|4| word word")
        log_messages = []
        original_log_secret = src.logger.log_secret_found
        src.logger.log_secret_found = lambda msg: log_messages.append(msg)
        results = analyze_verse_length_symmetry(sample_text, avg_threshold=0.5, stddev_threshold=0.5)
        src.logger.log_secret_found = original_log_secret
        self.assertIn("1", results)
        self.assertTrue(results["1"]["symmetric"])
        secret_logged = any("Verse length distribution symmetry detected in Surah 1" in msg for msg in log_messages)
        self.assertTrue(secret_logged)
        
    def test_analyze_verse_length_symmetry_non_symmetric(self):
        '''Test that analyze_verse_length_symmetry returns non-symmetric when verse lengths differ significantly.'''
        sample_text = ("3|1| one two three four\n"
                       "3|2| one\n"
                       "3|3| one two three four five six\n"
                       "3|4| one two")
        results = analyze_verse_length_symmetry(sample_text, avg_threshold=1.0, stddev_threshold=1.0)
        self.assertIn("3", results)
        self.assertFalse(results["3"]["symmetric"])
        
    def test_analyze_enhanced_semantic_symmetry_symmetry_detected(self):
        '''Test that analyze_enhanced_semantic_symmetry detects semantic symmetry when lemma overlap is high.'''
        sample_text = ("2|1| alpha beta gamma\n"
                       "2|2| alpha beta gamma")
        log_messages = []
        original_log_secret = src.logger.log_secret_found
        src.logger.log_secret_found = lambda msg: log_messages.append(msg)
        results = analyze_enhanced_semantic_symmetry(sample_text, symmetry_threshold=0.5)
        src.logger.log_secret_found = original_log_secret
        self.assertIn("2", results)
        self.assertGreaterEqual(results["2"]["symmetry_score"], 0.5)
        secret_logged = any("Enhanced semantic symmetry (lemma overlap) detected in Surah 2" in msg for msg in log_messages)
        self.assertTrue(secret_logged)
        
    def test_analyze_enhanced_semantic_symmetry_low_symmetry(self):
        '''Test that analyze_enhanced_semantic_symmetry returns low symmetry score when lemma overlap is minimal.'''
        sample_text = ("4|1| alpha beta gamma\n"
                       "4|2| delta epsilon zeta")
        results = analyze_enhanced_semantic_symmetry(sample_text, symmetry_threshold=0.5)
        self.assertIn("4", results)
        self.assertEqual(results["4"]["symmetry_score"], 0)
        
    def test_analyze_muqattaat_semantic_similarity(self):
        '''Test the analyze_muqattaat_semantic_similarity function with a sample group of Surahs.'''
        sample_text = (
            "2|1| A B C D\n"
            "2|2| E F G\n"
            "3|1| A B C D\n"
            "3|2| E F G H\n"
            "7|1| X Y Z\n"
            "7|2| W Z\n"
        )
        # Define a mapping: Surahs 2 and 3 share the same muqattaat "الم", Surah 7 has a different one.
        muqattaat_mapping = {"2": "الم", "3": "الم", "7": "XYZ"}
        log_results = []
        log_secrets = []
        original_log_result = src.logger.log_result
        original_log_secret = src.logger.log_secret_found
        src.logger.log_result = lambda msg: log_results.append(msg)
        src.logger.log_secret_found = lambda msg: log_secrets.append(msg)
        
        from src.analyzer import analyze_muqattaat_semantic_similarity
        analyze_muqattaat_semantic_similarity(sample_text, muqattaat_mapping)
        
        src.logger.log_result = original_log_result
        src.logger.log_secret_found = original_log_secret
        
        avg_logged = any("Average Semantic Similarity for Muqatta'at Group 'الم'" in msg for msg in log_results)
        self.assertTrue(avg_logged)
        secret_logged = any("POTENTIAL SECRET FOUND: [Surah 2] and [Surah 3] (Muqatta'at: الم)" in msg for msg in log_secrets)
        self.assertTrue(secret_logged)

    def test_compare_interpretations_with_analysis(self):
        '''Test the compare_interpretations_with_analysis function with different interpretations.'''
        interpretations = {
            "interpretation_1": {
                "source": "Journal A",
                "summary": "This interpretation is based on rhythmic patterns and unique identifier markers."
            },
            "interpretation_2": {
                "source": "Journal B",
                "summary": "This interpretation emphasizes divine mystery and is more theological."
            },
            "interpretation_3": {
                "source": "Journal C",
                "summary": "An ambiguous interpretation with no clear markers."
            }
        }
        captured_results = []
        captured_secrets = []
        original_log_result = src.logger.log_result
        original_log_secret = src.logger.log_secret_found
        src.logger.log_result = lambda msg: captured_results.append(msg)
        src.logger.log_secret_found = lambda msg: captured_secrets.append(msg)
        
        compare_interpretations_with_analysis(interpretations)
        
        src.logger.log_result = original_log_result
        src.logger.log_secret_found = original_log_secret

        result_1 = next((msg for msg in captured_results if "interpretation_1" in msg.lower()), "")
        self.assertIn("Supporting Evidence", result_1)
        secret_1 = next((msg for msg in captured_secrets if "interpretation_1" in msg.lower()), "")
        self.assertIn("POTENTIAL SECRET FOUND", secret_1)
        
        result_2 = next((msg for msg in captured_results if "interpretation_2" in msg.lower()), "")
        self.assertIn("Inconclusive/Neutral", result_2)
        secret_2 = next((msg for msg in captured_secrets if "interpretation_2" in msg.lower()), None)
        self.assertIsNone(secret_2)
        
        result_3 = next((msg for msg in captured_results if "interpretation_3" in msg.lower()), "")
        self.assertIn("Inconclusive/Neutral", result_3)
        secret_3 = next((msg for msg in captured_secrets if "interpretation_3" in msg.lower()), None)
        self.assertIsNone(secret_3)

if __name__ == '__main__':
    unittest.main()