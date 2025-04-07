import os
import re
import unittest
from collections import Counter
from src.main import main

class TestIntegration(unittest.TestCase):
    '''
    Integration tests for the core user flow.
    '''
    def test_integration_flow(self):
        self.maxDiff = None
        # Determine project root and log file path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_file = os.path.join(project_root, "quran_analysis.log")
        # Remove log file if it exists
        if os.path.exists(log_file):
            os.remove(log_file)
        # Ensure the data directory and file exist with sample data
        data_dir = os.path.join(project_root, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        data_file = os.path.join(data_dir, "quran-uthmani-min-test.txt")
        sample_data = "1|1|بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n"
        with open(data_file, "w", encoding="utf-8") as file:
            file.write(sample_data)
        
        # Set the environment variable to use the test file
        os.environ["DATA_FILE"] = data_file

        # Execute the main application flow and capture the returned analysis results
        result = main()
        # Verify that the returned result contains the gematria co-occurrence analysis
        self.assertIn("gematria_cooccurrence", result)
        self.assertIsInstance(result["gematria_cooccurrence"], Counter)
        
        # Verify that the log file was created and contains expected log messages
        with open(log_file, "r", encoding="utf-8") as file:
            log_content = file.read()
        self.assertIn("Application started.", log_content)
        self.assertIn("Starting word frequency analysis.", log_content)
        self.assertIn("Total unique words:", log_content)
        self.assertIn("Top 2000 most frequent words:", log_content)
        self.assertIn("Word frequency analysis completed.", log_content)
        
        # Validate that the total unique words count is present and greater than zero.
        total_unique_match = re.search(r"Total unique words:\s*(\d+)", log_content)
        self.assertIsNotNone(total_unique_match, "Total unique words count not found in logs.")
        total_unique = int(total_unique_match.group(1))
        self.assertGreater(total_unique, 0, "Expected total unique words to be greater than 0.")
        
        # Check for presence of expected word log messages without relying on exact counts.
        self.assertIn("Word: بسم", log_content)
        self.assertIn("Word: الله", log_content)
        self.assertIn("Word: الرحمن", log_content)
        self.assertIn("Word: الرحيم", log_content)
        
        # Additional assertions for word co-occurrence analysis
        self.assertIn("Starting word co-occurrence analysis.", log_content)
        self.assertIn("Co-occurrence analysis returned", log_content)
        
        # Assertions for Surah and Ayah level analyses (word frequency)
        self.assertIn("Starting Surah-level word frequency analysis.", log_content)
        self.assertIn("Surah-level word frequency analysis completed.", log_content)
        self.assertIn("Starting Ayah-level word frequency analysis.", log_content)
        self.assertIn("Ayah-level word frequency analysis completed.", log_content)

        # Assertions for ayah-level root word frequency analysis
        self.assertIn("Starting Ayah-level Root Word Frequency Analysis.", log_content)
        self.assertIn("Ayah-level Root Word Frequency Analysis completed.", log_content)
        self.assertIn("Ayah Root Word Frequency Analysis - Ayah:", log_content)
        self.assertRegex(log_content, r"Ayah Root Word Frequency Analysis - Ayah:\s*1\|1")
        self.assertIn("Top 5 Root Words:", log_content)
        self.assertRegex(log_content, r"Total Unique Root Words:\s*\d+")
        
        # Assertions for first and last root word frequency analysis
        self.assertIn("Starting Ayah First Root Word Frequency Analysis.", log_content)
        self.assertIn("Top 10 most frequent first root words:", log_content)
        self.assertIn("Total unique first root words:", log_content)
        self.assertIn("Starting Ayah Last Root Word Frequency Analysis.", log_content)
        self.assertIn("Top 10 most frequent last root words:", log_content)
        self.assertIn("Total unique last root words:", log_content)

        # Assertions for Gematria Value Co-occurrence Analysis
        self.assertIn("Starting Gematria Co-occurrence Analysis", log_content)
        self.assertIn("Gematria Co-occurrence Analysis completed.", log_content)
        self.assertIn("Top 10 most frequent Gematria value pairs:", log_content)
        self.assertIn("Total unique Gematria pairs:", log_content)
        
        # Assertions for word length distribution analysis
        self.assertIn("Word length distribution analysis completed.", log_content)
        
        # Assertions for surah-level root word frequency analysis
        self.assertIn("Starting surah-level root word frequency analysis.", log_content)
        
        # Assertions for root word frequency analysis
        self.assertIn("Starting root word frequency analysis.", log_content)
        self.assertIn("Root word frequency analysis completed.", log_content)
        
        # Assertions for root word co-occurrence analysis
        self.assertIn("Starting Root Word Co-occurrence Analysis...", log_content)
        self.assertIn("Root Word Co-occurrence Analysis Completed.", log_content)
        self.assertIn("Total unique root word pairs:", log_content)
        
        # Assertions for lemma word frequency and co-occurrence analysis
        self.assertIn("Starting lemma word frequency analysis.", log_content)
        self.assertIn("Lemma word frequency analysis completed.", log_content)
        self.assertIn("Starting Lemma Word Co-occurrence Analysis...", log_content)
        self.assertIn("Lemma Word Co-occurrence Analysis Completed.", log_content)
        
        # Additional assertions for Character Frequency Analyses at Surah and Ayah levels
        self.assertIn("Starting Surah-level Character Frequency Analysis.", log_content)
        self.assertIn("Surah-level Character Frequency Analysis completed.", log_content)
        self.assertIn("Starting Ayah-level Character Frequency Analysis.", log_content)
        self.assertIn("Ayah-level Character Frequency Analysis completed.", log_content)
        self.assertRegex(log_content, r"Surah-level Character Frequency Analysis - Surah: (1|Unknown)")
        self.assertRegex(log_content, r"Ayah-level Character Frequency Analysis - Surah: (1|Unknown), Ayah: (1|Unknown)")
        
        # Additional assertions for character frequency analysis
        self.assertIn("Starting Character Frequency Analysis", log_content)
        self.assertIn("Top 20 most frequent characters:", log_content)
        self.assertIn("Total unique characters:", log_content)
        
        # Additional assertions for word n-gram analysis at Quran level
        self.assertIn("Starting word n-gram analysis.", log_content)
        self.assertIn("Word n-gram analysis completed.", log_content)
        
        # Assertions for Surah-level and Ayah-level word n-gram analyses
        self.assertIn("Starting Surah-level word n-gram analysis.", log_content)
        self.assertIn("Starting Ayah-level word n-gram analysis.", log_content)
        self.assertIn("Surah Word N-gram Analysis:", log_content)
        self.assertIn("Ayah Word N-gram Analysis:", log_content)
        
        # Additional assertions for Character N-gram Analysis (new functions)
        self.assertIn("Starting Character N-gram Analysis at Quran level.", log_content)
        self.assertIn("Character N-gram Analysis at Quran level completed.", log_content)
        self.assertIn("Starting Character N-gram Analysis at Surah level.", log_content)
        self.assertIn("Character N-gram Analysis at Surah level completed.", log_content)
        self.assertIn("Starting Character N-gram Analysis at Ayah level.", log_content)
        self.assertIn("Character N-gram Analysis at Ayah level completed.", log_content)
        
        # New assertions for Word Collocation Analysis
        self.assertIn("Starting Word Collocation Analysis.", log_content)
        self.assertIn("Total unique collocation pairs:", log_content)
        self.assertIn("Word Collocation Analysis completed.", log_content)
        
        # New assertions for Semantic Group Co-occurrence Analysis at Ayah Level
        self.assertIn("Starting Semantic Group Co-occurrence Analysis at Ayah Level.", log_content)
        self.assertIn("Top 10 semantic group co-occurrence pairs:", log_content)
        self.assertIn("Total unique semantic group co-occurrence pairs found:", log_content)

        # New assertions for Anomaly Detection Analysis
        self.assertIn("Starting Anomaly Detection Analysis.", log_content)
        self.assertIn("Anomaly Detection Analysis Results:", log_content)
        self.assertIn("Anomaly Detection Analysis completed.", log_content)
        
        # New assertions for Gematria Value Distribution Analysis
        self.assertIn("Starting Gematria Value Distribution Analysis.", log_content)
        self.assertIn("Gematria Value Distribution Analysis completed.", log_content)
        self.assertIn("Gematria Value Distribution Analysis:", log_content)
        
        # Cleanup created files
        os.remove(data_file)
        os.remove(log_file)
        if not os.listdir(data_dir):
            os.rmdir(data_dir)

    def test_semantic_group_cooccurrence_analysis(self):
        self.maxDiff = None
        import io
        import logging
        from src.semantic_analyzer import analyze_semantic_group_cooccurrence_ayah
        log_stream = io.StringIO()
        stream_handler = logging.StreamHandler(log_stream)
        formatter = logging.Formatter('%(message)s')
        stream_handler.setFormatter(formatter)
        logger = logging.getLogger("quran_analysis")
        logger.addHandler(stream_handler)
        logger.setLevel(logging.INFO)
        
        sample_data = [
            {"semantic_groups": ["themeA", "themeB", "themeC"]},
            {"semantic_groups": ["themeA", "themeC"]},
            {"semantic_groups": ["themeB", "themeC", "themeD"]}
        ]
        expected_result = {
            ("themeA", "themeB"): 1,
            ("themeA", "themeC"): 2,
            ("themeB", "themeC"): 2,
            ("themeB", "themeD"): 1,
            ("themeC", "themeD"): 1
        }
        result = analyze_semantic_group_cooccurrence_ayah(sample_data)
        logger.removeHandler(stream_handler)
        log_contents = log_stream.getvalue()
        
        self.assertEqual(result, expected_result)
        self.assertIn("Top 10 semantic group co-occurrence pairs:", log_contents)
        self.assertIn("Total unique semantic group co-occurrence pairs found: 5", log_contents)

if __name__ == "__main__":
    unittest.main()