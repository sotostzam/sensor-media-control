package com.arvr.sensorcollector;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.PorterDuff;
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
public class NovelRemoteFragment extends Fragment
{
    private ImageButton mImageButtonTop, mImageButtonBottom, mImageButtonLeft, mImageButtonRight;
    private FragmentOneListener listener;

    public NovelRemoteFragment() {
        // Required empty public constructor
    }


    /**
    * Custom function which gets called on any of the 4 buttons' press.
     * Function is responsible for detecting press and release action of the user and set
     * variables accordingly to be read by the settings fragment.
     * The variables sent to the other fragment are "streamFlag", which tells whether the
     * button is held pressed or not, and the name of the button held pressed "buttonName".
    * @param imageButton The specific button pressed (ImageButton)
    * @param buttonName Name of the button (String)
    */
    @SuppressLint("ClickableViewAccessibility")
    public void customSetOnTouchListener(ImageButton imageButton, String buttonName)
    {
        imageButton.setOnTouchListener(new View.OnTouchListener() {
            @SuppressLint("ClickableViewAccessibility")
            @Override
            public boolean onTouch(View v, MotionEvent event)
            {
                boolean streamFlag;
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                {
                    imageButton.setColorFilter(getResources().getColor(android.R.color.holo_red_dark), PorterDuff.Mode.SRC_ATOP);
                    streamFlag = true;
                    listener.onSendFunction(streamFlag, buttonName);
                } else if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    imageButton.setColorFilter(getResources().getColor(R.color.blue_ppt), PorterDuff.Mode.SRC_ATOP);
                    streamFlag = false;
                    listener.onSendFunction(streamFlag, buttonName);
                }
                return false;
            }
        });
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @SuppressLint("ClickableViewAccessibility")
    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState)
    {
        mImageButtonTop = (ImageButton) view.findViewById(R.id.imageButtonTop);
        mImageButtonBottom = (ImageButton) view.findViewById(R.id.imageButtonBottom);
        mImageButtonLeft = (ImageButton) view.findViewById(R.id.imageButtonLeft);
        mImageButtonRight = (ImageButton) view.findViewById(R.id.imageButtonRight);

        // Changing colour of image during runtime taken from:
        // https://stackoverflow.com/a/35286182/6475377
        customSetOnTouchListener(mImageButtonTop, "TS");
        customSetOnTouchListener(mImageButtonBottom, "BS");
        customSetOnTouchListener(mImageButtonLeft, "LS");
        customSetOnTouchListener(mImageButtonRight, "RS");

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_novel_remote, container, false);
    }

    @Override
    public void onAttach(Context context)
    {
        super.onAttach(context);
        if(context instanceof FragmentOneListener)
        { this.listener = (FragmentOneListener) context; }

    }

    public static interface FragmentOneListener{
        public void onSendFunction(boolean streamFlag, String buttonName);
    }
}