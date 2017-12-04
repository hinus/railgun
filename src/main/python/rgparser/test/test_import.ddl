import os as o
from os.path import isdir as d, isfile as f

if f("D:\\"):
	print "File"
elif d("D:\\"):
	print "Directory"
else:
	print 0
