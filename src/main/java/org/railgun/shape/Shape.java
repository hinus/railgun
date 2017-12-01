package org.railgun.shape;

import javafx.scene.canvas.GraphicsContext;

/**
 * Created by hinus on 2017/6/3.
 */
public interface Shape {
    void draw(GraphicsContext gc);
    void setX(int x);
    void setY(int y);

    int getX();
    int getY();

    void setOffsetX(double offsetX);
    void setOffsetY(double offsetY);

    int getLayer();
    void setLayer(int layer);

    Shape shift(int x, int y);
    Shape rotate(int x0, int y0, double angular);
    Shape rotate(double angular);
    Shape scale(double scalar);
}
