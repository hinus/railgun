package org.railgun.vm.intrisinc;

import java.util.ArrayList;

/**
 * Created by hinus on 2017/12/13.
 */
public class LenMethod implements InnerMethod<Integer> {
    @Override
    public Integer call(Object... args) {
        Object o = args[0];

        if (o instanceof ArrayList) {
            return ((ArrayList) o).size();
        }

        return 0;
    }
}
