r1 = rect(100, 100, 180, 400, rgb(239, 65, 53));
r2 = rect(280, 100, 198, 400, rgb(255, 255, 255));
r3 = rect(478, 100, 222, 400, rgb(0, 85, 164));

l = [r1, r2, r3];

def flag() {
	draw l;
}

setUpdate(flag);