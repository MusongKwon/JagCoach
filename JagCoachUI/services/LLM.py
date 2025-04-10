from ollama import chat
from ollama import ChatResponse


def evaluate_speech(student_results, interactive_mode=False):
    final_grade = f"You scored a {student_results['final_grade']} out of a 100!\n"

    if student_results['mood'] is None:
        student_results_str = f"""{{
            pronunciation score: {student_results['pronunciation_score']} out of 10,
            speech rate score: {student_results['speech_rate']} out of 10,
            filler word score: {student_results['filler_word_ratio']} out of 10,
            facial expression score: {student_results['emotion_ratio']} out of 10,
            eye contact score: {student_results['eye_contact_ratio']} out of 10
        }}"""
    else:
        student_results_str = f"""{{
            delivery score: {student_results['mood']} out of 10,
            pronunciation score: {student_results['pronunciation_score']} out of 10,
            speech rate score: {student_results['speech_rate']} out of 10,
            filler word score: {student_results['filler_word_ratio']} out of 10,
            facial expression score: {student_results['emotion_ratio']} out of 10,
            eye contact score: {student_results['eye_contact_ratio']} out of 10
        }}"""

    # Initialize conversation history
    messages = [
        {
            'role': 'system',
            'content': f"""We are evaluating a presentation.
            {student_results_str}
            Only give a brief feedback for each category.
            """
        },
        {
            'role': 'user',
            'content': "How did I do?"
        }
    ]

    # Get initial AI feedback
    response: ChatResponse = chat(model='llama3.2', messages=messages)
    return final_grade + response['message']['content']
