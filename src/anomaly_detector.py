import logging
import statistics

def analyze_single_distribution(feature_name, distribution, context, threshold=2.0):
    '''
    Analyze a single frequency distribution for anomalies.

    For each entry in the distribution, computes the z-score and if the absolute value
    of the z-score exceeds the threshold, logs an anomaly message.

    :param feature_name: Name of the feature (e.g., "word_frequencies").
    :param distribution: Dictionary mapping feature items to their count.
    :param context: Context string specifying the Quranic level (e.g., "Quran", "Surah: 2", "Ayah: 2|3").
    :param threshold: Z-score threshold to qualify as an anomaly.
    '''
    logger = logging.getLogger("quran_analysis")
    values = list(distribution.values())
    if len(values) < 2:
        return
    mean_val = statistics.mean(values)
    stdev_val = statistics.stdev(values)
    if stdev_val == 0:
        return
    for key, count in distribution.items():
        z_score = (count - mean_val) / stdev_val
        if abs(z_score) >= threshold:
            anomaly_type = "High" if z_score > 0 else "Low"
            message = (f"Anomaly Detected: Feature '{key}' in '{feature_name}' at {context} - "
                       f"Count: {count}, Mean: {mean_val:.2f}, StdDev: {stdev_val:.2f}, "
                       f"z-score: {z_score:.2f} ({anomaly_type} anomaly).")
            logger.info(message)

def analyze_anomaly_detection(analysis_results):
    '''
    Perform anomaly detection across various Quranic feature analyses.

    This function iterates over the provided analysis results, computes statistical
    measures, and logs any features whose frequency deviates significantly from
    the expected distribution based on a z-score threshold.

    The analysis is performed on both global (Quran) level distributions as well as
    nested distributions at the Surah and Ayah levels.

    :param analysis_results: Dictionary containing various frequency analysis results.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.info("Anomaly Detection Analysis Results:")
    threshold = 2.0

    # Global frequency distributions (assumed to be at the Quran level)
    global_keys = [
        "word_frequencies", "root_word_frequencies", "character_frequencies",
        "word_ngrams", "character_ngrams", "word_cooccurrence",
        "word_collocation", "semantic_group_frequency", "semantic_group_cooccurrence",
        "first_root_word_frequency", "last_root_word_frequency"
    ]
    for key in global_keys:
        distribution = analysis_results.get(key)
        if distribution and isinstance(distribution, dict):
            analyze_single_distribution(key, distribution, "Quran", threshold)

    # Multi-level frequency distributions (Surah and Ayah levels)
    multi_level_keys = {
        "surah_word_frequencies": "Surah",
        "ayah_word_frequencies": "Ayah",
        "surah_root_word_frequencies": "Surah",
        "ayah_root_word_frequencies": "Ayah",
        "surah_word_ngrams": "Surah",
        "ayah_word_ngrams": "Ayah",
        "surah_character_ngrams": "Surah",
        "ayah_character_ngrams": "Ayah",
    }
    for key, level in multi_level_keys.items():
        multi_data = analysis_results.get(key)
        if multi_data and isinstance(multi_data, dict):
            for sub_key, distribution in multi_data.items():
                context_info = f"{level}: {sub_key}"
                if distribution and isinstance(distribution, dict):
                    analyze_single_distribution(key, distribution, context_info, threshold)

    logger.info("Anomaly Detection Analysis Completed.")