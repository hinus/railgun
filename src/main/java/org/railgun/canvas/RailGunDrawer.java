package org.railgun.canvas;

import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import org.railgun.Controls;
import org.railgun.shape.Circle;
import org.railgun.shape.Model;
import org.railgun.shape.Rect;
import org.railgun.shape.Star;

/**
 * Created by hinus on 2017/11/30.
 */
public class RailGunDrawer {
    private static RailGunDrawer railGunDrawer = new RailGunDrawer(Controls.getInstance().getCanvas());



    private RailGunDrawer(Canvas canvas) {

    }

    public static RailGunDrawer getRailGunDrawer() {
        return railGunDrawer;
    }

    public void drawCircle(int x, int y, double r) {
        Model.getModel().addShape(Circle.makeCircle(x, y, 2 * r, 2 * r, true));
    }

    public void drawStar(int x, int y, double r) {
        Model.getModel().addShape(Star.makeStar(x, y, 2 * r));
    }

    public void drawRect(int x, int y, double width, double height) {
        Model.getModel().addShape(Rect.makeRect(x, y, width, height, true, Color.RED));
    }
}
