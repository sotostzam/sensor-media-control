package com.arvr.sensorcollector;

import android.os.AsyncTask;

import java.io.IOException;

public class UDPThread extends AsyncTask<Void, Void, Void>
{
    String msensordata;


    public UDPThread(String sensordata)
    {
        this.msensordata = sensordata;
    }


    @Override
    protected Void doInBackground(Void... voids)
    {
        byte[] bytes;

        try {
            bytes = msensordata.getBytes("UTF-8");
            if (SettingsFragment.mPacket == null || SettingsFragment.mSocket == null)
                return null;

            SettingsFragment.mPacket.setData(bytes);
            SettingsFragment.mPacket.setLength(bytes.length);

            SettingsFragment.mSocket.send(SettingsFragment.mPacket);

        } catch (IOException e) {
            e.printStackTrace();

        }
        return null;
    }

}
