# Sensor Media Control

This repository contains a Python and an Android application, which were created during the course [Augmented and Virtual Reality](https://coutrixc.gricad-pages.univ-grenoble-alpes.fr/ar-vr-new-interaction-techniques/) (ARVR) for the MoSIG specialization 2021-2022.

***Project name: Manipulating videos and media remotely by using the Android’s motion sensors***

![main_layouts](/reports/img/main_layouts.png)

## Repository Structure

The structure of the repository is the following:

* The client folder contains the Android application's assets.
* The reports folder contain all the reports and experiments that were made during the span of the course.
* The server folder contains the files required to build and run the Python application.

## How to use

1. Clone the repository into a folder in your device.
2. Build and run the Android application using a framework (e.g [Android Studio](https://developer.android.com/studio))
3. Build and run the Python application by using `python server/server.py`.
    1. You will need to install the necessery libraries for this to work. Please check requirements.txt file.
4. Fill the IP shown in the Python app to the settings tab of the Android app.
5. Check the connection by pressing any of the regions on the screen. The sensor data should be transmitting while any button is help pressed.
