def foo():
	x = 1
	del x
	def bar():
		print x

	return bar

g = foo()
g()
