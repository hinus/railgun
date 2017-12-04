package org.railgun.vm.intrisinc;

import org.railgun.shape.Star;

/**
 * Created by hinus on 2017/12/4.
 */
public class StarMethod implements InnerMethod<Star> {
    @Override
    public Star call(Object... args) {
        return Star.makeStar((Integer)args[2],
                (Integer)args[1],
                ((Integer)args[0]).doubleValue());
    }
}
