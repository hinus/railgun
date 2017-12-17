package org.railgun.action;

import javafx.event.EventHandler;
import javafx.scene.input.MouseEvent;
import org.railgun.vm.Interpreter;
import org.railgun.vm.object.RGFunctionObject;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/5.
 */
public class MouseDragHandler implements EventHandler<MouseEvent> {
    @Override
    public void handle(MouseEvent event) {
        HashMap mouseMap = ActionController.getActionController().getMouseMap();

        if (mouseMap == null || mouseMap.isEmpty())
            return;

        RGFunctionObject fo = (RGFunctionObject)mouseMap.get("DRAG");

        if (fo == null)
            return;

        Interpreter.getInstance().run(fo, Integer.valueOf((int)event.getX()), Integer.valueOf((int)event.getY()));
    }
}
