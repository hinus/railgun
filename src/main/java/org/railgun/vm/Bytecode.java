package org.railgun.vm;

public class Bytecode {
    // Define org.railgun.vm.Bytecode Operator Code
    static final byte POP_TOP = 1;
    static final byte ROT_TWO = 2;
    static final byte DUP_TOP = 4;
    static final byte UNARY_NEGATIVE = 11;
    static final byte BINARY_MULTIPLY = 20;
    static final byte BINARY_DIVIDE = 21;
    static final byte BINARY_ADD = 23;
    static final byte BINARY_SUBSTRACT = 24;

    static final byte INPLACE_ADD = 55;
    static final byte INPLACE_SUBSTRACT = 56;
    static final byte INPLACE_MULTIPLY = 57;
    static final byte INPLACE_DIVIDE = 58;

    static final byte PRINT_ITEM = 71;
    static final byte PRINT_NEWLINE = 72;

    static final byte RETURN_VALUE = 83;
    static final byte POP_BLOCK = 87;

    static final byte HAVE_ARGUMENT = 90; /* Opcodes from here have an argument: */

    static final byte STORE_NAME = 90; /* Index in name list */
    static final byte STORE_ATTR = 95;  /* Index in name list */
    static final byte STORE_GLOBAL = 97;
    static final byte LOAD_CONST = 100; /* Index in const list */
    static final byte LOAD_NAME = 101; /* Index in name list */
    static final byte LOAD_ATTR = 106; /* Index in name list */
    static final byte COMPARE_OP = 107; /* Comparison operator */
    static final byte JUMP_ABSOLUTE = 113;
    static final byte POP_JUMP_IF_FALSE = 114;
    static final byte POP_JUMP_IF_TRUE = 115;
    static final byte LOAD_GLOBAL = 116; /* Index in name list */
    static final byte SETUP_LOOP = 120; /* Target address (relative) */
    static final byte LOAD_FAST  = 124; /* Local variable number */
    static final byte STORE_FAST = 125; /* Local variable number */

    static final byte CALL_FUNCTION = (byte) 131;
    static final byte MAKE_FUNCTION = (byte) 132;

    //new
    static final byte STORE_MAP = (byte) 54;
    static final byte BUILD_MAP = (byte) 105;
    static final byte BUILD_LIST = (byte) 103;

    public static class COMPARE {
        static final byte LESS = 0;
        static final byte LESS_EQUAL = 1;
        static final byte EQUAL = 2;
        static final byte NOT_EQUAL = 3;
        static final byte GREATER = 4;
        static final byte GREATER_EQUAL = 5;
    }
}

