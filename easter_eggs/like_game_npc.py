import random

def create_like_game_npc():
    if random.random() < 0.02:
        return {
            'x': random.randint(0, 9),
            'y': random.randint(0, 9),
            'type': '🤖',
            'dialogue': 'Do you like this game?',
            'options': ['Yes', 'No', 'Maybe'],
            'effects': {
                'Yes': 'skip',
                'No': 'teleport_void',
                'Maybe': 'neutral'
            }
        }
    return None