package com.arvr.sensorcollector;


import static android.content.Context.SENSOR_SERVICE;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;
import android.widget.ToggleButton;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Locale;

/**
 * A simple Fragment subclass.
 */
public class SettingsFragment extends Fragment
{
    private FragmentTwoListener listener;

    public static DatagramSocket mSocket = null;
    public static DatagramPacket mPacket = null;

    private static final double NS2S = 1.0f / 1000000000.0f; // nanosec to sec
    private double[] mGyroBuffer = new double[3];
    private double[] mRotationBuffer = new double[3];
    private double[] mAcceleroBuffer = new double[3];
    private boolean mGyroBufferReady = false;
    private boolean mRotationBufferReady = false;
    private boolean mAcceleroBufferReady = false;
    private double mGyroTime = 0;
    private double mAccTime = 0;
    StringBuilder mStrBuilder = new StringBuilder(256);
    private static final String CSV_ID_GYROSCOPE = "G";
    private static final String CSV_ID_ROTATION = "R";
    private String mSensordata;
    private int mCounter = 0;
    private int mScreenDelay = 15;
    private static boolean mStream_Active = false;
    public static SensorManager mSensor_Stream;
    private static int mDelay = SensorManager.SENSOR_DELAY_NORMAL;

    private EditText mIP_Adress;
    private EditText mPort;
    private ProgressBar mProgessBar;
    private ToggleButton mToggleButton_Stream;


    public class My_Hardware_SensorListener implements SensorEventListener
    {
        @Override
        public void onSensorChanged(SensorEvent event)
        {
            String timeStamp = new SimpleDateFormat("HHmmss").format(Calendar.getInstance().getTime());

            if (event.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
                mGyroBuffer[0] = event.values[0];
                mGyroBuffer[1] = event.values[1];
                mGyroBuffer[2] = event.values[2];
                mGyroBufferReady = true;
            }
            else if (event.sensor.getType() == Sensor.TYPE_ROTATION_VECTOR)
            {
                mRotationBuffer[0] = event.values[0];
                mRotationBuffer[1] = event.values[1];
                mRotationBuffer[2] = event.values[2];
                mRotationBufferReady = true;
            }
            else if(event.sensor.getType() == Sensor.TYPE_ACCELEROMETER)
            {
                mAcceleroBuffer[0] = event.values[0];
                mAcceleroBuffer[1] = event.values[1];
                mAcceleroBuffer[2] = event.values[2];
                mAcceleroBufferReady = true;

            }
            else {
                return;
            }


            boolean gyroReady = (mGyroBufferReady == true);
            boolean rotationReady = (mRotationBufferReady == true);
            boolean acceleroReady = (mAcceleroBufferReady == true);

            mStrBuilder.setLength(0);

            if (gyroReady && rotationReady && acceleroReady)
            {
                double[] finalBuffer = new double[9];
                int i = 0;
                for (; i < finalBuffer.length / 3; i++) {
                    finalBuffer[i] = mGyroBuffer[i];
                }
                for (; i < (finalBuffer.length / 3) + 3; i++) {
                    finalBuffer[i] = mAcceleroBuffer[i - 3];
                }
                for (; i < finalBuffer.length; i++) {
                    finalBuffer[i] = mRotationBuffer[i - 6];
                }

                // Get which button is held pressed
                String buttonName = listener.getButtonName();

                addSensorToString(mStrBuilder, buttonName, CSV_ID_GYROSCOPE, CSV_ID_ROTATION, finalBuffer);
                mGyroBufferReady = false;
                mRotationBufferReady = false;
                mAcceleroBufferReady = false;

                mStrBuilder.insert(0, String.format(Locale.ENGLISH, "%s,", timeStamp));
                mSensordata = mStrBuilder.toString();

                // Get streaming status
                boolean streamStatus = listener.getStreamStatus();

                // Check if streaming is allowed
                if (streamStatus) {
                    // Start a new thread for sending data over UDP
                    new UDPThread(mSensordata).execute();
                }
            }

            // Incase the gyro sensor is not responding / not present
            else if (rotationReady && acceleroReady && !gyroReady)
            {
                // Get which button is held pressed
                String buttonName = listener.getButtonName();

                mStrBuilder.append(String.format(Locale.ENGLISH,
                        "%s,%s,%s,%s," + "%7.3f,%7.3f,%7.3f," + "%7.3f,%7.3f,%7.3f,",
                        buttonName, "not_ready", "not_ready", "not_ready",
                        mAcceleroBuffer[0], mAcceleroBuffer[1], mAcceleroBuffer[2],
                        mRotationBuffer[0], mRotationBuffer[0], mRotationBuffer[0]));

                mGyroBufferReady = false;
                mRotationBufferReady = false;
                mAcceleroBufferReady = false;

                mStrBuilder.insert(0, String.format(Locale.ENGLISH, "%s,", timeStamp));
                mSensordata = mStrBuilder.toString();

                // Get streaming status
                boolean streamStatus = listener.getStreamStatus();

                // Check if streaming is allowed
                if (streamStatus) {
                    // Start a new thread for sending data over UDP
                    new UDPThread(mSensordata).execute();
                }
            }
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy)
        {
            // Blank, Auto-generated
        }
    }

    public class MyToggle_Button_Listener implements ToggleButton.OnCheckedChangeListener
    {

        @Override
        public void onCheckedChanged(CompoundButton buttonView, boolean isChecked)
        {
            if (buttonView == mToggleButton_Stream)
            {
                if (mStream_Active == true) {
                    // TODO: Implement stopStreaming()
                    // stopStreaming();
                }
                else
                {
                    boolean streaming = startStreaming();
                    if(streaming ==false)
                    {
                        // TODO: Implement stopStreaming()
                        // stopStreaming();
                    }

                }
                mToggleButton_Stream.setChecked(mStream_Active);
            }

            else {mToggleButton_Stream.setChecked(false);}
        }

    }

    My_Hardware_SensorListener myhardwaresensorlistener = new My_Hardware_SensorListener();



    public SettingsFragment() {
        // Required empty public constructor
    }


    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onAttach(Context context)
    {
        super.onAttach(context);
        if(context instanceof FragmentTwoListener)
        { this.listener = (FragmentTwoListener) context; }
    }

    public static interface FragmentTwoListener
    {
        public boolean getStreamStatus();
        public String getButtonName();
    }



    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {

        mIP_Adress = (EditText) view.findViewById(R.id.Edit_Address_Box);
        mPort = (EditText) view.findViewById(R.id.Edit_Port_Box);
        mProgessBar = (ProgressBar)view.findViewById(R.id.progressBar);
        mProgessBar.setVisibility(View.INVISIBLE);
        mToggleButton_Stream = (ToggleButton)view.findViewById(R.id.toggleButtonStream);

        mToggleButton_Stream.setOnCheckedChangeListener(new MyToggle_Button_Listener());
        mSensor_Stream = (SensorManager) requireActivity().getApplicationContext().getSystemService(SENSOR_SERVICE);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_settings, container, false);

    }


    public boolean start_Hardware_Sensors()
    {
        try {
            mSensor_Stream.registerListener(myhardwaresensorlistener,
                    mSensor_Stream.getDefaultSensor(Sensor.TYPE_GYROSCOPE), mDelay);

            mSensor_Stream.registerListener(myhardwaresensorlistener,
                    mSensor_Stream.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR), mDelay);

            mSensor_Stream.registerListener(myhardwaresensorlistener,
                    mSensor_Stream.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), mDelay);

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }

        return true;
    }


    private boolean start_UDP_Stream()
    {
        boolean isOnWifi = isOnWifi();
        if(isOnWifi == false)
        {

            Toast.makeText(getContext(), "Warning: Not connected to a WIFI network.", Toast.LENGTH_SHORT).show();
            // showDialog(R.string.error_warningwifi);
            return false;
        }


        InetAddress client_adress = null;
        try {
            // client_adress = InetAddress.getByName("10.188.203.222");
            client_adress = InetAddress.getByName(mIP_Adress.getText().toString());
        } catch (UnknownHostException e) {
            Toast.makeText(getContext(), "Error: Invalid IP address", Toast.LENGTH_SHORT).show();
            // showDialog(R.string.error_invalidaddr);
            return false;
        }
        try {
            mSocket = new DatagramSocket();
            mSocket.setReuseAddress(true);
        } catch (SocketException e) {
            mSocket = null;
            Toast.makeText(getContext(), "Unknown UDP network problem", Toast.LENGTH_SHORT).show();
            // showDialog(R.string.error_neterror);
            return false;}

        byte[] buf = new byte[256];
        int port;
        try {
            port = Integer.parseInt(mPort.getText().toString());
            mPacket = new DatagramPacket(buf, buf.length, client_adress, port);
        } catch (Exception e) {
            mSocket.close();
            mSocket = null;
            Toast.makeText(getContext(), "Unknown UDP network problem", Toast.LENGTH_SHORT).show();
            // showDialog(R.string.error_neterror);
            return false;
        }

        return true;


    }


    private boolean startStreaming()
    {

        boolean udp_ready = start_UDP_Stream();
        if (udp_ready == false)
        {
            return false;
        }


        mCounter =1;

        mScreenDelay = 3;

        boolean sensor_ready = start_Hardware_Sensors();
        if(sensor_ready == false)
        {
            Toast.makeText(getContext(), "Unknown sensor problem", Toast.LENGTH_SHORT).show();
            // showDialog(R.string.error_sensorerror);
            return false;
        }


        mStream_Active=true;
        mIP_Adress.setEnabled(false);
        mPort.setEnabled(false);


        mProgessBar.setVisibility(View.VISIBLE);


        return true;
    }


    private boolean isOnWifi() {
        // ConnectivityManager conman = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
        // assert conman != null;
        boolean connected = false;
        try {
            ConnectivityManager cm = (ConnectivityManager)getActivity().getApplicationContext().getSystemService(Context.CONNECTIVITY_SERVICE);
            NetworkInfo nInfo = cm.getActiveNetworkInfo();
            connected = nInfo != null && nInfo.isAvailable() && nInfo.isConnected();
            return connected;
        }catch (Exception e)
        {
            Log.e("Connectivity Exception", e.getMessage());
        }

        return connected;

        //return conman.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedOrConnecting();
    }


    private static void addSensorToString(StringBuilder strbuilder, String buttonName,
                                          String sensorid1, String sensorid2,
                                          double ...values)
    {

        if(values.length == 9)
        {
            strbuilder.append(String.format(Locale.ENGLISH,
                    "%s,%7.3f,%7.3f,%7.3f," +
                            "%7.3f,%7.3f,%7.3f," +
                            "%7.3f,%7.3f,%7.3f,",
                            buttonName,
                            values[0], values[1], values[2],
                            values[3], values[4], values[5],
                            values[6], values[7], values[8]));
        }

//        else if (values.length == 1)
//        {
//            strbuilder.append(String.format(Locale.ENGLISH, ",%s,%7.3f", sensorid, values[0]));
//        }
    }
}