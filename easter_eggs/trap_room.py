import random
import string

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def trap_room_triggered():
    return random.random() < 0.03

def create_hint(password):
    hint_indices = sorted(random.sample(range(6), 5))
    return [(i, password[i]) for i in hint_indices]

def create_trap_room():
    password = generate_password()
    hint = create_hint(password)
    return {
        'password': password,
        'hint': hint
    }
