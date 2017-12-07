package org.railgun.vm.intrisinc;

import org.railgun.Controls;
import org.railgun.action.*;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/7.
 */
public class MouseMapMethod implements InnerMethod<Void> {
    @Override
    public Void call(Object... args) {
        ActionController.getActionController().setMouseMap((HashMap)args[0]);
        Controls.getInstance().getCanvas().setOnMousePressed(new MouseLeftClickedHandler());
        Controls.getInstance().getCanvas().setOnMouseDragEntered(new MouseDragEnterHandler());
        Controls.getInstance().getCanvas().setOnMouseDragged(new MouseDragHandler());
        Controls.getInstance().getCanvas().setOnMouseDragReleased(new MouseDragReleaseHandler());
        return null;
    }
}
