DIR_RIGHT = 0;
DIR_LEFT = 1;
DIR_UP = 2;
DIR_DOWN = 3;

lattice_width = 20;
lattice_height = 20;

padding = 1;

direction = DIR_DOWN;

snake = [[120, 100], [100, 100], [80, 100], [60, 100], [40, 100]];

def update() {
	i = 0;
	while (i < len(snake)) {
		x = snake[i][0] + padding;
		y = snake[i][1] + padding;
		r = rect(x, y, lattice_width - padding * 2, lattice_height - padding * 2, rgb(65, 65, 65));
		draw r;
		i += 1;
	}
}

def onTimer() {
	i = len(snake) - 1;
	while (i > 0) {
		snake[i] = snake[i - 1];
		i -= 1;
	}
	
	if (direction == DIR_RIGHT) {
		snake[0] = [snake[1][0] + lattice_width, snake[1][1]];
	}
	elif (direction == DIR_DOWN) {
		snake[0] = [snake[1][0], snake[1][1] + lattice_height];
	}
	elif (direction == DIR_LEFT) {
		snake[0] = [snake[1][0] - lattice_width, snake[1][1]];
	}
	elif (direction == DIR_UP) {
		snake[0] = [snake[1][0], snake[1][1] - lattice_height];
	}
}

def onLeft() {
	global direction;
	if (direction != DIR_RIGHT) {
		direction = DIR_LEFT;
	}
}

def onRight() {
	global direction;
	if (direction != DIR_LEFT) {
		direction = DIR_RIGHT;
	}
}

def onUp() {
	global direction;
	if (direction != DIR_DOWN) {
		direction = DIR_UP;
	}
}

def onDown() {
	global direction;
	if (direction != DIR_UP) {
		direction = DIR_DOWN;
	}
}

setKeyMap({
	"VK_LEFT" : onLeft,
	"VK_RIGHT" : onRight,
	"VK_UP" : onUp,
	"VK_DOWN" : onDown,
});

setFrameCount(50);
addTimer(50, onTimer, True);
setUpdate(update);