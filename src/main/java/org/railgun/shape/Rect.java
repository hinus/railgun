package org.railgun.shape;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;

/**
 * Created by hinus on 2017/6/3.
 */
public class Rect extends AbstractShape {

    private double width;
    private double height;

    private boolean withBorder;
    private double borderWidth;

    private boolean isFilled;
    private Color color;

    public Rect(int x, int y, double width, double height) {
        super(0);
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    public static Rect makeRect(int x, int y, double width, double height, boolean isFilled, Color color) {
        Rect r = new Rect(x, y, width, height);
        r.withBorder = false;
        r.isFilled = isFilled;
        r.color = color;
        return r;
    }

    @Override
    public void draw(GraphicsContext gc) {
        double x = this.x + this.offsetX;
        double y = this.y + this.offsetY;

        if (withBorder) {
            gc.strokeRect(x, y, width, height);
        }

        if (isFilled) {
            Paint oldColor = gc.getFill();
            gc.setFill(color);
            gc.fillRect(x, y, width, height);
            gc.setFill(oldColor);
        }
    }
}
