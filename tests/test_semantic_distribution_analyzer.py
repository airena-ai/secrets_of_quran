import unittest
from src.semantic_distribution_analyzer import analyze_semantic_complexity_distribution_ayah

class TestSemanticDistributionAnalyzer(unittest.TestCase):
    '''
    Integration tests for the analyze_semantic_complexity_distribution_ayah function.
    '''
    def test_analyze_semantic_complexity_distribution_ayah(self):
        self.maxDiff = None
        # Create sample Quran data with minimal fields: verse_text, processed_text, roots, surah, ayah.
        sample_data = [
            {
                "surah": "1",
                "ayah": "1",
                "verse_text": "test",
                "processed_text": "test",
                "roots": ["A", "A", "B"]  # semantic density = 2
            },
            {
                "surah": "1",
                "ayah": "2",
                "verse_text": "example",
                "processed_text": "example",
                "roots": ["B", "C"]  # semantic density = 1
            },
            {
                "surah": "1",
                "ayah": "3",
                "verse_text": "another",
                "processed_text": "another",
                "roots": []  # semantic density = 0
            }
        ]
        result = analyze_semantic_complexity_distribution_ayah(sample_data)
        # Verify that quantile boundaries exist in the result for sufficient variability scenario.
        boundaries = result["quantile_boundaries"]
        self.assertIn("low_medium_threshold", boundaries)
        self.assertIn("medium_high_threshold", boundaries)
        # Verify that group_statistics exists and contains low, medium, high groups
        self.assertIn("group_statistics", result)
        groups = result["group_statistics"]
        self.assertIn("low", groups)
        self.assertIn("medium", groups)
        self.assertIn("high", groups)
        # Based on the semantic densities [2, 1, 0] the groups should be:
        # - low: density 0 (ayah 3)
        # - medium: density 1 (ayah 2)
        # - high: density 2 (ayah 1)
        self.assertEqual(groups["low"]["num_ayahs"], 1)
        self.assertEqual(groups["medium"]["num_ayahs"], 1)
        self.assertEqual(groups["high"]["num_ayahs"], 1)
        # Check that descriptive statistics keys are present
        for grp in ["low", "medium", "high"]:
            for stat in ["average_word_length_stats", "average_sentence_length_stats"]:
                self.assertIn(stat, groups[grp])
                stats_dict = groups[grp][stat]
                self.assertIn("mean", stats_dict)
                self.assertIn("median", stats_dict)
                self.assertIn("stdev", stats_dict)
                self.assertIn("min", stats_dict)
                self.assertIn("max", stats_dict)

    def test_analyze_semantic_complexity_distribution_ayah_with_insufficient_variability(self):
        self.maxDiff = None
        # Create sample data where all ayahs have the same semantic density (fallback scenario)
        sample_data = [
            {
                "surah": "1",
                "ayah": "1",
                "verse_text": "test",
                "processed_text": "test",
                "roots": ["A", "A"]  # semantic density = 2
            },
            {
                "surah": "1",
                "ayah": "2",
                "verse_text": "example",
                "processed_text": "example",
                "roots": ["A", "A"]  # semantic density = 2
            }
        ]
        result = analyze_semantic_complexity_distribution_ayah(sample_data)
        # In fallback, we expect quantile_boundaries to be None and all ayahs assigned to "medium".
        self.assertIsNone(result["quantile_boundaries"]["low_medium_threshold"])
        self.assertIsNone(result["quantile_boundaries"]["medium_high_threshold"])
        groups = result["group_statistics"]
        self.assertEqual(groups["low"]["num_ayahs"], 0)
        self.assertEqual(groups["medium"]["num_ayahs"], 2)
        self.assertEqual(groups["high"]["num_ayahs"], 0)

if __name__ == "__main__":
    unittest.main()