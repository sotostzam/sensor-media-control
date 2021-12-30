package com.arvr.sensorcollector;

import android.annotation.SuppressLint;
import android.graphics.PorterDuff;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.os.Handler;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;

/**
 * A simple Fragment subclass.
 */
public class OldRemoteFragment extends Fragment {

    private ImageButton mPlayButton, mPauseButton, mStopButton, mRewindButton, mFastforwardButton;
    private ImageButton mVolumeUpButton, mVolumeDownButton, mMuteButton, mOkButton;
    private ImageButton mPreviousButton, mNextButton;
    private ImageButton mEscapeButton, mOrangeButton, mGreenButton;
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
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        mPlayButton = (ImageButton) view.findViewById(R.id.playButton);
        mRewindButton = (ImageButton) view.findViewById(R.id.rewindButton);
        mFastforwardButton = (ImageButton) view.findViewById(R.id.fastForwardButton);
        mVolumeUpButton = (ImageButton) view.findViewById(R.id.volumeUpButton);
        mVolumeDownButton = (ImageButton) view.findViewById(R.id.volumeDownButton);
        mMuteButton = (ImageButton) view.findViewById(R.id.muteButton);
        mOkButton = (ImageButton) view.findViewById(R.id.okButton);
        mPreviousButton = (ImageButton) view.findViewById(R.id.previousButton);
        mNextButton = (ImageButton) view.findViewById(R.id.nextButton);
        mStopButton = (ImageButton) view.findViewById(R.id.stopButton);
        mPauseButton = (ImageButton) view.findViewById(R.id.pauseButton);
        mEscapeButton = (ImageButton) view.findViewById(R.id.escapeButton);
        mOrangeButton = (ImageButton) view.findViewById(R.id.orangeButton);
        mGreenButton = (ImageButton) view.findViewById(R.id.greenButton);


        mPlayButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mPlayButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Play";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mPlayButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mPauseButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mPauseButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Pause";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mPauseButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });


        mRewindButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mRewindButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Seek -";
                    new UDPThread(message).execute();
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mRewindButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mFastforwardButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mFastforwardButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Seek +";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mFastforwardButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mVolumeUpButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mVolumeUpButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Volume +";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mVolumeUpButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mVolumeDownButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mVolumeDownButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Volume -";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mVolumeDownButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mOkButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    // mOkButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "OK";
                    new UDPThread(message).execute();
                    // Flash the button
                    flashBtn(mOkButton, R.drawable.ok_button);

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    // mOkButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mMuteButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_UP) {
                    if (!mute[0]) {
                        mMuteButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                        mute[0] = true;
                        message = "Mute";
                        new UDPThread(message).execute();
                    } else {
                        mMuteButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                        mute[0] = false;
                        message = "Unmute";
                        new UDPThread(message).execute();
                    }

                }
                return false;
            }
        });

        mPreviousButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mPreviousButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Previous";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mPreviousButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mNextButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mNextButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Next";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mNextButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mStopButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    mStopButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Stop";
                    new UDPThread(message).execute();

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    mStopButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mEscapeButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    // mEscapeButton.setColorFilter(getResources().getColor(android.R.color.holo_red_light), PorterDuff.Mode.SRC_ATOP);
                    message = "ESC";
                    new UDPThread(message).execute();
                    flashBtn(mEscapeButton, R.drawable.esc_button);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    // mEscapeButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mOrangeButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    // mOrangeButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Not Used";
                    new UDPThread(message).execute();
                    // Flash the button
                    flashBtn(mOrangeButton, R.drawable.ok_button);

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    // mOrangeButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });

        mGreenButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                String message = "";
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    // mGreenButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    message = "Not Used";
                    new UDPThread(message).execute();
                    flashBtn(mGreenButton, R.drawable.ok_button);

                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    // mGreenButton.setColorFilter(getResources().getColor(android.R.color.holo_blue_light), PorterDuff.Mode.SRC_ATOP);
                }
                return false;
            }
        });
    }

    public void flashBtn (final ImageButton myBtnToFlash, int resourceID){
        myBtnToFlash.setBackgroundResource(resourceID);
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            public void run() {
                myBtnToFlash.setBackgroundResource(0);
            }
        }, 50);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_old_remote, container, false);
    }
}