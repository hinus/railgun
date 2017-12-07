package org.railgun.vm.intrisinc;

import org.railgun.action.ActionController;
import org.railgun.marshal.CodeObject;

/**
 * Created by hinus on 2017/12/7.
 */
public class UpdateFunctionMethod implements InnerMethod<Void> {
    @Override
    public Void call(Object... args) {
        ActionController.getActionController().setUpdateFunction((CodeObject)args[0]);
        return null;
    }
}
