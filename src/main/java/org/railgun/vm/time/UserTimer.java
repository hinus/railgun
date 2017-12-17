package org.railgun.vm.time;

import org.railgun.vm.object.Klass;
import org.railgun.vm.object.RGFunctionObject;
import org.railgun.vm.object.RGObject;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/13.
 */
public class UserTimer extends RGObject implements Comparable<UserTimer> {
    private int eventFrame;
    private RGFunctionObject onTimer;
    private boolean isLoop;

    private boolean enabled;

    // the frame count in which timer is registered.
    private long regFrame;

    public UserTimer(int eventFrame, RGFunctionObject onTimer, boolean isLoop) {
        this.eventFrame = eventFrame;
        this.onTimer = onTimer;
        this.isLoop = isLoop;
    }

    public UserTimer() {
    }

    public UserTimer(Klass klass, HashMap<String, Object> properties) {
        super(klass, properties);
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

    public RGFunctionObject getOnTimer() {
        return onTimer;
    }

    public void setOnTimer(RGFunctionObject onTimer) {
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

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}
