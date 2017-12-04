import marshal
import py_compile
import time
import ast

#codeobject = compile("body=[ClassDef(name='A', bases=[Name(id='object', ctx=Load())], body=[FunctionDef(name='__init__', args=arguments(args=[Name(id='self', ctx=Param()), Name(id='value', ctx=Param())], vararg=None, kwarg=None, defaults=[]), body=[Assign(targets=[Attribute(value=Name(id='self', ctx=Load()), attr='v', ctx=Store())], value=Name(id='value', ctx=Load()))], decorator_list=[]), FunctionDef(name='p', args=arguments(args=[Name(id='self', ctx=Param())], vararg=None, kwarg=None, defaults=[]), body=[Print(dest=None, values=[Attribute(value=Name(id='self', ctx=Load()), attr='v', ctx=Load())], nl=True), Return()], decorator_list=[])], decorator_list=[]), Assign(targets=[Name(id='a', ctx=Store())], value=Call(func=Name(id='A', ctx=Load()), args=[Num(n=1)], keywords=[], starargs=None, kwargs=None)), Expr(value=Call(func=Attribute(value=Name(id='a', ctx=Load()), attr='p', ctx=Load()), args=[], keywords=[], starargs=None, kwargs=None))]", '<string>', 'exec')
codeobject = compile(ast.parse('print 3+3*2'), '<string>', 'exec')
print codeobject
with open('output.pyc', 'wb') as fc:
	fc.write('\0\0\0\0')
	py_compile.wr_long(fc, long(time.time()))
	marshal.dump(codeobject, fc)
	fc.flush()
	fc.seek(0, 0)
	fc.write(py_compile.MAGIC)