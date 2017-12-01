package org.railgun;

import org.railgun.shape.Model;

/**
 * Created by hinus on 2017/12/1.
 */
public class Timer extends Thread {
    volatile boolean hasDone = false;

    long frameCnt = 0;

    @Override
    public void run() {
        while (!hasDone) {
            frameCnt += 1;
            long begin = System.currentTimeMillis();
            Model.getModel().update(frameCnt);
            long duration = System.currentTimeMillis() - begin;
            if (frameCnt % 50 == 0) {
                System.out.print(duration);
            }

            // make sure only 50 frames per second
            if (duration < 20) {
                try {
                    Thread.sleep(20 - duration);
                } catch (InterruptedException e) {
                }
            }
        }
    }

    public void exit() {
        hasDone = true;
    }
}
