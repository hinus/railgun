#-*- coding: UTF-8 -*-
#
# -----------------------------------------------------------------------------
# parser for dragon sword
# author : gzxuwei@corp.netease.com
# date : 2014-11-03
# -----------------------------------------------------------------------------

import tokenize as tk

token_types = {
	tk.INDENT : ('INDENT', ),
	tk.DEDENT : ('DEDENT', ),
	tk.NAME : ('NAME', ),
	tk.ENDMARKER : ('ENDMARKER', ),
	tk.NEWLINE : ('NEWLINE', ),
	}
	
	
reserved = {
	'class' : 'TAG_CLASS',
	'def' : 'TAG_DEF',
	'lambda' : 'TAG_LAMBDA',
	'from' : 'TAG_FROM',
	'as' : 'TAG_AS',
	'global' : 'TAG_GLOBAL',
	
	'if' : 'TAG_IF',
	'else' : 'TAG_ELSE',
	'elif' : 'TAG_ELIF',
	'for' : 'TAG_FOR',
	'while' : 'TAG_WHILE',
	
	'or' : 'TAG_OR',
	'and' : 'TAG_AND',
	'not' : 'TAG_NOT',
	'in' : 'TAG_IN',
	'is' : 'TAG_IS',
	
	'pass' : 'TAG_PASS',
	'del' : 'TAG_DEL',
	'break' : 'TAG_BREAK',
	'continue' : 'TAG_CONTINUE',
	'print' : 'TAG_PRINT',
	'return' : 'TAG_RETURN',
	'raise' : 'TAG_RAISE',
	'exec' : 'TAG_EXEC',
	'assert' : 'TAG_ASSERT',
	'yield' : 'TAG_YIELD',
	'import' : 'TAG_IMPORT',
	}
	
op_types = {
	':' : ':',
	'(' : '(',
	')' : ')', 
	'{' : '{', 
	'}' : '}', 
	'[' : '[', 
	']' : ']', 
	'<' : '<', 
	'>' : '>',
	'=' : '=',
	'==' : 'OP_EQ',
	'<=' : 'OP_LE',
	'>=' : 'OP_GE',
	'!=' : 'OP_NE',
	'<>' : 'OP_NNE',
	'<<' : 'OP_LEFT_SHIFT',
	'>>' : 'OP_RIGHT_SHIFT',
	'//' : 'OP_EXACT_DIVISION',
	'\*\*' : 'OP_POWER',
	}

# Token class.  This class is used to represent the tokens produced.
class LexToken(object):
    def __str__(self):
        return "LexToken(%s,%r,%d,%d)" % (self.type,self.value,self.lineno,self.lexpos)
		
    def __repr__(self):
        return str(self)

class PyLexer(object):
	def __init__(self, input_file):
		super(PyLexer, self).__init__()
		
		self.stopped = False
		self.lineno = 0
		
		self.gt = tk.generate_tokens(input_file.readline)
		
	def token(self):
		if self.stopped:
			return None
			
		if not self.gt:
			return None
			
		_type, _value, _pos_begin, _pos_end, __ = self.gt.next()
		
		# 如果是续行的情况，就直接跳过
		if _type == tk.NL:
			_type, _value, _pos_begin, _pos_end, __ = self.gt.next()
		
		if _type == tk.ENDMARKER:
			self.stopped = True
			
		token = LexToken()
		token.type = _type
		token.value = _value
		token.lineno = _pos_begin[0]
		token.lexpos = _pos_begin[1]
		
		self.lineno = _pos_end[0]
		
		self._post_process(token)
		
		return token
		
	# 后处理
	def _post_process(self, token):
		if token.type == tk.NAME:
			token.type = reserved.get(token.value.lower(), 'NAME')
		
		elif token.type == tk.OP:
			token.type = op_types[token.value]
		
		else:
			token.type = token_types[token.type][0]
		
		if token.type == 'TRUE':
			token.value = True
		elif token.type == 'FALSE':
			token.value = False
		
		return
		
	def input(self, _nothing):
		return
