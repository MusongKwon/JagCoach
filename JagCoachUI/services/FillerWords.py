import os
from JagCoachUI.config import config

def get_filler_word_ratio(transcript_text):
    dictionary_path = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "dictionary")
    filler_dictionary_path = os.path.join(dictionary_path, "filler_words.txt")

    dictionary = load_dictionary(filler_dictionary_path)
    stats = check_words_in_file(transcript_text, dictionary)

    return stats

def load_dictionary(dictionary_path):
    """Load words from a dictionary file into a set."""
    with open(dictionary_path, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)


def check_words_in_file(transcription_text, dictionary):
    words = transcription_text.strip().split()
    total_word_count = len(words)
    filler_word_count = 0
    for word in words:
        cleaned_word = word.lower().strip('.,!?()[]{}":;')
        if cleaned_word in dictionary:
            filler_word_count += 1

    # Avoid division by zero if file is empty
    if total_word_count == 0:
        return 0.0

    non_filler_word_ratio = (total_word_count - filler_word_count) / total_word_count
    return non_filler_word_ratio
def check_words_in_file(transcription_text, dictionary):
    words = transcription_text.strip().split()
    total_word_count = len(words)
    filler_word_count = 0
    for word in words:
        cleaned_word = word.lower().strip('.,!?()[]{}":;')
        if cleaned_word in dictionary:
            filler_word_count += 1

    # Avoid division by zero if file is empty
    if total_word_count == 0:
        return 0.0

    non_filler_word_ratio = (total_word_count - filler_word_count) / total_word_count

    return non_filler_word_ratio
