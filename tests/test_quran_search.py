import unittest
from src.quran_data_loader import load_quran_text, load_quran_data
from src.quran_search import (
    search_word_in_quran, 
    search_word_group, 
    search_word_in_surah,
    search_word_group_in_surah,
    count_word_occurrences,
    count_word_group_occurrences,
    count_word_occurrences_in_surah,
    search_word_in_verse_range,
    search_word_group_in_verse_range,
    search_verses_by_word_count
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

    def test_count_word_occurrences_in_surah(self):
        """
        Test the count_word_occurrences_in_surah function by ensuring it correctly counts occurrences of a word
        within a specific Surah, in a case-insensitive manner.
        """
        self.maxDiff = None
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'Allah is the Creator.'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'Praise be to ALLAH.'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'This verse does not have the word.'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'Allah appears in surah 2.'},
            {'surah_number': '2', 'ayah_number': '2', 'verse_text': 'Multiple ALLAH ALLAH occurrences here.'},
        ]
        from src.quran_search import count_word_occurrences_in_surah
        count_surah1 = count_word_occurrences_in_surah(quran_data, 'Allah', 1)
        self.assertEqual(count_surah1, 2, "Expected 2 occurrences of 'Allah' in Surah 1.")

        count_surah2 = count_word_occurrences_in_surah(quran_data, 'AllAh', 2)
        self.assertEqual(count_surah2, 3, "Expected 3 occurrences of 'Allah' in Surah 2 (case-insensitive).")

        count_nonexistent = count_word_occurrences_in_surah(quran_data, 'Nonexistent', 1)
        self.assertEqual(count_nonexistent, 0, "Expected 0 occurrences for a word that is not present in Surah 1.")

        count_empty = count_word_occurrences_in_surah(quran_data, '', 1)
        self.assertEqual(count_empty, 0, "Expected 0 occurrences when searching for an empty word.")

    def test_count_word_group_occurrences_in_surah(self):
        """
        Test the count_word_group_occurrences_in_surah function by ensuring it correctly counts occurrences of a word group
        within a specific Surah, using case-insensitive matching.
        """
        self.maxDiff = None
        from src.quran_search import count_word_group_occurrences_in_surah
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'Bismillah Ar-Rahman Ar-Rahim, Ar-Rahman Ar-Rahim'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'Ar-Rahman Ar-Rahim is mentioned here. Again, Ar-Rahman Ar-Rahim appears.'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'No matching phrase here.'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'Ar-Rahman Ar-Rahim in surah 2.'}
        ]
        expected_count = 4  # 2 occurrences in verse 1 and 2 in verse 2 for Surah 1
        actual_count = count_word_group_occurrences_in_surah(quran_data, 'Ar-Rahman Ar-Rahim', 1)
        self.assertEqual(actual_count, expected_count, "Expected {} occurrences of the phrase in Surah 1.".format(expected_count))
        
        # Test with different casing for the phrase
        actual_count_case = count_word_group_occurrences_in_surah(quran_data, 'aR-RAhman ar-Rahim', 1)
        self.assertEqual(actual_count_case, expected_count, "Case-insensitive search should yield {} occurrences.".format(expected_count))
        
        # Test with empty word group
        self.assertEqual(count_word_group_occurrences_in_surah(quran_data, '', 1), 0, "Empty word group should return 0 occurrences.")
        
        # Test for a Surah with no matching entries
        self.assertEqual(count_word_group_occurrences_in_surah(quran_data, 'Ar-Rahman Ar-Rahim', 3), 0, "No occurrences should be found for non-existent surah.")

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

    def test_search_word_group_in_verse_range(self):
        """
        Test the search_word_group_in_verse_range function for various scenarios:
        
        - Searching for an existing word group within a specific verse range.
        - Searching using case-insensitive mode.
        - Searching using case-sensitive mode.
        - Searching across surah boundaries.
        - Edge case where start_verse and end_verse are the same.
        - Searching for a non-existent word group.
        """
        self.maxDiff = None
        dummy_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'In the beginning bismillah and creation.'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'Bismillah is repeated in many verses.'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'In verse three bismillah God bless.'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'A different verse with no match.'},
            {'surah_number': '2', 'ayah_number': '2', 'verse_text': 'Ending verse with bismillah again.'},
            {'surah_number': '3', 'ayah_number': '1', 'verse_text': 'Verse in surah 3 but no match.'},
        ]

        # Case-insensitive search in range (1,1) to (1,3)
        results1 = search_word_group_in_verse_range(dummy_data, "bismillah", (1, 1), (1, 3))
        self.assertEqual(len(results1), 3, "Should find 3 verses in surah 1 with 'bismillah' in case-insensitive search.")

        # Case-sensitive search in the same range
        results2 = search_word_group_in_verse_range(dummy_data, "Bismillah", (1, 1), (1, 3), case_sensitive=True)
        self.assertEqual(len(results2), 1, "Case-sensitive search should find only 1 verse with exact 'Bismillah'.")
        self.assertEqual(results2[0]['ayah_number'], '2', "Expected verse with ayah number '2' for case-sensitive match.")

        # Search across surah boundaries: range (1,2) to (2,2) should include verses from surah 1 and 2.
        results3 = search_word_group_in_verse_range(dummy_data, "bismillah", (1, 2), (2, 2))
        self.assertEqual(len(results3), 3, "Should find 3 verses in range (1,2) to (2,2) containing 'bismillah'.")
        expected_ayahs = ['2', '3', '2']
        actual_ayahs = [res['ayah_number'] for res in results3]
        self.assertEqual(actual_ayahs, expected_ayahs, "Ayah numbers should be {} but got {}.".format(expected_ayahs, actual_ayahs))

        # Search for a non-existent word group
        results4 = search_word_group_in_verse_range(dummy_data, "nonexistent", (1, 1), (3, 1))
        self.assertEqual(results4, [], "Search for a non-existent word group should return an empty list.")

        # Edge case: When start_verse and end_verse are the same.
        results5 = search_word_group_in_verse_range(dummy_data, "bismillah", (2, 2), (2, 2))
        self.assertEqual(len(results5), 1, "Edge case: range with the same start and end should return 1 matching verse.")
        self.assertEqual(results5[0]['surah_number'], '2', "Expected surah number '2' for the matching verse.")
        self.assertEqual(results5[0]['ayah_number'], '2', "Expected ayah number '2' for the matching verse.")

    def test_search_verses_by_word_count(self):
        """
        Test that the search_verses_by_word_count function returns only verses with the exact specified word count.

        This test creates a temporary dummy Quran data file with controlled verses and verifies that 
        only verses with exactly 19 words are returned.
        """
        self.maxDiff = None
        import tempfile
        import os
        # Prepare dummy data lines in the expected file format: surah_number|ayah_number|verse_text
        dummy_lines = [
            "1|1|This verse has five words",
            "1|2|" + " ".join(["alpha{}".format(i) for i in range(1, 20)]),
            "2|1|Only seven words are here indeed",
            "2|2|" + " ".join(["beta{}".format(i) for i in range(1, 20)])
        ]
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as tmp_file:
            tmp_file.write("\n".join(dummy_lines))
            tmp_file_path = tmp_file.name

        try:
            quran_data = load_quran_data(tmp_file_path)
            results = search_verses_by_word_count(quran_data, 19)
            expected = [
                {'surah_number': '1', 'ayah_number': '2', 'verse_text': " ".join(["alpha{}".format(i) for i in range(1, 20)])},
                {'surah_number': '2', 'ayah_number': '2', 'verse_text': " ".join(["beta{}".format(i) for i in range(1, 20)])}
            ]
            self.assertEqual(results, expected, "The verses with exactly 19 words should be returned.")
        finally:
            os.remove(tmp_file_path)

    def test_search_verses_by_word_count_multiple(self):
        """
        Test that the search_verses_by_word_count_multiple function returns only verses with word counts 
        that are multiples of the specified number.

        This test includes:
        - A positive test case using a dummy dataset where some verses have word counts that are multiples of the given number.
        - A negative test case where a multiple_of value yields no matching verses.
        - Verification that a ValueError is raised when multiple_of is zero.
        """
        self.maxDiff = None
        dummy_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'word1 word2'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'word1 word2 word3'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'word1 word2 word3 word4'},
            {'surah_number': '1', 'ayah_number': '4', 'verse_text': 'word1'},
            {'surah_number': '1', 'ayah_number': '5', 'verse_text': 'word1 word2 word3 word4 word5 word6'}
        ]
        from src.quran_search import search_verses_by_word_count_multiple
        # Positive test: multiple_of = 2 should select verses with 2, 4, and 6 words.
        results_multiple_2 = search_verses_by_word_count_multiple(dummy_data, 2)
        for verse in results_multiple_2:
            word_count = len(verse['verse_text'].split())
            self.assertEqual(word_count % 2, 0, "Verse word count should be a multiple of 2.")
        self.assertEqual(len(results_multiple_2), 3, "Should return 3 verses with word count multiple of 2.")
        
        # Negative test: multiple_of = 5 should return an empty list as no verse has a word count that is a multiple of 5.
        results_multiple_5 = search_verses_by_word_count_multiple(dummy_data, 5)
        self.assertEqual(results_multiple_5, [], "Should return an empty list when no verse word count is a multiple of 5.")
        
        # Test that a ValueError is raised for multiple_of = 0.
        with self.assertRaises(ValueError):
            search_verses_by_word_count_multiple(dummy_data, 0)

    def test_calculate_gematrical_value(self):
        """
        Test the calculate_gematrical_value function with various scenarios,
        including an empty string, known Arabic words/phrases, and non-mapping characters.
        """
        self.maxDiff = None
        from src.quran_search import calculate_gematrical_value

        # Test with an empty string.
        self.assertEqual(calculate_gematrical_value(""), 0, "Empty string should return a gematrical value of 0.")

        # Test with a known simple Arabic word: "ابجد"
        # Mapping: ا=1, ب=2, ج=3, د=4. Sum=10.
        self.assertEqual(calculate_gematrical_value("ابجد"), 10, "Gematrical value of 'ابجد' should be 10.")

        # Test with the word "الله"
        # Calculation: ا=1, ل=30, ل=30, ه=5. Sum=66.
        self.assertEqual(calculate_gematrical_value("الله"), 66, "Gematrical value of 'الله' should be 66.")

        # Test with the phrase "بسم الله الرحمن الرحيم"
        # Expected calculation: بسم = 102, الله = 66,
        # الرحمن = 329, الرحيم = 289, Total = 786.
        self.assertEqual(calculate_gematrical_value("بسم الله الرحمن الرحيم"), 786, "Gematrical value of 'بسم الله الرحمن الرحيم' should be 786.")

        # Test with non-Arabic characters; they should be ignored.
        self.assertEqual(calculate_gematrical_value("123"), 0, "Non-mapped characters should contribute 0 to the gematrical value.")

    def test_search_words_by_gematrical_value(self):
        """
        Test the search_words_by_gematrical_value function with various scenarios,
        ensuring that words are correctly identified based on their gematrical value.

        Scenarios tested:
        - Target gematrical value of 66 for the word 'الله'.
        - Target gematrical value of 10 for the word 'ابجد'.
        - Target gematrical value of 0 for words with no mapped values (e.g., 'test').
        - Target gematrical value of 571 for the word 'مثال'.
        """
        self.maxDiff = None
        from src.quran_search import search_words_by_gematrical_value
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'الله ابجد test'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'مثال الله'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'ابجد ابجد'}
        ]
        # Test for gematrical value 66 ("الله")
        results_66 = search_words_by_gematrical_value(quran_data, 66)
        expected_66 = [
            {'word': 'الله', 'surah_number': '1', 'ayah_number': '1'},
            {'word': 'الله', 'surah_number': '1', 'ayah_number': '2'}
        ]
        self.assertEqual(results_66, expected_66, "Should return words with gematrical value 66 (for 'الله').")

        # Test for gematrical value 10 ("ابجد")
        results_10 = search_words_by_gematrical_value(quran_data, 10)
        expected_10 = [
            {'word': 'ابجد', 'surah_number': '1', 'ayah_number': '1'},
            {'word': 'ابجد', 'surah_number': '2', 'ayah_number': '1'},
            {'word': 'ابجد', 'surah_number': '2', 'ayah_number': '1'}
        ]
        self.assertEqual(results_10, expected_10, "Should return words with gematrical value 10 (for 'ابجد') occurring three times.")

        # Test for gematrical value 0 ("test")
        results_0 = search_words_by_gematrical_value(quran_data, 0)
        expected_0 = [
            {'word': 'test', 'surah_number': '1', 'ayah_number': '1'}
        ]
        self.assertEqual(results_0, expected_0, "Should return words with gematrical value 0 (for 'test').")

        # Test for gematrical value 571 ("مثال")
        results_571 = search_words_by_gematrical_value(quran_data, 571)
        expected_571 = [
            {'word': 'مثال', 'surah_number': '1', 'ayah_number': '2'}
        ]
        self.assertEqual(results_571, expected_571, "Should return words with gematrical value 571 (for 'مثال').")

    def test_search_word_groups_by_gematrical_value(self):
        """
        Test the search_word_groups_by_gematrical_value function with various scenarios,
        ensuring that it returns verses where the specified word group is found and its gematrical value matches the target.
        
        Scenarios:
        - When the word group gem value matches the target and occurs in verses.
        - When the target gem value does not match, should return an empty result.
        - When the word group does not occur in any verse, should return an empty list.
        """
        self.maxDiff = None
        from src.quran_search import search_word_groups_by_gematrical_value, calculate_gematrical_value
        dummy_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'The opening has الرحمن الرحيم as a sign.'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'This verse does not include the phrase.'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'In this verse, we again see الرحمن الرحيم in full.'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'No matching phrase here.'}
        ]
        phrase = "الرحمن الرحيم"
        target_value = 618  # Gematrical value for "الرحمن الرحيم"
        results = search_word_groups_by_gematrical_value(dummy_data, phrase, target_value)
        expected = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'The opening has الرحمن الرحيم as a sign.'},
            {'surah_number': '1', 'ayah_number': '3', 'verse_text': 'In this verse, we again see الرحمن الرحيم in full.'}
        ]
        self.assertEqual(results, expected, "Expected to find verses containing the phrase '{}' with gem value {}.".format(phrase, target_value))
        
        # Test scenario: target gem value does not match computed value; expect empty result even if phrase appears.
        wrong_target = 600
        results_wrong = search_word_groups_by_gematrical_value(dummy_data, phrase, wrong_target)
        self.assertEqual(results_wrong, [], "Expected empty result when target gem value {} does not match computed value for '{}'.".format(wrong_target, phrase))
        
        # Test scenario: phrase that does not appear in any verse.
        absent_phrase = "غير موجود"
        absent_computed = calculate_gematrical_value(absent_phrase)
        results_absent = search_word_groups_by_gematrical_value(dummy_data, absent_phrase, absent_computed)
        self.assertEqual(results_absent, [], "Expected empty result for phrase '{}' that is not present in any verse.".format(absent_phrase))

    def test_calculate_surah_gematrical_value(self):
        """
        Test the calculate_surah_gematrical_value function by using a dummy Quran data set.
        This test includes verses from different Surahs, ensuring that only verses from the specified Surah contribute
        to the calculated gematrical value.
        """
        self.maxDiff = None
        from src.quran_search import calculate_surah_gematrical_value
        quran_data = [
            {'surah_number': '1', 'ayah_number': '1', 'verse_text': 'بسم الله الرحمن الرحيم'},
            {'surah_number': '1', 'ayah_number': '2', 'verse_text': 'الله'},
            {'surah_number': '2', 'ayah_number': '1', 'verse_text': 'Some non-Arabic text'}
        ]
        # Expected for Surah 1:
        # "بسم الله الرحمن الرحيم" splits into ["بسم", "الله", "الرحمن", "الرحيم"]
        # Gematrical values: 102 + 66 + 329 + 289 = 786, and then adding "الله" = 66, total = 852.
        expected_total = 852
        calculated_total = calculate_surah_gematrical_value(quran_data, 1)
        self.assertEqual(calculated_total, expected_total, "Calculated gematrical value for Surah 1 should be {}.".format(expected_total))
        
        # For Surah 2, the non-Arabic text should yield a gematrical value of 0.
        calculated_total_surah2 = calculate_surah_gematrical_value(quran_data, 2)
        self.assertEqual(calculated_total_surah2, 0, "Calculated gematrical value for Surah 2 should be 0 since no mapped Arabic letters.")

    def test_calculate_verse_range_gematrical_value(self):
        """
        Test the calculate_verse_range_gematrical_value function by manually summing gematrical values
        for a defined verse range.
        
        This test loads the Quran data using load_quran_data, calculates the expected cumulative gematrical
        value for verses from verse number 1 to 5 (inclusive), and asserts that the function returns the expected value.
        """
        self.maxDiff = None
        quran_file_path = 'data/quran-uthmani-min.txt'
        from src.quran_search import calculate_verse_range_gematrical_value, calculate_gematrical_value
        from src.quran_data_loader import load_quran_data
        quran_data = load_quran_data(quran_file_path)
        
        # Define test verse range: verses 1 to 5
        start_verse = 1
        end_verse = 5
        
        # Manually calculate expected gematrical value
        expected_total = 0
        for idx, verse in enumerate(quran_data, start=1):
            if start_verse <= idx <= end_verse:
                verse_text = verse.get('verse_text', '')
                expected_total += calculate_gematrical_value(verse_text)
        
        # Call the new function
        actual_total = calculate_verse_range_gematrical_value(quran_data, start_verse, end_verse)
        self.assertEqual(actual_total, expected_total, "The gematrical value for verses {} to {} should be {}.".format(start_verse, end_verse, expected_total))
    
    def test_calculate_quran_gematrical_value(self):
        """
        Test the calculate_quran_gematrical_value function by monkey-patching the calculate_gematrical_value to return
        predictable values (using the length of the input text) and using dummy Quran data.
        """
        self.maxDiff = None
        import src.quran_search as qs
        dummy_quran_data = [
            {'verse_text': "abcd ef"},
            {'verse_text': "ghij"},
            {'verse_text': "kl mn op"}
        ]
        # Expected calculation:
        # First verse: "abcd ef" -> words: "abcd" (length 4) and "ef" (length 2) => 4 + 2 = 6
        # Second verse: "ghij" -> word: "ghij" (length 4) => 4
        # Third verse: "kl mn op" -> words: "kl" (2), "mn" (2), "op" (2) => 6
        # Total expected = 6 + 4 + 6 = 16.
        expected_total = 16
        
        original_func = qs.calculate_gematrical_value
        qs.calculate_gematrical_value = lambda text: len(text)
        try:
            result = qs.calculate_quran_gematrical_value(dummy_quran_data)
            self.assertEqual(result, expected_total, "Total gematrical value for the dummy Quran data should be {}.".format(expected_total))
        finally:
            qs.calculate_gematrical_value = original_func

if __name__ == '__main__':
    unittest.main()