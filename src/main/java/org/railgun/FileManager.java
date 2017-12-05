package org.railgun;

import javafx.scene.control.ButtonType;
import javafx.scene.control.Dialog;
import javafx.stage.FileChooser;

import java.io.*;
import java.util.Optional;

/**
 * Created by hinus on 2017/11/30.
 */
public class FileManager {
    private static FileManager instance = new FileManager();

    private String sourceFileName;
    private String binaryFileName;

    private boolean isDirty;

    public boolean isDirty() {
        return isDirty;
    }

    public void setDirty(boolean dirty) {
        isDirty = dirty;
    }

    private byte[] binaryContent;

    private FileManager() {
    }

    public static FileManager getInstance() {
        return instance;
    }

    public String getSourceFileName() {
        return sourceFileName;
    }

    public void setSourceFileName(String sourceFileName) {
        this.sourceFileName = sourceFileName;
    }

    public String getBinaryFileName() {
        return binaryFileName;
    }

    public byte[] getBinaryContent() {
        return binaryContent;
    }

    public void setBinaryContent(byte[] binaryContent) {
        this.binaryContent = binaryContent;
    }

    public void setBinaryFileName(String binaryFileName) {
        this.binaryFileName = binaryFileName;
    }

    public void clear() {
        this.sourceFileName = null;

        this.binaryContent = null;
        this.binaryFileName = null;
    }

    /**
     *
     * @return true, if save file successfully.
     */
    public boolean saveCurrentFile() {
        if (!isDirty)
            return true;

        String s = Controls.getInstance().getSourceCode().getText();

        if (sourceFileName != null && !sourceFileName.equals("")) {
            FileOutputStream fos = null;

            try {
                fos = new FileOutputStream(sourceFileName, false);
                fos.write(s.getBytes());
                fos.flush();
                fos.close();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
            }
        }
        else {
            FileChooser fileChooser = new FileChooser();
            fileChooser.setTitle("Save RailGun File");
            fileChooser.getExtensionFilters().addAll(
                    new FileChooser.ExtensionFilter("railgun file", "*.rg"));

            File selectedFile = fileChooser.showSaveDialog(Controls.getInstance().getMainStage());

            if (selectedFile == null)
                return false;

            try {
                FileOutputStream fos = new FileOutputStream(selectedFile);
                fos.write(s.getBytes());
                fos.flush();
                fos.close();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        isDirty = false;
        return true;
    }

    /**
     *
     * @return shouldContinue. If dirty file is saved, continue; if user choose to not save,
     * continue; else, abort.
     */
    public boolean tryToSaveDirtyFile() {
        Dialog<ButtonType> dialog = new Dialog<>();
        dialog.setHeaderText("Warning!");
        dialog.setContentText("File has not been saved, do you want to save it?");
        dialog.getDialogPane().getButtonTypes().addAll(ButtonType.YES, ButtonType.NO, ButtonType.CANCEL);
        Optional<ButtonType> result = dialog.showAndWait();

        if (!result.isPresent())
            return false;

        if (result.get() == ButtonType.NO) {
            return true;
        }
        else if (result.get() == ButtonType.YES) {
            return FileManager.getInstance().saveCurrentFile();
        }
        else if (result.get() == ButtonType.CANCEL) {
            return false;
        }
        else
            return false;
    }
}
