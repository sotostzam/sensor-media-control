package com.arvr.sensorcollector;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;
import androidx.viewpager2.widget.ViewPager2;

import android.os.Bundle;

import com.google.android.material.tabs.TabLayout;

public class MainActivity extends AppCompatActivity
        implements NovelRemoteFragment.FragmentOneListener, SettingsFragment.FragmentTwoListener {

    TabLayout tabLayout;
    ViewPager2 pager2;
    FragmentAdapter adapter;
    boolean streamFlag;
    String buttonName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tabLayout = findViewById(R.id.tab_layout);
        pager2 = findViewById(R.id.view_pager2);

        FragmentManager fm = getSupportFragmentManager();
        adapter = new FragmentAdapter(fm, getLifecycle());
        pager2.setAdapter(adapter);

        // Disable scrolling/swiping left and right between the two tabs
        pager2.setUserInputEnabled(false);

        tabLayout.addTab(tabLayout.newTab().setText("Remote 1"));
        tabLayout.addTab(tabLayout.newTab().setText("Remote 2"));
        tabLayout.addTab(tabLayout.newTab().setText("Settings"));


        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                pager2.setCurrentItem(tab.getPosition(), false);

            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {

            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {

            }
        });

        pager2.registerOnPageChangeCallback(new ViewPager2.OnPageChangeCallback() {
            @Override
            public void onPageSelected(int position) {
                tabLayout.selectTab(tabLayout.getTabAt(position));
            }
        });
    }


    /*
     The MainActivity controls the communication between the 2 fragments.
     onSendFunction() is used by the NovelRemoteFragment fragment to send the value of streamStatus
     and buttonName.
     getStreamStatus() and getButtonName() are used by the SettingsFragment to get these values.
     Communication happens via the listeners (interfaces) FragmentOneListener (of fragment
     NovelRemoteFragment) and FragmentOneListener (of fragment SettingsFragment), whose methods are
     overridden below.
     */

    @Override
    public void onSendFunction(boolean streamFlag, String buttonName) {
        this.streamFlag = streamFlag;
        this.buttonName = buttonName;
    }

    @Override
    public boolean getStreamStatus() {
        return this.streamFlag;
    }
    public String getButtonName() {
        return this.buttonName;
    }
}