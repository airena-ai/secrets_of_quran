import os
import re
import unittest
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

        # Execute the main application flow
        main()
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
        self.assertIn("Word Co-occurrence Analysis Results", log_content)
        self.assertIn("Co-occurrence analysis returned", log_content)
        self.assertIn("Total unique word pairs:", log_content)
        
        # Assertions for Surah and Ayah level analyses
        self.assertIn("Starting Surah-level word frequency analysis.", log_content)
        self.assertIn("Surah-level word frequency analysis completed.", log_content)
        self.assertIn("Surah-level Frequency Analysis - Surah 1 Top 10 Words:", log_content)
        self.assertIn("Starting Ayah-level word frequency analysis.", log_content)
        self.assertIn("Ayah-level word frequency analysis completed.", log_content)
        self.assertIn("Ayah-level Frequency Analysis - Surah 1, Ayah 1 Top 5 Words:", log_content)

        # Assertions for word length distribution analysis
        self.assertIn("Word Length Distribution Analysis:", log_content)
        self.assertIn("Total words analyzed:", log_content)
        self.assertIn("Average word length:", log_content)
        self.assertIn("Most frequent word length(s):", log_content)

        # Assertions for root word frequency analysis
        self.assertIn("Starting root word frequency analysis.", log_content)
        self.assertIn("Total unique root words found:", log_content)
        self.assertIn("Top 1000 most frequent root words:", log_content)
        
        # Assertions for root word co-occurrence analysis
        self.assertIn("Starting Root Word Co-occurrence Analysis...", log_content)
        self.assertIn("Root Word Co-occurrence Analysis Completed.", log_content)
        self.assertIn("Total unique root word pairs:", log_content)
        self.assertIn("Top 10000 most frequent root word pairs:", log_content)

        # Cleanup created files
        os.remove(data_file)
        os.remove(log_file)
        if not os.listdir(data_dir):
            os.rmdir(data_dir)

if __name__ == "__main__":
    unittest.main()