package org.railgun.shape;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.text.Font;

/**
 * Created by hinus on 2017/6/4.
 */
public class RGText extends AbstractShape {
    String text;
    Font font;

    private RGText(String text, int x, int y, String fontFamily, double fontSize) {
        this.text = text;
        this.x = x;
        this.y = y;

        this.font = Font.font(fontFamily, fontSize);
    }

    public static RGText makeText(String text, int x, int y, String fontFamily, double size) {
        RGText t = new RGText(text, x, y, fontFamily, size);
        return t;
    }

    @Override
    public void draw(GraphicsContext gc) {
        double x = this.x + this.offsetX;
        double y = this.y + this.offsetY;

        Font old = gc.getFont();
        gc.setFont(this.font);
        gc.fillText(text, x, y);
        gc.setFont(old);
    }
}