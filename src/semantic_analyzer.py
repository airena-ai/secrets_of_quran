''' 
Module for semantic analysis functionalities.
This module encapsulates functions to perform various semantic analyses, including
semantic group co-occurrence analysis at the Ayah level.
'''

import logging
from itertools import combinations

def analyze_semantic_group_cooccurrence_ayah(quran_data):
    '''
    Analyze the co-occurrence of semantic groups within each Ayah.

    For each ayah in quran_data, retrieves the list of semantic groups and generates all unique
    alphabetical pairs of semantic groups present in that ayah (excluding self-pairs), then counts
    the co-occurrence frequency of each pair across all ayahs.

    Logs:
        - Top 10 most frequent semantic group co-occurrence pairs.
        - Total number of unique semantic group co-occurrence pairs found.

    :param quran_data: List of dictionaries representing Quran data. Each dictionary should have a 
                       'semantic_groups' key with a list of semantic group strings for that ayah.
    :return: Dictionary where keys are tuples (groupA, groupB) and values are their co-occurrence counts.
    '''
    logger = logging.getLogger("quran_analysis")
    cooccurrence_counts = {}

    for ayah in quran_data:
        groups = ayah.get("semantic_groups", [])
        unique_groups = sorted(set(groups))
        if len(unique_groups) < 2:
            continue
        for pair in combinations(unique_groups, 2):
            cooccurrence_counts[pair] = cooccurrence_counts.get(pair, 0) + 1

    sorted_pairs = sorted(cooccurrence_counts.items(), key=lambda item: item[1], reverse=True)
    top_10 = sorted_pairs[:10]
    logger.info("Top 10 semantic group co-occurrence pairs: %s", top_10)
    logger.info("Total unique semantic group co-occurrence pairs found: %d", len(cooccurrence_counts))
    
    return cooccurrence_counts