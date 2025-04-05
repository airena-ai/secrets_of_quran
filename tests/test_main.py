'''Integration test for the main module to execute end-to-end analysis.'''

import os
import unittest
from unittest.mock import patch, MagicMock
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
        sample_text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        # Mock importlib.util.find_spec to simulate CAMeL Tools not being available
        with patch('importlib.util.find_spec', return_value=None):
            try:
                main.main()
                self.assertTrue(os.path.exists(log_file))
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_contents = f.read()
                self.assertIn("POTENTIAL SECRET FOUND:", log_contents)
                self.assertIn("Calculated numerical pattern: 42", log_contents)
                self.assertIn("Word Frequency Analysis (Top 20):", log_contents)
                self.assertIn("Arabic Root Word Frequency Analysis:", log_contents)
                self.assertIn("Top Root Word Frequencies:", log_contents)
                self.assertIn("--- Bigram Frequency Analysis ---", log_contents)
                self.assertIn("Top 20 Bigrams:", log_contents)
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(log_file):
                    os.remove(log_file)
                try:
                    os.rmdir(data_dir)
                except OSError:
                    pass

    def test_main_integration_with_camel_tools(self):
        '''Test the full execution of main() function end-to-end with CAMeL Tools available.'''
        data_dir = "data"
        file_path = os.path.join(data_dir, "quran-uthmani-min.txt")
        os.makedirs(data_dir, exist_ok=True)
        sample_text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        # Create mock objects for CAMeL Tools
        mock_spec = MagicMock()
        mock_analyzer = MagicMock()
        # When analyze is called, return a mock analysis with root information
        mock_analyzer.analyze.side_effect = lambda token: [{'root': 'سمو'}] if token == "بسم" else [{'root': 'الله'}] if token == "الله" else [{'root': 'رحم'}] if token in ["الرحمن", "الرحيم"] else [{'root': token}]
        
        mock_analyzer_class = MagicMock()
        mock_analyzer_class.builtin_analyzer.return_value = mock_analyzer
        
        # Apply the mocks to simulate CAMeL Tools being available and working
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
                self.assertIn("Arabic Root Word Frequency Analysis:", log_contents)
                self.assertIn("Top Root Word Frequencies:", log_contents)
                self.assertIn("--- Bigram Frequency Analysis ---", log_contents)
                self.assertIn("Top 20 Bigrams:", log_contents)
                
                # Verify that the root analysis was performed using CAMeL Tools
                # We should see the roots that our mock analyzer returned
                self.assertIn("Root 'سمو'", log_contents)
                self.assertIn("Root 'الله'", log_contents)
                self.assertIn("Root 'رحم'", log_contents)
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