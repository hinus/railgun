package org.railgun.vm.intrisinc;

import javafx.scene.paint.Color;
import org.railgun.shape.Rect;


/**
 * Created by hinus on 2017/12/4.
 */
public class RGRectMethod implements InnerMethod<Rect> {
    @Override
    public Rect call(Object... args) {
        return Rect.makeRect((Integer)args[4],
                (Integer)args[3],
                ((Integer)args[2]).doubleValue(),
                ((Integer)args[1]).doubleValue(),
                true, (Color)args[0]);
    }
}
