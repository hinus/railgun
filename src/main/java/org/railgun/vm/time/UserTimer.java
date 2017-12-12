package org.railgun.vm.time;

import org.railgun.marshal.CodeObject;

/**
 * Created by hinus on 2017/12/13.
 */
public class UserTimer implements Comparable<UserTimer> {
    private int eventFrame;
    private CodeObject onTimer;
    private boolean isLoop;

    // the frame count in which timer is registered.
    private long regFrame;

    public UserTimer(int eventFrame, CodeObject onTimer, boolean isLoop) {
        this.eventFrame = eventFrame;
        this.onTimer = onTimer;
        this.isLoop = isLoop;
    }

    public long getRegFrame() {
        return regFrame;
    }

    public void setRegFrame(long regFrame) {
        this.regFrame = regFrame;
    }

    public int getEventFrame() {
        return eventFrame;
    }

    public void setEventFrame(int eventFrame) {
        this.eventFrame = eventFrame;
    }

    public CodeObject getOnTimer() {
        return onTimer;
    }

    public void setOnTimer(CodeObject onTimer) {
        this.onTimer = onTimer;
    }

    public boolean isLoop() {
        return isLoop;
    }

    public void setLoop(boolean loop) {
        isLoop = loop;
    }

    @Override
    public int compareTo(UserTimer o) {
        if ((regFrame + eventFrame) < (o.getRegFrame() + o.getEventFrame()))
            return 1;
        else if ((regFrame + eventFrame) == (o.getRegFrame() + o.getEventFrame()))
            return 0;
        else
            return -1;
    }
}
