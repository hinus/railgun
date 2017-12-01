package org.railgun.action;

import org.railgun.marshal.CodeObject;

import java.util.HashMap;

/**
 * Created by hinus on 2017/12/2.
 */
public class ActionController {
    private static ActionController actionController = new ActionController();

    private HashMap keyMap = new HashMap<>();

    private CodeObject updateFunction;

    public CodeObject getUpdateFunction() {
        return updateFunction;
    }

    public void setUpdateFunction(CodeObject updateFunction) {
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
}
