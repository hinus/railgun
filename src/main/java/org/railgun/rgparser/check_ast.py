import ast

def main():
	f = open("init.py", 'r')
	s = f.read()

	n = ast.parse(s)
	print ast.dump(n)

	return

if __name__ == '__main__':
	main()
