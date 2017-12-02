#-*- coding: UTF-8 -*-
#
# -----------------------------------------------------------------------------
# instruction generator for python
# author : gzxuwei@corp.netease.com
# date : 2015-08-15
# -----------------------------------------------------------------------------

import ast
import SymtableVisitor
import Assem
import const

LOOP = 1
EXCEPT = 2
TRY_FINALLY = 3
END_FINALLY = 4

class CodeGen(object):
	def __init__(self, filename):
		super(CodeGen, self).__init__()

		self.filename = filename
		self.module_graph = None
		self.setups = []

		return

	def is_type(self, node, type_name):
		return node.__class__.__name__ == type_name

	def is_constant(self, node):
		if not self.is_type(node, "Str") and not self.is_type(node, "Num"):
			return -1

		if self.is_type(node, "Str"):
			return not (not node.s)

		else:
			return not (not node.n)

	def get_code(self):
		if self.module_graph:
			return self.module_graph.get_code()

		return None

	def visit(self, node, scope, graph):
		klass = node.__class__.__name__

		func = getattr(self, 'visit_%s' % klass, None)
		lineno = getattr(node, 'lineno', 0)

		if lineno:
			graph.emit("SET_LINENO", lineno)

		if func:
			func(node, scope, graph)

		return

	def visit_Tuple(self, node, scope, graph):
		if self.is_type(node.ctx, "Store"):
			graph.emit("UNPACK_SEQUENCE", len(node.elts))

		for elt in node.elts:
			self.visit(elt, scope, graph)

		if self.is_type(node.ctx, "Load"):
			graph.emit("BUILD_TUPLE", len(node.elts))

		return

	#
	# Statement
	#
	def visit_Module(self, node, scope, graph):
		symtable = SymtableVisitor.SymtableVisitor()
		symtable.visit(node, None)

		self.scopes = symtable.scopes
		scope = self.scopes[node]
		graph = Assem.PyFlowGraph("<module>", self.filename)

		graph.emit("SET_LINENO", 0)

		for stmt in node.body:
			self.visit(stmt, scope, graph)

		graph.emit("LOAD_CONST", None)
		graph.emit("RETURN_VALUE")

		self.module_graph = graph

		return

	def visit_Delete(self, node, scope, graph):
		for tgt in node.targets:
			self.visit(tgt, scope, graph)

		return

	def visit_Assign(self, node, scope, graph):
		self.visit(node.value, scope, graph)
		
		for index, tgt in enumerate(node.targets):
			if index < len(node.targets) - 1:
				graph.emit("DUP_TOP")

			self.visit(tgt, scope, graph)

		return

	def visit_AugAssign(self, node, scope, graph):
		e = node.target
		e_type = e.__class__.__name__

		if e_type == "Attribute":
			auge = ast.Attribute(e.value, e.attr, ast.AugLoad())
			self.visit(auge, scope, graph)
			self.visit(node.value, scope, graph)
			self.inplace_binop(node.op, graph)

			auge.ctx = ast.AugStore()
			self.visit(auge, scope, graph)

		elif e_type == "Subscript":
			auge = ast.Subscript(e.value, e.slice, ast.AugLoad())

			self.visit(auge, scope, graph)
			self.visit(node.value, scope, graph)
			self.inplace_binop(node.op, graph)
			auge.ctx = ast.AugStore()
			self.visit(auge, scope, graph)

		elif e_type == "Name":
			self._name_op("LOAD", node.id, scope, graph)
			self.visit(node.value, scope, graph)
			self.inplace_binop(node.op, graph)
			self._name_op("STORE", node.id, scope, graph)

		else:
			raise SyntaxError, "invalid node type (%s) for augmented assignment" % e_type

		return

	def inplace_binop(self, op, graph):
		op_type = op.__class__.__name__
		
		if op_type == "Add":
			graph.emit("INPLACE_ADD")

		elif op_type == "Sub":
			graph.emit("INPLACE_SUBTRACT")

		elif op_type == "Mult":
			graph.emit("INPLACE_MULTIPLY")

		elif op_type == "Div":
			graph.emit("INPLACE_DIVIDE")

		elif op_type == "Mod":
			graph.emit("INPLACE_MODULO")

		elif op_type == "Pow":
			graph.emit("INPLACE_POWER")

		elif op_type == "LShift":
			graph.emit("INPLACE_LSHIFT")

		elif op_type == "RShift":
			graph.emit("INPLACE_RSHIFT")

		elif op_type == "BitOr":
			graph.emit("INPLACE_OR")

		elif op_type == "BitXor":
			graph.emit("INPLACE_XOR")

		elif op_type == "BitAnd":
			graph.emit("INPLACE_AND")

		elif op_type == "FloorDiv":
			graph.emit("INPLACE_FLOOR_DIVIDE")

		return

	def visit_Print(self, node, scope, graph):
		dest = False
		if node.dest:
			self.visit(node.dest, scope, graph)
			dest = True

		for v in node.values:
			if dest:
				graph.emit("DUP_TOP")
				self.visit(v, scope, graph)
				graph.emit("ROT_TWO")
				graph.emit("PRINT_ITEM_TO")

			else:
				self.visit(v, scope, graph)
				graph.emit("PRINT_ITEM")

		if node.nl:
			if dest:
				graph.emit("PRINT_NEWLINE_TO")
			else:
				graph.emit("PRINT_NEWLINE")

		elif dest:
			graph.emit("POP_TOP")

		return

	def visit_decos(self, decos, scope, graph):
		for d in decos:
			self.visit(d, scope, graph)

		return

	def make_closure(self, args, scope, graph, old_graph):
		frees = scope.get_free_vars()

		if frees:
			for name in frees:
				old_graph.emit("LOAD_CLOSURE", name)
			old_graph.emit("BUILD_TUPLE", len(frees))
			old_graph.emit("LOAD_CONST", graph)
			old_graph.emit("MAKE_CLOSURE", args)

		else:
			old_graph.emit("LOAD_CONST", graph)
			old_graph.emit("MAKE_FUNCTION", args)

		return

	def visit_ClassDef(self, node, scope, graph):
		if node.decorator_list:
			self.visit_decos(node.decorator_list, scope, graph)

		graph.emit("LOAD_CONST", node.name)

		for base in node.bases:
			self.visit(base, scope, graph)

		graph.emit("BUILD_TUPLE", len(node.bases))

		old_graph = graph
		old_scope = scope

		scope = self.scopes[node]
		graph = Assem.PyFlowGraph(node.name, self.filename, klass = node.name, optimized = False)

		self._name_op("LOAD", "__name__", scope, graph)
		self._name_op("STORE", "__module__", scope, graph)

		for stmt in node.body:
			self.visit(stmt, scope, graph)

		graph.emit("LOAD_LOCALS")
		graph.emit("RETURN_VALUE")

		self.make_closure(0, scope, graph, old_graph)

		graph = old_graph
		scope = old_scope

		graph.emit("CALL_FUNCTION", 0)
		graph.emit("BUILD_CLASS")

		for deco in node.decorator_list:
			graph.emit("CALL_FUNCTION", 1)

		self._name_op("STORE", node.name, scope, graph)

		return

	def visit_FunctionDef(self, node, scope, graph):
		if node.decorator_list:
			self.visit_decos(node.decorator_list, scope, graph)

		for v in node.args.defaults:
			self.visit(v, scope, graph)

		old_graph = graph
		old_scope = scope

		scope = self.scopes[node]
		graph = Assem.PyFlowGraph(node.name, self.filename, args = node.args.args, 
				optimized = True, function_block = True)

		graph.set_cell_vars(scope.get_cell_vars())
		graph.set_free_vars(scope.get_free_vars())

		self.visit(node.args, scope, graph)

		for stmt in node.body:
			self.visit(stmt, scope, graph)

		graph.finish(False)

		self.make_closure(len(node.args.defaults), scope, graph, old_graph)
		
		for d in node.decorator_list:
			old_graph.emit("CALL_FUNCTION", 1)

		self._name_op("STORE", node.name, old_scope, old_graph)

		return

	def visit_Call(self, node, scope, graph):
		self.visit(node.func, scope, graph)

		n = len(node.args)
		code = 0
		
		for arg in node.args:
			self.visit(arg, scope, graph)

		if node.keywords:
			for w in node.keywords:
				self.visit(w, scope, graph)

			n |= len(node.keywords) << 8

		if node.starargs:
			self.visit(node.starargs, scope, graph)
			code |= 1

		if node.kwargs:
			self.visit(node.kwargs, scope, graph)
			code |= 2

		if code == 0:
			graph.emit("CALL_FUNCTION", n)

		elif code == 1:
			graph.emit("CALL_FUNCTION_VAR", n)

		elif code == 2:
			graph.emit("CALL_FUNCTION_KW", n)

		elif code == 3:
			graph.emit("CALL_FUNCTION_VAR_KW", n)

		return

	def visit_Return(self, node, scope, graph):
		if not graph.function_block:
			raise "return outside function, line %s" % node.lineno

		if node.value:
			self.visit(node.value, scope, graph)
		else:
			graph.emit("LOAD_CONST", None)

		graph.emit("RETURN_VALUE")

		return

	def visit_Compare(self, node, scope, graph):
		self.visit(node.left, scope, graph)

		n = len(node.ops)
		cleanup = None

		if n > 1:
			cleanup = graph.new_block()
			self.visit(node.comparators[0], scope, graph)

		for index, cmptor in enumerate(node.comparators[1:]):
			graph.emit("DUP_TOP")
			graph.emit("ROT_THREE")
			graph.emit("COMPARE_OP", self.get_op(node.ops[index]))
			graph.emit("JUMP_IF_FALSE_OR_POP", cleanup)
			graph.next_block()
			self.visit(cmptor, scope, graph)

		if n == 1:
			self.visit(node.comparators[0], scope, graph)
			graph.emit("COMPARE_OP", self.get_op(node.ops[0]))

		if n > 1:
			end = graph.new_block()
			graph.emit("JUMP_FORWARD", end)
			graph.next_block(cleanup)
			graph.emit("ROT_TWO")
			graph.emit("POP_TOP")
			graph.start_block(end)

		return


	def get_op(self, op):
		op_type = op.__class__.__name__

		if op_type == 'Eq':
			return '=='

		elif op_type == 'Gt':
			return '>'

		elif op_type == 'GtE':
			return '>='

		elif op_type == 'Lt':
			return '<'

		elif op_type == 'LtE':
			return '<='

		elif op_type == 'NotEq':
			return '!='

		elif op_type == 'Is':
			return 'is'

		elif op_type == 'IsNot':
			return 'is not'

		elif op_type == 'in':
			return 'in'

		elif op_type == 'not in':
			return 'not in'


	def visit_If(self, node, scope, graph):
		end = graph.new_block()
		next = None

		constant = self.is_constant(node.test)

		if (constant == 0):
			for stmt in node.orelse:
				self.visit(stmt, scope, graph)

		elif constant == 1:
			for stmt in node.body:
				self.visit(stmt, scope, graph)

		else:
			if node.orelse:
				next = graph.new_block()

			else:
				next = end

			self.visit(node.test, scope, graph)
			graph.emit("POP_JUMP_IF_FALSE", next)
			for stmt in node.body:
				self.visit(stmt, scope, graph)
			graph.emit("JUMP_FORWARD", end)

			if node.orelse:
				graph.next_block(next)
				for stmt in node.orelse:
					self.visit(stmt, scope, graph)

		graph.next_block(end)

		return

	def visit_Raise(self, node, scope, graph):
		n = 0

		if node.type:
			self.visit(node.type, scope, graph)
			n += 1

			if node.inst:
				self.visit(node.inst, scope, graph)
				n += 1

				if node.tback:
					self.visit(node.tback, scope, graph)
					n += 1

		graph.emit("RAISE_VARARGS", n)

		return

	def visit_TryExcept(self, node, scope, graph):
		body = graph.new_block()
		excpt = graph.new_block()
		orelse = graph.new_block()
		end = graph.new_block()

		graph.emit("SETUP_EXCEPT", excpt)
		graph.next_block(body)

		self.setups.append((EXCEPT, body))

		for stmt in node.body:
			self.visit(stmt, scope, graph)

		graph.emit("POP_BLOCK")

		self.setups.pop()
		graph.emit("JUMP_FORWARD", orelse)

		graph.next_block(excpt)

		for index, handler in enumerate(node.handlers):
			if not handler.type and index < len(node.handlers) - 1:
				raise SyntaxError, "default 'except:' must be last"

			excpt = graph.new_block()

			if handler.type:
				graph.emit("DUP_TOP")
				self.visit(handler.type, scope, graph)
				graph.emit("COMPARE_OP", "exception match")
				graph.emit("POP_JUMP_IF_FALSE", excpt)

			graph.emit("POP_TOP")

			if handler.name:
				self.visit(handler.name, scope, graph)

			else:
				graph.emit("POP_TOP")

			graph.emit("POP_TOP")
			for stmt in handler.body:
				self.visit(stmt, scope, graph)

			graph.emit("JUMP_FORWARD", end)
			graph.next_block(excpt)

		graph.emit("END_FINALLY")
		graph.next_block(orelse)

		for stmt in node.orelse:
			self.visit(stmt, scope, graph)

		graph.next_block(end)

		return

	def visit_TryFinally(self, node, scope, graph):
		body = graph.new_block()
		end = graph.new_block()

		graph.emit("SETUP_FINALLY", end)
		graph.next_block(body)

		self.setups.append((TRY_FINALLY, body))

		for stmt in node.body:
			self.visit(stmt, scope, graph)

		graph.emit("POP_BLOCK")
		self.setups.pop()

		graph.emit("LOAD_CONST", None)
		graph.next_block(end)
		self.setups.append((END_FINALLY, end))

		for stmt in node.finalbody:
			self.visit(stmt, scope, graph)

		graph.emit("END_FINALLY")
		self.setups.pop()

		return

	def visit_Assert(self, node, scope, graph):
		assertion_error = "AssertionError"

		self.visit(node.test, scope, graph)
		end = graph.new_block()

		graph.emit("POP_JUMP_IF_TRUE", end)
		graph.emit("LOAD_GLOBAL", assertion_error)

		if node.msg:
			self.visit(node.msg, scope, graph)
			graph.emit("CALL_FUNCTION", 1)

		graph.emit("RAISE_VARARGS", 1)
		graph.next_block(end)

		return

	def visit_While(self, node, scope, graph):
		constant = self.is_constant(node.test)

		if constant == 0:
			for stmt in node.orelse:
				self.visit(stmt, scope, graph)

			return

		loop = graph.new_block()
		end = graph.new_block()
		anchor = None
		orelse = None

		if node.orelse:
			orelse = graph.new_block()

		graph.emit("SETUP_LOOP", end)
		graph.next_block(loop)

		self.setups.append((LOOP, loop))

		if constant == -1:
			anchor = graph.new_block()
			self.visit(node.test, scope, graph)
			graph.emit("POP_JUMP_IF_FALSE", anchor)

		for stmt in node.body:
			self.visit(stmt, scope, graph)

		graph.emit("JUMP_ABSOLUTE", loop)

		if constant == -1:
			graph.next_block(anchor)

		graph.emit("POP_BLOCK")
		self.setups.pop()

		for stmt in node.orelse:
			self.visit(stmt, scope, graph)

		graph.next_block(end)

		return

	def visit_For(self, node, scope, graph):
		start = graph.new_block()
		cleanup = graph.new_block()
		end = graph.new_block()

		graph.emit("SETUP_LOOP", end)
		self.setups.append((LOOP, start))

		self.visit(node.iter, scope, graph)
		graph.emit("GET_ITER")

		graph.next_block(start)
		graph.emit("FOR_ITER", cleanup)
		self.visit(node.target, scope, graph)

		for stmt in node.body:
			self.visit(stmt, scope, graph)

		graph.emit("JUMP_ABSOLUTE", start)
		
		graph.next_block(cleanup)
		graph.emit("POP_BLOCK")

		self.setups.pop()

		for stmt in node.orelse:
			self.visit(stmt, scope, graph)

		graph.next_block(end)

		return

	def visit_Continue(self, node, scope, graph):
		if not self.setups:
			raise SyntaxError, "'continue' outside loop (%s, %d)" % \
			  	(self.filename, node.lineno)

		loop_type, block = self.setups[len(self.setups) - 1]

		if loop_type == LOOP:
			graph.emit("JUMP_ABSOLUTE", block)

		elif loop_type in (EXCEPT, TRY_FINALLY):
			top = len(self.setups)
			while top > 0:
				top -= 1
				loop_kind, loop_block = self.setups[top]

				if loop_kind == LOOP:
					break

				if loop_kind == END_FINALLY:
					msg = "'continue' not allowed inside 'finally' clause (%s, %d)"
					raise SyntaxError, msg % (node.filename, node.lineno)

			if loop_kind == LOOP:
				graph.emit("CONTINUE_LOOP", loop_block)

		elif loop_type == END_FINALLY:
			msg = "'continue' not allowed inside 'finally' clause (%s, %d)"
			raise SyntaxError, msg % (node.filename, node.lineno)

		return

	def visit_Break(self, node, scope, graph):
			top = len(self.setups)
			error_msg = "'break' outside loop (%s, %d)" % (self.filename, node.lineno)

			if top <= 0:
				raise SyntaxError, error_msg

			kind = 0
			while top > 0:
					top -= 1
					kind, block = self.setups[top]

					if kind == LOOP:
							break

			if kind != LOOP:
				raise SyntaxError, error_msg

			graph.emit("BREAK_LOOP")

			return

	def visit_With(self, node, scope, graph):
		block = graph.new_block()
		final = graph.new_block()

		self.visit(node.context_expr, scope, graph)
		graph.emit("SETUP_WITH", final)

		graph.next_block(block)
		self.setups.append((TRY_FINALLY, block))

		if node.optional_vars:
			self.visit(node.optional_vars, scope, graph)

		else:
			graph.emit("POP_TOP")

		for stmt in node.body:
			self.visit(stmt, scope, graph)

		graph.emit("POP_BLOCK")

		self.setups.pop()

		graph.emit("LOAD_CONST", None)
		graph.next_block(final)

		self.setups.append((END_FINALLY, final))
		graph.emit("WITH_CLEANUP")
		graph.emit("END_FINALLY")
		self.setups.pop()

		return

	def visit_Import(self, node, scope, graph):
		for alias in node.names:
			level = 0
			if graph.flags & const.CO_FUTURE_ABSIMPORT:
				level = -1

			graph.emit("LOAD_CONST", level)
			graph.emit("LOAD_CONST", None)
			graph.emit("IMPORT_NAME", alias.name)

			if alias.asname:
				self.compiler_import_as(alias.name, alias.asname)
			
			else:
				tmp = alias.name.split(".")[0]
				self._name_op("STORE", tmp, scope, graph)

		return

	def visit_ImportFrom(self, node, scope, graph):
		level = node.level
		if node.level == 0 and graph.flags & const.CO_FUTURE_ABSIMPORT:
			level = -1

		names = []
		for alias in node.names:
			names.append(alias.name)

		graph.emit("LOAD_CONST", level)
		graph.emit("LOAD_CONST", names)

		if node.module:
			graph.emit("IMPORT_NAME", node.module)
		else:
			graph.emit("IMPORT_NAME", "")

		for alias in node.names:
			if alias.name == "*":
				assert len(node.names) == 1
				graph.emit("IMPORT_STAR")
				return

			graph.emit("IMPORT_FROM", alias.name)
			store_name = alias.name
			if alias.asname:
				store_name = alias.asname

			self._name_op("STORE", store_name, scope, graph)

		graph.emit("POP_TOP")

		return

	def visit_Exec(self, node, scope, graph):
		self.visit(node.body, scope, graph)

		if node.globals:
			self.visit(node.globals, scope, graph)

			if node.locals:
				self.visit(node.locals, scope, graph)

			else:
				graph.emit("DUP_TOP")

		else:
			graph.emit("LOAD_CONST", None)
			graph.emit("DUP_TOP")
		
		graph.emit("EXEC_STMT")

		return

	#
	# Expression
	#
	def visit_BoolOp(self, node, scope, graph):
		end = graph.new_block()

		if self.is_type(node.op, "And"):
			jumpi = "JUMP_IF_FALSE_OR_POP"
		else:
			jumpi = "JUMP_IF_TRUE_OR_POP"

		for v in node.values[:-1]:
			self.visit(v, scope, graph)
			graph.emit(jumpi, end)

		self.visit(node.values[-1], scope, graph)
		graph.next_block(end)

		return

	def visit_Expr(self, node, scope, graph):
		if node.value.__class__.__name__ not in ("Str", "Num"):
			self.visit(node.value, scope, graph)
			graph.emit("POP_TOP")
		return

	def visit_Name(self, node, scope, graph):
		if self.is_type(node.ctx, "Store"):
			self._name_op("STORE", node.id, scope, graph)
		elif self.is_type(node.ctx, "Load"):
			self._name_op("LOAD", node.id, scope, graph)
		elif self.is_type(node.ctx, "Del"):
			self._name_op("DELETE", node.id, scope, graph)
		else:
			raise "Unknown name context", node.ctx

		return

	def _name_op(self, prefix, name, scope, graph):
		scope_type = scope.check_name(name)

		if scope_type == const.SC_LOCAL:
			if graph.optimized:
				graph.emit(prefix + '_FAST', name)
			else:
				graph.emit(prefix + '_NAME', name)

		elif scope_type == const.SC_GLOBAL_EXPLICIT:
			graph.emit(prefix + '_GLOBAL', name)

		elif scope_type == const.SC_GLOBAL_IMPLICIT:
			if graph.optimized:
				graph.emit(prefix + '_GLOBAL', name)
			else:
				graph.emit(prefix + '_NAME', name)

		elif scope_type == const.SC_FREE or scope_type == const.SC_CELL:
			graph.emit(prefix + '_DEREF', name)

		else:
			raise RuntimeError, "unsupported scope for var %s: %d" % \
				  (name, scope_type)

	def visit_Repr(self, node, scope, graph):
		self.visit(node,value, scope, graph)
		graph.emit("UNARY_CONVERT")
		return

	def visit_Num(self, node, scope, graph):
		graph.emit("LOAD_CONST", node.n)
		return

	def visit_BinOp(self, node, scope, graph):
		self.visit(node.left, scope, graph)
		self.visit(node.right, scope, graph)
		self.binop(node.op, graph)

		return

	def binop(self, op, graph):
		op_class = op.__class__.__name__

		if op_class == "Add":
			graph.emit("BINARY_ADD")

		elif op_class == "Sub":
			graph.emit("BINARY_SUBTRACT")

		elif op_class == "Mult":
			graph.emit("BINARY_MULTIPLY")

		elif op_class == "Div":
			graph.emit("BINARY_DIVIDE")

		elif op_class == "Mod":
			graph.emit("BINARY_MODULO")

		elif op_class == "Pow":
			graph.emit("BINARY_POWER")

		elif op_class == "LShift":
			graph.emit("BINARY_LSHIFT")

		elif op_class == "RShift":
			graph.emit("BINARY_RSHIFT")

		elif op_class == "BitOr":
			graph.emit("BINARY_OR")

		elif op_class == "BitXor":
			graph.emit("BINARY_XOR")

		elif op_class == "BitAnd":
			graph.emit("BINARY_AND")

		elif op_class == "FloorDiv":
			graph.emit("BINARY_FLOOR_DIVIDE")

		return

	def visit_UnaryOp(self, node, scope, graph):
		self.visit(node.operand, scope, graph)
		self.unaryop(node.op, graph)

		return

	def unaryop(self, op, graph):
		node_type = op.__class__.__name__

		if node_type == "Invert":
			graph.emit("UNARY_INVERT")

		elif node_type == "Not":
			graph.emit("UNARY_NOT")

		elif node_type == "UAdd":
			graph.emit("UNARY_POSITIVE")

		elif node_type == "USub":
			graph.emit("UNARY_NEGATIVE")

		return 0

	def visit_Lambda(self, node, scope, graph):
		for v in node.args.defaults:
			self.visit(v, scope, graph)

		old_scope = scope
		old_graph = graph

		scope = self.scopes[node]
		graph = Assem.PyFlowGraph("<lambda>", self.filename, args = node.args.args,
				optimized = True, function_block = True)

		graph.set_cell_vars(scope.get_cell_vars())
		graph.set_free_vars(scope.get_free_vars())

		self.visit(node.args, scope, graph)

		self.visit(node.body, scope, graph)

		if scope.generator:
			graph.emit("POP_TOP")

		else:
			graph.emit("RETURN_VALUE")

		self.make_closure(len(node.args.defaults), scope, graph, old_graph)

		scope = old_scope
		graph = old_graph

		return

	def visit_IfExp(self, node, scope, graph):
		end = graph.new_block()
		next = graph.new_block()

		self.visit(node.test, scope, graph)
		graph.emit("POP_JUMP_IF_FALSE", next)
		self.visit(node.body, scope, graph)
		graph.emit("JUMP_FORWARD", end)
		graph.next_block(next)
		self.visit(node.orelse)
		graph.next_block(end)

		return

	def visit_Str(self, node, scope, graph):
		graph.emit("LOAD_CONST", node.s)
		return

	def visit_Attribute(self, node, scope, graph):
		ctx_name = node.ctx.__class__.__name__
		if ctx_name != "AugStore":
			self.visit(node.value, scope, graph)

		if ctx_name == "AugLoad":
			graph.emit("DUP_TOP")
			graph.emit("LOAD_ATTR", node.attr)

		elif ctx_name == "Load":
			graph.emit("LOAD_ATTR", node.attr)

		elif ctx_name == "Store":
			graph.emit("STORE_ATTR", node.attr)

		elif ctx_name == "AugStore":
			graph.emit("ROT_TWO")
			graph.emit("STORE_ATTR", node.attr)

		elif ctx_name == "Del":
			graph.emit("DELETE_ATTR", node.attr)

		else:
			raise SyntaxError, "wrong context for Attribute"

		return

	def visit_Subscript(self, node, scope, graph):
		ctx_type = node.ctx.__class__.__name__
		if ctx_type != "AugStore":
			self.visit(node.value, scope, graph)

		self.visit_slice(node.slice, ctx_type, scope, graph)

		return

	def visit_slice(self, node_slice, ctx_type, scope, graph):
		kind = node_slice.__class__.__name__
		kindname = ""

		if kind == "Index":
			kindname = "index"
			if ctx_type != "AugStore":
				self.visit(node_slice.value, scope, graph)

		elif kind == "Ellipsis":
			kindname = "ellipsis"
			if ctx_type != "AugStore":
				graph.emit("LOAD_CONST", Ellipsis)

		elif kind == "Slice":
			kindname = "slice"
			if not node_slice.step:
				self.visit_simple_slice(node_slice, scope, graph, ctx_type)
				return

			if ctx_type != "AugStore":
				self.visit_complex_slice(node_slice, scope, graph, ctx_type)

		elif kind == "ExtSlice":
			kindname = "extended slice"

			if ctx_type != "AugStore":
				for sub in node_slice.dims:
					self.visit_nested_slice(sub, scope, graph, ctx_type)

				graph.emit("BUILD_TUPLE", len(node_slice.dims))

		self.visit_handle_subscr(kindname, ctx_type, scope, graph)

		return

	def visit_simple_slice(self, node, scope, graph, ctx_type):
		op = ""
		slice_offset = 0
		stack_count = 0

		if node.lower:
			slice_offset += 1
			stack_count += 1

			if ctx_type != "AugStore":
				self.visit(node.lower, scope, graph)

		if node.upper:
			slice_offset += 2
			stack_count += 1

			if ctx_type != "AugStore":
				self.visit(node.upper, scope, graph)

		if ctx_type == "AugLoad":
			if stack_count == 0:
				graph.emit("DUP_TOP")

			elif stack_count == 1:
				graph.emit("DUP_TOPX", 2)

			elif stack_count == 2:
				graph.emit("DUP_TOPX", 3)

		elif ctx_type == "AugStore":
			if stack_count == 0:
				graph.emit("ROT_TWO")

			elif stack_count == 1:
				graph.emit("ROT_THREE")

			elif stack_count == 2:
				graph.emit("ROT_FOUR")
		
		if ctx_type in ("AugLoad", "Load"):
			op = "SLICE"

		elif ctx_type in ("AugStore", "Store"):
			op = "STORE_SLICE"

		elif ctx_type == "Del":
			op = "DELETE_SLICE"

		graph.emit("%s+%d" % (op, slice_offset))

		return

	def visit_complex_slice(self, node, scope, graph, ctx):
		n = 2

		if node.lower:
			self.visit(node.lower, scope, graph)

		else:
			graph.emit("LOAD_CONST", None)

		if node.upper:
			self.visit(node.upper, scope, graph)

		else:
			graph.emit("LOAD_CONST", None)

		if node.step:
			n += 1
			if self.is_type(node.step, "Name") and node.step.id == "None":
				graph.emit("LOAD_CONST", None)
			else:
				self.visit(node.step, scope, graph)

		graph.emit("BUILD_SLICE", n)

		return

	def visit_nested_slice(self, node, scope, graph, ctx):
		node_type = node.__class__.__name__

		if node_type == "Ellipsis":
			graph.emit("LOAD_CONST", Ellipsis)

		elif node_type == "Slice":
			self.visit_complex_slice(node, scope, graph, ctx)

		elif node_type == "Index":
			self.visit(node.value, scope, graph)

		else:
			raise SyntaxError, "extended slice invalid in nested slice"

		return

	def visit_handle_subscr(self, kindname, ctx_type, scope, graph):
		op = ""

		if ctx_type in ("AugLoad", "Load"):
			op = "BINARY_SUBSCR"

		elif ctx_type in ("AugStore", "Store"):
			op = "STORE_SUBSCR"

		elif ctx_type == "Del":
			op = "DELETE_SUBSCR"

		else:
			raise SyntaxError, "invalid %s kind %s in subscript" % (kindname, ctx_type)

		if ctx_type == "AugLoad":
			graph.emit("DUP_TOPX", 2)

		elif ctx_type == "AugStore":
			graph.emit("ROT_THREE")

		graph.emit(op)

		return


	def visit_Dict(self, node, scope, graph):
		n = len(node.values)
		graph.emit("BUILD_MAP", 0xFFFF if n > 0xFFFF else n)

		for index, v in enumerate(node.values):
			self.visit(v, scope, graph)
			self.visit(node.keys[index], scope, graph)
			graph.emit("STORE_MAP")

		return

	def visit_List(self, node, scope, graph):
		n = len(node.elts)

		if self.is_type(node.ctx, "Store"):
			graph.emit("UNPACK_SEQUENCE", n)

		for v in node.elts:
			self.visit(v, scope, graph)

		if self.is_type(node.ctx, "Load"):
			graph.emit("BUILD_LIST", n)

		return

	def visit_ListComp(self, node, scope, graph):
		graph.emit("BUILD_LIST", 0)
		self.visit_listcomp_generator(node.generators, 0, node.elt, scope, graph)

	def visit_listcomp_generator(self, generators, gen_index, elt, scope, graph):
		start = graph.new_block()
		skip = graph.new_block()
		if_cleanup = graph.new_block()
		anchor = graph.new_block()

		l = generators[gen_index]

		self.visit(l.iter, scope, graph)
		graph.emit("GET_ITER")
		graph.next_block(start)
		graph.emit("FOR_ITER", anchor)
		graph.next_block()
		self.visit(l.target, scope, graph)

		n = len(l.ifs)

		for stmt in l.ifs:
			self.visit(stmt, scope, graph)
			graph.emit("POP_JUMP_IF_FALSE", if_cleanup)
			graph.next_block()

		gen_index += 1
		if gen_index < len(generators):
			self.visit_listcomp_generator(generators, gen_index, elt, scope, graph)

		if gen_index >= len(generators):
			self.visit(elt, scope, graph)
			graph.emit("LIST_APPEND", gen_index + 1)
			graph.next_block(skip)

		graph.next_block(if_cleanup)
		graph.emit("JUMP_ABSOLUTE", start)

		graph.next_block(anchor)

		return

	def visit_DictComp(self, node, scope, graph):
		self.compiler_comprehension("<dictcomp>", node, node.key, node.value, scope, graph)

		return

	def visit_SetComp(self, node, scope, graph):
		self.compiler_comprehension("<setcomp>", node, node.elt, None, scope, graph)

		return

	def visit_GeneratorExp(self, node, scope, graph):
		self.compiler_comprehension("<genexpr>", node, node.elt, None, scope, graph)

		return

	def visit_comprehension_generator(self, generators, gen_index, elt, val, node_type, scope, graph):
		start = graph.new_block()
		skip = graph.new_block()
		if_cleanup = graph.new_block()
		anchor = graph.new_block()

		gen = generators[gen_index]

		if gen_index == 0:
			graph.argcount = 1
			graph.emit("LOAD_FAST", ".0")

		else:
			self.visit(gen.iter, scope, graph)
			graph.emit("GET_ITER")

		graph.next_block(start)
		graph.emit("FOR_ITER", anchor)
		graph.next_block()
		self.visit(gen.target, scope, graph)

		for e in gen.ifs:
			self.visit(e, scope, graph)
			graph.emit("POP_JUMP_IF_FALSE", if_cleanup)
			graph.next_block()

		gen_index += 1

		if gen_index < len(generators):
			self.visit_comprehension_generator(generators, 
					gen_index, elt, val, node_type, scope, graph)

		if gen_index >= len(generators):
			if node_type == "DictComp":
				self.visit(val, scope, graph)
				self.visit(elt, scope, graph)
				graph.emit("MAP_ADD", gen_index + 1)

			elif node_type == "SetComp":
				self.visit(elt, scope, graph)
				graph.emit("SET_ADD", gen_index + 1)
			
			elif node_type == "GeneratorExp":
				self.visit(elt, scope, graph)
				graph.emit("YIELD_VALUE")
				graph.emit("POP_TOP")

			graph.next_block(skip)

		graph.next_block(if_cleanup)
		graph.emit("JUMP_ABSOLUTE", start)
		graph.next_block(anchor)

		return

	def compiler_comprehension(self, name, node, elt, val, scope, graph):
		old_scope = scope
		old_graph = graph
		node_type = node.__class__.__name__

		scope = self.scopes[node]
		graph = Assem.PyFlowGraph(name, self.filename, args = (),
				optimized = True, function_block = True)

		graph.set_cell_vars(scope.get_cell_vars())
		graph.set_free_vars(scope.get_free_vars())

		if self.is_type(node, 'DictComp'):
			graph.emit("BUILD_MAP", 0)

		elif self.is_type(node, "SetComp"):
			graph.emit("BUILD_SET", 0)

		self.visit_comprehension_generator(node.generators, 0, elt, val, node_type, scope, graph)
		
		if node_type != "GeneratorExp":
			graph.emit("RETURN_VALUE")
		else:
			graph.set_flag(const.CO_GENERATOR)
			graph.finish(False)

		self.make_closure(0, scope, graph, old_graph)

		scope = old_scope
		graph = old_graph

		self.visit(node.generators[0].iter, scope, graph)

		old_graph.emit("GET_ITER")
		old_graph.emit("CALL_FUNCTION", 1)

		return

	def visit_Yield(self, node, scope, graph):
		scope.generator = 1
		if not isinstance(scope, FunctionScope):
			raise SyntaxError, "can not yield outside funtion"

		if node.value:
			self.visit(node.value, scope, graph)

		else:
			graph.emit("LOAD_CONST", None)

		graph.emit("YIELD_VALUE")

		return

	#
	# auxilary
	#
	def visit_arguments(self, node, scope, graph):
		for index, arg in enumerate(node.args):
			if self.is_type(arg, "Tuple"):
				arg_id = ".%d" % index
				#self._name_op("LOAD", arg_id, scope, graph)
				graph.emit("LOAD_FAST", ".%d" % index)
				self.visit(arg, scope, graph)

		return

