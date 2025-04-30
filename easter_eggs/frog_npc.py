import random

def create_frog():
    if random.random() < 0.04:
        return {
            'x': random.randint(0, 9),
            'y': random.randint(0, 9),
            'type': '🐸',
            'dialogue': 'What walks on four legs in the morning, two at noon, and three in the evening?',
            'answer': 'man'
        }
    return None

def handle_frog(answer):
    if answer.strip().lower() == 'man':
        return 'wizard_room'
    else:
        return 'boss_room'