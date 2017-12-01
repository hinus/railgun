r = roundrect(175, 75, 450, 450, 10, 10)
line1 = line(325, 75, 325, 525)
line2 = line(175, 225, 625, 225)
line3 = line(475, 75, 475, 525)
line4 = line(175, 375, 625, 375)

board = [r, line1, line2, line3, line4]

l = [2, 1, 0, 2, 3, 5, 4, 9, 8, 7]

def onLeft():
	if l[0] % 3 == 0:
		return
	
	l[l[0]] = l[l[0] + 1]
	l[0] = l[0] + 1
	l[l[0]] = 0
	
	
def onRight():
	if l[0] % 3 == 1:
		return
		
	l[l[0]] = l[l[0] - 1]
	l[0] = l[0] - 1
	l[l[0]] = 0
	
def onUp():
	if l[0] >= 7:
		return
		
	l[l[0]] = l[l[0] + 3]
	l[0] = l[0] + 3
	l[l[0]] = 0
	
def onDown():
	if l[0] <= 3:
		return
		
	l[l[0]] = l[l[0] - 3]
	l[0] = l[0] - 3
	l[l[0]] = 0

KeyMap = {
	"VK_LEFT" : onLeft,
	"VK_RIGHT" : onRight,
	"VK_UP" : onUp,
	"VK_DOWN" : onDown,
}

def update():
	print board