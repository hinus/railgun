c = circle(100, 100, 50, rgb(0, 86, 163));
c1 = circle(200, 200, 50, rgb(78, 78, 78));

l = [c, c1];

speedX = 2;
speedY = 1;

def update(){
	global speedX, speedY;
	if ( speedX < 100 or speedX > 800)
	{
		draw c;
	}
}