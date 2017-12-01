package org.railgun.shape;

import javafx.scene.canvas.GraphicsContext;

/**
 * Created by hinus on 2017/12/2.
 */
public class RGLine extends AbstractShape {
    private int x2;
    private int y2;

    public RGLine(int x, int y, int x2, int y2) {
        this.x = x;
        this.y = y;
        this.x2 = x2;
        this.y2 = y2;
    }

    @Override
    public void draw(GraphicsContext gc) {
        gc.strokeLine(x, y, x2, y2);
    }
}
