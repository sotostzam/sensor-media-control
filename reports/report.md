# Augmented and Virtual Reality

> ## Manipulating videos and media remotely by using the Android’s motion sensors

## Table of Contents

- [Augmented and Virtual Reality](#augmented-and-virtual-reality)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
    - [Original Idea](#original-idea)
  - [Problem](#problem)
  - [Related Work (SOTA)](#related-work-sota)
    - [Phone's sensors](#phones-sensors)
    - [Physical buttons](#physical-buttons)
  - [Prototype](#prototype)
    - [Architecture](#architecture)
      - [Android Application](#android-application)
        - [Layout](#layout)
        - [Remote](#remote)
        - [Settings](#settings)
      - [Python Application](#python-application)
        - [Communication](#communication)
        - [Settings](#settings-1)
        - [Operations](#operations)
    - [Limitations](#limitations)
  - [Experiments](#experiments)
  - [Results and Discussion](#results-and-discussion)
  - [Conclusion](#conclusion)

## Introduction

Media production as well as consumption is on the rise since quite some time, and with the advent of smartphones, the consumption has only increased even more. People consume media on various types of devices ranging from smartphones, televisions and computer. Traditionally media controlling has been primarily done through physical buttons present on the television set itself, and later on, all those functionalities were transferred to a small rectangular device dubbed as 'remote' which consists of several physical buttons.

### Original Idea

Our original idea consisted of having an application running in the background of an Android device which would have the ability to control the media devices present around the house. We could simply pickup our Android device lying around and with a chosen long-press on the screen, we could move the phone around in specific orientation in order to control the television playing a movie.

## Problem

The problem that we focussed mainly on was the control of media devices, more specifically, control the current video playing on a computer. The various actions that we wanted to control can be grouped and summarized in the following figure.

![controls](img/phone-controls.png)

Our idea was to group the different functionalities based on the phone's orientation.

## Related Work (SOTA)

We researched on the available pre-existing prototypes that could possibly be based upon our idea. We found a couple of projects, and we decided to group them on the basis of their type of control.

### Phone's sensors
1. Use of Smartphones as 3D Controller 
   * This is a project made by former ENSIMAG students, wherein they made use of smartphone to control and manipulate 3D objects virtually. Blender was utilized to display the 3D object, controlled with Python scripts. The idea was interesting provided a good amount of fuel for our idea,but the main drawback of this was that it was limited to a single application, and that too without any real usage.
   * [Link](https://ensiwiki.ensimag.fr/index.php?title=Use_of_smartphones_as_3D_controller) to the wiki page of the project
2. Android Experiment: 3D controller
   * A part of the 2016 Android Experiments I/O Challenge, this prototype and its API  came close to our idea and vision. It enables a user to make use of Android phone's orientation, but the user must build their own application in order to utilize this functionality.
   * [Link](https://experiments.withgoogle.com/3d-controller) to 3D controller

### Physical buttons
  1. Media remote control from Android
     * This is a type of remote modelled on a smartphone that is the most common one. It;s the simplest one in terms of type, wherein the physical buttons of an actual remote are modelled as soft clickable buttons on an Android application. The connection is typically made available via Bluetooth, or sometimes even direct WiFi.
     * [Link](https://profandroid.com/network/bluetooth/media-remote.html) to an implementation of such concept

The common issue with all the above prototypes is that the user has to turn on the screen everytime, unlock the phone, press a couple of buttons maybe to navigate to the app and initialise the connection. We aim to build a prototype which would reduce the need for a user to do all this and can quickly go about controlling the media smoothly.

## Prototype

### Architecture

The architecture of the complete framework of the project is described in this section. The most basic idea is that an Android runtime application is connected via a WiFi channel to a python server. This server is responsible for handling these connections, and react to the messages by manipulating the device's resources, in which it is run. The following image gives a visual representation on the exact communication framework.

![Framework](img/framework.png)

#### Android Application

We developed an Android application using Android Studio, which mainly uses Java to program the application's functionalities. We decided to build two remotes - one would be our novel remote, and another would be the conventional remote that we all are familiar with. For this, we created 3 GUIs - 2 for the two different types of remote, and 1 for the settings. So essentially, we have:
* Layout
* Remote
* Settings

We also make use of the APIs provided by Android though Java for accessing the data from gyroscope, accelerometer, and rotation vector sensors. Each of the 3 sensors have 3 values pertaining to x, y and z orientation.

![App Screenshots](img/app-screenshots.png)

##### Layout

The first tab is our novel proposed idea, called "Layout". It consists of 4 buttons covering the majority portion of the screen. The 4 buttons correspond to the 4 action units that we call as "Left screen", "Right screen", "Top screen" and "Bottom screen".

After having connected through the Settings tab to the Python server, the Android application enters into a streaming mode, wherein it continuously streams the data from gyroscope, accelerometer, and rotation vector sensors. But by default, the streaming is put on a conditional mode. The app will stream only as long as one of the 4 buttons are held pressed. As soon as any of the button is released, the streaming stops (but the connectivity remains).

The string that is sent from Android is of the following format:

```
[timeStamp, buttonName,
 gyroX, gyroY, gyroZ,
 acceleroX, acceleroY, acceleroZ,
 rotX, rotY, rotZ]
```

##### Remote

The second tab is the typical "Remote", wherein we place the most common buttons on any remote like play, pause, volume up, down, etc. Pressing any of the buttons streams a static message identifying the specific button pressed.

In this case, the string that is sent from Android is of the following format:

```
[actionName]
```
Where `actionName` is the action specific to the button pressed, for example "Play", "Stop", "Next", etc.

##### Settings

The third tab is the settings tab, wherein the user can specify the IP address of the computer the Android app would connect to. The port is always fixed to 50000 in the Python side, so it's not required to change it.

#### Python Application

For this application, there are dependencies that need to be included. Most of them are Python's out of the box dependencies, so they are already included. In addition to these libraries, the following list showcases the external libraries needed:

* [Pycaw](https://github.com/AndreMiras/pycaw) (Used to control the device's volume)
* [Keyboard](https://pypi.org/project/keyboard/) (Used to simulate keyboard actions)

##### Communication

To begin with, the communication is achieved by using a simple UDP protocol, which does not requires direct connection between the Android application and the Python backend. Instead the Android sends the data through a pre-defined port (default is 50000) in the same network. Then the Python backend is able to receive these data in its buffer and extract the information.

There are several messages that can exist in this communication channel. These messages describe the exact user's motion as well as the region of the screen pressed. The following table explains the different possibilities thoroughly.

|    Action     | Tilt up | Tilt Down | Tilt Left | Tilt Right |
|:--------------|:-------:|:---------:|:---------:|:----------:|
| Left screen   | LSTU    | LSTD      | LSTL      | LSTR       |
| Right screen  | RSTU    | RSTD      | RSTL      | RSTR       |
| Top screen    | TSTU    | TSTD      | TSTL      | TSTR       |
| Bottom screen | BSTU    | BSTD      | BSTL      | BSTR       |

##### Settings

This Python application supports saving and loading of custom settings, depending on the user's need. In more details, the user can choose the preferred action for each kind of gesture, and save the configuration. This configuration is later saved in separate file called `settings.json`. Additionally, when an action is received through the communication channel, it is checked against the existing setting configuration, and the appropriate action is executed.

##### Operations

When an action is triggered, the appropriate function is called based on the setting configuration. This behavior enables the application to be easily extended in order to support all kinds of external APIs for device manipulation. In this project we made use of the two libraries mentioned above to showcase this behavior, one being volume control and the other button presses.

### Limitations

## Experiments

The Python application contains a tab called **Interaction Testing**. This tab is where the experiments held place. The user interface of this tab looks like the following image:

![Experiment_Tab](img/experiment_tab.png)

In this tab, there are buttons to be matched for the most common actions, that a remote application is used for, namely `Play/Pause`, `Next`, `Previous`, `Stop`, `Mute`, `OK` and `ESC`. In addition to these four bars are present, two for volume and two for the seeking actions. On of each set shows the required value that has to be matches, while the other shows the current user's value.

The experiments consist of two categories, namely *Speed Tests* and *Interaction Tests*. The purpose of the speed tests is to give an overall idea of the time difference required to do an action with each approach. This category requires the user to hold the Android device for the duration of this experiment. On the other hand, the interaction tests aim to extract information by a more natural way of using the two approaches. This category requires the user to leave the device down between each test. This aims to simulate the more common way of picking up the remote device to perform just a simple action. In total there are four sets of experiments run with the following order:

1. Speed test using the **Layout** tab
2. Speed test using the **Remote** tab
3. Interaction test using the **Layout** tab
4. Interaction test using the **Remote** tab

## Results and Discussion

## Conclusion
