package org.railgun.vm.intrisinc;

import javafx.scene.paint.Color;

/**
 * Created by hinus on 2017/12/4.
 */
public class RgbMethod implements InnerMethod<Color> {
    @Override
    public Color call(Object... args) {
        return Color.rgb((Integer)args[2], (Integer)args[1], (Integer)args[0]);
    }
}
