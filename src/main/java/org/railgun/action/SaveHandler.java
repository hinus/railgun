package org.railgun.action;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.stage.FileChooser;
import org.railgun.Controls;
import org.railgun.FileManager;

import java.io.*;

/**
 * Created by hinus on 2017/11/30.
 */
public class SaveHandler implements EventHandler<ActionEvent> {
    @Override
    public void handle(ActionEvent event) {
        FileManager.getInstance().saveCurrentFile();
    }
}
