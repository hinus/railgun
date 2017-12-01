package org.railgun;

import com.sun.org.apache.xpath.internal.operations.Mod;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import org.railgun.action.*;
import org.railgun.animation.TransitionController;
import org.railgun.marshal.BinaryFileParser;
import org.railgun.shape.Circle;
import org.railgun.shape.Rect;
import org.railgun.shape.Star;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;


/**
 * Created by hinus on 2017/11/30.
 */
public class RailGun extends Application {
    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        Controls controlsManager = Controls.getInstance();
        controlsManager.setMainStage(primaryStage);


        // initialize canvas
        BorderPane mainPane = new BorderPane();
        Canvas canvas = new Canvas(1000, 600);
        mainPane.setCenter(canvas);
        Controls.getInstance().setCanvas(canvas);

        Scene scene = new Scene(mainPane, 1000, 750);
        scene.setOnKeyPressed(new KeyPressedHandler());

        controlsManager.setMainPane(mainPane);

        createMenu(mainPane, primaryStage);

        TextArea sourceCode = new TextArea("");
        sourceCode.setDisable(true);
        mainPane.setBottom(sourceCode);
        controlsManager.setSourceCode(sourceCode);
        sourceCode.textProperty().addListener(new TextChangedHandler());

        /*
        initPropertyPanel(mainPane);
        initMVC(canvas);
        initSceneAction(scene);
        initCanvasAction(canvas);

        canvas.setOnKeyTyped(new PaintToolAction());

        */
        primaryStage.setTitle("RailGun");
        primaryStage.setScene(scene);
        primaryStage.show();

        // some test case
        /*
        /// Chinese flag
        Star s = Star.makeStar(200, 200, 60);
        Star s2 = Star.makeStar(300, 140, 20);
        s2.rotate(-0.8771);
        Star s3 = Star.makeStar(340, 180, 20);
        s3.rotate(-0.4786);
        Star s4 = Star.makeStar(340, 240, 20);
        s4.rotate(0.0584);
        Star s5 = Star.makeStar(300, 280, 20);
        s5.rotate(0.3381);
        */


        /*
        Rect redRect = Rect.makeRect(100, 100, 180, 400, true, Color.rgb(239, 65, 53));
        Rect whiteRect = Rect.makeRect(280, 100, 198, 400, true, Color.WHITE);
        Rect blueRect = Rect.makeRect(478, 100, 222, 400, true, Color.rgb(0, 85, 164));*/


        /*
        try {
            File f = new File("C:/test.pyc");
            FileInputStream fis = new FileInputStream(f);
            byte[] buf = new byte[10 * 1024];
            fis.read(buf);
            BinaryFileParser.parse(buf);
        } catch (IOException e) {
            e.printStackTrace();
        }*/

        /*
        Circle c = Circle.makeCircle(200, 200, 60, 60, true);
        c.setMoveController(new TransitionController(c, 400, 0, 500, 0, true));
        */
    }

    public void createMenu(BorderPane mainPane, Stage mainStage) {
        MenuBar menuBar = new MenuBar();
        Menu menuFile = new Menu("File");

        MenuItem openFile = new MenuItem("Open");
        MenuItem newFile = new MenuItem("New");
        MenuItem saveFile = new MenuItem("Save");
        MenuItem closeFile = new MenuItem("Close");
        MenuItem exitMain = new MenuItem("Exit");

        MenuItem openBinary = new MenuItem("Open Binary");

        menuFile.getItems().addAll(openFile, newFile, saveFile, closeFile, new SeparatorMenuItem(), openBinary, new SeparatorMenuItem(), exitMain);

        Menu menuRun = new Menu("Run");

        MenuItem compileRG = new MenuItem("Compile");
        MenuItem runRG = new MenuItem("Run");

        menuRun.getItems().addAll(compileRG, runRG);

        menuBar.getMenus().addAll(menuFile, menuRun);

        // set actions
        openFile.setOnAction(new OpenFileHandler());
        newFile.setOnAction(new NewFileHandler());
        saveFile.setOnAction(new SaveHandler());
        closeFile.setOnAction(new CloseHandler());

        openBinary.setOnAction(new OpenBinaryHandler());

        exitMain.setOnAction(new ExitHandler());

        compileRG.setOnAction(new CompileHandler());
        runRG.setOnAction(new RunHandler());

        mainPane.setTop(menuBar);
    }
}
