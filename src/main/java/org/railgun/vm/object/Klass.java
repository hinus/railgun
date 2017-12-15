package org.railgun.vm.object;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/13.
 */
public class Klass {
    protected HashMap<String, Object> klassProps;

    public Klass() {
        klassProps = new HashMap<>();
    }

    public Klass(HashMap<String, Object> klassProps) {
        this.klassProps = klassProps;
    }

    public RGObject allocate() {
        RGObject o = new RGObject(this, new HashMap<>());

        return o;
    }

    public Object getAttr(String name) {
        if (klassProps.containsKey(name))
            return klassProps.get(name);

        return null;
    }
}
