import random
import time

def create_time_portal(level):
    if random.random() < 0.05:
        return {
            'x': random.randint(0, 9),
            'y': random.randint(0, 9),
            'type': '🌀',
            'trigger': 'time_portal',
            'time': int(time.time())
        }
    return None

def handle_time_portal(player, entity):
    current_second = int(time.time()) % 60
    if current_second % 2 == 0:
        return max(1, player['level'] - 1)
    else:
        return player['level'] + 1