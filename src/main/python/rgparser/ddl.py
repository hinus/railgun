#-*- coding: UTF-8 -*-
#
# -----------------------------------------------------------------------------
# parser for dragon sword
# author : gzxuwei@corp.netease.com
# date : 2013-11-03
# -----------------------------------------------------------------------------

import sys, ast
import marshal
import py_compile
import time
sys.path.insert(0,"./ddlib")

if sys.version_info[0] >= 3:
    raw_input = input

exec_file = ''
_debug = False

tokens = (
	'NEWLINE',
	'ENDMARKER',
	'STRING',
	
	'TAG_CLASS',
	'TAG_DEF',
	'TAG_LAMBDA',
	'TAG_FROM',
	'TAG_AS',
	'TAG_GLOBAL',
	
	'TAG_IF',
	'TAG_ELSE',
	'TAG_ELIF',
	'TAG_FOR',
	'TAG_WHILE',
	'TAG_TRY',
	'TAG_EXCEPT',
	'TAG_FINALLY',
	
	'TAG_DRAW',
	'TAG_PASS',
	'TAG_DEL',
	'TAG_BREAK',
	'TAG_CONTINUE',
	'TAG_RETURN',
	'TAG_RAISE',
	'TAG_EXEC',
	'TAG_ASSERT',
	'TAG_YIELD',
	'TAG_IMPORT',
	
	'TAG_OR',
	'TAG_AND',
	'TAG_NOT',
	'TAG_IN',
	'TAG_IS',
	
	'OP_LE',
	'OP_GE',
	'OP_EQ',
	'OP_NE',
	'OP_NNE',
	
	'OP_LEFT_SHIFT',
	'OP_RIGHT_SHIFT',
	'OP_EXACT_DIVISION',
	'OP_POWER',

	'ADD_ASN',
	'SUB_ASN',
	'MUL_ASN',
	'DIV_ASN',
	'MOD_ASN',
	'AND_ASN',
	'OR_ASN',
	'XOR_ASN',
	'LSHIFT_ASN',
	'RSHIFT_ASN',
	'POW_ASN',
	'FDIV_ASN',
	
	'NAME',
	'NUMBER',
    )

Add = ast.Add()
Sub = ast.Sub()
Mult = ast.Mult()
Div = ast.Div()
Mod = ast.Mod()
Pow = ast.Pow()
LShift = ast.LShift()
RShift = ast.RShift()
BitOr = ast.BitOr()
BitAnd = ast.BitAnd()
BitXor = ast.BitXor()
FloorDiv = ast.FloorDiv()

op_dict = {
	"+" : Add,
	"-" : Sub,
	"*" : Mult,
	"/" : Div,
	"//" : FloorDiv,
	"%" : Mod,
	"**" : Pow,
	"<<" : LShift,
	">>" : RShift,
	"|" : BitOr,
	"&" : BitAnd,
	"^" : BitXor,

	"+=" : Add,
	"-=" : Sub,
	"*=" : Mult,
	"/=" : Div,
	"%=" : Mod,
	"**=" : Pow,
	"<<=" : LShift,
	">>=" : RShift,
	"|=" : BitOr,
	"&=" : BitAnd,
	"^=" : BitXor,
	"//=" : FloorDiv,
}
	
# 递归下降地设置Context属性
def set_context(obj, ctx):
	if isinstance(obj, ast.Tuple):
		for item in obj.elts:
			set_context(item, ctx)

	elif isinstance(obj, list):
		for item in obj:
			set_context(item, ctx)

		return

	obj.ctx = ctx
		
	return


# 分析的起点
def p_file_input(p):
	'''file_input : ENDMARKER
			| file_content ENDMARKER'''

	if len(p) == 3:
		item = p[1]
		while isinstance(item, list):
			item = item[0]

		p[0] = ast.Module(p[1], lineno = item.lineno, col_offset = item.col_offset)
		print ast.dump(p[0])
	codeobject = compile(p[0], '<string>', 'exec')
	print exec_file
	with open(exec_file + 'b', 'wb') as fc:
		print exec_file
		fc.write('\0\0\0\0')
		py_compile.wr_long(fc, long(time.time()))
		marshal.dump(codeobject, fc)
		fc.flush()
		fc.seek(0, 0)
		fc.write(py_compile.MAGIC)
		
	if not _debug:
		co = compile(p[0], exec_file, 'exec')
		#exec co

	return
	
def p_file_content(p):
	'''file_content : file_content NEWLINE
			| file_content stmt
			| NEWLINE
			| stmt'''
			
	if len(p) == 2:
		p[0] = []
		if p.get_item(1).type == "stmt":
			p[0].append(p[1])
	else:
		p[0] = p[1]
		if p.get_item(2).type == "stmt":
			p[0].append(p[2])

	return

def p_decorator(p):
	'''decorator : "@" dotted_name NEWLINE
		| "@" dotted_name "(" ")" NEWLINE
		| "@" dotted_name "(" arglist ")" NEWLINE
		'''

	if len(p[2]) == 1:
		p[2] = ast.Name(id = p[2], ctx = ast.Load(), lineno = 0, col_offset = 0)
	
	elif len(p[2]) > 1:
		left = p[2][0]
		to_treat = p[2][1:]
		attr = None

		for right in to_treat:
			attr = ast.Attribute(value = left, attr = right, 
				lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos, 
				ctx = ast.Load())

		p[2] = attr

	if len(p) == 4:
		p[0] = p[2]

	elif len(p) == 6:
		p[0]= ast.Call(func = p[2], args = [], keywords = [], starargs = None, kwargs = None,
				lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	return

def p_decorators(p):
	'''decorators : decorator
		| decorators decorator'''

	if len(p) == 2:
		p[0] = [p[1],]
	else:
		p[0] = p[1]
		p[0].append(p[2])

	return

def p_decorated(p):
	'''decorated : decorators classdef
		| decorators funcdef'''

	p[0] = p[2]
	p[0].decorator_list = p[1]

	return

def p_classdef(p):
	'''classdef : TAG_CLASS NAME ":" suite
			| TAG_CLASS NAME "(" testlist ")" ":" suite
			| TAG_CLASS NAME "(" ")" ":" suite'''
	
	p[0] = ast.ClassDef(name = p[2], bases = [], body = None, decorator_list = [], 
		lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	if len(p) == 5:
		p[0].body = p[4]

	elif len(p) == 8:
		base = p[4]
		if not isinstance(base, list):
			base = [base,]

		p[0].bases = base
		p[0].body = p[7]

	elif len(p) == 7:
		p[0].body = p[6]

	return
	
def p_exprlist(p):
	'''exprlist : expr
			| exprlist "," expr'''
			
	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		if isinstance(p[1], ast.Tuple):
			p[0] = p[1]
		else:
			p[0] = ast.Tuple(elts = [p[1],], ctx = ast.Load(), 
				lineno = p[1].lineno, col_offset = p[1].col_offset)

		p[0].elts.append(p[3])

	return
			
def p_expr(p):
	'''expr : xor_expr
			| expr "|" xor_expr'''
	
	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		item = p[1]
		while isinstance(item, list):
			item = item[0]

		p[0] = ast.BinOp(left = p[1], op = ast.BitOr(), right = p[3],
				lineno = item.lineno, col_offset = item.col_offset)

	return
	
def p_xor_expr(p):
	'''xor_expr : and_expr
			| xor_expr "^" and_expr'''
			
	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		item = p[1]
		while isinstance(item, list):
			item = item[0]

		p[0] = ast.BinOp(left = p[1], op = BitXor, right = p[3],
				lineno = item.lineno, col_offset = item.col_offset)

	return

def p_and_expr(p):
	'''and_expr : shift_expr
			| and_expr "&" shift_expr'''

	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		item = p[1]
		while isinstance(item, list):
			item = item[0]

		p[0] = ast.BinOp(left = p[1], op = BitAnd, right = p[3],
			lineno = item.lineno, col_offset = item.col_offset)

	return
			
def p_shift_expr(p):
	'''shift_expr : arith_expr
			| shift_expr OP_LEFT_SHIFT arith_expr
			| shift_expr OP_RIGHT_SHIFT arith_expr'''
			
	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		item = p[1]
		while isinstance(item, list):
			item = item[0]

		p[0] = ast.BinOp(left = p[1], op = op_dict.get(p[2]), right = p[3],
			lineno = item.lineno, col_offset = item.col_offset)

	return
	
def p_arith_expr(p):
	'''arith_expr : term
			| arith_expr "+" term
			| arith_expr "-" term'''
	
	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		p[0] = ast.BinOp(p[1], op_dict.get(p[2]), p[3], lineno = p[1].lineno, col_offset = p[1].col_offset)
			
	return
	
def p_term(p):
	'''term : term "*" factor
			| term "/" factor
			| term "%" factor
			| term OP_EXACT_DIVISION factor
			| factor '''

	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		item = p[1]
		while isinstance(item, list):
			item = item[0]

		p[0] = ast.BinOp(left = p[1], op = op_dict.get(p[2]), right = p[3], lineno = item.lineno, col_offset = item.col_offset)

	return
			
def p_factor(p):
	'''factor : "+" factor
			| "-" factor
			| "~" factor
			| power'''

	if len(p) == 2:
		p[0] = p[1]
		
	else:
		item = p.get_item(1)
		if p[1] == "+":
			p[0] = ast.UnaryOp(op = ast.UAdd(), operand = p[2], lineno = item.lineno, col_offset = item.lexpos)
		
		elif p[1] == "-":
			p[0] = ast.UnaryOp(op = ast.USub(), operand = p[2], lineno = item.lineno, col_offset = item.lexpos)
		
		elif p[1] == "~":
			p[0] = ast.UnaryOp(op = ast.Invert(), operand = p[2], lineno = item.lineno, col_offset = item.lexpos)
			
	return
	
def p_power(p):
	'''power : atom
			| atom trailers
			| atom OP_POWER factor
			| atom trailers OP_POWER factor'''

	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 3 or len(p) == 5:
		item = p[2]
		old_item = p[2]

		while item:
			if isinstance(item, ast.Call):
				old_item = item
				item = item.func

			else:
				old_item = item
				item = item.value

		p[0] = p[2]
		if isinstance(old_item, ast.Call):
			old_item.func = p[1]
		else:
			old_item.value = p[1]

		item = p[1]
		while isinstance(item, list):
			item = item[0]

		p[0].lineno = item.lineno
		p[0].col_offset = item.col_offset

	elif len(p) == 4:
		p[0] = ast.BinOp(p[1], Pow, p[3], lineno = p[1].lineno, col_offset = p[1].col_offset)

	# 把 trailor 处理完了，再处理pow
	if len(p) == 5:
		p[0] = ast.BinOp(p[0], Pow, p[4], lineno = p[1].lineno, col_offset = p[1].col_offset)
			
	return
	
def p_trailers(p):
	'''trailers : trailers trailer
			| trailer'''

	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 3:
		if isinstance(p[2], ast.Call):
			p[0] = p[2]
			p[0].func = p[1]
			p[0].lineno = p[1].lineno
			p[0].col_offset = p[1].col_offset

		elif isinstance(p[2], ast.Attribute):
			p[0] = p[2]
			p[0].value = p[1]
			p[0].lineno = p[1].lineno
			p[0].col_offset = p[1].col_offset
			
	return
	
def p_trailer(p):
	'''trailer : "(" ")"
			| "(" arglist ")"
			| "[" subscriptlist "]"
			| "." NAME'''

	if p[1] == "(": # call function, the first element is type
		p[0] = ast.Call(func = None, args = [], keywords = [], starargs = None, kwargs = None, lineno = 0, col_offset = 0)
		if len(p) == 4:
			p[0].args = p[2]

	elif p[1] == "[":
		p[0] = ast.Subscript(value = None, slice = p[2], lineno = 0, col_offset = 0, ctx = ast.Load())

	elif p[1] == ".":
		p[0] = ast.Attribute(value = None, attr = p[2], lineno = 0, col_offset = 0, ctx = ast.Load())

	return

	
def p_arglist_piece(p):
	'''arglist_piece : argument
			| arglist_piece "," argument'''

	if len(p) == 2:
		p[0] = [p[1],]
	else:
		p[0] = p[1]
		p[0].append(p[3])
	
	return
	
	
def p_arglist(p):
	'''arglist : arglist_piece
			| arglist_piece ","'''
			
	p[0] = p[1]
	return
	
def p_argument(p):
	'''argument : test
			| test comp_for
			| test "=" test'''

	if len(p) == 2:
		p[0] = p[1]
	return
	
def p_subscriptlist(p):
	'''subscriptlist : subscriptlist "," subscript
			| subscriptlist ","
			| subscript'''
			
	if len(p) == 2:
		p[0] = p[1]

	return
			
def p_subscript(p):
	'''subscript : "." "." "."
			| test
			| ":"
			| test ":"
			| ":" test
			| test ":" test
			| ":" sliceop
			| test ":" sliceop
			| ":" test sliceop
			| test ":" test sliceop'''
	
	if len(p) == 2 and p.get_item(1).type == "test":
		p[0] = ast.Index(value = p[1], ctx = ast.Load(), lineno = p[1].lineno, col_offset = p[1].col_offset)

	elif len(p) == 2 and p[1] == ":":
		p[0] = ast.Slice(lower = None, upper = None, step = None, lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

			
	return
	
def p_sliceop(p):
	'''sliceop : ":"
			| ":" test'''
			
	return
	
def p_atom(p):
	'''atom : "(" ")"
			| "(" yield_expr ")"
			| "(" testlist_comp ")"
			| "[" "]"
			| "[" listmaker "]"
			| "{" "}"
			| "{" dictormaker "}"
			| "{" setmaker "}"
			| "`" testlist1 "`"
			| NAME
			| NUMBER
			| strings'''
			
	if len(p) == 2:
		item = p.get_item(1)
		if isinstance(item, ddlex.LexToken):
			if item.type == "NUMBER":
				p[0] = ast.Num(eval(p[1]), lineno = item.lineno, col_offset = item.lexpos)
			elif item.type == "NAME":
				p[0] = ast.Name(id = p[1], ctx = ast.Load(), lineno = item.lineno, col_offset = item.lexpos)

		elif item.type == "strings":
			p[0] = p[1]
			p[0].s = ''.join(p[0].s)

	elif len(p) == 3:
		if p[1] == "[":
			p[0] = ast.List(elts = [], ctx = ast.Load(), lineno = p.get_item(1).lineno,
				col_offset = p.get_item(1).lexpos)
		
	elif len(p) == 4:
		if p[1] == "(":
			p[0] = p[2]
			p[0].lineno = p.get_item(1).lineno
			p[0].col_offset = p.get_item(1).lexpos

		elif p[1] == "[":
			p[0] = ast.List(elts = p[2].elts, ctx= ast.Load(),
				lineno = p.get_item(1).lineno,
				col_offset = p.get_item(1).lexpos)

		elif p[1] == "{" and p.get_item(2).type == "dictormaker":
			p[0] = p[2]
			p[0].lineno = p.get_item(1).lineno
			p[0].col_offset = p.get_item(1).lexpos

	return

def p_strings(p):
	'''strings : strings STRING
		| STRING'''

	if len(p) == 2:
		p[0] = ast.Str(s = [eval(p[1]),], lineno = p.get_item(1).lineno,
			col_offset = p.get_item(1).lexpos)

	else:
		p[0] = p[1]
		p[0].s.append(eval(p[2]))

	return
	
def p_testlist1(p):
	'''testlist1 : test
			| testlist1 "," test'''
			
	return
	
def p_listmaker(p):
	'''listmaker : testlist
			| test list_for'''
			
	if len(p) == 2:
		p[0] = p[1]

	return
	
def p_dictormaker_piece(p):
	'''dictormaker_piece : test ":" test
		| dictormaker_piece "," test ":" test'''
	
	if len(p) == 4:
		p[0] = ast.Dict(keys = [p[1],], values = [p[3],], lineno = 0, col_offset = 0)

	elif len(p) == 6:
		p[0] = p[1]
		p[0].keys.append(p[3])
		p[0].values.append(p[5])

	return
	
def p_dictormaker(p):
	'''dictormaker : dictormaker_piece
			| dictormaker_piece ","
			| test ":" test comp_for
			'''
	if len(p) == 2 or len(p) == 3:
		p[0] = p[1]

	return

def p_setmaker_piece(p):
	'''setmaker_piece : test
		| setmaker_piece "," test'''
	return

def p_setmaker(p):
	'''setmaker : setmaker_piece
		| setmaker_piece ","
		| test comp_for'''

	return
	
def p_testlist_comp(p):
	'''testlist_comp : testlist
			| test comp_for'''
			
	if len(p) == 2:
		p[0] = p[1]

	return
	
	
def p_comp_iter(p):
	'''comp_iter : comp_for
			| comp_if'''
	
def p_comp_for(p):
	'''comp_for : TAG_FOR exprlist TAG_IN or_test
			| TAG_FOR exprlist TAG_IN or_test comp_iter'''
			
	return
	
def p_comp_if(p):
	'''comp_if : TAG_IF old_test
			| TAG_IF old_test comp_iter'''
			
	return
	
def p_list_iter(p):
	'''list_iter : list_for
			| list_if'''

	return
	
def p_list_for(p):
	'''list_for : TAG_FOR exprlist TAG_IN testlist_safe
			| TAG_FOR exprlist TAG_IN testlist_safe list_iter'''
	return
	
def p_list_if(p):
	'''list_if : TAG_IF old_test
			| TAG_IF old_test list_iter'''
			
	return
	
def p_testlist(p):
	'''testlist : testlist_anns
			| testlist_anns ","'''
			
	if len(p) == 2:
		if isinstance(p[1], list):
			item = p[1]
			while isinstance(item, list):
				item = item[0]

			p[0] = ast.Tuple(elts = p[1], ctx = ast.Load(), lineno = item.lineno, col_offset = item.col_offset)
		else:
			p[0] = p[1]

	elif len(p) == 3:
		if isinstance(p[1], list):
			item = p[1]
			while isinstance(item, list):
				item = item[0]

			p[0] = ast.Tuple(elts = p[1], ctx = ast.Load(), lineno = item.lineno, col_offset = item.col_offset)
		else:
			p[0] = ast.Tuple(elts = [p[1],], ctx = ast.Load(), lineno = p[1].lineno, col_offset = p[1].col_offset)

	return
	
def p_testlist_anns(p):
	'''testlist_anns : testlist_anns "," test
			| test'''
			
	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		p[0] = p[1]
		if isinstance(p[0], list):
			p[0].append(p[3])
		else:
			p[0] = [p[1], p[3]]

	return
	
def p_test(p):
	'''test : or_test
			| or_test TAG_IF or_test TAG_ELSE test
			| lambdef'''

	if len(p) == 2:
		p[0] = p[1]

	return
	
def p_or_test(p):
	'''or_test : and_test
			| or_test TAG_OR and_test'''
			
	if len(p) == 2:
		p[0] = p[1]
	
	else:
		p[0] = ast.BoolOp(op = ast.Or(), values = [p[1], p[3]], lineno = p[1].lineno, col_offset = p[1].col_offset)

	return
	
def p_and_test(p):
	'''and_test : not_test
			| and_test TAG_AND not_test'''
			
	if len(p) == 2:
		p[0] = p[1]
	
	else:
		p[0] = ast.BoolOp(op = ast.And(), values = [p[1], p[3]], lineno = p[1].lineno, col_offset = p[1].col_offset)

	return
	
def p_not_test(p):
	'''not_test : TAG_NOT not_test
			| comparison'''
			
	if len(p) == 2:
		p[0] = p[1]
		
	else:
		p[0] = ast.UnaryOp(op = ast.Not(), operand = p[2], lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	return
	

def p_comparison(p):
	'''comparison : expr
			| comparison comp_op expr'''
	
	if len(p) == 2:
		p[0] = p[1]

	elif len(p) == 4:
		if isinstance(p[1], ast.Compare):
			p[0] = p[1]
			p[0].ops.append(p[2])
			p[0].comparators.append(p[3])
		else:
			p[0] = ast.Compare(left = p[1], ops = [p[2], ], comparators = [p[3],],
				lineno = p[1].lineno, col_offset = p[1].col_offset)

	return
	
def p_comp_op(p):
	'''comp_op : ">"
			| "<"
			| OP_EQ
			| OP_GE
			| OP_LE
			| OP_NE
			| OP_NNE
			| TAG_IN
			| TAG_NOT TAG_IN
			| TAG_IS
			| TAG_IS TAG_NOT'''

	if len(p) == 2:
		if p.get_item(1).type == 'OP_EQ':
			p[0] = ast.Eq()

		elif p.get_item(1).type == '>':
			p[0] = ast.Gt()

		elif p.get_item(1).type == '<':
			p[0] = ast.Lt()

		elif p.get_item(1).type == 'OP_GE':
			p[0] = ast.GtE()

		elif p.get_item(1).type == 'OP_LE':
			p[0] = ast.LtE()

		elif p.get_item(1).type == 'OP_NE':
			p[0] = ast.NotEq()

		elif p.get_item(1).type == 'OP_NNE':
			p[0] = ast.NotEq()

		elif p[1] == 'is':
			p[0] = ast.Is()

		elif p[1] == 'in':
			p[0] = ast.In()

	elif len(p) == 3:
		if p[1] == 'is':
			p[0] = ast.IsNot()

		elif p[1] == 'not':
			p[0] = ast.NotIn()

	return
	
def p_lambdef(p):
	'''lambdef : TAG_LAMBDA ":" test
			| TAG_LAMBDA varargslist ":" test'''
			
	return
	

def p_varargslist(p):
	'''varargslist : varargs_one "," varargs_two
			| varargs_two
			| varargs_one
			| varargs_one ","'''

	if len(p) == 2:
		if p.get_item(1).type == "varargs_one":
			item = p[1]
			while isinstance(item, list):
				item = item[0]

			p[0] = ast.arguments(args = p[1], vararg = None, kwarg = None, defaults = [], lineno = item.lineno, col_offset = item.col_offset)
	return
	
def p_varargs_one(p):
	'''varargs_one : varargs_one "," fpdef
			| varargs_one "," fpdef "=" test
			| fpdef
			| fpdef "=" test'''

	if len(p) == 2:
		p[0] = []
		p[0].append(p[1])

	elif len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])

	return

def p_varargs_two(p):
	'''varargs_two : "*" NAME
		| OP_POWER NAME
		| "*" NAME "," OP_POWER NAME '''

	return

def p_fpdef(p):
	'''fpdef : NAME
			| "(" fplist ")"'''
	
	if len(p) == 2:
		item = p.get_item(1)
		p[0] = ast.Name(id = p[1], ctx = ast.Param(), lineno = item.lineno, col_offset = item.lexpos)

	return
	
def p_fplist_top(p):
	'''fplist_top : fpdef
			| fplist_top "," fpdef'''
	
	return
	
def p_fplist(p):
	'''fplist : fplist_top
			| fplist_top ","'''
	
	return
	
	
def p_funcdef(p):
	'''funcdef : TAG_DEF NAME parameters suite'''

	p[0] = ast.FunctionDef(name = p[2], args = p[3], body = p[4], decorator_list = [], lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	return
	
def p_parameters(p):
	'''parameters : "(" ")"
			| "(" varargslist ")"'''
	
	if len(p) == 3:
		p[0] = ast.arguments([], None, None, [], lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)
	else:
		p[0] = p[2]

	return
	
def p_suite(p):
	'''suite : "{" stmts "}"'''

	if len(p) == 2:
		p[0] = p[1]

	else:
		p[0] = p[2]
			
	return
	
def p_testlist_safe_piece(p):
	'''testlist_safe_piece : old_test
		| testlist_safe_piece "," old_test'''
	
	return
	
def p_testlist_safe(p):
	'''testlist_safe : testlist_safe_piece
			| testlist_safe_piece ","'''
			
	return
	
def p_old_test(p):
	'''old_test : or_test 
			| old_lambdef'''
			
	return
	
def p_old_lambdef(p):
	'''old_lambdef : TAG_LAMBDA ":" old_test
			| TAG_LAMBDA varargslist ":" old_test'''
			
	return
	
def p_stmts(p):
	'''stmts : stmt
			| stmts stmt'''
			
	p[0] = []

	if len(p) == 2:
		p[0].append(p[1])
	elif len(p) == 3:
		p[0] = p[1]
		p[0].append(p[2])

	return
	
def p_stmt(p):
	'''stmt : simple_stmt
			| compound_stmt'''
	
	p[0] = p[1]

	return
	
def p_compound_stmt(p):
	'''compound_stmt : if_stmt
			| while_stmt
			| for_stmt
			| try_stmt
			| funcdef
			| classdef
			| decorated'''

	p[0] = p[1]

	return
	
def p_if_stmt(p):
	'''if_stmt : TAG_IF "(" test ")" suite
			| TAG_IF "(" test ")" suite TAG_ELSE suite
			| TAG_IF "(" test ")" suite elif_list
			| TAG_IF "(" test ")" suite elif_list TAG_ELSE suite'''
			
	this_orelse = []
	if len(p) == 8:
		this_orelse = p[7]

	elif len(p) == 7:
		this_orelse = [p[6],]

	elif len(p) == 9:
		this_orelse = [p[6],]

		item = p[6]
		while len(item.orelse) > 0 and isinstance(item.orelse[0], ast.If):
			item = item.orelse[0]

		item.orelse = p[8]

	p[0] = ast.If(test = p[3], body = p[5], orelse = this_orelse, 
		lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	return
	
def p_while_stmt(p):
	'''while_stmt : TAG_WHILE "(" test ")" suite
			| TAG_WHILE "(" test ")" suite TAG_ELSE suite'''
	
	p[0] = ast.While(test = p[3], body = p[5], orelse = [], lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	if len(p) == 8:
		p[0].orelse = p[7]

	return
	
def p_for_stmt(p):
	'''for_stmt : TAG_FOR exprlist TAG_IN testlist ":" suite
			| TAG_FOR exprlist TAG_IN testlist ":" suite TAG_ELSE ":" suite'''
	
	if len(p) == 7:
		this_orelse = []

	elif len(p) == 10:
		this_orelse = p[9]

	set_context(p[2], ast.Store())

	p[0] = ast.For(target = p[2], iter = p[4],
		body = p[6], orelse = this_orelse,
		lineno = p.get_item(1).lineno,
		col_offset = p.get_item(1).lexpos)
	
	return

def p_try_stmt(p):
	'''try_stmt : TAG_TRY ":" suite TAG_FINALLY ":" suite
		| TAG_TRY ":" suite except_clauses
		| TAG_TRY ":" suite except_clauses TAG_ELSE ":" suite
		| TAG_TRY ":" suite except_clauses TAG_FINALLY ":" suite
		| TAG_TRY ":" suite except_clauses TAG_ELSE ":" suite TAG_FINALLY ":" suite
		'''
	return

def p_except_clauses(p):
	'''except_clauses : except_clauses except_clause ":" suite
		| except_clause ":" suite'''
	return

def p_except_clause(p):
	'''except_clause : TAG_EXCEPT
		| TAG_EXCEPT test
		| TAG_EXCEPT test TAG_AS test
		| TAG_EXCEPT test "," test '''

	return
	
def p_elif_list(p):
	'''elif_list : TAG_ELIF test ":" suite
			| elif_list TAG_ELIF test ":" suite'''
	
	if len(p) == 5:
		p[0] = ast.If(test = p[2], body = p[4],
			orelse = [], lineno = p.get_item(1).lineno,
			col_offset = p.get_item(1).lexpos)

	else:
		p[0] = p[1]
		p[0].orelse = [ast.If(test = p[3], body = p[5], orelse = [],
			lineno = p[1].lineno, col_offset = p[1].col_offset),]
	
	return
	
def p_simple_stmt(p):
	'''simple_stmt : simple_stmt ";" small_stmt NEWLINE
			| simple_stmt ";" small_stmt ";" NEWLINE
			| small_stmt NEWLINE
			| small_stmt ";" NEWLINE'''
			
	if len(p) == 3:
		p[0] = p[1]
	
	elif len(p) == 4:
		p[0] = p[1]

	return
	
def p_small_stmt(p):
	'''small_stmt : expr_stmt
			| print_stmt
			| del_stmt
			| pass_stmt
			| flow_stmt
			| import_stmt
			| global_stmt
			| exec_stmt
			| assert_stmt'''
			
	p[0] = p[1]

	return
	
def p_expr_stmt(p):
	'''expr_stmt : testlist augassign yield_expr
		| testlist augassign testlist
		| testlist expr_stmt_bottom
		| testlist'''
	
	if len(p) == 2:
		p[0] = ast.Expr(p[1], lineno = p[1].lineno, col_offset = p[1].col_offset)
	
	elif len(p) == 3:
		values = p[2].pop()
		targets = [p[1], ]
		targets.extend(p[2])

		item = p[1]
		while isinstance(item, list):
			item = item[0]

		set_context(targets, ast.Store())
		p[0] = ast.Assign(targets = targets, value = values, lineno = item.lineno, col_offset = item.col_offset)

	elif len(p) == 4:
		set_context(p[1], ast.Store())
		p[0] = ast.AugAssign(target = p[1], value = p[3], op = p[2], lineno = p[1].lineno, col_offset = p[1].col_offset)


	return

def p_augassign(p):
	'''augassign : ADD_ASN
		| SUB_ASN
		| MUL_ASN
		| DIV_ASN
		| MOD_ASN
		| AND_ASN
		| OR_ASN
		| XOR_ASN
		| LSHIFT_ASN
		| RSHIFT_ASN
		| POW_ASN
		| FDIV_ASN'''

	p[0] = op_dict.get(p[1])

	return

def p_expr_stmt_bottom(p):
	'''expr_stmt_bottom : "=" yield_expr
		| "=" testlist
		| expr_stmt_bottom "=" yield_expr
		| expr_stmt_bottom "=" testlist'''

	if len(p) == 3:
		p[0] = []
		p[0].append(p[2])

	elif len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])

	return


def p_print_stmt(p):
	'''print_stmt : TAG_DRAW
			| TAG_DRAW testlist'''
			
	if len(p) == 3:
		if isinstance(p[2], list):
			p_values = p[2]
		else:
			p_values = [p[2], ]

		p[0] = ast.Print(dest = None, values = p_values, nl = True, lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	return
	
def p_del_stmt(p):
	'''del_stmt : TAG_DEL exprlist'''

	targets = p[2]
	if not isinstance(targets, list):
		targets = [p[2],]

	set_context(targets, ast.Del())
	p[0] = ast.Delete(targets = targets, lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	return 
	
def p_pass_stmt(p):
	'''pass_stmt : TAG_PASS'''
	p[0] = ast.Pass(lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	return
	
def p_flow_stmt(p):
	'''flow_stmt : break_stmt
			| continue_stmt
			| return_stmt
			| raise_stmt
			| yield_stmt'''

	p[0] = p[1]
	
	return
	
def p_break_stmt(p):
	'''break_stmt : TAG_BREAK'''
	p[0] = ast.Break(lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)
	
	return
	
def p_continue_stmt(p):
	'''continue_stmt : TAG_CONTINUE'''
	p[0] = ast.Continue(lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)
	
	return
	
def p_return_stmt(p):
	'''return_stmt : TAG_RETURN
			| TAG_RETURN testlist'''
			

	item = p.get_item(1)
	if len(p) == 2:
		p[0] = ast.Return(lineno = item.lineno, col_offset = item.lexpos)
	elif len(p) == 3:
		p[0] = ast.Return(value = p[2], lineno = item.lineno, col_offset = item.lexpos)

	return
	
def p_raise_stmt(p):
	'''raise_stmt : TAG_RAISE
			| TAG_RAISE test
			| TAG_RAISE test "," test
			| TAG_RAISE test "," test "," test'''
			
	return
	
def p_import_stmt(p):
	'''import_stmt : import_name
			| import_from'''
		
	p[0] = p[1]
	return
	
def p_import_name(p):
	'''import_name : TAG_IMPORT dotted_as_names'''
	
	p[0] = ast.Import(names = [],
			lineno = p.get_item(1).lineno,
			col_offset = p.get_item(1).lexpos)

	for item in p[2]:
		p[0].names.append(ast.alias(
				name = '.'.join(item[0]), 
				asname = item[1]))
	return
	
def p_import_from(p):
	'''import_from : TAG_FROM dotted_name TAG_IMPORT "*"
			| TAG_FROM dotted_name TAG_IMPORT import_as_names'''
	if p[4] == "*":
		pass

	else:
		p[0] = ast.ImportFrom(module = '.'.join(p[2]), 
			names = [], level = 0,
			lineno = p.get_item(1).lineno,
			col_offset = p.get_item(1).lexpos)

		for item in p[4]:
			p[0].names.append(ast.alias(name = item[0], asname = item[1]))

	return
	
def p_import_as_name(p):
	'''import_as_name : NAME
			| NAME TAG_AS NAME'''
			
	if len(p) == 2:
		p[0] = [p[1], None]
	else:
		p[0] = [p[1], p[3]]

	return
	
def p_dotted_as_name(p):
	'''dotted_as_name : dotted_name
			| dotted_name TAG_AS NAME'''

	if len(p) == 2:
		p[0] = [p[1], None]
	else:
		p[0] = [p[1], p[3]]

	return
	
def p_import_as_names(p):
	'''import_as_names : import_as_names_ann 
		| import_as_names_ann ","'''

	p[0] = p[1]

	return
		
def p_import_as_names_ann(p):
	'''import_as_names_ann : import_as_name
			| import_as_names_ann "," import_as_name'''

	if len(p) == 2:
		p[0] = [p[1],]

	elif len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])

	return
	
def p_dotted_as_names(p):
	'''dotted_as_names : dotted_as_names "," dotted_as_name
			| dotted_as_name'''

	if len(p) == 2:
		p[0] = [p[1],]

	elif len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])
			
	return
	
def p_dotted_name(p):
	'''dotted_name : NAME
			| dotted_name "." NAME'''
			
	if len(p) == 2:
		p[0] = []
		p[0].append(p[1])

	elif len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])

	return
	
def p_global_stmt(p):
	'''global_stmt : TAG_GLOBAL namelist'''

	p[0] = ast.Global(names = p[2], lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	return
	
def p_namelist(p):
	'''namelist : NAME
			| namelist "," NAME'''

	if len(p) == 2:
		p[0] = [p[1],]
	
	else:
		p[0] = p[1]
		p[0].append(p[3])
			
	return
	
def p_yield_stmt(p):
	'''yield_stmt : yield_expr'''

	p[0] = p[1]
	
	return
	
def p_exec_stmt(p):
	'''exec_stmt : TAG_EXEC expr 
			| TAG_EXEC expr TAG_IN test
			| TAG_EXEC expr TAG_IN test "," test'''
			
	return
	
def p_assert_stmt(p):
	'''assert_stmt : TAG_ASSERT test
			| TAG_ASSERT test "," test'''
			
	return
	
def p_yield_expr(p):
	'''yield_expr : TAG_YIELD
			| TAG_YIELD testlist'''
			
	p[0] = ast.Yield(value = [], lineno = p.get_item(1).lineno, col_offset = p.get_item(1).lexpos)

	if len(p) == 3:
		p[0].value = p[2]

	return
	
def p_error(p):
	if p:
		print("Syntax error at '%s', lineno: %d, type: %s" % (p.value, p.lineno, p.type))
	else:
		print("Syntax error at EOF")

	return
		

import ddlex
import ddyacc as yacc
yacc.PY_FLAG = True
yacc.yacc()

def run(fileName):
	global exec_file
	exec_file = fileName
	try:
		f = open(fileName)
	except EOFError, IOError:
		pass

	if f:
		yacc.parse('', debug = _debug, lexer = ddlex.DDLexer(f))
		f.close()

	return


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'Usage:', sys.argv[0], 'fileName'
		sys.exit(0)
				
	else:
		run(sys.argv[1])

