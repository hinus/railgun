package org.railgun.vm.object;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/13.
 */
public class RGObject {
    private Klass klass;

    private HashMap<String, Object> properties;

    public RGObject(Klass klass, HashMap<String, Object> properties) {
        this.klass = klass;
        this.properties = properties;
    }

    public RGObject() {
    }

    public Klass getKlass() {
        return klass;
    }

    public void setKlass(Klass klass) {
        this.klass = klass;
    }

    public HashMap<String, Object> getProperties() {
        return properties;
    }

    public void setProperties(HashMap<String, Object> properties) {
        this.properties = properties;
    }

    public void setAttr(String name, Object value) {
        this.properties.put(name, value);
    }

    public Object getAttr(String name) {
        Object o = null;

        if (properties.containsKey(name))
            o = properties.get(name);
        else
            o = klass.getAttr(name);

        if (o != null && o instanceof BuiltinMethodObject) {
            ((BuiltinMethodObject) o).setOwner(this);
        }

        return o;
    }
}
