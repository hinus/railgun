l = [1, 2, 3]
d = {1:'a', 2:'b', 3:'c'}

for value in l:
	if value in d:
		print value, d[value]

d[1] = 3
print d[1]
