let player = { x: 0, y: 0, health: 3, keys: 0, shield: 0 };
let maze = [];
let entities = [];
let level = 1;
let speedBoost = false;
let monsterTimers = [];
let gamePaused = false;
let touchStartX = 0;
let touchStartY = 0;

async function loadMaze() {
    const response = await fetch(`/maze/${level}`);
    const data = await response.json();
    maze = data.maze;
    entities = data.entities;
    player.x = 0;
    player.y = 0;
    player.health = 3;
    player.keys = 0;
    player.shield = 0;
    speedBoost = false;
    gamePaused = false;
    document.getElementById('level').textContent = `LEVEL: ${level}`;
    renderMaze();
    updateStatus();
    clearMonsterTimers();
    startMonsterMovement();
    hideOverlay();
}

function renderMaze() {
    const mazeDiv = document.getElementById('maze');
    mazeDiv.innerHTML = '';
    mazeDiv.style.setProperty('--cols', maze[0].length); //เพิ่มปรับขนาด
    mazeDiv.style.gridTemplateColumns = `repeat(${maze[0].length}, 1fr)`;
    maze.forEach((row, y) => {
        row.forEach((cell, x) => {
            let content = cell;
            if (player.x === x && player.y === y) {
                content = player.health > 0 ? '😳' : '😵';
            }
            for (const e of entities) {
                if (e.x === x && e.y === y) {
                    content = e.type;
                }
            }
            const cellDiv = document.createElement('div');
            cellDiv.textContent = content;
            mazeDiv.appendChild(cellDiv);
        });
    });
}

function move(dir) {
    if (gamePaused) return;
    let dx = 0, dy = 0;
    if (dir === 'up') dy = -1;
    if (dir === 'down') dy = 1;
    if (dir === 'left') dx = -1;
    if (dir === 'right') dx = 1;

    const moveUnits = speedBoost ? 2 : 1;

    for (let i = 0; i < moveUnits; i++) {
        const newX = player.x + dx;
        const newY = player.y + dy;
        if (maze[newY] && maze[newY][newX] && maze[newY][newX] !== '🧱') {
            player.x = newX;
            player.y = newY;
        }
        handleCollision();
    }
    renderMaze();
}

function handleCollision() {
    for (const e of entities) {
        if (e.x === player.x && e.y === player.y) {
            if (e.type === '♥️') {
                player.health = Math.min(player.health + 1, 3);
                entities = entities.filter(en => en !== e);
            }
            if (e.type === '⚡') {
                speedBoost = true;
                setTimeout(() => speedBoost = false, 3000);
                entities = entities.filter(en => en !== e);
            }
            if (e.type === '🛡️') {
                player.shield++;
                entities = entities.filter(en => en !== e);
            }
            if (e.type === '🗝️') {
                player.keys++;
                entities = entities.filter(en => en !== e);
            }
            if (e.type === '🚪') {
                if (player.keys >= 3) {
                    showOverlay("🎉 You passed the level!", true);
                } else {
                    showFlash("🔒 Need more Keys!");
                }
            }
        }
    }
    if (player.health <= 0) {
        showOverlay("😵 You lose!", false);
    }
    updateStatus();
}

function updateStatus() {
    document.getElementById('health').textContent = `♥️: ${player.health}`;
    document.getElementById('keys').textContent = `🗝️: ${player.keys}/3`;
    document.getElementById('shield').textContent = `🛡️: ${player.shield}`;
}

function restartGame() {
    level = 1;
    hideOverlay();
    loadMaze();
}

function nextLevel() {
    level++;
    hideOverlay();
    loadMaze();
}

function clearMonsterTimers() {
    for (const timer of monsterTimers) {
        clearInterval(timer);
    }
    monsterTimers = [];
}

function startMonsterMovement() {
    for (const e of entities) {
        if (['👻', '👿', '🐲'].includes(e.type)) {
            let interval = 3000;
            let speed = 1;
            if (e.type === '👿') speed = 2;
            if (e.type === '🐲') { speed = 2; interval = 2000; }

            const timer = setInterval(() => {
                if (gamePaused || player.health <= 0) return;
                for (let i = 0; i < speed; i++) {
                    if (player.x > e.x) e.x++;
                    else if (player.x < e.x) e.x--;
                    if (player.y > e.y) e.y++;
                    else if (player.y < e.y) e.y--;
                }
                if (e.x === player.x && e.y === player.y) {
                    if (player.shield > 0) {
                        player.shield--;
                        showFlash("🛡️ Shield saved you!");
                    } else {
                        const damage = e.atk || 1;
                        player.health -= damage;
                        showFlash(`💥 Took ${damage} damage!`);
                        if (player.health <= 0) {
                            showOverlay("😵 You lose!", false);
                        }
                    }
                }
                renderMaze();
                updateStatus();
            }, interval);
            monsterTimers.push(timer);
        }
    }
}

function showFlash(message = "") {
    const flash = document.getElementById('flash');
    flash.innerHTML = `<div>${message}</div>`;
    flash.style.display = 'flex';
    setTimeout(() => { flash.style.display = 'none'; }, 500);
}

function showOverlay(message, win) {
    gamePaused = true;
    clearMonsterTimers();
    const overlay = document.getElementById('overlay');
    overlay.innerHTML = `<div>${message}</div>`;
    if (win) {
        overlay.innerHTML += `<button onclick="nextLevel()">🔀 Next Level</button>`;
    } else {
        overlay.innerHTML += `<button onclick="restartGame()">🔄 Restart</button>`;
    }
    overlay.style.display = 'flex';
}

function hideOverlay() {
    document.getElementById('overlay').style.display = 'none';
}

// Keyboard Controls
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' || e.key === 'w') move('up');
    if (e.key === 'ArrowDown' || e.key === 's') move('down');
    if (e.key === 'ArrowLeft' || e.key === 'a') move('left');
    if (e.key === 'ArrowRight' || e.key === 'd') move('right');
});

// Touch Controls
document.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
});

document.addEventListener('touchend', (e) => {
    const deltaX = e.changedTouches[0].clientX - touchStartX;
    const deltaY = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
        if (deltaX > 0) move('right');
        else move('left');
    } else {
        if (deltaY > 0) move('down');
        else move('up');
    }
});

// 🔒 ป้องกันรีเฟรชหน้าจอโดยไม่ตั้งใจ (F5, Ctrl+R, swipe บนมือถือ)
document.addEventListener('keydown', function (e) {
    if ((e.key === 'F5') || (e.ctrlKey && e.key.toLowerCase() === 'r')) {
      e.preventDefault();
    }
  });
  window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    e.returnValue = '';
  });
  

// Start the game
loadMaze();
