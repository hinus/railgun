package org.railgun.vm.object;

import java.util.LinkedList;

/**
 * Created by hinus on 2017/12/13.
 */
public class ListKlass extends Klass {
    public static ListKlass listKlass = new ListKlass();

    public static ListKlass getListKlass() {
        return listKlass;
    }

    private ListKlass() {
        super();
        klassProps.put("addFirst", new AddFirstMethod());
        klassProps.put("get", new GetMethod());
        klassProps.put("set", new SetMethod());
        klassProps.put("length", new LengthMethod());
    }

    public RGObject allocate() {
        RGObject o = super.allocate();
        o.setAttr("elements", new LinkedList<>());
        return o;
    }
}

class AddFirstMethod extends AbstractBuiltinMethodObject<Void> {
    @Override
    public Void call(Object... args) {
        ((LinkedList)this.owner.getAttr("elements")).addFirst(args[0]);
        return null;
    }
}

class GetMethod extends AbstractBuiltinMethodObject<Object> {
    @Override
    public Object call(Object... args) {
        return (Object) ((LinkedList)this.owner.getAttr("elements")).get(((Integer)args[0]).intValue());
    }
}

class SetMethod extends AbstractBuiltinMethodObject<Void> {
    @Override
    public Void call(Object... args) {
        ((LinkedList)this.owner.getAttr("elements")).set(((Integer)args[0]).intValue(), args[1]);
        return null;
    }
}

class LengthMethod extends AbstractBuiltinMethodObject<Integer> {
    @Override
    public Integer call(Object... args) {
        return ((LinkedList)this.owner.getAttr("elements")).size();
    }
}