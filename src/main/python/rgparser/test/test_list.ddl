def double(x):
	return x * 2

a = [1, 2, 3]
b = map(double, a)

for index, value in enumerate(b):
	print index, value

