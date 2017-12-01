package org.railgun.shape;

import javafx.scene.canvas.GraphicsContext;

/**
 * Created by hinus on 2017/6/4.
 */
public class Arrow extends AbstractShape {
    double x1;
    double y1;
    double x2;
    double y2;

    private Arrow(double x1, double y1, double x2, double y2) {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
    }

    @Override
    public void draw(GraphicsContext gc) {

    }
}
