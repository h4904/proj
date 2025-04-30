def create_quiz_room():
    return {
        'type': 'quiz_room',
        'question': 'What is the capital of France?',
        'answer': 'paris',
        'reward': 'key'
    }

def handle_quiz_answer(answer):
    return answer.strip().lower() == 'paris'