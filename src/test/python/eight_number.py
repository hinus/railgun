r = roundrect(175, 75, 450, 450, 10, 10)
line1 = line(325, 75, 325, 525)
line2 = line(175, 225, 625, 225)
line3 = line(475, 75, 475, 525)
line4 = line(175, 375, 625, 375)

board = [r, line1, line2, line3, line4]

l = [2, 1, 0, 2, 3, 5, 4, 9, 8, 7]

def move(dir):
	if dir == 1 and l[0] % 3 == 0:
		return
	
	if dir == -1 and l[0] % 3 == 1:
		return
		
	if l[0] + dir < 1 or l[0] + dir > 9:
		return
		
	l[l[0]] = l[l[0] + dir]
	l[0] = l[0] + dir
	l[l[0]] = 0

def onLeft():
	move(1)
	
def onRight():
	move(-1)
	
def onUp():
	move(3)
	
def onDown():
	move(-3)

KeyMap = {
	"VK_LEFT" : onLeft,
	"VK_RIGHT" : onRight,
	"VK_UP" : onUp,
	"VK_DOWN" : onDown,
}

def update():
	i = 1
	while i <= 9:
		if l[i] == 0:
			i += 1
			continue
		
		x = 250 + (i + 2) % 3 * 150
		y = 150 + (i - 1) / 3 * 150
		t = rgtext(l[i], x, y, "Arial Black", 24)
		
		print t
		i += 1
		
	print board