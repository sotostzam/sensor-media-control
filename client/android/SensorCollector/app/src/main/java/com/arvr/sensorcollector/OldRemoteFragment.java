package com.arvr.sensorcollector;

import android.annotation.SuppressLint;
import android.graphics.PorterDuff;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;

/**
 * A simple Fragment subclass.
 */
public class OldRemoteFragment extends Fragment {

    private ImageButton mPlayButton, mPauseButton, mRewindButton, mFastforwardButton;
    private ImageButton mVolumeUpButton, mVolumeDownButton, mMuteButton;
    final boolean[] mute = {false};
    final boolean[] play = {false};


    public OldRemoteFragment() {
        // Required empty public constructor
    }



    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState)
    {
        mPlayButton = (ImageButton) view.findViewById(R.id.playButton);
        mRewindButton = (ImageButton) view.findViewById(R.id.rewindButton);
        mFastforwardButton = (ImageButton) view.findViewById(R.id.fastForwardButton);
        mVolumeUpButton = (ImageButton) view.findViewById(R.id.volumeUpButton);
        mVolumeDownButton = (ImageButton) view.findViewById(R.id.volumeDownButton);
        mMuteButton = (ImageButton) view.findViewById(R.id.muteButton);



        mPlayButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mPlayButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                }

                String message = "";

                if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    mPlayButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                    if(!play[0])
                    {
                        mPlayButton.setImageResource(android.R.drawable.ic_media_pause);
                        play[0] = true;
                        message = "Play";
                        new UDPThread(message).execute();
                    }
                    else
                    {
                        mPlayButton.setImageResource(android.R.drawable.ic_media_play);
                        play[0] = false;
                        message = "Pause";
                        new UDPThread(message).execute();
                    }
                }
                return false;
            }
        });


        mRewindButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mRewindButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Rewind";
                    new UDPThread(message).execute();
                } else if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    mRewindButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mFastforwardButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mFastforwardButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Fastforward";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    mFastforwardButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mVolumeUpButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mVolumeUpButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Volume Increase";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    mVolumeUpButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mVolumeDownButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mVolumeDownButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Volume Decrease";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    mVolumeDownButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mMuteButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    if(!mute[0])
                    {
                        mMuteButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                        mute[0] = true;
                        message = "Mute";
                        new UDPThread(message).execute();
                    }
                    else
                    {
                        mMuteButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                        mute[0] = false;
                        message = "Unmute";
                        new UDPThread(message).execute();
                    }

                }
                return false;
            }
        });
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_old_remote, container, false);
    }
}