#-*- coding: UTF-8 -*-
#
# -----------------------------------------------------------------------------
# parser for dragon sword
# author : gzxuwei@corp.netease.com
# date : 2013-11-03
# -----------------------------------------------------------------------------

import sys, re
sys.path.insert(0,"./dsparserlib")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
	'DEDENT',
	'INDENT',
	'NEWLINE',
	'ENDMARKER',
	
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
	
	'TAG_PRINT',
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
	
	'NAME',
	'FLOAT',
	'INTEGER',
    )
	

literals = [':', '(', ')', '{', '}', '[', ']', '<', '>', '=']

def p_file_input(p):
	'''file_input : ENDMARKER
			| file_content ENDMARKER'''
	print 'what the fuck!', p[0], p[1]
	return
	
def p_file_content(p):
	'''file_content : file_content NEWLINE
			| file_content stmt
			| NEWLINE
			| stmt'''
			
	return

def p_classdef(p):
	'''classdef : TAG_CLASS NAME ":" suite
			| TAG_CLASS NAME "(" testlist ")" ":" suite
			| TAG_CLASS NAME "(" ")" ":" suite'''
	
	print 'find a class defination'
	
	return
	
def p_exprlist(p):
	'''exprlist : expr
			| exprlist "," expr'''
			
	return
			
def p_expr(p):
	'''expr : xor_expr
			| expr "|" xor_expr'''
	
	return
	
def p_xor_expr(p):
	'''xor_expr : and_expr
			| and_expr "^" xor_expr_listing'''
			
def p_xor_expr_listing(p):
	'''xor_expr_listing : and_expr
			| and_expr "^" xor_expr_listing'''
	
	return
	
def p_and_expr(p):
	'''and_expr : shift_expr
			| shift_expr "&" and_expr_listing'''
			
def p_and_expr_listing(p):
	'''and_expr_listing : shift_expr
			| shift_expr "&" and_expr_listing'''
			
	return
	
def p_shift_expr(p):
	'''shift_expr : arith_expr
			| shift_expr OP_LEFT_SHIFT arith_expr
			| shift_expr OP_RIGHT_SHIFT arith_expr'''
			
	return
	
def p_arith_expr(p):
	'''arith_expr : term
			| arith_expr "+" term
			| arith_expr "-" term'''
	
	return
	
def p_term(p):
	'''term : term "*" factor
			| term "/" factor
			| term "%" factor
			| term OP_EXACT_DIVISION factor
			| factor '''
			
	return
			
def p_factor(p):
	'''factor : "+" factor
			| "-" factor
			| "~" factor
			| power'''
			
	return
	
def p_power(p):
	'''power : atom
			| atom trailers
			| atom OP_POWER factor
			| atom trailers OP_POWER factor'''
			
	return
	
def p_trailers(p):
	'''trailers : trailers trailer
			| trailer'''
			
	return
	
def p_trailer(p):
	'''trailer : "(" ")"
			| "(" arglist ")"
			| "[" subscriptlist "]"
			| "." NAME'''
	
def p_arglist_piece(p):
	'''arglist_piece : argument
			| arglist_piece "," argument'''
	
	return
	
	
def p_arglist(p):
	'''arglist : arglist_piece
			| arglist_piece ","'''
			
	return
	
def p_argument(p):
	'''argument : test
			| test comp_for
			| test "=" test'''
	return
	
def p_subscriptlist(p):
	'''subscriptlist : subscriptlist "," subscript
			| subscriptlist ","
			| subscript'''
			
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
			| "{" dictorsetmaker "}"
			| "`" testlist1 "`"
			| NAME
			| INTEGER
			| FLOAT'''
			
	return
	
def p_testlist1(p):
	'''testlist1 : test
			| testlist1 "," test'''
			
	return
	
def p_listmaker(p):
	'''listmaker : testlist
			| test list_for'''
			
	return
	
def p_dsmaker_piece(p):
	'''dsmaker_piece : test ":" test
		| test
		| dsmaker_piece "," test ":" test
		| dsmaker_piece "," test'''
	
	return
	
def p_dictorsetmaker(p):
	'''dictorsetmaker : dsmaker_piece
			| dsmaker_piece ","
			| test ":" test comp_for
			| test comp_for
			'''
	return
	
def p_testlist_comp(p):
	'''testlist_comp : testlist
			| test comp_for'''
			
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
			
	return
	
def p_testlist_anns(p):
	'''testlist_anns : testlist_anns "," test
			| test'''
			
	return
	
def p_test(p):
	'''test : or_test
			| or_test TAG_IF or_test TAG_ELSE test
			| lambdef'''
	return
	
def p_or_test(p):
	'''or_test : and_test
			| or_test TAG_OR and_test'''
			
	return
	
def p_and_test(p):
	'''and_test : not_test
			| and_test TAG_AND not_test'''
			
	return
	
def p_not_test(p):
	'''not_test : TAG_NOT not_test
			| comparison'''
			
	return
	

def p_comparison(p):
	'''comparison : expr
			| comparison comp_op expr'''
	
	print 'find a comparison', p[0], p[1]
	
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
	return
	
def p_lambdef(p):
	'''lambdef : TAG_LAMBDA ":" test
			| TAG_LAMBDA varagslist ":" test'''
			
	return
	

def p_varagslist(p):
	'''varagslist : NAME'''
	return
	
	
def p_fpdef(p):
	'''fpdef : NAME
			| "(" fplist ")"'''
	
	return
	
def p_fplist_pc(p):
	'''fplist_pc : fpdef
			| fplist_pc "," fpdef'''
	
	return
	
def p_fplist(p):
	'''fplist : fplist_pc
			| fplist_pc ","'''
	
	return
	
	
def p_funcdef(p):
	'''funcdef : TAG_DEF NAME parameters ":" suite'''
	return
	
def p_parameters(p):
	'''parameters : "(" ")"
			| "(" varagslist ")"'''
	
	return
	
def p_suite(p):
	'''suite : simple_stmt
			| NEWLINE INDENT stmts DEDENT'''
			
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
			| TAG_LAMBDA varagslist ":" old_test'''
			
	return
	
def p_stmts(p):
	'''stmts : stmt
			| stmts stmt'''
			
	return
	
def p_stmt(p):
	'''stmt : simple_stmt
			| compound_stmt'''
	
	return
	
def p_compound_stmt(p):
	'''compound_stmt : if_stmt
			| while_stmt
			| for_stmt
			| funcdef
			| classdef'''

	return
	
def p_if_stmt(p):
	'''if_stmt : TAG_IF test ":" suite
			| TAG_IF test ":" suite TAG_ELSE ":" suite
			| TAG_IF test ":" suite elif_list
			| TAG_IF test ":" suite elif_list TAG_ELSE ":" suite'''
			
	return
	
def p_while_stmt(p):
	'''while_stmt : TAG_WHILE test ":" suite
			| TAG_WHILE test ":" suite TAG_ELSE ":" suite'''
	
	return
	
def p_for_stmt(p):
	'''for_stmt : TAG_FOR exprlist TAG_IN testlist ":" suite
			| TAG_FOR exprlist TAG_IN testlist ":" suite TAG_ELSE ":" suite'''
	
	return
	
def p_elif_list(p):
	'''elif_list : TAG_ELIF test ":" suite
			| elif_list TAG_ELIF test ":" suite'''
	
	return
	
def p_simple_stmt(p):
	'''simple_stmt : simple_stmt ";" small_stmt NEWLINE
			| simple_stmt ";" small_stmt ";" NEWLINE
			| small_stmt NEWLINE
			| small_stmt ";" NEWLINE'''
			
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
			
	return
	
def p_expr_stmt(p):
	'''expr_stmt : testlist'''
	
	print 'GOT expression'
	return
	
def p_print_stmt(p):
	'''print_stmt : TAG_PRINT
			| TAG_PRINT testlist'''
			
	print 'Waring : got a print'
	return
	
def p_del_stmt(p):
	'''del_stmt : TAG_DEL exprlist'''
	
	return 
	
def p_pass_stmt(p):
	'''pass_stmt : TAG_PASS'''
	
	return
	
def p_flow_stmt(p):
	'''flow_stmt : break_stmt
			| continue_stmt
			| return_stmt
			| raise_stmt
			| yield_stmt'''
	
	return
	
def p_break_stmt(p):
	'''break_stmt : TAG_BREAK'''
	
	return
	
def p_continue_stmt(p):
	'''continue_stmt : TAG_CONTINUE'''
	
	return
	
def p_return_stmt(p):
	'''return_stmt : TAG_RETURN
			| TAG_RETURN testlist'''
			
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
		
	return
	
def p_import_name(p):
	'''import_name : TAG_IMPORT dotted_as_names'''
	
	return
	
def p_import_from(p):
	'''import_from : TAG_FROM dotted_name TAG_IMPORT "*"
			| TAG_FROM dotted_name TAG_IMPORT import_as_names'''
	return
	
def p_import_as_name(p):
	'''import_as_name : NAME
			| NAME TAG_AS NAME'''
			
	return
	
def p_dotted_as_name(p):
	'''dotted_as_name : dotted_name
			| dotted_name TAG_AS NAME'''
	return
	
def p_import_as_names(p):
	'''import_as_names : import_as_names import_as_name
			| import_as_name
			| import_as_name ","
			| import_as_names import_as_name ","'''
			
	return
	
def p_dotted_as_names(p):
	'''dotted_as_names : dotted_as_names "," dotted_as_name
			| dotted_as_name'''
			
	return
	
def p_dotted_name(p):
	'''dotted_name : NAME
			| dotted_name "." NAME'''
			
	return
	
def p_global_stmt(p):
	'''global_stmt : TAG_GLOBAL namelist'''
	
def p_namelist(p):
	'''namelist : NAME
			| namelist "," NAME'''
			
	return
	
def p_yield_stmt(p):
	'''yield_stmt : yield_expr'''
	
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
			
	return
	
def p_error(p):
	if p:
		print("Syntax error at '%s', lineno: %d, type: %s" % (p.value, p.lineno, p.type))
	else:
		print("Syntax error at EOF")
		



import pylex
import yacc
yacc.PY_FLAG = True
yacc.yacc()

def run(fileName):
	try:
		f = open(fileName)
	except EOFError, IOError:
		pass
	if f:
		yacc.parse('', lexer = pylex.PyLexer(f))
		f.close()


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'Usage:', sys.argv[0], 'fileName'
		sys.exit(0)
				
	else:
		run(sys.argv[1])
