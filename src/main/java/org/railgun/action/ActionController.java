package org.railgun.action;

import org.railgun.vm.object.RGFunctionObject;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/2.
 */
public class ActionController {
    private static ActionController actionController = new ActionController();

    private HashMap keyMap = new HashMap<>();

    private HashMap mouseMap = new HashMap();

    private volatile RGFunctionObject updateFunction;

    public RGFunctionObject getUpdateFunction() {
        return updateFunction;
    }

    public void setUpdateFunction(RGFunctionObject updateFunction) {
        this.updateFunction = updateFunction;
    }

    public ActionController() {
    }

    public HashMap getKeyMap() {
        return keyMap;
    }

    public void setKeyMap(HashMap keyMap) {
        this.keyMap = keyMap;
    }

    public static ActionController getActionController() {
        return actionController;
    }

    public HashMap getMouseMap() {
        return mouseMap;
    }

    public void setMouseMap(HashMap mouseMap) {
        this.mouseMap = mouseMap;
    }
}
