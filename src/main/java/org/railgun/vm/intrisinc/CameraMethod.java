package org.railgun.vm.intrisinc;

import javafx.scene.Camera;
import javafx.scene.PerspectiveCamera;
import org.railgun.Controls;

import javax.sound.midi.ControllerEventListener;

/**
 * Created by hinus on 2017/12/6.
 */
public class CameraMethod implements InnerMethod {
    @Override
    public Object call(Object... args) {
        PerspectiveCamera camera = new PerspectiveCamera(true);
        Controls.getInstance().getGraph3d().getChildren().add(camera);
        Controls.getInstance().setCamera(camera);
        camera.setTranslateZ(10);
        return camera;
    }
}
