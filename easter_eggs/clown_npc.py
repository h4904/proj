import random

def create_clown():
    if random.random() < 0.02:
        return {
            'x': random.randint(0, 9),
            'y': random.randint(0, 9),
            'type': '🤡',
            'dialogue': 'Want to see a trick?'
        }
    return None

def handle_clown():
    return random.choice(['gift', 'trap', 'teleport'])