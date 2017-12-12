global c;

def drawCircle(x, y) {
	global c;
	c = circle(x, y, random(30), rgb(86, 0, 164));
}

def dragMouse(x, y) {
	c.x = x;
	c.y = y;
}

setMouseMap({
	"LEFT_CLICK" : drawCircle,
	"DRAG" : dragMouse,
});

def update() {
	draw c;
}

setUpdate(update);