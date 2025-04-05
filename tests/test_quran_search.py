import unittest
from src.quran_data_loader import load_quran_text
from src.quran_search import (
    search_word_in_quran, 
    search_word_group, 
    search_word_in_surah,
    search_word_group_in_surah,
    count_word_occurrences,
    count_word_group_occurrences
)

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

    def test_search_word_group_in_surah(self):
        """
        Test the search_word_group_in_surah function for various scenarios:
        
        - Scenario 1: Search for a word group that exists in a specific Surah (case-insensitive).
        - Scenario 2: Search for a word group that exists multiple times in a specific Surah.
        - Scenario 3: Search for a non-existent word group in a Surah.
        - Scenario 4: Verify case-sensitive search differentiates correctly.
        - Scenario 5: Ensure that filtering by a Surah number with no entries returns an empty list.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'Bismillah Ar-Rahman Ar-Rahim'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'The phrase Ar-Rahman Ar-Rahim is repeated.'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'This verse does not contain the target phrase.'},
            {'surah_number': '2', 'ayah_number': '2', 'verse_text': 'Test Phrase appears here.'},
            {'surah_number': '2', 'ayah_number': '3', 'verse_text': 'Another Test Phrase instance in surah 2.'},
            {'surah_number': '3', 'ayah_number': '1', 'verse_text': 'A mixture of text with Al-Rahman Al-Rahim present.'},
            {'surah_number': '3', 'ayah_number': '2', 'verse_text': 'A mixture of text with al-rahman al-rahim in lower case.'},
            {'surah_number': '4', 'ayah_number': '1', 'verse_text': 'CaseSensitive Example'},
            {'surah_number': '4', 'ayah_number': '2', 'verse_text': 'casesensitive example'}
        ]
        # Scenario 1: Search for "Al-Rahman Al-Rahim" in surah 3 (case-insensitive)
        results_surah3 = search_word_group_in_surah(quran_data, "Al-Rahman Al-Rahim", 3)
        self.assertEqual(len(results_surah3), 2, "Expect 2 verses from surah 3 containing 'Al-Rahman Al-Rahim' in case-insensitive search.")
        ayah_numbers_surah3 = sorted([verse.get('ayah_number') for verse in results_surah3])
        self.assertEqual(ayah_numbers_surah3, ['1', '2'], "Expected ayah numbers ['1', '2'] for surah 3 phrase occurrence.")

        # Scenario 2: Search for "Test Phrase" in surah 2 (multiple occurrences)
        results_surah2 = search_word_group_in_surah(quran_data, "Test Phrase", 2)
        self.assertEqual(len(results_surah2), 2, "Expect 2 verses from surah 2 containing 'Test Phrase'.")
        ayah_numbers_surah2 = sorted([verse.get('ayah_number') for verse in results_surah2])
        self.assertEqual(ayah_numbers_surah2, ['2', '3'], "Expected ayah numbers ['2', '3'] for surah 2 phrase occurrence.")

        # Scenario 3: Search for a word group that does not exist in surah 1
        results_no_match = search_word_group_in_surah(quran_data, "NonexistentPhrase", 1)
        self.assertEqual(results_no_match, [], "Expect no matches for 'NonexistentPhrase' in surah 1.")

        # Scenario 4: Test case-sensitive search in surah 4
        results_surah4_cs = search_word_group_in_surah(quran_data, "CaseSensitive Example", 4, case_sensitive=True)
        self.assertEqual(len(results_surah4_cs), 1, "Expect 1 verse from surah 4 with exact case-sensitive match.")
        self.assertEqual(results_surah4_cs[0].get('ayah_number'), '1', "Expected match with ayah number '1' for case-sensitive search.")
        results_surah4_ci = search_word_group_in_surah(quran_data, "CaseSensitive Example", 4, case_sensitive=False)
        self.assertEqual(len(results_surah4_ci), 2, "Expect 2 verses from surah 4 in case-insensitive search.")

        # Scenario 5: Search in a surah number with no matching entries
        results_wrong_surah = search_word_group_in_surah(quran_data, "Test Phrase", 5)
        self.assertEqual(results_wrong_surah, [], "Expect empty list for surah 5 with no entries.")

    def test_count_word_occurrences(self):
        """
        Test the count_word_occurrences function to ensure it correctly counts the total occurrences
        of a given word in the Quran data, handling case-insensitivity.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'Allah is the Creator.'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'The mercy of ALLAH is boundless.'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'Allahu Akbar.'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'Some text without the word.'},
            {'surah_number': '2', 'ayah_number': '2', 'verse_text': 'Allah, Allah, and again Allah.'}
        ]
        expected_count = 6  # 1 + 1 + 1 + 0 + 3 = 6 occurrences of "Allah"
        actual_count = count_word_occurrences(quran_data, 'Allah')
        self.assertEqual(actual_count, expected_count, "The count of 'Allah' occurrences should be {}.".format(expected_count))
        
        # Test with different casing for the search word
        actual_count_mixed_case = count_word_occurrences(quran_data, 'aLLaH')
        self.assertEqual(actual_count_mixed_case, expected_count, "The count should be case-insensitive and match {} occurrences.".format(expected_count))

    def test_count_word_group_occurrences(self):
        """
        Test the count_word_group_occurrences function to ensure it correctly counts the total occurrences
        of a given word group (phrase) in the Quran data, handling case-insensitivity and multiple occurrences.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'Bismillah Ar-Rahman Ar-Rahim, Ar-Rahman Ar-Rahim'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'Ar-Rahman Ar-Rahim is mentioned here. Again, Ar-Rahman Ar-Rahim appears.'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'No matching phrase here.'}
        ]
        # Count occurrences of the phrase "Ar-Rahman Ar-Rahim" (case-insensitive)
        expected_count = 4  # 2 in the first verse and 2 in the second verse
        actual_count = count_word_group_occurrences(quran_data, 'Ar-Rahman Ar-Rahim')
        self.assertEqual(actual_count, expected_count, "The count of 'Ar-Rahman Ar-Rahim' occurrences should be {}.".format(expected_count))
        
        # Test with different casing for the search phrase
        actual_count_case = count_word_group_occurrences(quran_data, 'ar-rahman ar-rahim')
        self.assertEqual(actual_count_case, expected_count, "The count should be case-insensitive and match {} occurrences.".format(expected_count))
        
        # Test with an empty word group should return 0
        self.assertEqual(count_word_group_occurrences(quran_data, ''), 0, "An empty word group should return 0 occurrences.")

    def test_search_word_in_verse_range(self):
        """
        Test the search_word_in_verse_range function for various scenarios:
        
        - Searching for a word that exists within a specific verse range.
        - Searching for a word that does not exist within the range.
        - Searching with different verse ranges spanning multiple surahs and within a single surah.
        - Testing both case-sensitive and case-insensitive searches.
        - Testing edge case where start_verse and end_verse are the same.
        """
        self.maxDiff = None
        dummy_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'Alpha beta gamma'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'Alpha beta delta'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'Beta gamma'},
            {'surah_number': '2', 'ayah_number': '2', 'verse_text': 'alpha Beta gamma'},
            {'surah_number': '3', 'ayah_number': '1', 'verse_text': 'Gamma delta'},
        ]
        from src.quran_search import search_word_in_verse_range

        # Test case 1: Search for "alpha" in range (1,1) to (1,2) case-insensitive
        results = search_word_in_verse_range(dummy_data, "alpha", (1,1), (1,2))
        self.assertEqual(len(results), 2, "Should find 2 verses in surah 1 containing 'alpha' with case-insensitive search.")

        # Test case 2: Search for "beta" in range (1,2) to (2,2) case-insensitive
        results = search_word_in_verse_range(dummy_data, "beta", (1,2), (2,2))
        self.assertEqual(len(results), 3, "Should find 3 verses in the specified range containing 'beta' case-insensitively.")

        # Test case 3: Search for "gamma" in range (2,1) to (3,1) case-insensitive
        results = search_word_in_verse_range(dummy_data, "gamma", (2,1), (3,1))
        self.assertEqual(len(results), 3, "Should find 3 verses in the specified range containing 'gamma'.")

        # Test case 4: Case-sensitive search: Search for "Alpha" in range (1,1) to (2,2)
        results = search_word_in_verse_range(dummy_data, "Alpha", (1,1), (2,2), case_sensitive=True)
        self.assertEqual(len(results), 2, "Case-sensitive search for 'Alpha' should match only 2 verses.")

        # Test case 5: Edge case where start_verse and end_verse are the same.
        results = search_word_in_verse_range(dummy_data, "beta", (2,1), (2,1))
        self.assertEqual(len(results), 1, "Edge case: range with same start and end should return 1 matching verse.")

        # Test case 6: Search for a word not present in the range.
        results = search_word_in_verse_range(dummy_data, "nonexistent", (1,1), (3,1))
        self.assertEqual(results, [], "Search for a nonexistent word should return an empty list.")

if __name__ == '__main__':
    unittest.main()