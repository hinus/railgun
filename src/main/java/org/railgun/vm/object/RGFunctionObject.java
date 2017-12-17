package org.railgun.vm.object;

import org.railgun.marshal.CodeObject;

import java.util.List;
import java.util.Map;

/**
 * Created by YeomanSlow on 2017/12/13.
 */
public class RGFunctionObject {
    public CodeObject co;

    public Map<String, Object> globalsTable;
    public List<Object> defaultsTable;
    public Map<String, Object> closureTable;
    public int argcount;
    public String name;

    public RGFunctionObject(CodeObject co, Map<String, Object> globalsTable, List<Object> defaultsTable) {
        this.co = co;
        this.globalsTable = globalsTable;
        this.defaultsTable = defaultsTable;
        this.name = co.name;
        this.argcount = co.argcount;
    }

}
