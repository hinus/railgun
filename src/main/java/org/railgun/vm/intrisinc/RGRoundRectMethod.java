package org.railgun.vm.intrisinc;

import org.railgun.shape.RGRoundRect;

/**
 * Created by hinus on 2017/12/4.
 */
public class RGRoundRectMethod implements InnerMethod<RGRoundRect> {
    @Override
    public RGRoundRect call(Object... args) {
        return RGRoundRect.makeRoundRect((Integer) args[5],
                (Integer)args[4], (Integer)args[3],
                (Integer) args[2], (Integer)args[1],
                (Integer)args[0]);
    }
}
