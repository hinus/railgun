#-*- coding: UTF-8 -*-

import ast
from Scope import *

class SymtableVisitor(object):
	def __init__(self):
		super(SymtableVisitor, self).__init__()
		self.scopes = {}
		self.module = None
		self.klass = None

		return

	def is_type(self, node, type_name):
		return node.__class__.__name__ == type_name

	def visit(self, node, parent):
		klass = node.__class__.__name__

		func = getattr(self, 'visit_%s' % klass, None)

		if func:
			func(node, parent)

		return

	def visit_ClassDef(self, node, parent):
		for deco in node.decorator_list:
			self.visit(deco, parent)

		for base in node.bases:
			self.visit(base, parent)

		parent.add_def(node.name)
		scope = ClassScope(node.name, self.module)

		if parent.nested or isinstance(parent, FunctionScope):
			scope.nested = 1

		scope.add_def('__module__')
		self.scopes[node] = scope
		prev = self.klass
		self.klass = node.name
		
		for stmt in node.body:
			self.visit(stmt, scope)

		self.klass = prev
		self.handle_free_vars(scope, parent)

		scope.debug()

		return

	def visit_FunctionDef(self, node, parent):
		if node.decorator_list:
			self.visit(node.decorator_list, parent)

		for default in node.args.defaults:
			self.visit(default, parent)

		parent.add_def(node.name)
		scope = FunctionScope(node.name, self.module, self.klass)

		if parent.nested or isinstance(parent, FunctionScope):
			scope.nested = 1

		self.scopes[node] = scope
		self.visit(node.args, scope)
		
		for stmt in node.body:
			self.visit(stmt, scope)

		self.handle_free_vars(scope, parent)

		scope.debug()

		return

	def visit_Module(self, node, parent):
		scope = self.module = self.scopes[node] = ModuleScope()
		for stmt in node.body:
			self.visit(stmt, scope)

		scope.debug()
		return

	def visit_Return(self, node, parent):
		self.visit(node.value, parent)

		return

	def visit_Delete(self, node, parent):
		for tgt in node.targets:
			self.visit(tgt, parent)

		return

	def visit_Name(self, node, parent):
		if self.is_type(node.ctx, "Store"):
			parent.add_def(node.id)
		else:
			parent.add_use(node.id)

		return

	def visit_Global(self, node, parent):
		for name in node.names:
			parent.add_global(name)

		return

	def visit_Print(self, node, parent):
		if node.dest:
			self.visit(node.dest, parent)

		for v in node.values:
			self.visit(v, parent)

		return

	def visit_For(self, node, parent):
		self.visit(node.target, parent)
		self.visit(node.iter, parent)

		for stmt in node.body:
			self.visit(stmt, parent)

		for stmt in node.orelse:
			self.visit(stmt, parent)
			
		return

	def visit_While(self, node, parent):
		self.visit(node.test, parent)

		for stmt in node.body:
			self.visit(stmt, parent)

		for stmt in node.orelse:
			self.visit(stmt, parent)
			
		return

	def visit_If(self, node, parent):
		self.visit(node.test, parent)

		for stmt in node.body:
			self.visit(stmt, parent)

		for stmt in node.orelse:
			self.visit(stmt, parent)
			
		return

	def visit_Raise(self, node, parent):
		if node.type:
			self.visit(node.type, parent)

			if node.inst:
				self.visit(node.inst, parent)

				if node.tback:
					self.visit(node.tback, parent)
		return

	def visit_TryExcept(self, node, parent):

		return

	def visit_Expr(self, node, parent):
		self.visit(node.value, parent)

		return

	def visit_With(self, node, parent):
		self.visit(node.context_expr, parent)

		if node.optional_vars:
			self.visit(node.optional_vars, parent)

		for stmt in node.body:
			self.visit(stmt, parent)

		return

	def visit_Import(self, node, parent):
		pass

	def visit_Assign(self, node, parent):
		for target in node.targets:
			self.visit(target, parent)

		self.visit(node.value, parent)

		return

	def visit_Call(self, node, parent):
		self.visit(node.func, parent)

		for arg in node.args:
			self.visit(arg, parent)

		for keyword in node.keywords:
			self.visit(keyword, parent)

		if node.starargs:
			self.visit(node.starargs, parent)

		if node.kwargs:
			self.visit(node.kwargs, parent)

		return

	#
	# expressions
	#
	def visit_BoolOp(self, node, parent):
		for v in node.values:
			self.visit(v, parent)

		return

	def visit_BinOp(self, node, parent):
		self.visit(node.left, parent)
		self.visit(node.right, parent)

		return

	def visit_Tuple(self, node, parent):
		for name in node.elts:
			self.visit(name, parent)

		return

	def visit_ListComp(self, node, parent):
		self.visit(node.elt, parent)

		for comp in node.generators:
			self.visit_comprehension(comp, parent)

		return

	def visit_DictComp(self, node, parent):
		self.handle_comprehension("<dictcomp>", node, node.key, node.value, parent)

		return

	def visit_SetComp(self, node, parent):
		self.handle_comprehension("<setcomp>", node, node.elt, None, parent)

		return

	def visit_GeneratorExp(self, node, parent):
		self.handle_comprehension("<genexpr>", node, node.elt, None, parent)

		return

	def visit_arguments(self, node, parent):
		self.do_args(node.args, parent)

		if node.vararg:
			parent.add_param(node.vararg)

		if node.kwarg:
			parent.add_param(node.kwarg)

		return

	def do_args(self, args, parent):
		for arg in args:
			if arg.__class__.__name__ == "Tuple":
				self.do_args(arg.elts, parent)
			else:
				parent.add_param(arg.id)

		return

	def visit_comprehension(self, node, parent):
		self.visit(node.target, parent)
		self.visit(node.iter, parent)

		for if_stmt in node.ifs:
			self.visit(if_stmt, parent)

		return

	def handle_free_vars(self, scope, parent):
		parent.add_child(scope)
		scope.handle_children()

		return

	def handle_comprehension(self, scope_name, node, elt, value, parent):
		outermost = node.generators[0]

		self.visit(outermost.iter, parent)

		scope = CompScope(scope_name, self.module, self.klass)
		if parent.nested or isinstance(parent, FunctionScope) or isinstance(parent, CompScope):
			scope.nested = 1
		self.scopes[node] = scope

		self.visit(outermost.target, scope)
		self.visit(outermost.ifs, scope)

		for comp in node.generators[1:]:
			self.visit(comp, scope)

		if value:
			self.visit(value, scope)
		self.visit(elt, scope)

		self.handle_free_vars(scope, parent)
		scope.debug()

		return

	def visit_Lambda(self, node, parent):
		for default in node.args.defaults:
			self.visit(default, parent)

		scope = FunctionScope("<lambda>", self.module, self.klass)

		if parent.nested or isinstance(parent, FunctionScope):
			scope.nested = 1

		self.scopes[node] = scope
		self.visit(node.args, scope)
		
		self.visit(node.body, scope)

		self.handle_free_vars(scope, parent)

		scope.debug()

		return

