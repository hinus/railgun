package org.railgun.vm.intrisinc;

/**
 * Created by hinus on 2017/12/4.
 */
public interface InnerMethod<V> {
    V call(Object ... args);
}
