package org.railgun.vm;

import org.railgun.canvas.RailGunDrawer;
import org.railgun.marshal.BinaryFileParser;
import org.railgun.marshal.CodeObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.*;

public class Interpreter {

    private static boolean x86 = false;

    // Stack based Virtual Machine
    private static class Frame {
        public List<Object> consts;
        public List<Object> names;
        public Map<String, Object> namesTable;
        public Map<String, Object> varnamesTable;
        public List<Object> varnames;
        public Stack<Object> stack;
        public byte[] optArr;
        public int pc;

        Frame(List<Object> consts, List<Object> names, List<Object> varnames, byte[] optArr, Stack<Object> stack, int pc) {
            this.consts = consts;
            this.names = names;
            this.varnames = varnames;
            namesTable = new HashMap<>();
            varnamesTable = new HashMap<>();
            this.stack = stack;
            this.optArr = optArr;
            this.pc = pc;
        }
    }

    // Init stack trace
    Stack<Frame> stackTrace = new Stack<>();
    public void run (byte[] sourceBytes) {
        // Read code object from bytecode
        CodeObject co = BinaryFileParser.parse(sourceBytes);

        // Construct base frame
        Frame baseFrame = new Frame(co.consts, co.names, co.varnames, co.bytecodes, new Stack<>(), 0);

        // Interpret current frame
        interpret(baseFrame, new Object[0]);
    }

    // Interpret Instructions
    void interpret (Frame curFrame, Object[] args) {
        // Program Counter
        int pc = curFrame.pc;
        // Bytecodes Array
        byte[] optArr = curFrame.optArr;
        // Bytecode Array Length
        int optLength = optArr.length;

        // Bytecode constant pools
        List<Object> consts = curFrame.consts;
        // Bytecode local variable
        List<Object> varnames = curFrame.varnames;
        Map<String, Object> varnamesTable = curFrame.varnamesTable;
        // Bytecode global variable
        List<Object> names = curFrame.names;
        Map<String, Object> namesTable = curFrame.namesTable;
        Stack<Object> stack = curFrame.stack;

        // Process Input Arguments
        for (int i = args.length; i > 0; ++i) {
            varnamesTable.put ((String) varnames.get(args.length - i), args[i]);
        }

        while (pc < optLength) {
            // TODO: Make sure current pc is at optcode, not optarg
            byte optcode = optArr[pc++];
            boolean haveArgument = (optcode & 0xFF) >= Bytecode.HAVE_ARGUMENT;
            int optarg = -1;
            if (haveArgument) {
                optarg = x86 ? (optArr[pc++] & 0xFF) : ((optArr[pc++] & 0xFF) + ((optArr[pc++] & 0xFF) << 8));
            }
            Integer lhs, rhs;
            switch (optcode) {
                case Bytecode.POP_TOP:
                    stack.pop();
                    break;
                // 57
                case Bytecode.INPLACE_MULTIPLY:
                    // 20
                case Bytecode.BINARY_MULTIPLY:
                    rhs = (Integer) stack.pop();
                    lhs = (Integer) stack.pop();
                    stack.push(lhs * rhs);
                    break;
                // 58
                case Bytecode.INPLACE_DIVIDE:
                    // 21
                case Bytecode.BINARY_DIVIDE:
                    rhs = (Integer) stack.pop();
                    lhs = (Integer) stack.pop();
                    stack.push(lhs / rhs);
                    break;
                // 55
                case Bytecode.INPLACE_ADD:
                    // 23
                case Bytecode.BINARY_ADD:
                    rhs = (Integer) stack.pop();
                    lhs = (Integer) stack.pop();
                    stack.push(lhs + rhs);
                    break;
                // 56
                case Bytecode.INPLACE_SUBSTRACT:
                    // 24
                case Bytecode.BINARY_SUBSTRACT:
                    rhs = (Integer) stack.pop();
                    lhs = (Integer) stack.pop();
                    stack.push(lhs - rhs);
                    break;
                // 71
                case Bytecode.PRINT_ITEM:
                    System.out.print(stack.pop());
                    break;
                // 72
                case Bytecode.PRINT_NEWLINE:
                    System.out.println();
                    break;
                // 83
                case Bytecode.RETURN_VALUE:
                    break;

                // TODO: Have Argument
                // 90
                case Bytecode.STORE_NAME:
                    namesTable.put((String)names.get(optarg), stack.pop());
                    break;
                // 101
                case Bytecode.LOAD_NAME:
                    String viariableName = (String)names.get(optarg);

                    if (viariableName.equals("circle")) {
                        stack.push(viariableName);
                    }
                    else {
                        stack.push(namesTable.get(viariableName));
                    }
                    break;
                // 100
                case Bytecode.LOAD_CONST:
                    stack.push(consts.get(optarg));
                    break;
                // 107
                case Bytecode.COMPARE_OP:
                    // TODO: Only for Integer
                    rhs = (Integer) stack.pop();
                    lhs = (Integer) stack.pop();
                    switch (optarg) {
                        case Bytecode.COMPARE.LESS:
                            stack.push(lhs < rhs);
                            break;
                        case Bytecode.COMPARE.LESS_EQUAL:
                            stack.push(lhs <= rhs);
                            break;
                        case Bytecode.COMPARE.EQUAL:
                            stack.push(lhs == rhs);
                            break;
                        case Bytecode.COMPARE.NOT_EQUAL:
                            stack.push(lhs != rhs);
                            break;
                        case Bytecode.COMPARE.GREATER:
                            stack.push(lhs > rhs);
                            break;
                        case Bytecode.COMPARE.GREATER_EQUAL:
                            stack.push(lhs >= rhs);
                            break;
                    }
                    break;
                // 113
                case Bytecode.JUMP_ABSOLUTE:
                    pc = optarg;
                    break;
                // 114
                case Bytecode.POP_JUMP_IF_FALSE:
                    if (! (Boolean) stack.pop())
                        pc = optarg;
                    break;
                // 115
                case Bytecode.POP_JUMP_IF_TRUE:
                    if ((Boolean) stack.pop())
                        pc = optarg;
                    break;
                // 120
                case Bytecode.SETUP_LOOP:
                    break;
                // 124
                case Bytecode.LOAD_FAST:
                    String fastVarName = (String)varnames.get(optarg);

                    if (fastVarName.equals("circle")) {
                        stack.push(fastVarName);
                    }
                    else {
                        stack.push(varnamesTable.get(fastVarName));
                    }
                    break;
                // 125
                case Bytecode.STORE_FAST:
                    varnamesTable.put((String)varnames.get(optarg), stack.pop());
                    break;
                // 131
                case Bytecode.CALL_FUNCTION:
                    // Process Callee Arguments
                    Object[] nextArgs = new Object[optarg];
                    for (int i = 0; i < optarg; ++i) {
                        nextArgs[i] = stack.pop();
                    }
                    curFrame.pc = pc;
                    stackTrace.push(curFrame);

                    Object o = stack.peek();

                    if (o instanceof String) {
                        String funcName = (String) o;
                        if (funcName.equals("circle")) {
                            RailGunDrawer.getRailGunDrawer().drawCircle((Integer) nextArgs[2],
                                    (Integer)nextArgs[1],
                                    ((Integer) nextArgs[0]).doubleValue());
                        }
                    } else {
                        CodeObject co = (CodeObject) stack.peek();
                        interpret(new Frame(co.consts, co.names, co.varnames, co.bytecodes, new Stack<>(), 0), nextArgs);
                    }
                    break;
                // 132
                case Bytecode.MAKE_FUNCTION:
                    break;
                case Bytecode.BUILD_LIST:
                    ArrayList<Object> arr=new ArrayList<Object>();
                    for (int i = 0; i < optarg; ++i) {
                        arr.add(stack.pop());
                    }
                    stack.push(arr);
                    break;
                //105
                case Bytecode.BUILD_MAP:
                    HashMap<Object, Object> mp = new HashMap<Object, Object>();
                    stack.push(mp);
                    break;
                //54
                case Bytecode.STORE_MAP:
                    Object objLeft = stack.pop();
                    Object objRight = stack.pop();
                    //mp.put(objLeft, objRight);
                    HashMap<Object, Object> map = (HashMap<Object, Object>) (stack.peek());
                    map.put(objLeft, objRight);
                    break;

            }
        }
    }

    void readFile (String fileName) {
        byte [] sourceByte = null;
        try {
            File file = new File(fileName);
            sourceByte = new byte[(int) file.length()];
            InputStream in = new FileInputStream(file);
            in.read(sourceByte);
        } catch (Exception e) {}
        run (sourceByte);


    }

    /*
    public static void main (String[] args) {
        Interpreter test = new Interpreter();
        test.readFile("C:\\Users\\d00424111\\Desktop\\PythonProject\\test.pyc");
    }
    */
}

