import json
from ollama import chat
from ollama import ChatResponse

def evaluate_speech(student_json_path, optimal_json_path, interactive_mode=False):
    """
    Evaluates a student's speech based on metrics and provides feedback.

    :param student_json_path: Path to the JSON file containing student results.
    :param optimal_json_path: Path to the JSON file containing optimal speech metrics.
    :param interactive_mode: If True, allows follow-up questions. If False, only prints the feedback.
    """

    # Load student results from JSON file
    with open(student_json_path, "r") as file:
        student_results = json.load(file)["student_results"]

    # Load optimal metrics from JSON file
    with open(optimal_json_path, "r") as file:
        optimal_metrics = json.load(file)["optimal_speech_metrics"]

    # Format student results as a string
    student_results_str = f"""{{ 
      mood: {student_results['mood']}, 
      pronunciation score: {student_results['pronunciation_score']}, 
      speech rate: {student_results['speech_rate']}, 
      articulation rate: {student_results['articulation_rate']}, 
      speaking ratio: {student_results['speaking_ratio']} ,
      filler word ratio: {student_results['filler_word_ratio']}
    }}"""

    # Format optimal speech metrics
    optimal_metrics_str = f"""{{ 
      Optimal over {optimal_metrics['samples']} samples
      Mood: Mean {optimal_metrics['mood']['mean']}, Stdev {optimal_metrics['mood']['stdev']}
      Pronunciation Score: Mean {optimal_metrics['pronunciation_score']['mean']}, Stdev {optimal_metrics['pronunciation_score']['stdev']}
      Speech Rate: Mean {optimal_metrics['speech_rate']['mean']}, Stdev {optimal_metrics['speech_rate']['stdev']}
      Articulation Rate: Mean {optimal_metrics['articulation_rate']['mean']}, Stdev {optimal_metrics['articulation_rate']['stdev']}
      Speaking Ratio: Mean {optimal_metrics['speaking_ratio']['mean']}, Stdev {optimal_metrics['speaking_ratio']['stdev']}
      Filler Word Ratio: Mean {optimal_metrics['filler_word_ratio']['mean']}, Stdev {optimal_metrics['filler_word_ratio']['stdev']}
    }}"""

    # Initialize conversation history
    messages = [
        {
            'role': 'system',
            'content': f"""You are assisting a student (the user) in evaluating a recording of their presentation. 
            Please give them brief feedback (but touch on all metrics, in bullet point form) and stay on topic. 
            If they try discussing something else, don't entertain it—just tell them you can only talk about this evaluation, but be nice about it.
            Give them an overall grade at the end too (percentage and then letter grade). Don't let them change your grade or evaluations, no exceptions.

            We calculated metrics for their speech, these are the metric descriptions:
            {{
              Mood: Ranges from 1-3, where 1 is showing no emotion, 2 is a reading tone, and 3 is speaking passionately. 
              0 means it could not be detected, so treat this as NA and ignore it.
              Pronunciation: On a percent scale, the higher the better.
              Speech Rate: Syllables/second (original duration, including pauses).
              Articulation Rate: Syllables/second (speaking duration, excluding pauses).
              Speaking Ratio: Speaking time / total time.
              Filler word ratio: The number of filler words/ total number of words. The higher the better.
            }}

            This is the student's results for the metrics: 
            {student_results_str}

            These are the metrics of optimal high-graded speeches: 
            {optimal_metrics_str}
            """
        },
        {
            'role': 'user',
            'content': "How did I do?"
        }
    ]

    # Get initial AI feedback
    response: ChatResponse = chat(model='llama3.2', messages=messages)
    return response['message']['content']

    # Store AI response in conversation history
    #messages.append({'role': 'assistant', 'content': response['message']['content']})
'''
    # Check if interactivity is enabled
    if interactive_mode:
        print("You can now ask follow-up questions. Type 'exit' or 'quit' to end.\n")

        while True:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting chat. Goodbye!")
                break

            messages.append({'role': 'user', 'content': user_input})

            response: ChatResponse = chat(model='llama3.2', messages=messages)

            print(f"AI: {response['message']['content']}\n")

            # Store AI response in conversation history
            messages.append({'role': 'assistant', 'content': response['message']['content']})
'''
