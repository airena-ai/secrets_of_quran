import logging
import statistics
from collections import Counter, defaultdict

def analyze_surah_sentence_length_distribution_by_index(data):
    '''
    Analyze sentence length distribution for each Surah index.
    For each Surah index (obtained from the "surah_number" field in each data item),
    this function collects the sentence lengths (number of words in an ayah) for all ayahs,
    computes the frequency distribution and summary statistics: average, median, mode, and standard deviation.
    Logs the results for each surah index.

    :param data: List of dictionaries representing Quran data.
    :return: Dictionary mapping each surah index (int) to a summary dictionary with keys:
             "frequency", "average", "median", "mode", "std_dev".
    '''
    logger = logging.getLogger("quran_analysis")
    surah_lengths = defaultdict(list)
    for item in data:
        try:
            surah_index = int(item.get("surah_number", 0))
        except ValueError:
            continue
        text = item.get("processed_text") or item.get("verse_text", "")
        words = text.split() if text else []
        surah_lengths[surah_index].append(len(words))
    
    results = {}
    for surah_index, lengths in surah_lengths.items():
        if not lengths:
            continue
        freq = dict(Counter(lengths))
        avg = statistics.mean(lengths)
        med = statistics.median(lengths)
        counts = Counter(lengths)
        max_count = max(counts.values())
        modes = sorted([l for l, count in counts.items() if count == max_count])
        std_dev = statistics.stdev(lengths) if len(lengths) > 1 else 0
        results[surah_index] = {
            "frequency": freq,
            "average": avg,
            "median": med,
            "mode": modes,
            "std_dev": std_dev
        }
        logger.info("Surah Index %d - Sentence Length Distribution: %s", surah_index, freq)
        logger.info("Summary Statistics - Average: %.2f, Median: %.2f, Mode: %s, Std Dev: %.2f", avg, med, modes, std_dev)
    return results

def analyze_ayah_sentence_length_distribution_by_index(data):
    '''
    Analyze sentence length distribution for each Ayah index across all Surahs.
    For each Ayah index (obtained from the "ayah" field in each data item, converted to int),
    this function collects the sentence lengths (number of words in an ayah) from all surahs,
    computes the frequency distribution and summary statistics: average, median, mode, and standard deviation.
    Logs the results for each ayah index.

    :param data: List of dictionaries representing Quran data.
    :return: Dictionary mapping each ayah index (int) to a summary dictionary with keys:
             "frequency", "average", "median", "mode", "std_dev".
    '''
    logger = logging.getLogger("quran_analysis")
    ayah_lengths = defaultdict(list)
    for item in data:
        try:
            ayah_index = int(item.get("ayah", 0))
        except ValueError:
            continue
        text = item.get("processed_text") or item.get("verse_text", "")
        words = text.split() if text else []
        ayah_lengths[ayah_index].append(len(words))
    
    results = {}
    for ayah_index, lengths in ayah_lengths.items():
        if not lengths:
            continue
        freq = dict(Counter(lengths))
        avg = statistics.mean(lengths)
        med = statistics.median(lengths)
        counts = Counter(lengths)
        max_count = max(counts.values())
        modes = sorted([l for l, count in counts.items() if count == max_count])
        std_dev = statistics.stdev(lengths) if len(lengths) > 1 else 0
        results[ayah_index] = {
            "frequency": freq,
            "average": avg,
            "median": med,
            "mode": modes,
            "std_dev": std_dev
        }
        logger.info("Ayah Index %d - Sentence Length Distribution: %s", ayah_index, freq)
        logger.info("Summary Statistics - Average: %.2f, Median: %.2f, Mode: %s, Std Dev: %.2f", avg, med, modes, std_dev)
    return results