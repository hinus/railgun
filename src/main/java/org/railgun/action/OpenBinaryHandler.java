package org.railgun.action;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.TextArea;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import org.railgun.Controls;
import org.railgun.FileManager;

import java.io.*;

/**
 * Created by hinus on 2017/12/1.
 */
public class OpenBinaryHandler implements EventHandler<ActionEvent> {
    private File initialDirectory = null;

    @Override
    public void handle(ActionEvent event) {
        Stage mainStage = Controls.getInstance().getMainStage();
        FileManager fileManager = FileManager.getInstance();

        if (fileManager.isDirty()) {
            if (!fileManager.tryToSaveDirtyFile()) {
                return;
            }
        }

        Controls.getInstance().closeTimer();

        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Binary File");
        if (initialDirectory != null)
            fileChooser.setInitialDirectory(initialDirectory);
        else
            fileChooser.setInitialDirectory(new File("C:\\hinusDocs\\github\\railgun\\src\\main\\python\\rgparser\\rg"));
        fileChooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("RailGun Binary File", "*.rgb"));

        File selectedFile = fileChooser.showOpenDialog(mainStage);

        if (selectedFile == null) {
            return;
        }

        String sourceFileName = selectedFile.getAbsolutePath();

        initialDirectory = selectedFile.getParentFile();

        fileManager.setBinaryFileName(sourceFileName);

        long length = selectedFile.length();
        if (length > 256 * 1024) {
            System.out.println("binary file is too large");
            return;
        }
        byte[] sourceContent = new byte[(int)length];

        try {
            FileInputStream fileInputStream = new FileInputStream(selectedFile);
            fileInputStream.read(sourceContent);
            fileManager.setBinaryContent(sourceContent);

            fileInputStream.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
