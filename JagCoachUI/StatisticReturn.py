def get_dictionary_path(transcript_path):
    dictionary_path = 'fillerwords.txt'
    print(f"dictionary path: {dictionary_path}")

    dictionary = load_dictionary(dictionary_path)
    print(f"Dictionary loaded: {dictionary}")

    # Write results to an existing file
    with open("statistic_return.txt", "a", encoding="utf-8") as output_file:
        output_file.write(f"{transcript_path} {check_words_in_file(transcript_path, dictionary)}\n")
    print("All files processed successfully!")


def load_dictionary(dictionary_path):
    """Load words from a dictionary file into a set."""
    with open(dictionary_path, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)


def check_words_in_file(file_path, dictionary):
    """Check each word in a file against the dictionary."""
    total_word_count = 0
    filler_word_count = 0
    # (total - filler) / total words
    statistics = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.strip().split()
            total_word_count += len(words)
            for word in words:
                cleaned_word = word.lower().strip('.,!?()[]{}":;')  # Remove punctuation
                if cleaned_word in dictionary:
                    filler_word_count += 1
                    print(f"Match found: {cleaned_word}")
    non_filler_word_count = ((total_word_count - filler_word_count) / total_word_count)

    statistics.append(non_filler_word_count)
    statistics.append(filler_word_count)

    print(f"Total words in file: {total_word_count}")
    print(f"Total filler words found: {filler_word_count}")
    print(f"Non-filler words in file: {non_filler_word_count}")
    return statistics

