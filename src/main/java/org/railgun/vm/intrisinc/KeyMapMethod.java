package org.railgun.vm.intrisinc;

import org.railgun.action.ActionController;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/7.
 */
public class KeyMapMethod implements InnerMethod<Void> {
    @Override
    public Void call(Object... args) {
        ActionController.getActionController().setKeyMap((HashMap)args[0]);
        return null;
    }
}
