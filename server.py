from flask import Flask, render_template, jsonify, request, abort
import random
from collections import deque
import os
import time

# Easter Egg Modules
#from easter_eggs.unicorn import spawn_unicorn, handle_unicorn
#from easter_eggs.trap_room import generate_password, trap_room_triggered, create_hint, create_trap_room
#from easter_eggs.wizard_npc import create_wizard, handle_wizard
#from easter_eggs.frog_npc import create_frog, handle_frog
#from easter_eggs.glitch_room import create_glitch_room
#from easter_eggs.quiz_room import create_quiz_room, handle_quiz_answer
#from easter_eggs.clown_npc import create_clown, handle_clown
#from easter_eggs.like_game_npc import create_like_game_npc

LOG_RETENTION_DAYS = 1

app = Flask(__name__)

ALLOWED_METHODS = ['GET', 'POST']
BAD_USER_AGENTS = ['curl', 'wget', 'python-requests', 'httpie']

if not os.path.exists('logs'):
    os.makedirs('logs')

def log_player_action(ip, path):
    log_file = 'logs/player_logs.txt'
    temp_file = 'logs/temp_logs.txt'
    now = time.time()
    retention_seconds = LOG_RETENTION_DAYS * 24 * 60 * 60

    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f_in, open(temp_file, 'w', encoding='utf-8') as f_out:
            for line in f_in:
                try:
                    timestamp_str = line.split(' - ')[0]
                    log_time = time.mktime(time.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S'))
                    if now - log_time <= retention_seconds:
                        f_out.write(line)
                except Exception:
                    continue
        os.replace(temp_file, log_file)

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - IP: {ip} - Path: {path}\n")

@app.before_request
def security_checks():
    if request.method not in ALLOWED_METHODS:
        abort(405, description="Method Not Allowed")

    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

    ua = (request.headers.get('User-Agent') or "").lower()
    if any(bad_ua in ua for bad_ua in BAD_USER_AGENTS):
        abort(403, description="Forbidden")

    if 'Host' not in request.headers:
        abort(400, description="Bad Request - Missing Host")

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    path = request.path
    log_player_action(ip, path)

# ------------------------------
# ระบบ Maze + Entity
# ------------------------------

def generate_maze(size):
    maze = [['⬜' for _ in range(size)] for _ in range(size)]
    wall_count = int(size * size * 0.25)
    while wall_count > 0:
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        if maze[y][x] == '⬜':
            maze[y][x] = '🧱'
            wall_count -= 1
    return maze

def is_reachable(maze, start, targets):
    size = len(maze)
    queue = deque([start])
    visited = set()
    visited.add(start)
    found = set()

    while queue:
        x, y = queue.popleft()
        if (x, y) in targets:
            found.add((x, y))
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[ny][nx] != '🧱' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return found == targets

#def maybe_add_one_easter_egg(maze, entities, used_positions, level):#easer egg
    options = [
        ('trap_room', create_trap_room, 0.04),
        ('portal', handle_time_portal, 0.03),
        ('unicorn', handle_unicorn, 0.02),
        ('glitch', create_glitch_room, 0.03),
        ('wizard', handle_wizard, 0.03),
        ('frog', handle_frog, 0.05),
        ('quiz', create_quiz_room, 0.04),
        ('clown', handle_clown, 0.08),
        ('like_npc', create_like_game_npc, 0.04),
    ]

    random.shuffle(options)
    for name, func, chance in options:
        #if name == "wizard":#ทดสอบ easter egg
        if random.random() < chance:#แบบสุ่ม
            maze[:] = [['⬜' for _ in row] for row in maze]  # clear all walls
            entities[:] = []  # remove all existing entities
            used_positions.clear()
            if name in ['portal', 'wizard', 'frog']:
                func(maze, entities, used_positions, level)
            elif name == 'trap_room':
                func(maze, entities, used_positions, level)
            else:
                func(maze, entities, used_positions)
            break


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/maze/<int:level>')
def maze(level):
    FINAL_LEVEL = 30

    if level > FINAL_LEVEL:
        return jsonify({'win': True})

    size = min(8 + (level - 1), 12)
    while True:
        maze = generate_maze(size)
        entities = []
        used_positions = set()

        normal_monsters = minibosses = bosses = 0

        if level in [10, 20]: bosses = 1
        elif level == 30: bosses = 3
        elif 1 <= level <= 5: normal_monsters = 1
        elif 6 <= level <= 9: normal_monsters = 2
        elif 11 <= level <= 15: normal_monsters = 3
        elif 16 <= level <= 19: normal_monsters = 4
        elif 21 <= level <= 28: normal_monsters = 5

        if level in [3, 6, 9]: minibosses = 1; normal_monsters = max(0, normal_monsters - 1)
        elif level in [13, 16, 19]: minibosses = 2; normal_monsters = max(0, normal_monsters - 2)
        elif level in [23, 26]: minibosses = 2; normal_monsters = max(0, normal_monsters - 1)
        elif level == 29: minibosses = 3; normal_monsters = 0

        def place_entity(symbol, amount):
            nonlocal used_positions
            empty_cells = [(x, y) for y in range(size) for x in range(size) if maze[y][x] == '⬜' and (x, y) not in used_positions]
            for _ in range(amount):
                if not empty_cells: break
                x, y = random.choice(empty_cells)
                used_positions.add((x, y))
                entities.append({'type': symbol, 'x': x, 'y': y})
                empty_cells.remove((x, y))

        place_entity('👻', normal_monsters)
        place_entity('👿', minibosses)
        place_entity('🐲', bosses)

        for item in ['♥️', '♥️', '⚡', '⚡', '🛡️', '🛡️', '🗝️', '🗝️', '🗝️']:
            place_entity(item, 1)

        place_entity('🚪', 1)

        important_targets = set((e['x'], e['y']) for e in entities)
        important_targets.add((0, 0))

        if is_reachable(maze, (0, 0), important_targets):
            break

    #maybe_add_one_easter_egg(maze, entities, used_positions, level)

    return jsonify({'maze': maze, 'entities': entities, 'level': level})

import os
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
