package org.railgun.shape;

import org.railgun.canvas.View;

import java.util.ArrayList;

/**
 * Created by hinus on 2017/12/1.
 */
public class Model {
    private static Model model = new Model();

    public static Model getModel() {
        return model;
    }

    private ArrayList<Shape> shapes;

    private Model() {
        shapes = new ArrayList<>();
    }

    public void addShape(Shape shape) {
        shapes.add(shape);
    }

    public void update(long frameCnt) {
        for (Shape shape : shapes) {
            shape.update(frameCnt);
        }

        View.getView().update(shapes);
    }
}
