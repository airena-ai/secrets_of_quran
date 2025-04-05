import unittest
from src.quran_data_loader import load_quran_text
from src.quran_search import search_word_in_quran, search_word_group, search_word_in_surah

class TestQuranSearch(unittest.TestCase):
    def test_search_allah_word(self):
        """
        Test that searching for the word 'اللَّهِ' returns at least one verse using case-insensitive search.
        """
        self.maxDiff = None
        quran_file_path = 'data/quran-uthmani-min.txt'
        quran_data = load_quran_text(quran_file_path)
        search_word = 'اللَّهِ'
        results = search_word_in_quran(quran_data, search_word)
        self.assertTrue(len(results) > 0, "Search for '{}' should return at least one verse".format(search_word))

    def test_search_word_group(self):
        """
        Test the search_word_group function.

        Scenario 1: Searching for an existing word group "رَبِّ العٰلَمينَ" should return at least one verse,
                    and the first result should correspond to verse 1:2 and contain the searched word group.
        Scenario 2: Searching for a non-existing word group should return an empty list.
        """
        self.maxDiff = None
        quran_file_path = 'data/quran-uthmani-min.txt'
        quran_data = load_quran_text(quran_file_path)

        # Scenario 1: Search for an existing word group.
        word_group = "رَبِّ العٰلَمينَ"
        results = search_word_group(quran_data, word_group)
        self.assertTrue(len(results) > 0, "Search for '{}' should return at least one verse".format(word_group))
        first_verse = results[0]
        self.assertEqual(first_verse.get('surah_number'), '1', "Expected surah number '1' for the first matching verse")
        self.assertEqual(first_verse.get('ayah_number'), '2', "Expected ayah number '2' for the first matching verse")
        self.assertIn(word_group, first_verse.get('verse_text', ''), "The verse text should contain the word group '{}'".format(word_group))

        # Scenario 2: Search for a non-existing word group.
        non_existing_group = "nonExistingWordGroup"
        results_non_existing = search_word_group(quran_data, non_existing_group)
        self.assertEqual(results_non_existing, [], "Search for '{}' should return an empty list".format(non_existing_group))

    def test_case_insensitive_search_word(self):
        """
        Test the search_word_in_quran function in case-insensitive mode using a dummy dataset.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'This is a Test verse.'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'This is a test verse.'}
        ]
        # Default mode is case-insensitive.
        results = search_word_in_quran(quran_data, "Test")
        self.assertEqual(len(results), 2, "Case-insensitive search should match both verses where casing differs.")

    def test_case_sensitive_search_word(self):
        """
        Test the search_word_in_quran function in case-sensitive mode using a dummy dataset.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'This is a Test verse.'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'This is a test verse.'}
        ]
        results = search_word_in_quran(quran_data, "Test", case_sensitive=True)
        self.assertEqual(len(results), 1, "Case-sensitive search should match only the verse with exact case.")
        self.assertEqual(results[0]['ayah_number'], '1', "Expected to match verse with ayah number '1' due to exact case match.")

    def test_case_insensitive_search_word_group(self):
        """
        Test the search_word_group function in case-insensitive mode using a dummy dataset.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'A wonderful Journey begins here.'},
            {'surah_number': '2', 'ayah_number': '2', 'verse_text': 'a wonderful journey begins here.'}
        ]
        results = search_word_group(quran_data, "wonderful Journey")
        self.assertEqual(len(results), 2, "Case-insensitive group search should match both verses ignoring case differences.")

    def test_case_sensitive_search_word_group(self):
        """
        Test the search_word_group function in case-sensitive mode using a dummy dataset.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'A wonderful Journey begins here.'},
            {'surah_number': '2', 'ayah_number': '2', 'verse_text': 'a wonderful journey begins here.'}
        ]
        results = search_word_group(quran_data, "wonderful Journey", case_sensitive=True)
        self.assertEqual(len(results), 1, "Case-sensitive group search should match only the verse with exact case.")
        self.assertEqual(results[0]['ayah_number'], '1', "Expected to match verse with ayah number '1' due to exact case match.")

    def test_search_word_in_surah(self):
        """
        Test the search_word_in_surah function for a specific Surah.

        Scenario 1: Search for a word that exists in the specified Surah.
        Scenario 2: Search for a word that does not exist in the specified Surah.
        Also verifies case-insensitive search behavior.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'Allah is the Creator.'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'Praise be to ALLAH.'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'This verse does not mention the keyword.'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'Surah two verse with Allah mentioned.'},
            {'surah_number': '2', 'ayah_number': '2', 'verse_text': 'Another verse in surah two.'}
        ]
        # Scenario 1: Search for 'Allah' in surah 1 (case-insensitive)
        results_existing = search_word_in_surah('Allah', 1, quran_data)
        self.assertEqual(len(results_existing), 2, "Expect 2 verses from surah 1 containing 'Allah'.")
        verses_numbers = sorted([verse.get('ayah_number') for verse in results_existing])
        self.assertEqual(verses_numbers, ['1', '2'], "Expected ayah numbers ['1', '2'] for verses containing 'Allah' in surah 1.")

        # Additional check: Case-insensitive search using different casing
        results_case = search_word_in_surah('allAh', 1, quran_data)
        self.assertEqual(len(results_case), 2, "Case-insensitive search should match both verses regardless of case.")

        # Scenario 2: Search for a word that does not exist in surah 1
        results_non_existing = search_word_in_surah('NonExistentWord', 1, quran_data)
        self.assertEqual(results_non_existing, [], "Expect an empty list when searching for a non-existent word in surah 1.")

if __name__ == '__main__':
    unittest.main()