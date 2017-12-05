package org.railgun.action;

import javafx.event.EventHandler;
import javafx.scene.input.MouseEvent;

/**
 * Created by hinus on 2017/12/5.
 */
public class MouseDragEnterHandler implements EventHandler<MouseEvent> {
    @Override
    public void handle(MouseEvent event) {
        System.out.println("drag begin");
        event.consume();
    }
}
