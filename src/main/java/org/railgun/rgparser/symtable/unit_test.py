import SymtableVisitor as SV
import CodeGen
import ast

def test_file(fname):
	pass

def test_flowgraph():
	import Assem
	f = Assem.PyFlowGraph("f", "h.py")
	f.emit("LOAD_CONST", 1)
	f.emit("PRINT_ITEM")
	f.emit("PRINT_NEWLINE")
	f.emit("LOAD_CONST", None)
	f.emit("RETURN_VALUE")

	g = Assem.PyFlowGraph("r", "h.py")
	g.emit("LOAD_CONST", f)
	g.emit("MAKE_FUNCTION", 0)
	g.emit("STORE_NAME", "func")
	g.emit("LOAD_NAME", "func")
	g.emit("CALL_FUNCTION", 0)
	g.emit("POP_TOP")
	g.emit("LOAD_CONST", None)
	g.emit("RETURN_VALUE")

	co = g.get_code()
	print co.co_consts
	import dis
	dis.dis(co)
	exec co

	return


if __name__ == "__main__":
	#fname = "testfiles/test_func.ldd"
	#fname = "testfiles/test_if.ldd"
	#fname = "testfiles/test_control.ldd"
	#fname = "testfiles/test_datas.ldd"
	#fname = "testfiles/test_try.ldd"
	#fname = "testfiles/test_comp.ldd"
	#fname = "testfiles/test_class.ldd"
	#fname = "testfiles/test_with.ldd"
	#fname = "testfiles/test_stmt.ldd"
	fname = "testfiles/test_subscr.ldd"
	#test_file("testfiles/test_assign_print.ldd")
	#test_flowgraph()

	f = open(fname)
	s = f.read()
	st = ast.parse(s)

	print ast.dump(st)
	codeGen = CodeGen.CodeGen(fname)
	codeGen.visit(st, None, None)
	co = codeGen.get_code()

	import dis
	print "========="
	dis.dis(co)
	#dis.dis(co.co_consts[2])
	#print "========="
	#dis.dis(co.co_consts[2].co_consts[2])
	#print co.co_consts[2].co_consts[2].co_names
	#print co.co_consts[4].co_argcount

	print "========="

	co = compile(st, "s", "exec")
	#print co.co_consts[3].co_varnames
	dis.dis(co)
	#print "========="
	#dis.dis(co.co_consts[1])
	#dis.dis(co.co_consts[1].co_consts[1])
	#print co.co_consts[1].co_consts[2].co_names

	#exec co
