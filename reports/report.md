# Augmented and Virtual Reality

> ## Manipulating videos and media remotely by using the Android’s motion sensors

## Table of Contents

1. [Introduction](#introduction)
    1. [Original Idea](#original-idea)
2. [Problem](#problem)
3. [Related Work](#related-work)
4. [Problem](#problem)
5. [Prototype](#prototype)
    1. [Architecture](#architecture)
        1. [Android Application](#android-application)
        2. [Python Application](#python-application)
            1. [Communication](#communication)
            2. [Settings](#settings)
            3. [Operations](#operations)
    2. [Limitations](#limitations)
6. [Experiments](#experiments)
7. [Results and Discussion](#results-and-discussion)
8. [Conclusion](#conclusion)

## Introduction

Media production as well as consumption is on the rise since quite some time, and with the advent of smartphones, the consumption has only increased even more. People consume media on various types of devices ranging from smartphones, televisions and computer. Traditionally media controlling has been primarily done through physical buttons present on the television set itself, and later on, all those functionalities were transferred to a small rectangular device dubbed as 'remote' which consists of several physical buttons.

### Original Idea

Our original idea consisted of having an application running in the background of an Android device which would have the ability to control the media devices present around the house. We could simply pickup our Android device lying around and with a chosen long-press on the screen, we could move the phone around in specific orientation in order to control the television playing a movie.

## Problem

The problem that we focussed mainly on was the control of media devices, more specifically, control the current video playing on a computer. The various actions that we wanted to control can be grouped and summarized in the following figure.

![controls](img/phone-controls.png)

Our idea was to group the different functionalities based on the phone's orientation.

## Related Work (SOTA)

* Phone's sensors
* Simulating physical buttons

## Prototype

### Architecture

The architecture of the complete framework of the project is described in this section. The most basic idea is that an Android runtime application is connected via a WiFi channel to a python server. This server is responsible for handling these connections, and react to the messages by manipulating the device's resources, in which it is run. The following image gives a visual representation on the exact communication framework.

![Framework](img/framework.png)

#### Android Application

To be added...

#### Python Application

For this application, there are dependencies that need to be included. Most of them are Python's out of the box dependencies, so they are already included. In addition to these libraries, the following list showcases the external libraries needed:

* [Pycaw](https://github.com/AndreMiras/pycaw) (Used to control the device's volume)
* [Keyboard](https://pypi.org/project/keyboard/) (Used to simulate keyboard actions)

##### Communication

To begin with, the commnication is achieved by using a simple UDP protocol, which does not requires direct connection between the Android application and the Python backend. Instead the Android sends the data through a pre-defined port (default is 50000) in the same network. Then the Python backend is able to receive these data in its buffer and extract the information.

There are several messages that can exist in this communication channel. These messages describe the exact user's motion as well as the region of the screen pressed. The following table explaines the different possibilies thoroughly.

|    Action     | Tilt up | Tilt Down | Tilt Left | Tilt Right |
|:--------------|:-------:|:---------:|:---------:|:----------:|
| Left screen   | LSTU    | LSTD      | LSTL      | LSTR       |
| Right screen  | RSTU    | RSTD      | RSTL      | RSTR       |
| Top screen    | TSTU    | TSTD      | TSTL      | TSTR       |
| Bottom screen | BSTU    | BSTD      | BSTL      | BSTR       |

##### Settings

This Python application supports saving and loading of custom settings, depending on the user's need. In more details, the user can choose the prefered action for each kind of gesture, and save the configuration. This configuration is later saved in separate file called `settings.json`. Additionally, when an action is received through the communication channel, it is checked against the existing setting configuration, and the appropriate action is executed.

##### Operations

When an action is triggered, the appropriate function is called based on the setting configuration. This behavior enables the application to be easily extended in order to support all kinds of external APIs for device manipulation. In this project we made use of the two libraries mentioned above to showcase this behavior, one being volume control and the other button presses.

### Limitations

## Experiments

The Python application contains a tab called **Interaction Testing**. This tab is where the experiments held place. The user interface of this tab looks like the following image:

![Experiment_Tab](img/experiment_tab.png)

In this tab, there are buttons to be matched for the most common actions, that a remote application is used for, namely `Play/Pause`, `Next`, `Previous`, `Stop`, `Mute`, `OK` and `ESC`. In addition to these four bars are present, two for volume and two for the seeking actions. On of each set shows the required value that has to be matches, while the other shows the current user's value.

The experiments consist of two categories, namely *Speed Tests* and *Interaction Tests*. The purpose of the speed tests is to give an overall idea of the time difference required to do an action with each approach. This category requires the user to hold the Android device for the duration of this experiment. On the other hand, the interaction tests aim to extract information by a more natural way of using the two approaches. This category requires the user to leave the device down between each test. This aims to simulate the more common way of picking up the remote device to perform jsut a simple action. In total there are four sets of experiments run with the following order:

1. Speed test using the **Layout** tab
2. Speed test using the **Remote** tab
3. Interaction test using the **Layout** tab
4. Interaction test using the **Remote** tab

## Results and Discussion

## Conclusion
