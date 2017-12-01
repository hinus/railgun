package org.railgun.action;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import org.railgun.Controls;
import org.railgun.FileManager;

/**
 * Created by hinus on 2017/11/30.
 */
public class NewFileHandler implements EventHandler<ActionEvent> {
    @Override
    public void handle(ActionEvent event) {
        FileManager fileManager = FileManager.getInstance();

        if (fileManager.isDirty()) {
            if (!fileManager.tryToSaveDirtyFile()) {
                return;
            }
        }

        Controls controls = Controls.getInstance();
        controls.getSourceCode().setDisable(false);
        controls.getSourceCode().clear();
        controls.closeTimer();

        FileManager.getInstance().clear();
    }
}
