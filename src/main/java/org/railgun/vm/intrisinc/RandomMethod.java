package org.railgun.vm.intrisinc;

import java.util.Random;

/**
 * Created by hinus on 2017/12/4.
 */
public class RandomMethod implements InnerMethod<Integer> {
    Random random = new Random();
    @Override
    public Integer call(Object... args) {
        return random.nextInt((Integer)args[0]);
    }
}
