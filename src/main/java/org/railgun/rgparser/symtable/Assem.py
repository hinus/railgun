#-*- coding: UTF-8 -*-
#
# -----------------------------------------------------------------------------
# bytecode generators for python
# author : gzxuwei@corp.netease.com
# date : 2015-08-14
# -----------------------------------------------------------------------------

import const
import dis
import types

RAW = "RAW"
FLAT = "FLAT"
CONV = "CONV"
DONE = "DONE"

class FlowGraph(object):
	def __init__(self):
		super(FlowGraph, self).__init__()
		self.current = self.entry = Block()
		self.exit = Block("exit")
		self.blocks = set()
		self.blocks.add(self.entry)
		self.blocks.add(self.exit)

		self._debug = False

		return

	def start_block(self, block):
		if self._debug:
			if self.current:
				print "end", repr(self.current)
				print "	next", self.current.next
				print "	preve", self.current.prev
				print "	", self.current.get_children()
			print repr(block)

		self.current = block

		return

	def next_block(self, block = None):
		if block is None:
			block = self.new_block()

		self.current.add_next(block)
		self.start_block(block)

		return

	def new_block(self):
		b = Block()
		self.blocks.add(b)
		return b

	def start_exit_block(self):
		self.start_block(self.exit)
		return

	def _enable_debug(self):
		self._debug = True

		return

	def _disable_debug(self):
		self._debug = False

		return

	def emit(self, *inst):
		if len(inst) == 2 and isinstance(inst[1], Block):
			self.current.add_out_edge(inst[1])

		self.current.emit(inst)

		return

	def get_blocks_inorder(self):
		return self.order_blocks()

	def get_blocks(self):
		return list(self.blocks)

	def get_root(self):
		return self.entry

	def get_contained_graphs(self):
		l = []
		for b in self.get_blocks():
			l.extend(b.get_contained_graphs())

		return l

	def order_blocks(self):
		order = []
		remaining = set()
		todo = [self.entry]

		while todo:
			b = todo.pop()
			if b in remaining:
				continue

			remaining.add(b)

			for c in b.get_children():
				if c not in remaining:
					todo.append(c)

		dominators = {}
		for b in remaining:
			dominators.setdefault(b, set())

			for c in b.get_followers():
				while True:
					dominators.setdefault(c, set()).add(b)

					if c.prev and c.prev[0] is not b:
						c = c.prev[0]
					else:
						break

		def find_next():
			for b in remaining:
				for c in dominators[b]:
					if c in remaining:
						break
				else:
					return b

			assert 0, 'circular dependency, cannot find next block'

		b = self.entry

		while True:
			order.append(b)
			remaining.discard(b)

			if b.next:
				b = b.next[0]
				continue

			elif b is not self.exit and not b.has_unconditional_transfer():
				order.append(self.exit)

			if not remaining:
				break

			b = find_next()

		return order

class PyFlowGraph(FlowGraph):
	hasjrel = set()
	for i in dis.hasjrel:
		hasjrel.add(dis.opname[i])
	hasjabs = set()
	for i in dis.hasjabs:
		hasjabs.add(dis.opname[i])

	def __init__(self, name, filename, optimized = 0, args = (), klass = None, function_block = False):
		super(PyFlowGraph, self).__init__()
		self.name = name
		self.filename = filename
		self.docstring = None
		self.args = args
		self.argcount = len(args)
		self.klass = klass
		self.optimized = optimized
		self.function_block = function_block

		if optimized:
			self.flags = const.CO_OPTIMIZED | const.CO_NEWLOCALS
		else:
			self.flags = 0

		self.consts = []
		self.names = []
		self.freevars = []
		self.cellvars = []
		self.closure = []
		self.varnames = []
		self.stage = RAW

		return

	def set_doc_string(self, doc):
		self.docstring = doc

		return

	def set_flag(self, flag):
		self.flags = self.flags | flag
		if flag == const.CO_VARARGS:
			self.argcount = self.argcount - 1

		return

	def check_flag(self, flag):
		if self.flag & flag:
			return 1

	def set_free_vars(self, names):
		self.freevars = list(names)

		return

	def set_cell_vars(self, names):
		self.cellvars = names

		return

	def finish(self, is_lambda):
		self.start_exit_block()
		if not is_lambda:
			self.emit("LOAD_CONST", None)
		self.emit("RETURN_VALUE")

		return

	def get_code(self):
		assert self.stage == RAW
		self.compute_stack_depth()
		self.flatten_graph()
		assert self.stage == FLAT
		self.convert_args()
		assert self.stage == CONV
		self.make_byte_code()
		assert self.stage == DONE
		return self.new_code_object()

	def compute_stack_depth(self):
		depth = {}
		exit = None

		for b in self.get_blocks():
			depth[b] = find_depth(b.get_instructions())

		seen = {}
		
		def max_depth(b, d):
			if b in seen:
				return d
			seen[b] = 1
			d = d + depth[b]
			children = b.get_children()

			if children:
				return max([max_depth(c, d) for c in children])

			else:
				if not b.label == "exit":
					return max_depth(self.exit, d)
				else:
					return d

		self.stacksize = max_depth(self.entry, 0)

		return

	def flatten_graph(self):
		assert self.stage == RAW
		self.insts = insts = []
		pc = 0
		begin = {}
		end = {}

		for b in self.get_blocks_inorder():
			begin[b] = pc
			for inst in b.get_instructions():
				insts.append(inst)

				if len(inst) == 1:
					pc += 1
				elif inst[0] != "SET_LINENO":
					pc += 3

			end[b] = pc
		pc = 0

		for i in range(len(insts)):
			inst = insts[i]
			if len(inst) == 1:
				pc = pc + 1

			elif inst[0] != "SET_LINENO":
				pc += 3

			opname = inst[0]
			if opname in self.hasjrel:
				oparg = inst[1]
				offset = begin[oparg] - pc
				insts[i] = opname, offset

			elif opname in self.hasjabs:
				insts[i] = opname, begin[inst[1]]

		self.stage = FLAT

		return

	def convert_args(self):
		assert self.stage == FLAT
		self.consts.insert(0, self.docstring)
		self.sort_cellvars()

		for i in range(len(self.insts)):
			t = self.insts[i]

			if len(t) == 2:
				opname, oparg = t
				conv_func = self._converters.get(opname, None)

				if conv_func:
					self.insts[i] = opname, conv_func(self, oparg)

		self.stage = CONV

		return

	def sort_cellvars(self):
		cells = {}
		for name in self.cellvars:
			cells[name] = 1

		self.cellvars = [name for name in self.varnames if name in cells]

		for name in self.cellvars:
			del cells[name]

		self.cellvars = self.cellvars + cells.keys()
		self.closure = self.cellvars + self.freevars

		return

	def _lookup_name(self, name, l):
		t = type(name)
		for index, item in enumerate(l):
			if t == type(item) and item == name:
				return index

		end = len(l)
		l.append(name)
		return end

	_converters = {}
	def _convert_LOAD_CONST(self, arg):
		if hasattr(arg, 'get_code'):
			arg = arg.get_code()

		return self._lookup_name(arg, self.consts)

	def _convert_LOAD_FAST(self, arg):
		self._lookup_name(arg, self.names)
		return self._lookup_name(arg, self.varnames)

	_convert_STORE_FAST = _convert_LOAD_FAST
	_convert_DELETE_FAST = _convert_LOAD_FAST

	def _convert_LOAD_NAME(self, arg):
		if self.klass is None:
			self._lookup_name(arg, self.varnames)
		return self._lookup_name(arg, self.names)

	_convert_STORE_NAME = _convert_LOAD_NAME
	_convert_DELETE_NAME = _convert_LOAD_NAME
	_convert_IMPORT_NAME = _convert_LOAD_NAME
	_convert_IMPORT_FROM = _convert_LOAD_NAME
	_convert_STORE_ATTR = _convert_LOAD_NAME
	_convert_LOAD_ATTR = _convert_LOAD_NAME
	_convert_DELETE_ATTR = _convert_LOAD_NAME
	_convert_LOAD_GLOBAL = _convert_LOAD_NAME
	_convert_STORE_GLOBAL = _convert_LOAD_NAME
	_convert_DELETE_GLOBAL = _convert_LOAD_NAME

	def _convert_DEREF(self, arg):
		self._lookup_name(arg, self.names)
		self._lookup_name(arg, self.varnames)
		return self._lookup_name(arg, self.closure)

	_convert_LOAD_DEREF = _convert_DEREF
	_convert_STORE_DEREF = _convert_DEREF

	def _convert_LOAD_CLOSURE(self, arg):
		self._lookup_name(arg, self.varnames)
		return self._lookup_name(arg, self.closure)

	_cmp = list(dis.cmp_op)
	def _convert_COMPARE_OP(self, arg):
		return self._cmp.index(arg)

	for name, obj in locals().items():
		if name[:9] == "_convert_":
			opname = name[9:]
			_converters[opname] = obj

	del name, obj, opname

	opnum = {}
	for num in range(len(dis.opname)):
		opnum[dis.opname[num]] = num
	del num

	def make_byte_code(self):
		assert self.stage == CONV
		self.lnotab = lnotab = LineNumberTable()

		for t in self.insts:
			opname = t[0]
			if len(t) == 1:
				lnotab.add_code(self.opnum[opname])

			else:
				oparg = t[1]

				if opname == "SET_LINENO":
					lnotab.next_line(oparg)
					continue

				hi, lo = twobyte(oparg)

				try:
					lnotab.add_code(self.opnum[opname], lo, hi)
				except ValueError:
					print opname, oparg
					print self.opnum[opname], lo, hi
					raise

		self.stage = DONE

	def new_code_object(self):
		assert self.stage == DONE

		if (self.flags & const.CO_NEWLOCALS) == 0:
			nlocals = 0
		else:
			nlocals = len(self.varnames)

		argcount = self.argcount

		return types.CodeType(argcount, nlocals, self.stacksize, self.flags,
				self.lnotab.get_code(), self.get_consts(),
				tuple(self.names), tuple(self.varnames),
				self.filename, self.name, self.lnotab.firstline,
				self.lnotab.get_table(), tuple(self.freevars),
				tuple(self.cellvars))

	def get_consts(self):
		l = []
		for elt in self.consts:
			if isinstance(elt, PyFlowGraph):
				elt = elt.get_code()
			l.append(elt)

		return tuple(l)

def is_jump(opname):
	if opname[:4] == "JUMP":
		return 1

def twobyte(val):
	assert isinstance(val, int)
	return divmod(val, 256)

class Block(object):
	_count = 0

	def __init__(self, label = ''):
		self.insts = []
		self.out_edges = set()
		self.label = label
		self.bid = Block._count
		self.next = []
		self.prev = []
		Block._count = Block._count + 1

	def __repr__(self):
		if self.label:
			return "<block %s id=%d>" % (self.label, self.bid)
		else:
			return "<block id=%d>" % (self.bid)

	def __str__(self):
		insts = map(str, self.insts)
		return "<block %s %d:\n%s>" % (self.label, self.bid, '\n'.join(insts))

	def emit(self, inst):
		self.insts.append(inst)

		return

	def get_instructions(self):
		return self.insts

	def add_out_edge(self, block):
		self.out_edges.add(block)
		return

	def add_next(self, block):
		self.next.append(block)
		block.prev.append(self)

		return

	_uncond_transfer = ('RETURN_VALUE', 'RAISE_VARARGS', 'JUMP_ABSOLUTE',
			'JUMP_FORWARD', 'CONTINUE_LOOP',)

	def has_unconditional_transfer(self):
		try:
			op, arg = self.insts[-1]
		except (IndexError, ValueError):
			return

		return op in self._uncond_transfer

	def get_children(self):
		return list(self.out_edges) + self.next

	def get_followers(self):
		followers = set(self.next)
		for inst in self.insts:
			if inst[0] in PyFlowGraph.hasjrel:
				followers.add(inst[1])

		return followers

	def get_contained_graphs(self):
		contained = []

		for inst in self.insts:
			if len(inst) == 1:
				continue

			arg = inst[1]
			if hasattr(arg, 'graph'):
				contained.append(arg.graph)

		return contained

class LineNumberTable(object):
	def __init__(self):
		super(LineNumberTable, self).__init__()

		self.code = []
		self.code_offset = 0
		self.firstline = 0
		self.lastline = 0
		self.lastoff = 0
		self.lnotab = []

		return

	def add_code(self, *args):
		for arg in args:
			self.code.append(chr(arg))

		self.code_offset += len(args)

		return

	def next_line(self, lineno):
		if self.firstline == 0:
			self.firstline = lineno
			self.lastline = lineno

		else:
			addr = self.code_offset - self.lastoff
			line = lineno - self.lastline

			if line >= 0:
				push = self.lnotab.append
				while addr > 255:
					push(255)
					push(0)
					addr -= 255

				while line > 255:
					push(addr)
					push(255)
					line -= 255
					addr = 0

				if addr > 0 or line > 0:
					push(addr)
					push(line)

				self.lastline = lineno
				self.lastoff = self.code_offset

		return

	def get_code(self):
		return ''.join(self.code)

	def get_table(self):
		return ''.join(map(chr, self.lnotab))

class StackDepthTracker:
	# XXX 1. need to keep track of stack depth on jumps
	# XXX 2. at least partly as a result, this code is broken

	def find_depth(self, insts, debug=0):
		depth = 0
		maxDepth = 0
		for i in insts:
			opname = i[0]
			delta = self.effect.get(opname, None)
			if delta is not None:
				depth = depth + delta
			else:
				# now check patterns
				for pat, pat_delta in self.patterns:
					if opname[:len(pat)] == pat:
						delta = pat_delta
						depth = depth + delta
						break
				# if we still haven't found a match
				if delta is None:
					meth = getattr(self, opname, None)
					if meth is not None:
						depth = depth + meth(i[1])
			if depth > maxDepth:
				maxDepth = depth
		return maxDepth

	effect = {
		'POP_TOP': -1,
		'DUP_TOP': 1,
		'LIST_APPEND': -1,
		'SET_ADD': -1,
		'MAP_ADD': -2,
		'SLICE+1': -1,
		'SLICE+2': -1,
		'SLICE+3': -2,
		'STORE_SLICE+0': -1,
		'STORE_SLICE+1': -2,
		'STORE_SLICE+2': -2,
		'STORE_SLICE+3': -3,
		'DELETE_SLICE+0': -1,
		'DELETE_SLICE+1': -2,
		'DELETE_SLICE+2': -2,
		'DELETE_SLICE+3': -3,
		'STORE_SUBSCR': -3,
		'DELETE_SUBSCR': -2,
		# PRINT_EXPR?
		'PRINT_ITEM': -1,
		'RETURN_VALUE': -1,
		'YIELD_VALUE': -1,
		'EXEC_STMT': -3,
		'BUILD_CLASS': -2,
		'STORE_NAME': -1,
		'STORE_ATTR': -2,
		'DELETE_ATTR': -1,
		'STORE_GLOBAL': -1,
		'BUILD_MAP': 1,
		'COMPARE_OP': -1,
		'STORE_FAST': -1,
		'IMPORT_STAR': -1,
		'IMPORT_NAME': -1,
		'IMPORT_FROM': 1,
		'LOAD_ATTR': 0, # unlike other loads
		# close enough...
		'SETUP_EXCEPT': 3,
		'SETUP_FINALLY': 3,
		'FOR_ITER': 1,
		'WITH_CLEANUP': -1,
		}

	# use pattern match
	patterns = [
		('BINARY_', -1),
		('LOAD_', 1),
		]

	def UNPACK_SEQUENCE(self, count):
		return count-1

	def BUILD_TUPLE(self, count):
		return -count+1

	def BUILD_LIST(self, count):
		return -count+1

	def BUILD_SET(self, count):
		return -count+1

	def CALL_FUNCTION(self, argc):
		hi, lo = divmod(argc, 256)
		return -(lo + hi * 2)

	def CALL_FUNCTION_VAR(self, argc):
		return self.CALL_FUNCTION(argc)-1

	def CALL_FUNCTION_KW(self, argc):
		return self.CALL_FUNCTION(argc)-1

	def CALL_FUNCTION_VAR_KW(self, argc):
		return self.CALL_FUNCTION(argc)-2

	def MAKE_FUNCTION(self, argc):
		return -argc

	def MAKE_CLOSURE(self, argc):
		# XXX need to account for free variables too!
		return -argc

	def BUILD_SLICE(self, argc):
		if argc == 2:
			return -1
		elif argc == 3:
			return -2

	def DUP_TOPX(self, argc):
		return argc

find_depth = StackDepthTracker().find_depth
