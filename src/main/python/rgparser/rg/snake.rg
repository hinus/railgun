DIR_RIGHT = 0;
DIR_LEFT = 1;
DIR_UP = 2;
DIR_DOWN = 3;

lattice_width = 20;
lattice_height = 20;

padding = 1;

direction = DIR_DOWN;

snake = [[120, 100], [100, 100], [80, 100], [60, 100], [40, 100]];

food = [120, 140];

def update() {
	i = 0;
	while (i < snake.length()) {
		x = snake[i][0] + padding;
		y = snake[i][1] + padding;
		r = rect(x, y, lattice_width - padding * 2, lattice_height - padding * 2, rgb(65, 65, 65));
		draw r;
		i += 1;
	}
	
	x = food[0] + padding;
	y = food[1] + padding;
	r = rect(x, y, lattice_width - padding * 2, lattice_height - padding * 2, rgb(186, 65, 65));
	draw r;
}

def touchFood(head) {
	return ((head[0] == food[0]) and (head[1] == food[1]));
}

def onTimer() {
	if (direction == DIR_RIGHT) {
		head = [snake[0][0] + lattice_width, snake[0][1]];
	}
	elif (direction == DIR_DOWN) {
		head = [snake[0][0], snake[0][1] + lattice_height];
	}
	elif (direction == DIR_LEFT) {
		head = [snake[0][0] - lattice_width, snake[0][1]];
	}
	elif (direction == DIR_UP) {
		head = [snake[0][0], snake[0][1] - lattice_height];
	}

	if (touchFood(head)) {
		snake.addFirst(head);
		generateNewFood();
		return;
	}

	i = snake.length() - 1;
	while (i > 0) {
		snake[i] = snake[i - 1];
		i -= 1;
	}
	
	snake[0] = head;
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

def generateNewFood() {
	x = random(25);
	y = random(25);
	
	while (isOnSnake(x * 20, y * 20)) {
		x = random(25);
		y = random(25);
	}
	
	global food;
	food = [x * 20, y * 20];
}

def isOnSnake(x, y) {
	i = snake.length() - 1;
	while (i >= 0) {
		if (snake[i][0] == x and snake[i][1] == y) {
			return True;
		}
		i -= 1;
	}
	
	return False;
}

def doTimer() {
	onTimer();
}

setFrameCount(50);
c = addTimer(10, doTimer, True);
setUpdate(update);