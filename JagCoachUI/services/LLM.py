from JagCoachUI.services.JagCoachFileAnalysis import get_elements_dictionary
from ollama import chat
from ollama import ChatResponse

def evaluate_speech(interactive_mode=False):
    
    student_results = get_elements_dictionary()
    print(student_results)
    final_grade = f"You scored a {student_results['final_grade']} out of a 100!\n"

    if student_results['mood'] is None:
        student_results_str = f"""{{
            pronunciation score: {student_results['pronunciation_score']} out of 24,
            speech rate score: {student_results['speech_rate']} out of 12,
            articulation score: {student_results['articulation_rate']} out of 20,
            pauses score: {student_results['speaking_ratio']} out of 20,
            filler word score: {student_results['filler_word_ratio']} out of 24
        }}"""
    else:
        student_results_str = f"""{{
            delivery score: {student_results['mood']} out of 16,
            pronunciation score: {student_results['pronunciation_score']} out of 20,
            speech rate score: {student_results['speech_rate']} out of 10,
            articulation score: {student_results['articulation_rate']} out of 17,
            pauses score: {student_results['speaking_ratio']} out of 17,
            filler word score: {student_results['filler_word_ratio']} out of 20
        }}"""

    # Initialize conversation history
    messages = [
        {
            'role': 'system',
            'content': f"""We are evaluating a presentation.
            {student_results_str}
            ONLY give a brief feedback for each category.
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
