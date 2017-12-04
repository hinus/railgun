package org.railgun.vm.intrisinc;

import javafx.scene.paint.Color;
import org.railgun.shape.Circle;

import java.util.concurrent.Callable;

/**
 * Created by hinus on 2017/12/4.
 */
public class CircleMethod implements InnerMethod<Circle>{
    @Override
    public Circle call(Object... args) {
        return Circle.makeCircle((Integer) args[3],
                (Integer)args[2],
                ((Integer) args[1]).doubleValue(),
                (Color)args[0]);
    }
}
