import random

def create_wizard():
    if random.random() < 0.04:
        return {
            'x': random.randint(0, 9),
            'y': random.randint(0, 9),
            'type': '🧙',
            'dialogue': 'Shall I skip this level for you?',
            'effect': 'skip_randomly'
        }
    return None

def handle_wizard(player):
    if random.random() < 0.5:
        return player['level'] + 1
    return player['level']