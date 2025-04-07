import os
import unittest
from src.main import main

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the core user flow.
    """

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
        # Verify that the log file was created and contains expected log messages related to frequency analysis
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, "r", encoding="utf-8") as file:
            log_content = file.read()
        self.assertIn("Application started.", log_content)
        self.assertIn("Starting word frequency analysis.", log_content)
        self.assertIn("Total unique words:", log_content)
        self.assertIn("Top 50 most frequent words:", log_content)
        self.assertIn("Word frequency analysis completed.", log_content)
        # Optionally check for specific frequency outputs for known words based on sample data processing
        self.assertIn("Total unique words: 4", log_content)
        self.assertIn("Word: بسم, Count: 1", log_content)
        self.assertIn("Word: الله, Count: 1", log_content)
        self.assertIn("Word: الرحمن, Count: 1", log_content)
        self.assertIn("Word: الرحيم, Count: 1", log_content)

        # Cleanup created files
        os.remove(data_file)
        os.remove(log_file)
        if not os.listdir(data_dir):
            os.rmdir(data_dir)

if __name__ == "__main__":
    unittest.main()