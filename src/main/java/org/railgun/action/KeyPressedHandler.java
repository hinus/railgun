package org.railgun.action;

import javafx.event.EventHandler;
import javafx.scene.input.KeyEvent;
import org.railgun.marshal.CodeObject;
import org.railgun.vm.Interpreter;

/**
 * Created by hinus on 2017/12/2.
 */
public class KeyPressedHandler implements EventHandler<KeyEvent> {
    @Override
    public void handle(KeyEvent event) {
        CodeObject co = null;
        switch (event.getCode()) {
            case UP:
                co = (CodeObject) ActionController.getActionController().getKeyMap().get("VK_UP");
                break;
            case DOWN:
                co = (CodeObject) ActionController.getActionController().getKeyMap().get("VK_DOWN");
                break;
            case LEFT:
                co = (CodeObject) ActionController.getActionController().getKeyMap().get("VK_LEFT");
                break;
            case RIGHT:
                co = (CodeObject) ActionController.getActionController().getKeyMap().get("VK_RIGHT");
                break;
            case SPACE:
                co = (CodeObject) ActionController.getActionController().getKeyMap().get("VK_SPACE");
                break;
        }
        Interpreter.getInstance().run(co);
    }
}
