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
import android.widget.Button;
import android.widget.ImageButton;

/**
 * A simple Fragment subclass.
 */
public class FirstFragment extends Fragment
{
    private ImageButton mImageButtonTop, mImageButtonBottom, mImageButtonLeft, mImageButtonRight;
    private FragmentOneListener listener;

    public FirstFragment() {
        // Required empty public constructor
    }

    @SuppressLint("ClickableViewAccessibility")
    public void customSetOnTouchListener(ImageButton imageButton)
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
                    listener.onSendFunction(streamFlag);
                } else if (event.getAction() == MotionEvent.ACTION_UP)
                {
                    imageButton.setColorFilter(getResources().getColor(R.color.blue_ppt), PorterDuff.Mode.SRC_ATOP);
                    streamFlag = false;
                    listener.onSendFunction(streamFlag);
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
        customSetOnTouchListener(mImageButtonTop);
        customSetOnTouchListener(mImageButtonBottom);
        customSetOnTouchListener(mImageButtonLeft);
        customSetOnTouchListener(mImageButtonRight);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_first, container, false);
    }

    @Override
    public void onAttach(Context context)
    {
        super.onAttach(context);
        if(context instanceof FragmentOneListener)
        { this.listener = (FragmentOneListener) context; }

    }

    public static interface FragmentOneListener{
        public void onSendFunction(boolean streamFlag);
    }
}