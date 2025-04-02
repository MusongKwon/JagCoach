def get_filler_word_ratio(transcript_text):
    dictionary = {'just', 'accordingly', 'so', 'um', 'er', 'very', 'right', 'hmm', 'about', 'okay', 
                  'literally', 'ah', 'actually', 'well', 'yeah', 'like', 'absolutely', 'umm', 'basically', 'totally'}
    
    words = transcript_text.strip().split()
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
