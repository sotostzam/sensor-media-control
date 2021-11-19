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
            if (SecondFragment.mPacket == null || SecondFragment.mSocket == null)
                return null;

            SecondFragment.mPacket.setData(bytes);
            SecondFragment.mPacket.setLength(bytes.length);

            SecondFragment.mSocket.send(SecondFragment.mPacket);

        } catch (IOException e) {
            e.printStackTrace();

        }
        return null;
    }

}
