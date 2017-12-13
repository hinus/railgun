package org.railgun.vm.object;

/**
 * Created by hinus on 2017/12/13.
 */
public abstract class AbstractBuiltinMethodObject<V> extends RGObject implements BuiltinMethodObject<V> {
    protected RGObject owner;
    protected Klass klass;

    @Override
    public void setOwner(RGObject owner) {
        this.owner = owner;
        this.klass = owner.getKlass();
    }

    @Override
    public void setKlass(Klass klass) {
        this.klass = klass;
    }
}
