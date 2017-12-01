package org.railgun;

import javafx.scene.canvas.Canvas;
import javafx.scene.control.TextArea;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;

/**
 * Created by hinus on 2017/11/30.
 */
public class Controls {
    private static Controls instance = new Controls();

    private TextArea sourceCode;
    private Stage mainStage;
    private BorderPane mainPane;

    private Timer timer;

    public Timer getTimer() {
        return timer;
    }

    public void setTimer(Timer timer) {
        this.timer = timer;
    }

    public void closeTimer() {
        if (this.timer != null) {
            this.timer.exit();
            this.timer = null;
        }
    }

    public BorderPane getMainPane() {
        return mainPane;
    }

    public void setMainPane(BorderPane mainPane) {
        this.mainPane = mainPane;
    }

    private Canvas canvas;

    public static Controls getInstance() {
        return instance;
    }

    public TextArea getSourceCode() {

        return sourceCode;
    }

    public void setSourceCode(TextArea sourceCode) {
        this.sourceCode = sourceCode;
    }

    public Stage getMainStage() {
        return mainStage;
    }

    public void setMainStage(Stage mainStage) {
        this.mainStage = mainStage;
    }

    public Canvas getCanvas() {
        return canvas;
    }

    public void setCanvas(Canvas canvas) {
        this.canvas = canvas;
    }

    private Controls() {
    }
}
