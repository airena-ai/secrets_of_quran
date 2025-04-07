import logging
from src.tokenizer import tokenize_text

def analyze_word_cooccurrence(quran_data):
    '''
    Analyze word co-occurrence within each ayah of the Quran data.
    
    Each ayah's processed text is tokenized into words, and all unique word pairs 
    that co-occur within the same ayah are counted. Word pairs are stored in alphabetical 
    order to ensure consistency.
    
    :param quran_data: List of dictionaries. Each dictionary should contain 'surah', 'ayah',
                       and either 'processed_text' (preferred) or 'verse_text'.
    :return: Dictionary with keys as tuples (word1, word2) and values as co-occurrence counts.
    '''
    logger = logging.getLogger("quran_analysis")
    pair_counts = {}
    
    for item in quran_data:
        # Use 'processed_text' if available; otherwise fall back to 'verse_text'
        text = item.get("processed_text") or item.get("verse_text", "")
        tokens = text.split() if text else []
        if len(tokens) < 2:
            continue
        for i in range(len(tokens) - 1):
            for j in range(i + 1, len(tokens)):
                pair = tuple(sorted((tokens[i], tokens[j])))
                if pair in pair_counts:
                    pair_counts[pair] += 1
                else:
                    pair_counts[pair] = 1
                    
    sorted_pairs = sorted(pair_counts.items(), key=lambda item: item[1], reverse=True)
    top_10000 = sorted_pairs[:10000]
    logger.info("Word Co-occurrence Analysis Results - TOP 10000 Pairs:")
    for pair, count in top_10000:
        logger.info("Pair: %s, Count: %d", str(pair), count)
    logger.info("Total unique word pairs: %d", len(pair_counts))
    return pair_counts

def analyze_root_word_cooccurrence(quran_data, top_n_pairs=10000):
    '''
    Analyze the co-occurrence of root words within each Ayah of the Quran data.
    
    This function iterates over each Ayah, extracts the list of root words from the 'roots' key,
    and generates all unique pairs of roots (avoiding pairing a root with itself and ensuring
    that (root1, root2) is treated the same as (root2, root1)). It counts the occurrences of 
    each unique root word pair across all Ayahs.
    
    The function logs the analysis results including:
    - A header indicating the start of root word co-occurrence analysis.
    - The total number of unique root word pairs.
    - The top N most frequent root word pairs along with their counts.
    - A footer indicating the end of the analysis.
    
    :param quran_data: List of dictionaries. Each dictionary represents an Ayah and should contain
                       a 'roots' key with a list of root words.
    :param top_n_pairs: Integer specifying the number of top frequent pairs to log (default is 10000).
    '''
    from collections import Counter
    logger = logging.getLogger("quran_analysis")
    root_pair_counts = Counter()
    for ayah_data in quran_data:
        roots = ayah_data.get('roots', [])
        if len(roots) > 1:
            for i in range(len(roots)):
                for j in range(i + 1, len(roots)):
                    pair = tuple(sorted((roots[i], roots[j])))
                    root_pair_counts[pair] += 1

    logger.info("\n--- Root Word Co-occurrence Analysis ---")
    logger.info("Total unique root word pairs: %d", len(root_pair_counts))
    logger.info("Top %d most frequent root word pairs:", top_n_pairs)
    for pair, count in root_pair_counts.most_common(top_n_pairs):
        logger.info("  Root Pair: %s, Count: %d", str(pair), count)
    logger.info("--- End Root Word Co-occurrence Analysis ---\n")

def analyze_lemma_word_cooccurrence(quran_data, top_n_pairs=10000):
    '''
    Analyze the co-occurrence of lemma words within each Ayah of the Quran data.
    
    This function iterates over each Ayah, extracts the list of lemma words from the 'lemmas' key,
    and generates all unique pairs of lemmas (avoiding pairing a lemma with itself and ensuring
    that (lemma1, lemma2) is treated the same as (lemma2, lemma1)). It counts the occurrences of 
    each unique lemma word pair across all Ayahs.
    
    The function logs the analysis results including:
    - A header indicating the start of lemma word co-occurrence analysis.
    - The total number of unique lemma word pairs.
    - The top N most frequent lemma word pairs along with their counts.
    - A footer indicating the end of the analysis.
    
    :param quran_data: List of dictionaries. Each dictionary represents an Ayah and should contain
                       a 'lemmas' key with a list of lemma words.
    :param top_n_pairs: Integer specifying the number of top frequent pairs to log (default is 10000).
    '''
    from collections import Counter
    logger = logging.getLogger("quran_analysis")
    lemma_pair_counts = Counter()
    for ayah_data in quran_data:
        lemmas = ayah_data.get('lemmas', [])
        if len(lemmas) > 1:
            for i in range(len(lemmas)):
                for j in range(i + 1, len(lemmas)):
                    pair = tuple(sorted((lemmas[i], lemmas[j])))
                    lemma_pair_counts[pair] += 1

    logger.info("\n--- Lemma Word Co-occurrence Analysis ---")
    logger.info("Total unique lemma word pairs: %d", len(lemma_pair_counts))
    logger.info("Top %d most frequent lemma word pairs:", top_n_pairs)
    for pair, count in lemma_pair_counts.most_common(top_n_pairs):
        logger.info("  Lemma Pair: %s, Count: %d", str(pair), count)
    logger.info("--- End Lemma Word Co-occurrence Analysis ---\n")    