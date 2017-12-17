package org.railgun.action;

import javafx.event.EventHandler;
import javafx.scene.input.KeyEvent;
import org.railgun.vm.Interpreter;
import org.railgun.vm.object.RGFunctionObject;

/**
 * Created by hinus on 2017/12/2.
 */
public class KeyPressedHandler implements EventHandler<KeyEvent> {
    @Override
    public void handle(KeyEvent event) {
        RGFunctionObject fo = null;
        switch (event.getCode()) {
            case UP:
                fo = (RGFunctionObject) ActionController.getActionController().getKeyMap().get("VK_UP");
                break;
            case DOWN:
                fo = (RGFunctionObject) ActionController.getActionController().getKeyMap().get("VK_DOWN");
                break;
            case LEFT:
                fo = (RGFunctionObject) ActionController.getActionController().getKeyMap().get("VK_LEFT");
                break;
            case RIGHT:
                fo = (RGFunctionObject) ActionController.getActionController().getKeyMap().get("VK_RIGHT");
                break;
            case SPACE:
                fo = (RGFunctionObject) ActionController.getActionController().getKeyMap().get("VK_SPACE");
                break;
        }

        if (fo != null)
            Interpreter.getInstance().run(fo);
    }
}
