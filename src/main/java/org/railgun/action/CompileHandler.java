package org.railgun.action;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import org.railgun.FileManager;

/**
 * Created by hinus on 2017/11/30.
 */
public class CompileHandler implements EventHandler<ActionEvent> {
    @Override
    public void handle(ActionEvent event) {
        FileManager fileManager = FileManager.getInstance();
        String sourceFileName = fileManager.getSourceFileName();
        if (sourceFileName != null) {
            Process p = null;
            try {
                p = Runtime.getRuntime().exec("cmd /c \"cd .\\main\\python\\rgparser && python ddl.py\" " + fileManager.getSourceFileName());
            } catch (IOException e) {
                e.printStackTrace();
            }
            int exitVal = 0;

            try {
                exitVal = p.waitFor();
            } catch (InterruptedException e) {
                // TODO: Need to process exitVal != 0;
                e.printStackTrace();
            }

            String binaryFileName = sourceFileName + "b";

            File binaryFile = new File(binaryFileName);
            if (binaryFile == null || !binaryFile.exists()) {
                return;
            }

            fileManager.setBinaryFileName(binaryFileName);

            byte[] sourceContent = new byte[(int) binaryFile.length()];

            try {
                FileInputStream fileInputStream = new FileInputStream(binaryFile);
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
}
