package org.railgun.action;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;

/**
 * Created by hinus on 2017/11/30.
 */
public class ExitHandler implements EventHandler<ActionEvent> {
    @Override
    public void handle(ActionEvent event) {
        System.exit(0);
    }
}
