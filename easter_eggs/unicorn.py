import random

def spawn_unicorn(level):
    if random.random() < 0.03:
        return {
            'x': random.randint(0, 9),
            'y': random.randint(0, 9),
            'type': '🦄',
            'effect': 'rainbow',
        }
    return None

def handle_unicorn(player):
    player['shield'] += 2
    player['health'] = min(player['health'] + 2, 3)