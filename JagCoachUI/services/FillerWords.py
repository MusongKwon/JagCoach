import os
from JagCoachUI.config import config

def get_filler_word_ratio(transcript_path):
    dictionary_path = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "dictionary\\")
    filler_dictionary_path = os.path.join(dictionary_path, "filler_words.txt")
    #'uploads/dictionary/filler_words.txt'

    dictionary = load_dictionary(filler_dictionary_path)
    stats = check_words_in_file(transcript_path, dictionary)

    # Write results to an existing file
    with open("uploads/processed_audio/filler_word_ratio.txt", "w", encoding="utf-8") as output_file:
        # Write the formatted line with the stats aligned
        output_file.write(f"filler_word_ratio= {stats}\n")


def load_dictionary(dictionary_path):
    """Load words from a dictionary file into a set."""
    with open(dictionary_path, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)


def check_words_in_file(file_path, dictionary):
    """Check each word in a file against the dictionary."""
    total_word_count = 0
    filler_word_count = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.strip().split()
            total_word_count += len(words)
            for word in words:
                cleaned_word = word.lower().strip('.,!?()[]{}":;')  # Remove punctuation
                if cleaned_word in dictionary:
                    filler_word_count += 1

    # Avoid division by zero if file is empty
    if total_word_count == 0:
        return 0.0

    non_filler_word_ratio = (total_word_count - filler_word_count) / total_word_count

    return non_filler_word_ratio
