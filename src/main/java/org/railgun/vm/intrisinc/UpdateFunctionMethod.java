package org.railgun.vm.intrisinc;

import org.railgun.action.ActionController;
import org.railgun.vm.object.RGFunctionObject;

/**
 * Created by hinus on 2017/12/7.
 */
public class UpdateFunctionMethod implements InnerMethod<Void> {
    @Override
    public Void call(Object... args) {
        ActionController.getActionController().setUpdateFunction((RGFunctionObject) args[0]);
        return null;
    }
}
