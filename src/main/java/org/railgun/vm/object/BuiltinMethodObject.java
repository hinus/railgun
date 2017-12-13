package org.railgun.vm.object;

/**
 * Created by hinus on 2017/12/13.
 */
public interface BuiltinMethodObject<V> {
    V call(Object... args);

    void setOwner(RGObject owner);

    void setKlass(Klass klass);
}
