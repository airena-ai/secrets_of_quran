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
        # Verify that the log file was created and contains expected log messages
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, "r", encoding="utf-8") as file:
            log_content = file.read()
        self.assertIn("Application started.", log_content)
        self.assertIn("Completed data loading.", log_content)
        self.assertIn("Tokenization complete:", log_content)
        self.assertIn("Lemma:", log_content)
        self.assertIn("Root:", log_content)

        # Enhance integration test: Parse log lines for processed tokens and check expected lemma and root.
        processed_lines = [line for line in log_content.splitlines() if "Token processed -" in line]
        self.assertGreater(len(processed_lines), 0, "No token processed log lines found.")
        for line in processed_lines:
            # Expecting line format: "Token processed - Original: %s, Normalized: %s, Lemma: %s, Root: %s"
            parts = line.split("Token processed -")[-1].strip().split(", ")
            self.assertEqual(len(parts), 4, "Log line does not have four parts.")
            original_val = parts[0].split("Original:")[-1].strip()
            normalized_val = parts[1].split("Normalized:")[-1].strip()
            lemma_val = parts[2].split("Lemma:")[-1].strip()
            root_val = parts[3].split("Root:")[-1].strip()
            self.assertNotEqual(lemma_val, "", "Lemma value is empty.")
            self.assertNotEqual(root_val, "", "Root value is empty.")
        # Cleanup created files
        os.remove(data_file)
        os.remove(log_file)
        if not os.listdir(data_dir):
            os.rmdir(data_dir)

if __name__ == "__main__":
    unittest.main()