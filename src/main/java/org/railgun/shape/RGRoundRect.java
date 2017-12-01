package org.railgun.shape;

import javafx.scene.canvas.GraphicsContext;

/**
 * Created by hinus on 2017/12/2.
 */
public class RGRoundRect extends AbstractShape {
    private int arcWidth;
    private int arcHeight;

    private int width;
    private int height;

    private RGRoundRect(int x, int y, int w, int h, int arcWith, int arcHeight) {
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = h;
        this.arcWidth = arcWith;
        this.arcHeight = arcHeight;
    }

    public static RGRoundRect makeRoundRect(int x, int y, int w, int h, int arcWidth, int arcHeight) {
        return new RGRoundRect(x, y, w, h, arcWidth, arcHeight);
    }

    @Override
    public void draw(GraphicsContext gc) {
        gc.strokeRoundRect(x, y, width, height, arcWidth, arcHeight);
    }
}
