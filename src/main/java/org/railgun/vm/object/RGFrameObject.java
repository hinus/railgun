package org.railgun.vm.object;

import org.railgun.marshal.CodeObject;

import java.util.List;
import java.util.Map;
import java.util.Stack;

/**
 * Created by YeomanSlow on 2017/12/13.
 */
public class RGFrameObject {
    public CodeObject co;
    public List<Object> consts; // co_consts
    public List<Object> names; // co_names
    public List<Object> varnames; // co_varnames
    public byte[] optArr; // co_code

    public Map<String, Object> frameGlobalsTable; // globals
    public Map<String, Object> frameLocalsTable; // locals

    public Stack<Object> frameStack;
    public Stack<Integer> blockStack;
    public int pc;

    public RGFrameObject(CodeObject co, Map<String, Object> localsTable, Map<String, Object> globalsTable, int pc) {
        this.co = co;
        this.consts = co.consts;
        this.names = co.names;
        this.varnames = co.varnames;
        this.optArr = co.bytecodes;

        this.frameLocalsTable = localsTable;
        this.frameGlobalsTable = globalsTable;
        this.frameStack = new Stack<>();
        this.blockStack = new Stack<>();
        this.pc = pc;
    }
}
