package org.railgun.vm.intrisinc;

import org.railgun.Timer;

/**
 * Created by hinus on 2017/12/13.
 */
public class FrameCountMethod implements InnerMethod<Void> {
    @Override
    public Void call(Object... args) {
        int frameCount = ((Integer) args[0]).intValue();
        Timer.setFramesPerSecond(frameCount);
        return null;
    }
}
