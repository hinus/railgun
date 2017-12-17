package org.railgun;

import org.railgun.action.ActionController;
import org.railgun.canvas.View;
import org.railgun.vm.Interpreter;
import org.railgun.vm.object.RGFunctionObject;
import org.railgun.vm.time.UserTimerManager;

/**
 * Created by hinus on 2017/12/1.
 */
public class Timer extends Thread {
    volatile boolean hasDone = false;

    static int framesPerSecond = 40;
    static long frameDuration = 1000 / framesPerSecond;

    public static volatile long frameCnt = 0;

    public static void setFramesPerSecond(int framesPerSecond) {
        if (framesPerSecond <= 0 || framesPerSecond > 60)
            return;

        Timer.framesPerSecond = framesPerSecond;
        frameDuration = 1000 / framesPerSecond;
    }

    @Override
    public void run() {
        while (!hasDone) {
            frameCnt += 1;
            long begin = System.currentTimeMillis();
            RGFunctionObject fo = ActionController.getActionController().getUpdateFunction();

            if (fo != null) {
                View.getView().clear();
                Interpreter.getInstance().run(fo);
            }

            UserTimerManager.getManager().refresh(frameCnt);

            long duration = System.currentTimeMillis() - begin;

            // make sure only 50 frames per second
            if (duration < frameDuration) {
                try {
                    Thread.sleep(frameDuration - duration);
                } catch (InterruptedException e) {
                }
            }
        }
    }

    public void exit() {
        hasDone = true;
    }
}
