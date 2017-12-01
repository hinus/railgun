package org.railgun.animation;

import org.railgun.Controls;
import org.railgun.shape.Shape;

/**
 * Created by hinus on 2017/12/1.
 */
public class TransitionController implements Controller{
    private Shape owner;

    private int targetX;
    private int targetY;

    private int duration;

    private int startFrame;

    private boolean autoReplay;

    public TransitionController(Shape owner, int targetX, int targetY, int duration, int startFrame, boolean autoReplay) {
        this.owner = owner;
        this.targetX = targetX;
        this.targetY = targetY;
        this.duration = duration;
        this.startFrame = startFrame;
        this.autoReplay = autoReplay;
    }

    public void update(long frameCnt) {
        long frame = (frameCnt - startFrame) % duration;
        double x = targetX * frame * 1.0 / duration;
        double y = targetY * frame * 1.0 / duration;

        if ((frameCnt & 63) == 0)
            System.out.println(x);

        owner.setOffsetX((int)x);
        owner.setOffsetY((int)y);
    }
}
