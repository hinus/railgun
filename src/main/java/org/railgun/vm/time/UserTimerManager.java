package org.railgun.vm.time;

import org.railgun.Timer;
import org.railgun.marshal.CodeObject;
import org.railgun.vm.Interpreter;

import java.util.PriorityQueue;

/**
 * Created by hinus on 2017/12/13.
 */
public class UserTimerManager {
    private static UserTimerManager manager = new UserTimerManager();

    private PriorityQueue<UserTimer> timerQueue;

    private UserTimerManager() {
        timerQueue = new PriorityQueue<>();
    }

    public static UserTimerManager getManager() {
        return manager;
    }

    public UserTimer addTimer(int frame, CodeObject onTimer, boolean isLoop) {
        UserTimer u = (UserTimer) UserTimerKlass.getInstance().allocate();
        u.setEventFrame(frame);
        u.setOnTimer(onTimer);
        u.setLoop(isLoop);
        u.setEnabled(true);

        u.setRegFrame(Timer.frameCnt);
        timerQueue.add(u);

        return u;
    }

    public void refresh(long frameCnt) {
        if (timerQueue.isEmpty())
            return;

        UserTimer topTimer = timerQueue.peek();
        if (frameCnt < topTimer.getRegFrame() + topTimer.getEventFrame())
            return;

        while (topTimer.getRegFrame() + topTimer.getEventFrame() < frameCnt) {
            if (topTimer.isEnabled()) {
                Interpreter.getInstance().run(topTimer.getOnTimer());
            }

            timerQueue.remove();

            if (topTimer.isEnabled() && topTimer.isLoop()) {
                topTimer.setRegFrame(frameCnt);
                timerQueue.add(topTimer);
            }

            if (timerQueue.isEmpty())
                break;

            topTimer = timerQueue.peek();
        }
    }
}
