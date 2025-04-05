'''Integration test for the main module to execute end-to-end analysis.'''

import os
import unittest
from unittest.mock import MagicMock
import importlib.util
from src import main

class TestMainIntegration(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_main_integration_fallback(self):
        '''Test the full execution of main() function end-to-end with CAMeL Tools fallback.'''
        data_dir = "data"
        file_path = os.path.join(data_dir, "quran-uthmani-min.txt")
        os.makedirs(data_dir, exist_ok=True)
        sample_text = ("1|1| بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n"
                       "1|2| بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")
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
            finally:
                if os.path.exists(log_file):
                    os.remove(log_file)

    def test_main_integration_with_camel_tools(self):
        '''Test the full execution of main() function end-to-end with CAMeL Tools available.'''
        data_dir = "data"
        file_path = os.path.join(data_dir, "quran-uthmani-min.txt")
        os.makedirs(data_dir, exist_ok=True)
        sample_text = ("2|1| الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\n"
                       "2|2| الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        from unittest.mock import patch, MagicMock
        mock_spec = MagicMock()
        mock_analyzer = MagicMock()
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
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(log_file):
                    os.remove(log_file)
                try:
                    os.rmdir(data_dir)
                except OSError:
                    pass

if __name__ == '__main__':
    unittest.main()