'''Integration test for the main module to execute end-to-end analysis.'''

import os
import unittest
from unittest.mock import MagicMock, patch
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
        sample_text = ("1|1| بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n"
                       "1|2| آية من سورة الفاتحة\n"
                       "2|1|الم بداية سورة البقرة\n"
                       "2|2|آية من سورة البقرة\n"
                       "3|1|الم بداية سورة آل عمران\n"
                       "3|2|آية من سورة آل عمران")
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
                self.assertIn("----- Comparative Analysis: Root Word Frequencies -----", log_contents)
                self.assertIn("----- Comparative Analysis: Lemma Frequencies -----", log_contents)
                self.assertIn("Contextual Analysis of Verses Following Muqatta'at", log_contents)
                self.assertIn("Preceding Context Verses Frequency Analysis", log_contents)
                self.assertIn("Muqatta'at Sequences Frequency Analysis:", log_contents)
                self.assertIn("Surah 2 (Al-Baqarah) with Muqatta'at", log_contents)
                self.assertIn("--- Muqatta'at Sequence Length Analysis ---", log_contents)
                self.assertIn("Total Surahs with Muqatta'at Analyzed:", log_contents)
                self.assertIn('"muqattaat":', log_contents)
                self.assertIn("FINAL CONCLUSION: MUQATTA'AT MYSTERY", log_contents)
                self.assertIn("Pearson correlation coefficient between Muqatta'at Abjad value and verse count:", log_contents)
                self.assertIn("Analysis: Muqatta'at Surah Verse Parity", log_contents)
                self.assertIn("Average conjunction frequency per verse (Surahs with Muqatta'at):", log_contents)
                self.assertIn("Average conjunction frequency per verse (Surahs without Muqatta'at):", log_contents)
            finally:
                if os.path.exists(log_file):
                    os.remove(log_file)

    def test_main_integration_with_camel_tools(self):
        '''Test the full execution of main() function end-to-end with CAMeL Tools available.'''
        data_dir = "data"
        file_path = os.path.join(data_dir, "quran-uthmani-min.txt")
        os.makedirs(data_dir, exist_ok=True)
        sample_text = (
            "2|1|الم الحمد لله رب العالمين\n"
            "2|2|الم الحمد لله رب العالمين\n"
            "3|1|الم الحمد لله رب العالمين\n"
            "3|2|الم الحمد لله رب العالمين"
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)

        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        mock_spec = MagicMock()
        mock_analyzer = MagicMock()
        # Simulate CAMeL Tools behavior
        mock_analyzer.analyze.side_effect = (
            lambda token: [{'root': 'حمد'}] if token == "الْحَمْدُ" else [{'root': token}, {'lemma': token}]
        )

        with patch('importlib.util.find_spec', return_value=mock_spec), \
            patch('camel_tools.morphology.database.MorphologyDB.builtin_db', return_value=MagicMock()), \
            patch('src.analyzer.Analyzer', return_value=mock_analyzer):            
            try:
                main.main()

                # Assertions
                self.assertTrue(mock_analyzer.analyze.call_count > 0)
                self.assertTrue(os.path.exists(log_file))
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_contents = f.read()
                
                # Verify expected content
                self.assertIn("POTENTIAL SECRET FOUND:", log_contents)
                self.assertIn("Calculated numerical pattern: 42", log_contents)
                self.assertIn("Word Frequency Analysis (Top 20):", log_contents)
                self.assertIn("Arabic Root Word Frequency Analysis", log_contents)
                self.assertIn("Top Root Word Frequencies:", log_contents)
                self.assertIn("----- Comparative Analysis: Root Word Frequencies -----", log_contents)
                self.assertIn("----- Comparative Analysis: Lemma Frequencies -----", log_contents)
                self.assertIn("Contextual Analysis of Verses Following Muqatta'at", log_contents)
                self.assertIn("Preceding Context Verses Frequency Analysis", log_contents)
                self.assertIn("Muqatta'at Sequences Frequency Analysis:", log_contents)
                self.assertIn("Surah 2 (Al-Baqarah) with Muqatta'at", log_contents)
                self.assertIn("--- Muqatta'at Sequence Length Analysis ---", log_contents)
                self.assertIn("Total Surahs with Muqatta'at Analyzed:", log_contents)
                self.assertIn('"muqattaat":', log_contents)
                self.assertIn("FINAL CONCLUSION: MUQATTA'AT MYSTERY", log_contents)
                self.assertIn("Pearson correlation coefficient between Muqatta'at Abjad value and verse count:", log_contents)
                self.assertIn("Analysis: Muqatta'at Surah Verse Parity", log_contents)
                self.assertIn("Average conjunction frequency per verse (Surahs with Muqatta'at):", log_contents)
                self.assertIn("Average conjunction frequency per verse (Surahs without Muqatta'at):", log_contents)
            finally:
                # Cleanup
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
        self.assertIn("2", result["muqattaat_surahs"])
        self.assertIn("4", result["non_muqattaat_surahs"])
        self.assertAlmostEqual(result["avg_verse_length_muq"], 3.0)
        self.assertAlmostEqual(result["avg_verse_length_non_muq"], 3.0)
        self.assertLessEqual(len(result["top_words_muq"]), 10)
        self.assertLessEqual(len(result["top_words_non_muq"]), 10)

    def test_finalize_muqattaat_analysis(self):
        '''Test the finalize_muqattaat_analysis() function for correct integration and output.'''
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        sample_log_content = (
            "POTENTIAL SECRET FOUND: Test secret 1\n"
            "Regular log entry\n"
            "POTENTIAL SECRET FOUND: Test secret 2\n"
        )
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(sample_log_content)
        
        try:
            from src.analyzer import finalize_muqattaat_analysis
            conclusion = finalize_muqattaat_analysis()
            
            self.assertIsInstance(conclusion, str)
            self.assertGreater(len(conclusion), 0)
            self.assertIn("FINAL CONCLUSION: MUQATTA'AT MYSTERY", conclusion)
            
            with open(log_file, 'r', encoding='utf-8') as f:
                updated_log = f.read()
            
            self.assertIn("FINAL CONCLUSION: MUQATTA'AT MYSTERY", updated_log)
            self.assertIn("Final Conclusions on Muqatta'at Mystery:", updated_log)
            self.assertIn("partially solved", updated_log.lower())
            self.assertIn("Summary of Potential Secrets Found:", updated_log)
            
        finally:
            if os.path.exists(log_file):
                os.remove(log_file)

    def test_finalize_muqattaat_analysis_integration(self):
        '''Test the integration of finalize_muqattaat_analysis() within the main function.'''
        data_dir = "data"
        file_path = os.path.join(data_dir, "quran-uthmani-min.txt")
        os.makedirs(data_dir, exist_ok=True)
        sample_text = ("2|1|الم بداية سورة البقرة\n"
                       "2|2|آية من سورة البقرة")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        with patch('src.analyzer.finalize_muqattaat_analysis') as mock_finalize:
            mock_finalize.return_value = "TEST CONCLUSION"
            
            try:
                main.main()
                mock_finalize.assert_called_once()
                self.assertTrue(os.path.exists(log_file))
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(log_file):
                    os.remove(log_file)
                try:
                    os.rmdir(data_dir)
                except OSError:
                    pass

    def test_compare_interpretations_with_analysis(self):
        '''Test the compare_interpretations_with_analysis() function for correct processing of interpretations.'''
        sample_interpretations = {
            "1": {
                "source": "Scholar A",
                "summary": "The Muqatta'at serve as phonetic markers or unique identifiers for Surahs."
            },
            "2": {
                "source": "Scholar B",
                "summary": "The Muqatta'at represent divine mysteries that only Allah knows."
            }
        }
        
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        try:
            from src.analyzer import compare_interpretations_with_analysis
            compare_interpretations_with_analysis(sample_interpretations)
            
            self.assertTrue(os.path.exists(log_file))
            
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            self.assertIn("Interpretation 1 by Scholar A", log_content)
            self.assertIn("Supporting Evidence", log_content)
            self.assertIn("POTENTIAL SECRET FOUND", log_content)
            
            self.assertIn("Interpretation 2 by Scholar B", log_content)
            self.assertIn("Inconclusive/Neutral", log_content)
            
        finally:
            if os.path.exists(log_file):
                os.remove(log_file)

if __name__ == '__main__':
    unittest.main()