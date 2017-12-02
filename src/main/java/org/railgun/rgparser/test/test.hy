import os

class A(object):
	def testFile(self, filePath):
		if os.path.isfile(filePath):
			if 1 == 1:
				return True
				
			else:
				return False