import random

def create_glitch_room():
    return {
        'type': 'glitch_room',
        'has_hidden_exit': True,
        'entities': [{'x': 5, 'y': 5, 'type': '🕳️', 'effect': 'exit'}]
    }