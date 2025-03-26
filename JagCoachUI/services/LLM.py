import json
from ollama import chat
from ollama import ChatResponse

def evaluate_speech(student_json_path, interactive_mode=False):

    # Load student results from JSON file
    with open(student_json_path, "r") as file:
        student_results = json.load(file)["student_results"]

    if student_results['mood'] == None:
        student_results_str = f"""{{
            final grade: {student_results['final_grade']} out of 100,
            pronunciation: {student_results['pronunciation_score']} out of 24,
            speech rate: {student_results['speech_rate']} out of 12,
            articulation: {student_results['articulation_rate']} out of 20,
            pauses: {student_results['speaking_ratio']} out of 20,
            filler word: {student_results['filler_word_ratio']} out of 24
        }}"""
    else:
        student_results_str = f"""{{
            final grade: {student_results['final_grade']} out of 100,
            delivery: {student_results['mood']} out of 16,
            pronunciation score: {student_results['pronunciation_score']} out of 20,
            speech rate: {student_results['speech_rate']} out of 10,
            articulation: {student_results['articulation_rate']} out of 17,
            pauses: {student_results['speaking_ratio']} out of 17,
            filler word: {student_results['filler_word_ratio']} out of 20
        }}"""

    # Initialize conversation history
    messages = [
        {
            'role': 'system',
            'content': f"""You are assisting a presenter in evaluating a recording of their presentation.
            This is the student's grades of the presentation: 
            {student_results_str}

            The final grade is the sum of the individual metrics.
            First, give the presenter the final grade of the presentation. 
            Then, give them brief feedback of each of the metrics.
            Keep in mind that for the metrics pauses and filler word, a higher score does not mean there were more pauses or filler words respectively.
            A higher score means there were fewer pauses and filler words resulting in a higher score.
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
