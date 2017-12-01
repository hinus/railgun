package org.railgun.shape;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;

import static java.lang.Math.cos;
import static java.lang.Math.sin;

/**
 * Created by hinus on 2017/12/1.
 */
public class Star extends AbstractShape {
    public double radius;
    public Color color;
    public double rotateAngular = 0.0;

    public double[] xs = new double[5];
    public double[] ys = new double[5];

    private double bx;
    private double by;

    static double angular = 72 * Math.PI / 180;

    public Star(int x, int y, double radius, Color color) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;

        for (int i = 0; i < 5; i++) {
            double a = 3 * Math.PI / 2 + angular * i + rotateAngular;
            xs[i] = (int) (x + radius * Math.cos(a));
            ys[i] = (int) (y + radius * Math.sin(a));
        }

        bx = x;
        by = (int) (y + radius * Math.sin(angular / 4) / Math.sin(Math.PI - 3 * angular / 4));

        int tx = (int)((bx - x) * cos(rotateAngular) - (by - y) * sin(rotateAngular)) + x;
        int ty = (int)((by - y) * cos(rotateAngular) + (bx - x) * sin(rotateAngular)) + y;

        bx = tx;
        by = ty;
    }

    public static Star makeStar(int x, int y, double radius) {
        return new Star(x, y, radius, Color.YELLOW);
    }

    @Override
    public void draw(GraphicsContext gc) {
        double[] xa = {xs[0], xs[2], bx, xs[3]};
        double[] ya = {ys[0], ys[2], by, ys[3]};

        double[] xb = {xs[1], xs[4], bx};
        double[] yb = {ys[1], ys[4], by};

        Paint oldColor = gc.getFill();
        gc.setFill(this.color);
        gc.fillPolygon(xa, ya, 4);
        gc.fillPolygon(xb, yb, 3);
        gc.setFill(oldColor);

        /*
        gc.moveTo(xs[0], ys[0]);
        gc.lineTo(xs[2], ys[2]);
        gc.lineTo(xs[4], ys[4]);
        gc.lineTo(xs[1], ys[1]);
        gc.lineTo(xs[3], ys[3]);
        gc.lineTo(xs[0], ys[0]);

        gc.stroke();*/
    }

    public Star copy() {
        return new Star(this.x, this.y, this.radius, this.color);
    }

    public Shape rotate(double rotateAngular) {
        this.rotateAngular = rotateAngular;

        for (int i = 0; i < 5; i++) {
            double a = 3 * Math.PI / 2 + angular * i + rotateAngular;
            xs[i] = (int) (x + radius * Math.cos(a));
            ys[i] = (int) (y + radius * Math.sin(a));
        }

        bx = x;
        by = (int) (y + radius * Math.sin(angular / 4) / Math.sin(Math.PI - 3 * angular / 4));

        int tx = (int)((bx - x) * cos(rotateAngular) - (by - y) * sin(rotateAngular)) + x;
        int ty = (int)((by - y) * cos(rotateAngular) + (bx - x) * sin(rotateAngular)) + y;

        bx = tx;
        by = ty;

        return this;
    }

    public Shape shift(int x, int y) {
        this.x += x;
        this.y += y;

        for (int i = 0; i < 5; i++) {
            xs[i] += x;
            ys[i] += y;
        }

        bx = x;
        by = (int) (y + radius * Math.sin(angular / 4) / Math.sin(Math.PI - 3 * angular / 4));

        int tx = (int)((bx - x) * cos(rotateAngular) - (by - y) * sin(rotateAngular)) + x;
        int ty = (int)((by - y) * cos(rotateAngular) + (bx - x) * sin(rotateAngular)) + y;

        bx = tx;
        by = ty;

        return this;
    }

    @Override
    public Shape scale(double scalar) {
        this.radius *= scalar;

        for (int i = 0; i < 5; i++) {
            double a = 3 * Math.PI / 2 + angular * i + rotateAngular;
            xs[i] = (int) (x + radius * Math.cos(a));
            ys[i] = (int) (y + radius * Math.sin(a));
        }

        bx = x;
        by = (int) (y + radius * Math.sin(angular / 4) / Math.sin(Math.PI - 3 * angular / 4));

        int tx = (int)((bx - x) * cos(rotateAngular) - (by - y) * sin(rotateAngular)) + x;
        int ty = (int)((by - y) * cos(rotateAngular) + (bx - x) * sin(rotateAngular)) + y;

        bx = tx;
        by = ty;

        return this;
    }
}
