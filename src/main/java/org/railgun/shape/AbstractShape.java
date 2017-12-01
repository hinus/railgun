package org.railgun.shape;

import static java.lang.Math.cos;
import static java.lang.Math.sin;

/**
 * Created by hinus on 2017/11/30.
 */
public abstract class AbstractShape implements Shape {
    private int layer;

    protected int x;
    protected int y;

    protected double offsetX;
    protected double offsetY;

    public AbstractShape(int layer) {
        this.layer = layer;
    }

    public AbstractShape() {
    }

    @Override
    public int getLayer() {
        return layer;
    }

    @Override
    public void setLayer(int layer) {
        this.layer = layer;
    }

    @Override
    public void setX(int x) {
        this.x = x;
    }

    @Override
    public void setY(int y) {
        this.y = y;
    }

    @Override
    public void setOffsetX(double offsetX) {
        System.out.println("offset is " + offsetX + " target x is " + (this.x + offsetX));
        this.offsetX = offsetX;
    }

    @Override
    public void setOffsetY(double offsetY) {
        this.offsetY = offsetY;
    }

    @Override
    public void update(long frameCnt) {

    }

    @Override
    public Shape shift(int x, int y) {
        this.x += x;
        this.y += y;

        return this;
    }

    @Override
    public Shape rotate(int x0, int y0, double angular) {
        int tx = (int)((x - x0) * cos(angular) - (y - y0) * sin(angular)) + x0;
        int ty = (int)((y - y0) * cos(angular) + (x - x0) * sin(angular)) + y0;

        this.x = tx;
        this.y = ty;

        this.rotate(angular);

        return this;
    }

    @Override
    public Shape rotate(double angular) {
        return null;
}

    public AbstractShape copy() {
        return null;
    }

    @Override
    public Shape scale(double scalar) {
        return null;
    }
}
