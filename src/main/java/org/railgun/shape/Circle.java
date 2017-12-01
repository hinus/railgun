package org.railgun.shape;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;

/**
 * Created by hinus on 2017/11/30.
 */
public class Circle extends AbstractShape {
    private double width;
    private double height;

    private double centerX;
    private double centerY;

    private boolean withBorder;
    private double borderWidth;

    private boolean isFilled;
    private Color color;

    public Circle(int x, int y, double width, double height) {
        super(0);
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;

        this.centerX = this.x + this.width / 2;
        this.centerY = this.y + this.height / 2;
    }

    public static Circle makeCircle(int x, int y, double width, double height, boolean isFilled) {
        Circle r = new Circle(x, y, width, height);
        r.withBorder = false;
        r.isFilled = isFilled;
        r.color = Color.rgb(127, 127, 127);
        return r;
    }

    public static Circle makeCircle(int x, int y, double radius, Color color) {
        Circle r = new Circle(x, y, radius, radius);
        r.withBorder = false;
        r.isFilled = true;
        r.color = color;
        return r;
    }

    @Override
    public void draw(GraphicsContext gc) {
        double x = this.x + this.offsetX;
        double y = this.y + this.offsetY;

        if (withBorder) {
            gc.strokeOval(x, y, width, height);
        }

        if (isFilled) {
            Paint oldColor = gc.getFill();
            gc.setFill(color);
            gc.fillOval(x, y, width, height);
            gc.setFill(oldColor);
        }
    }
}
