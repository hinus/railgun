package org.railgun.action;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import org.railgun.Controls;
import org.railgun.FileManager;
import org.railgun.Timer;
import org.railgun.vm.Interpreter;

/**
 * Created by hinus on 2017/11/30.
 */
public class RunHandler implements EventHandler<ActionEvent> {
    @Override
    public void handle(ActionEvent event) {
        Timer timer = new Timer();
        Controls.getInstance().setTimer(timer);
        timer.setDaemon(true);
        timer.start();

        new Interpreter().run(FileManager.getInstance().getBinaryContent());
    }
}
