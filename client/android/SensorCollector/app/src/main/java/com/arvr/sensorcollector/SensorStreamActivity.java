package com.arvr.sensorcollector;

import android.app.Fragment;
import android.app.TabActivity;
import android.hardware.SensorManager;
import android.os.Bundle;

public class SensorStreamActivity extends TabActivity {

    public static SensorManager mSensor_Stream;
    private static int mDelay = SensorManager.SENSOR_DELAY_NORMAL;
    private static final boolean mbGyroscope = true;

    public static int getmDelay() {
        return mDelay;
    }

    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        mSensor_Stream = (SensorManager) getSystemService(SENSOR_SERVICE);

    }

}
