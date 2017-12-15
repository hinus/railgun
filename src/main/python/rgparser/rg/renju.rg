OFFSET_X = 220;
OFFSET_Y = 50;
LATTICE_WIDTH = 37;
CHESS_RADIUS = 15;

FRAME_COUNTE = 3;

EMPTY = 0;
BLACK = 1;
WHITE = 2;

board = [];
turn = BLACK;

# initialize the chess board
i = 0;
while (i < 15) {
	l = [];
	j = 0;
	while (j < 15) {
		l.addFirst(EMPTY);
		j += 1;
	}

	board.addFirst(l);
	i += 1;
}

def restart() {
	i = 0;
	while (i < 15) {
		j = 0;
		while (j < 15) {
			board[i][j] = EMPTY;
			j += 1;
		}
		i += 1;
	}
}

def update() {
	i = 0;
	while (i < 15) {
		x = OFFSET_X + i * LATTICE_WIDTH;
		draw line(x, OFFSET_Y, x, OFFSET_Y + 14 * LATTICE_WIDTH);
		i += 1;
	}
	
	i = 0;
	while (i < 15) {
		y = OFFSET_Y + i * LATTICE_WIDTH;
		draw line(OFFSET_X, y, OFFSET_X + 14 * LATTICE_WIDTH, y);
		i += 1;
	}

	i = 0;
	while (i < 15) {
		j = 0;
		while (j < 15) {
			if (board[i][j] == BLACK) {
				draw circle(OFFSET_X + LATTICE_WIDTH * j - CHESS_RADIUS, OFFSET_Y + LATTICE_WIDTH * i - CHESS_RADIUS, CHESS_RADIUS * 2, rgb(55, 55, 55));
			}
			elif (board[i][j] == WHITE) {
				draw circle(OFFSET_X + LATTICE_WIDTH * j - CHESS_RADIUS, OFFSET_Y + LATTICE_WIDTH * i - CHESS_RADIUS, CHESS_RADIUS * 2, rgb(128, 128, 255));
			}
			j += 1;
		}
		i += 1;
	}
}

def addChess(x, y) {
	global turn;
	line = (x - OFFSET_X + LATTICE_WIDTH / 2) / LATTICE_WIDTH;
	row = (y - OFFSET_Y + LATTICE_WIDTH / 2) / LATTICE_WIDTH;
	
	if (board[row][line] == EMPTY) {
		board[row][line] = turn;
		turn = 3 - turn;
	}
}

setMouseMap({
	"LEFT_CLICK" : addChess,
});

setKeyMap({
	"VK_SPACE" : restart,
});

setFrameCount(FRAME_COUNTE);
setUpdate(update);