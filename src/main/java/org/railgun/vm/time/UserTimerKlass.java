package org.railgun.vm.time;

import org.railgun.vm.object.AbstractBuiltinMethodObject;
import org.railgun.vm.object.Klass;
import org.railgun.vm.object.RGObject;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/14.
 */
public class UserTimerKlass extends Klass {
    private static UserTimerKlass instance = new UserTimerKlass();

    public static UserTimerKlass getInstance() {
        return instance;
    }

    private UserTimerKlass() {
        super();
        this.klassProps.put("stop", new UserTimerStopMethod());
    }

    @Override
    public RGObject allocate() {
        return new UserTimer(this, null);
    }
}

class UserTimerStopMethod extends AbstractBuiltinMethodObject<Void> {
    @Override
    public Void call(Object... args) {
        ((UserTimer)this.owner).setEnabled(false);
        return null;
    }
}