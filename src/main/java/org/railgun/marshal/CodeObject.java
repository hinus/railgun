package org.railgun.marshal;

import java.util.ArrayList;

/**
 * Created by hinus on 2017/12/1.
 */
public class CodeObject {
    public int argcount;
    public int nlocals;
    public int stacksize;
    public int flag;

    public byte[] bytecodes;
    public ArrayList names;
    public ArrayList consts;
    public ArrayList varnames;

    public ArrayList freevars;
    public ArrayList cellvars;

    public String fileName;
    public String name;
    public int lineno;
    public byte[] notable;

    public CodeObject(int argcount, int nlocals, int stacksize, int flag, byte[] bytecodes,
                      ArrayList names, ArrayList consts, ArrayList varnames, ArrayList freevars, ArrayList cellvars,
                      String fileName, String name, int lineno, byte[] notable) {
        this.argcount = argcount;
        this.nlocals = nlocals;
        this.stacksize = stacksize;
        this.flag = flag;
        this.bytecodes = bytecodes;
        this.names = names;
        this.consts = consts;
        this.varnames = varnames;
        this.freevars = freevars;
        this.cellvars = cellvars;
        this.fileName = fileName;
        this.name = name;
        this.lineno = lineno;
        this.notable = notable;
    }
}
