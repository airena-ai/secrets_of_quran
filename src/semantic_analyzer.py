'''
Module for semantic analysis of Quran text.
'''
import logging
from collections import Counter
from itertools import combinations

def analyze_semantic_group_cooccurrence_ayah(quran_data):
    '''
    Analyze semantic group co-occurrence within Quranic verses (Ayahs).

    For each Ayah in quran_data, iterates over the list of semantic groups (under the key 'semantic_groups'),
    computes all unique unordered pairs (combinations) of semantic groups, and counts their frequencies.

    Logs:
    - A header indicating the start of semantic group co-occurrence analysis.
    - The top 10 most frequent semantic group co-occurrence pairs with their counts.
    - The total number of unique semantic group co-occurrence pairs found.

    :param quran_data: List of dictionaries representing Quran data, each containing a 'semantic_groups' key.
    :return: Dictionary mapping each unordered pair of semantic groups (as a tuple) to its frequency count.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Semantic Group Co-occurrence Analysis at Ayah Level.")
    cooccurrence_counter = Counter()
    for ayah in quran_data:
        groups = ayah.get("semantic_groups", [])
        if groups and len(groups) > 1:
            for pair in combinations(sorted(groups), 2):
                cooccurrence_counter[pair] += 1
    top_10 = cooccurrence_counter.most_common(10)
    logger.info("Top 10 semantic group co-occurrence pairs: %s", top_10)
    logger.info("Total unique semantic group co-occurrence pairs found: %d", len(cooccurrence_counter))
    return dict(cooccurrence_counter)