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
 * Created by hinus on 2017/11/30.
 */
public class OpenFileHandler implements EventHandler<ActionEvent> {
    private File initialDirectory = null;

    @Override
    public void handle(ActionEvent event) {
        Stage mainStage = Controls.getInstance().getMainStage();
        TextArea ta = Controls.getInstance().getSourceCode();

        FileManager fileManager = FileManager.getInstance();

        if (fileManager.isDirty()) {
            if (!fileManager.tryToSaveDirtyFile()) {
                return;
            }
        }

        Controls.getInstance().closeTimer();

        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Source File");
        if (initialDirectory != null)
            fileChooser.setInitialDirectory(initialDirectory);
        fileChooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("RailGun Source File", "*.rg"));

        File selectedFile = fileChooser.showOpenDialog(mainStage);

        if (selectedFile == null) {
            return;
        }

        String sourceFileName = selectedFile.getAbsolutePath();

        initialDirectory = selectedFile.getParentFile();

        fileManager.setSourceFileName(sourceFileName);

        String binaryFileName = sourceFileName + "b";

        File binaryFile = new File(binaryFileName);
        if (binaryFile != null && binaryFile.exists()) {
            fileManager.setBinaryFileName(binaryFileName);
        }

        long length = selectedFile.length();
        if (length > 256 * 1024) {
            System.out.println("source code file is too large");
            return;
        }
        byte[] sourceContent = new byte[(int)length];

        try {
            FileInputStream fileInputStream = new FileInputStream(selectedFile);
            fileInputStream.read(sourceContent);
            BufferedReader reader = new BufferedReader(new InputStreamReader(new ByteArrayInputStream(sourceContent)));

            String s;
            ta.clear();
            ta.setDisable(false);
            while ((s = reader.readLine()) != null) {
                ta.appendText(s);
                ta.appendText("\n");
            }
            fileManager.setDirty(false);

            reader.close();
            fileInputStream.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
