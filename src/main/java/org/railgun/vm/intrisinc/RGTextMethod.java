package org.railgun.vm.intrisinc;

import org.railgun.shape.RGText;

/**
 * Created by hinus on 2017/12/4.
 */
public class RGTextMethod implements InnerMethod<RGText> {
    @Override
    public RGText call(Object... args) {
        return RGText.makeText(args[4].toString(), (Integer)args[3], (Integer)args[2],
                (String)args[1], ((Integer)args[0]).doubleValue());
    }
}
