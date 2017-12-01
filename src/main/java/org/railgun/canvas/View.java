package org.railgun.canvas;

import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import org.railgun.Controls;
import org.railgun.shape.Shape;

import java.util.ArrayList;

/**
 * Created by hinus on 2017/12/1.
 */
public class View {
    private static View view = new View(Controls.getInstance().getCanvas());

    private Canvas canvas;
    private GraphicsContext graph;

    private View(Canvas canvas) {
        this.canvas = canvas;
        this.graph = canvas.getGraphicsContext2D();
        this.graph.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
    }

    public static View getView() {
        return view;
    }

    public void update(ArrayList<Shape> shapes) {
        graph.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
        for (Shape shape : shapes) {
            shape.draw(graph);
        }
    }

    public void drawShape(Shape shape) {
        shape.draw(graph);
    }

    public void clear() {
        this.graph.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
    }
}
