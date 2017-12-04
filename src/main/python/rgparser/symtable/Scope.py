#-*- coding: UTF-8 -*-

from const import *

class Scope(object):
	def __init__(self, name, module, klass = None):
		self.name = name
		self.module = module
		self.defs = {}
		self.uses = {}
		self.globals = {}
		self.params = {}
		self.frees = {}
		self.cells = {}
		self.children = []

		self.nested = None
		self.generator = None
		self.klass = None
		
		if klass is not None:
			for i in range(len(klass)):
				if klass[i] != '_':
					self.klass = klass[i:]
					break

	def __repr__(self):
		return "<%s: %s>" % (self.__class__.__name__, self.name)

	def mangle(self, name):
		return name

	def add_def(self, name):
		self.defs[self.mangle(name)] = 1

		return

	def add_use(self, name):
		self.uses[self.mangle(name)] = 1

		return

	def add_global(self, name):
		name = self.mangle(name)

		# 局部变量覆盖全局变量 ?
		if name in self.uses or name in self.defs:
			pass

		if name in self.params:
			raise SyntaxError, "%s in %s in globals and parameters" % (name, self.name)

		self.globals[name] = 1
		self.module.add_def(name)

		return

	def add_param(self, name):
		name = self.mangle(name)
		self.defs[name] = 1
		self.params[name] = 1

		return

	def get_names(self):
		d = {}
		d.update(self.defs)
		d.update(self.uses)
		d.update(self.globals)
		
		return d.keys()

	def add_child(self, child):
		self.children.append(child)

		return

	def get_children(self):
		return self.children

	def check_name(self, name):
		if name in self.globals:
			return SC_GLOBAL_EXPLICIT

		if name in self.cells:
			return SC_CELL

		if name in self.defs:
			return SC_LOCAL

		if self.nested and (name in self.frees or name in self.uses):
			return SC_FREE

		if self.nested:
			return SC_UNKNOWN

		else:
			return SC_GLOBAL_IMPLICIT

	def get_free_vars(self):
		if not self.nested:
			return ()

		free = {}
		free.update(self.frees)

		# 这里使用了自由变量的定义去计算，但上面的self.frees又是什么鬼
		for name in self.uses.keys():
			if name not in self.defs and name not in self.globals:
				free[name] = 1

		return free.keys()

	def handle_children(self):
		for child in self.children:
			frees = child.get_free_vars()
			globals = self.add_frees(frees)
			for name in globals:
				child.force_global(name)

		return

	# 当前结点的某些子结点有可能把一个name当成free ref，这是因为
	# 在处理这些子结点的时候，它的 enclosing scope 没有被处理。现在
	# es处理完了，再回过头来处理子结点。
	def force_global(self, name):
		self.globals[name] = 1
		if name in self.frees:
			del self.frees[name]

		for child in self.children:
			if child.check_name(name) == SC_FREE:
				child.force_global(name)

		return

	# 处理嵌套作用域里的自由变量
	def add_frees(self, names):
		child_globals = []

		for name in names:
			sc = self.check_name(name)

			if self.nested:
				if sc == SC_UNKNOWN or sc == SC_FREE or isinstance(self, ClassScope):
					self.frees[name] = 1
				
				elif sc == SC_GLOBAL_IMPLICIT:
					child_globals.append(name)

				elif isinstance(self, FunctionScope) and sc == SC_LOCAL:
					self.cells[name] = 1

				elif sc != SC_CELL:
					child_globals.append(name)

			else:
				if sc == SC_LOCAL:
					self.cells[name] = 1

				elif sc != SC_CELL:
					child_globals.append(name)

		return child_globals

	def get_cell_vars(self):
		return self.cells.keys()

	def debug(self):
		print "==========="
		print "name is", self.name
		if self.nested:
			print "nested"
		print "defs is", self.defs
		print "params is", self.params
		print "cells is", self.cells
		print "frees is", self.frees
		print "global is", self.globals
		print "use is", self.uses

		return

class ModuleScope(Scope):
	def __init__(self):
		super(ModuleScope, self).__init__("global", self)

class FunctionScope(Scope):
	pass

class ClassScope(Scope):
	def __init__(self, name, module):
		super(ClassScope, self).__init__(name, module)

class CompScope(Scope):
	def __init__(self, name, module, klass = None):
		super(CompScope, self).__init__(name, module, klass)
