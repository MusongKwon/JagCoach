from JagCoachUI.services.JagCoachFileAnalysis import get_elements_dictionary
from JagCoachUI.services.FaceAnalysis import process_video
from ollama import chat
from ollama import ChatResponse

def evaluate_speech(mp4_file, interactive_mode=False):
    emotion_ratio,  eye_contact_ratio = process_video(mp4_file)
    student_results = get_elements_dictionary(emotion_ratio, eye_contact_ratio)
    print(student_results)
    final_grade = f"You scored a {student_results['final_grade']} out of a 100!\n"

    if student_results['mood'] is None:
        student_results_str = f"""{{
            pronunciation score: {student_results['pronunciation_score']} out of 20,
            speech rate score: {student_results['speech_rate']} out of 9,
            articulation score: {student_results['articulation_rate']} out of 14,
            pauses score: {student_results['speaking_ratio']} out of 14,
            filler word score: {student_results['filler_word_ratio']} out of 20,
            facial expression score: {student_results['emotion_ratio']} out of 6,
            eye contact score: {student_results['eye_contact_ratio']} out of 17
        }}"""
    else:
        student_results_str = f"""{{
            delivery score: {student_results['mood']} out of 10,
            pronunciation score: {student_results['pronunciation_score']} out of 18,
            speech rate score: {student_results['speech_rate']} out of 8,
            articulation score: {student_results['articulation_rate']} out of 13,
            pauses score: {student_results['speaking_ratio']} out of 13,
            filler word score: {student_results['filler_word_ratio']} out of 18,
            facial expression score: {student_results['emotion_ratio']} out of 5,
            eye contact score: {student_results['eye_contact_ratio']} out of 15
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
