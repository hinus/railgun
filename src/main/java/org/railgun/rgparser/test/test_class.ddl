class A(object):
	def __init__(self, value):
		self.v = value

	def p(self):
		print self.v
		return

a = A(1)
a.p()
