package org.railgun.vm.object;

/**
 * Created by hinus on 2017/12/15.
 */
public class NoneObject extends RGObject {
    private static NoneObject instance = new NoneObject();

    public static NoneObject getInstance() {
        return instance;
    }

    private NoneObject() {

    }
}
