package org.railgun.vm.intrisinc;

import org.railgun.shape.RGLine;

/**
 * Created by hinus on 2017/12/4.
 */
public class RGLineMethod implements InnerMethod<RGLine> {
    @Override
    public RGLine call(Object... args) {
        return new RGLine((Integer) args[3],
                (Integer)args[2],
                (Integer) args[1],
                (Integer)args[0]);
    }
}
