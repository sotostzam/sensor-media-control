package com.arvr.sensorcollector;

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
        mPauseButton = (ImageButton) view.findViewById(R.id.pauseButton);
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

                } else if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    mPlayButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mPauseButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mPauseButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);

                } else if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    mPauseButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mRewindButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mRewindButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);

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
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mFastforwardButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);

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
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mVolumeUpButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);

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
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    mVolumeDownButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);

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

                if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    if(!mute[0])
                    {
                        mMuteButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                        mute[0] = true;
                    }
                    else
                    {
                        mMuteButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                        mute[0] = false;
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