from ollama import chat
from ollama import ChatResponse
import pandas as pd

def custom_evaluate_speech(student_results, rubric, transcript, interactive_mode=False):
    rubric = pd.read_csv(rubric)
    rubric_str = rubric.to_string()

    # Initialize conversation history
    messages = [
        {
            'role': 'system',
            'content': f"""You're evaluating a student's presentation. Here's the rubric: {rubric_str} 
            presentation transcript: {transcript}
            our analysis results: {student_results}
            Briefly grade the generated transcript of the person presenting using the rubric 
            (give a number score for each criteria, per the rubric).
            Talk in the 3rd person
            If mentions visual aid, give it NA because you're not meant for analyzing that
            Dont explicitly mention the transcript or analysis results
            Dont give an overall grade 
            """
        },
        {
            'role': 'user',
            'content': "How did I do?"
        }
    ]

    # Get initial AI feedback
    response: ChatResponse = chat(model='llama3.2', messages=messages)
    print(transcript)
    return response['message']['content']
