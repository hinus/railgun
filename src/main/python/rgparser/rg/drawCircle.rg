c = circle(100, 100, 50, rgb(0, 86, 163));
c1 = circle(200, 200, 50, rgb(78, 78, 78));

l = [c, c1];

speedX = 2;
speedY = 3;

def update() {
	global speedX, speedY;
	if (c.x + speedX < 100 or c.x + speedX > 800) {
		speedX = -speedX;
	}
		
	c.x += speedX;
	
	if (c.y + speedY < 100 or c.y + speedY > 600) {
		speedY = -speedY;
	}
		
	c.y += speedY;
	
	draw l;
}