package org.railgun;

import org.railgun.action.ActionController;
import org.railgun.canvas.View;
import org.railgun.marshal.CodeObject;
import org.railgun.vm.Interpreter;

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
            CodeObject co = ActionController.getActionController().getUpdateFunction();

            if (co != null) {
                View.getView().clear();
                Interpreter.getInstance().run(co);
            }

            long duration = System.currentTimeMillis() - begin;

            // make sure only 50 frames per second
            if (duration < 50) {
                try {
                    Thread.sleep(50 - duration);
                } catch (InterruptedException e) {
                }
            }
        }
    }

    public void exit() {
        hasDone = true;
    }
}
