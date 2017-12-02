#-*- coding: UTF-8 -*-
#
# -----------------------------------------------------------------------------
# bytecode generators for python
# author : gzxuwei@corp.netease.com
# date : 2015-06-05
# -----------------------------------------------------------------------------

import opcode
import types

class DDCodeGenerator(object):
	def __init__(self):
		self.argcount = 0
		self.nlocals = 0
		self.stacksize = 0
		self.flags = 0

		self.consts = ()
		self.names = ()
		self.varnames = ()

		self.filename = ""
		self.name = ""

		self.freevars = ()
		self.cellvars = ()

		self.lnotab = LineNumberTable()

		return

	def add_code(self, instruction):
		self.lnotab.add_code(instruction)
		return

	def get_code(self):
		return self.lnotab.get_code()
			
	def make_code_object(self):
		co = types.CodeType(self.argcount, self.nlocals, self.stacksize, self.flags,
			self.get_code(), self.consts, self.names, self.varnames,
			self.filename, self.name, 
			self.lnotab.firstline, 
			self.lnotab.getTable(), self.freevars, self.cellvars)

		return co


class LineNumberTable(object):
	def __init__(self):
		super(LineNumberTable, self).__init__()
		self.firstline = 0
		self.code = []
		self.lnotab = []
		self.inst_offset = 0

		return

	def getTable(self):
		return ''.join(self.lnotab)

	def add_code(self, instruction):
		str_opcode = instruction[0]

		if str_opcode == "SET_LINENO":
			if self.firstline == 0:
				self.firstline = instruction[1]
				self.lastline = self.firstline
				return
			else:
				line_offset = instruction[1] - self.lastline
				self.lastline = instruction[1]
				self.lnotab.append(chr(self.inst_offset))
				self.lnotab.append(chr(line_offset))
				self.inst_offset = 0
				return

		int_opcode = opcode.opmap.get(str_opcode, -1)

		if int_opcode < 0:
			return

		self.code.append(chr(int_opcode))
		self.inst_offset += 1

		if len(instruction) > 1:
			for arg in instruction[1:]:
				hi, lo = divmod(arg, 256)

				self.code.append(chr(lo))
				self.code.append(chr(hi))
				self.inst_offset += 2

		return

	def get_code(self):
		return ''.join(self.code)
			
co = None

def foo():
	g = DDCodeGenerator()
	g.name = "g"
	g.filename = "<string>"
	g.consts = (1, None)
	g.stacksize = 1
	g.co_flags = 19
	g.freevars = ('x', )

	g.add_code(('SET_LINENO', 5))
	g.add_code(('LOAD_DEREF', 0))
	g.add_code(('LOAD_CONST', 0))
	g.add_code(('INPLACE_ADD', ))
	g.add_code(('STORE_DEREF', 0))
	g.add_code(('SET_LINENO', 6))
	g.add_code(('LOAD_DEREF', 0))
	g.add_code(('PRINT_ITEM', ))
	g.add_code(('PRINT_NEWLINE', ))
	g.add_code(('LOAD_CONST', 1))
	g.add_code(('RETURN_VALUE', ))

	cog = g.make_code_object()

	f = DDCodeGenerator()
	f.name = "f"
	f.filename = "<string>"
	f.consts = (1, cog, None)
	f.stacksize = 2
	f.co_flags = 3
	f.cellvars = ('x', )
	f.varnames = ('g', )

	f.add_code(('SET_LINENO', 2))
	f.add_code(('LOAD_CONST', 0))
	f.add_code(('STORE_DEREF', 0))

	f.add_code(('SET_LINENO', 3))
	f.add_code(('LOAD_DEREF', 0))
	f.add_code(('PRINT_ITEM', ))
	f.add_code(('PRINT_NEWLINE', ))

	f.add_code(('SET_LINENO', 4))
	f.add_code(('LOAD_CLOSURE', 0))
	f.add_code(('BUILD_TUPLE', 1))
	f.add_code(('LOAD_CONST', 1))
	f.add_code(('MAKE_CLOSURE', 0))
	f.add_code(('STORE_FAST', 0))
	f.add_code(('LOAD_FAST', 1))
	f.add_code(('RETURN_VALUE', ))

	cof = f.make_code_object()

	m = DDCodeGenerator()

	m.name = "<module>"
	m.filename = "<string>"
	m.consts = (cof, None)
	m.names = ('f', )
	m.stacksize = 1
	m.flags = 64

	m.add_code(('SET_LINENO', 1))
	m.add_code(('LOAD_CONST', 0))
	m.add_code(('MAKE_FUNCTION', 0))
	m.add_code(('STORE_NAME', 0))
	m.add_code(('SET_LINENO', 7))
	m.add_code(('LOAD_CONST', 1))
	m.add_code(('RETURN_VALUE', ))

	global co
	co = m.make_code_object()

	return

