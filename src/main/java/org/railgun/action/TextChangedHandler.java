package org.railgun.action;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import org.railgun.FileManager;

/**
 * Created by hinus on 2017/11/30.
 */
public class TextChangedHandler implements ChangeListener {
    @Override
    public void changed(ObservableValue observable, Object oldValue, Object newValue) {
        FileManager.getInstance().setDirty(true);
    }
}
