'''Integration test for the main module to execute end-to-end analysis.'''

import os
import unittest
from unittest.mock import MagicMock
import importlib.util
from src import main

class TestMainIntegration(unittest.TestCase):
    '''Test cases for end-to-end integration of the Quran Secrets application.'''
    def setUp(self):
        '''Set maximum diff for assertions.'''
        self.maxDiff = None

    def test_main_integration_fallback(self):
        '''Test the full execution of main() function end-to-end with CAMeL Tools fallback.'''
        data_dir = "data"
        file_path = os.path.join(data_dir, "quran-uthmani-min.txt")
        os.makedirs(data_dir, exist_ok=True)
        sample_text = ("1|1| بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n"
                       "1|2| بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        from unittest.mock import patch
        with patch('importlib.util.find_spec', return_value=None):
            try:
                main.main()
                self.assertTrue(os.path.exists(log_file))
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_contents = f.read()
                self.assertIn("POTENTIAL SECRET FOUND:", log_contents)
                self.assertIn("Calculated numerical pattern: 42", log_contents)
                self.assertIn("Word Frequency Analysis (Top 20):", log_contents)
                self.assertIn("Arabic Root Word Frequency Analysis", log_contents)
                self.assertIn("Top Root Word Frequencies:", log_contents)
                self.assertIn("--- Bigram Frequency Analysis ---", log_contents)
                self.assertIn("Top 20 Bigrams:", log_contents)
                self.assertIn("Verse Repetition Analysis:", log_contents)
                self.assertRegex(log_contents, r'Within Surah - Surah \d+: Verse \'.+\' repeated \d+ times at Ayahs \[.+\]')
                self.assertRegex(log_contents, r'Across Quran - Verse \'.+\' repeated \d+ times at locations: \[.+\]')
                self.assertIn("[Palindrome Analysis]", log_contents)
                self.assertIn("[Abjad Numerical Pattern]", log_contents)
                self.assertIn("[Semantic Symmetry (Word Overlap)]", log_contents)
                self.assertIn("Lemma Analysis:", log_contents)
                self.assertIn("Surah Verse Counts:", log_contents)
                self.assertIn("Verse length consistency", log_contents)
                self.assertIn("Verse length distribution symmetry detected", log_contents)
                self.assertIn("Enhanced semantic symmetry (lemma overlap) detected", log_contents)
                self.assertIn("#################### Muqatta'at Analysis ####################", log_contents)
                self.assertIn("MUQATTA'AT POSITION ANALYSIS:", log_contents)
                self.assertIn("Muqatta'at Sequences Frequency Analysis:", log_contents)
                self.assertIn("#################### Muqatta'at Numerical Analysis ####################", log_contents)
                self.assertIn("Total Abjad Sum:", log_contents)
                # New assertion to verify contextual analysis logs
                self.assertIn("Contextual Analysis of Verses Following Muqatta'at", log_contents)
                # New assertion to verify thematic analysis logs
                self.assertIn("Surah 2 (Al-Baqarah) with Muqatta'at 'الم': Theme - Guidance and Divine Law", log_contents)
            finally:
                if os.path.exists(log_file):
                    os.remove(log_file)

    def test_main_integration_with_camel_tools(self):
        '''Test the full execution of main() function end-to-end with CAMeL Tools available.'''
        data_dir = "data"
        file_path = os.path.join(data_dir, "quran-uthmani-min.txt")
        os.makedirs(data_dir, exist_ok=True)
        # Updated sample text to include a Surah with a proper Muqatta'at sequence for testing.
        sample_text = ("2|1|الم الحمد لله رب العالمين\n"
                       "2|2|الم الحمد لله رب العالمين\n"
                       "3|1| الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِين\n"
                       "3|2| الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِين")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        from unittest.mock import patch, MagicMock
        mock_spec = MagicMock()
        mock_analyzer = MagicMock()
        # For token "الحمد", return a root of 'حمد'; for other tokens, return the token itself.
        mock_analyzer.analyze.side_effect = lambda token: [{'root': 'حمد'}, {'lemma': 'حمد'}] if token == "الحمد" else [{'root': token}, {'lemma': token}]
        mock_analyzer_class = MagicMock()
        mock_analyzer_class.builtin_analyzer.return_value = mock_analyzer
        
        with patch('importlib.util.find_spec', return_value=mock_spec), \
             patch.dict('sys.modules', {'camel_tools': MagicMock(), 
                                          'camel_tools.morphology': MagicMock(),
                                          'camel_tools.morphology.analyzer': MagicMock()}), \
             patch('camel_tools.morphology.analyzer.Analyzer', mock_analyzer_class):
            try:
                main.main()
                self.assertTrue(os.path.exists(log_file))
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_contents = f.read()
                self.assertIn("POTENTIAL SECRET FOUND:", log_contents)
                self.assertIn("Calculated numerical pattern: 42", log_contents)
                self.assertIn("Word Frequency Analysis (Top 20):", log_contents)
                self.assertIn("Arabic Root Word Frequency Analysis", log_contents)
                self.assertIn("Top Root Word Frequencies:", log_contents)
                self.assertIn("--- Bigram Frequency Analysis ---", log_contents)
                self.assertIn("Top 20 Bigrams:", log_contents)
                self.assertIn("Verse Repetition Analysis:", log_contents)
                self.assertIn("Root 'حمد'", log_contents)
                self.assertRegex(log_contents, r'Within Surah - Surah \d+: Verse \'.+\' repeated \d+ times at Ayahs \[.+\]')
                self.assertRegex(log_contents, r'Across Quran - Verse \'.+\' repeated \d+ times at locations: \[.+\]')
                self.assertIn("[Palindrome Analysis]", log_contents)
                self.assertIn("[Abjad Numerical Pattern]", log_contents)
                self.assertIn("[Semantic Symmetry (Word Overlap)]", log_contents)
                self.assertIn("Lemma Analysis:", log_contents)
                self.assertIn("Surah Verse Counts:", log_contents)
                self.assertIn("Verse length consistency", log_contents)
                self.assertIn("Verse length distribution symmetry detected", log_contents)
                self.assertIn("Enhanced semantic symmetry (lemma overlap) detected", log_contents)
                self.assertIn("#################### Muqatta'at Analysis ####################", log_contents)
                self.assertIn("MUQATTA'AT POSITION ANALYSIS:", log_contents)
                self.assertIn("Muqatta'at Sequences Frequency Analysis:", log_contents)
                self.assertIn("#################### Muqatta'at Numerical Analysis ####################", log_contents)
                self.assertIn("Total Abjad Sum:", log_contents)
                self.assertIn("Sequence 'الم' occurred 2 times", log_contents)
                self.assertIn("Sequence 'الحمد' occurred 2 times", log_contents)
                # New assertion to verify contextual analysis logs
                self.assertIn("Contextual Analysis of Verses Following Muqatta'at", log_contents)
                # New assertion to verify thematic analysis logs
                self.assertIn("Surah 2 (Al-Baqarah) with Muqatta'at 'الم': Theme - Guidance and Divine Law", log_contents)
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(log_file):
                    os.remove(log_file)
                try:
                    os.rmdir(data_dir)
                except OSError:
                    pass

    def test_compare_surahs_muqattaat_vs_non_muqattaat(self):
        '''Test the compare_surahs_muqattaat_vs_non_muqattaat() function for correct categorization and analysis.'''
        sample_text = ("2|1|الم بداية السورة\n"
                       "2|2|نص الآية الثانية\n"
                       "4|1|هذه آية عادية\n"
                       "4|2|وهذه آية أخرى")
        from src.analyzer import compare_surahs_muqattaat_vs_non_muqattaat
        result = compare_surahs_muqattaat_vs_non_muqattaat(sample_text)
        # Check that Surah 2 is categorized as having Muqatta'at and Surah 4 is not.
        self.assertIn("2", result["muqattaat_surahs"])
        self.assertIn("4", result["non_muqattaat_surahs"])
        # Expected average for both groups should be 3.0 as each line has 3 words.
        self.assertAlmostEqual(result["avg_verse_length_muq"], 3.0)
        self.assertAlmostEqual(result["avg_verse_length_non_muq"], 3.0)
        # Top words lists should have at most 10 entries.
        self.assertLessEqual(len(result["top_words_muq"]), 10)
        self.assertLessEqual(len(result["top_words_non_muq"]), 10)

if __name__ == '__main__':
    unittest.main()