package org.railgun.action;

import javafx.event.EventHandler;
import javafx.scene.input.MouseEvent;
import org.railgun.marshal.CodeObject;
import org.railgun.vm.Interpreter;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/4.
 */
public class MouseLeftClickedHandler implements EventHandler<MouseEvent> {
    @Override
    public void handle(MouseEvent event) {
        HashMap mouseMap = ActionController.getActionController().getMouseMap();

        if (mouseMap == null || mouseMap.isEmpty())
            return;

        CodeObject co = (CodeObject)mouseMap.get("LEFT_CLICK");

        if (co == null)
            return;

        Interpreter.getInstance().run(co, Integer.valueOf((int)event.getX()), Integer.valueOf((int)event.getY()));
    }
}
