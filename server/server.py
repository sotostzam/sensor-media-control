import tkinter as tk
from tkinter import ttk
import socket, traceback
import threading
import json

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import keyboard
import random
import time
import csv

class Server:
    """
    Main server class. It initializes the variables needed to display the graphical user interface
    and opens a UDP socket which listens to a user-defined port.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.settings = {}
        self.populate_settings()

        self.ACTIONS = {"Not Used"    : {"function": self.not_used,      "has_params": False},
                        "Play/Pause"  : {"function": self.play_pause,    "has_params": False},
                        "Previous"    : {"function": self.previous,      "has_params": False},
                        "Next"        : {"function": self.next,          "has_params": False},
                        "Stop"        : {"function": self.stop,          "has_params": False},
                        "Volume +"    : {"function": self.increase_vol,  "has_params": True},
                        "Volume -"    : {"function": self.decrease_vol,  "has_params": True},
                        "Seek +"      : {"function": self.increase_seek, "has_params": True},
                        "Seek -"      : {"function": self.decrease_seek, "has_params": True},
                        "Scroll UP"   : {"function": self.scroll_up,     "has_params": True},
                        "Scroll DOWN" : {"function": self.scroll_down,   "has_params": True},
                        "Mute"        : {"function": self.mute,          "has_params": False}}

        self.TYPES = ["Constant",
                      "Incremental",
                      "Steps"]

        self.active_status         = False
        self.test_status           = False
        self.experiment_info_shown = False

        # Get default audio device using PyCAW
        self.devices   = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume    = cast(self.interface, POINTER(IAudioEndpointVolume))

        # Window and canvas initialization parameters
        self.width  = 700
        self.height = 400
        self.window = tk.Tk()
        self.window.title("Android's Sensors")
        self.window.resizable(False, False)

        self.create_tabs_frame()
        self.create_udp_stream()

    def populate_settings(self):
        """
        This function populates the application's setting on startup. If there is not a settings.json file present, 
        create one with default parameters.
        """
        try:
            with open('./server/settings.json') as json_file:
                self.settings = json.load(json_file)
        except:
            print('No settings file found. Created file with default settings.')
            self.settings['LSTU'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['LSTD'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['LSTL'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['LSTR'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['RSTU'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['RSTD'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['RSTL'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['RSTR'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['TSTU'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['TSTD'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['TSTL'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['TSTR'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['BSTU'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['BSTD'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['BSTL'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}
            self.settings['BSTR'] = {'Interaction' : 'Not Used', 'Type' : 'Not Used'}

    def save_settings(self):
        """
        Save settings from the application to a json file.
        """
        with open('./server/settings.json', 'w') as json_settings:
            json.dump(self.settings, json_settings)

    def create_tabs_frame(self):
        self.tab_widget = ttk.Notebook(self.window, width=self.width, height=self.height)
        self.tab_widget.grid(row=0, column=0, sticky="news")
        
        s = ttk.Style()
        s.configure('TNotebook', tabposition=tk.NSEW)
        s.configure('TNotebook.Tab', padding=[50,2])

        self.general_frame = tk.Frame(self.tab_widget)
        self.general_frame.columnconfigure(0, weight=1)
        self.general_frame.rowconfigure(0, weight=1)
        self.general_frame.rowconfigure(1, weight=1)
        self.general_frame.rowconfigure(2, weight=1)
        self.create_general(self.general_frame)

        self.settings_frame = tk.Frame(self.tab_widget)
        self.settings_frame.columnconfigure(0, weight=1)
        self.settings_frame.rowconfigure(0, weight=1)
        self.create_settings(self.settings_frame)

        self.interaction_frame = tk.Frame(self.tab_widget)
        self.interaction_frame.grid(row=0, column=0, sticky="nswe")
        self.interaction_frame.columnconfigure(0, minsize=100, weight=1)
        self.interaction_frame.rowconfigure(2, minsize=100, weight=1)
        self.create_interaction_frame(self.interaction_frame)

        self.tab_widget.add(self.general_frame, text='General')
        self.tab_widget.add(self.settings_frame, text='Settings')
        self.tab_widget.add(self.interaction_frame, text='Interaction Testing')         

        def experiments_popup():
            popup_window = tk.Toplevel()
            popup_window.wm_title("Experiments Information")
            popup_window.resizable(False, False)

            popup_master_frame = tk.Frame(popup_window)
            popup_master_frame.grid(padx=20)

            popup_master_label = tk.Message(popup_master_frame, width=300, text="The experiments consist of two modes as follows:")
            popup_master_label.grid(row=0, column=0, sticky="w", pady=10)

            popup_modes_group = tk.Frame(popup_master_frame)
            popup_modes_group.grid(row=1, column=0, sticky="w")

            mode_1 = tk.Label(popup_modes_group, text="Speed mode:", font='Helvetica 10 bold')
            mode_1.grid(row=0, column=0, sticky="w")

            mode_1_explanation = tk.Message(popup_modes_group, width=300, text="Compares the speed between the different approaches by holding the phone at all times.")
            mode_1_explanation.grid(row=0, column=1, sticky="w")

            mode_2 = tk.Label(popup_modes_group, text="Interactive mode:", font='Helvetica 10 bold')
            mode_2.grid(row=1, column=0, sticky="w")

            mode_2 = tk.Message(popup_modes_group, width=300, text="Compares the speed in a more natural way, like having to pick up the phone each time between " +
                                                                   "each action. After each matched action, please let the phone down.")
            mode_2.grid(row=1, column=1, sticky="w")

            confirm_button = ttk.Button(popup_master_frame, text="Got It", command=popup_window.destroy)
            confirm_button.grid(row=2, column=0, pady=20)

        def on_tab_change(event):
            tab = event.widget.tab('current')['text']
            if tab == 'Interaction Testing' and not self.experiment_info_shown:
                experiments_popup()
                self.experiment_info_shown = True

        self.tab_widget.bind('<<NotebookTabChanged>>', on_tab_change)

    def create_general(self, parent):

        def toggle_activation():
            if self.active_status:
                self.active_status = False
                self.active_btn.config(text="Enable Interaction")
            else:
                self.active_status = True
                self.active_btn.config(text="Disable Interaction")

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Connection Information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        status_frame = tk.Frame(parent)
        status_frame.grid(row=0, column=0, sticky="we", padx=0)
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=1)

        conn_info_frame = tk.Frame(status_frame)
        conn_info_frame.grid(row=0, column=0, sticky="we", padx=0)

        conn_info = tk.Label(conn_info_frame, text="Connection", font=("Courier", 24), anchor="w",)
        conn_info.grid(row=0, column=0, sticky="we", columnspan=2)

        server_label = tk.Label(conn_info_frame, text="Server:")
        server_label.grid(row=1, column=0, sticky="we")
        current_ip_address = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
        label_server_var = tk.Label(conn_info_frame, text=str(current_ip_address[0]))
        label_server_var.grid(row=1, column=1, sticky="w", padx=25)

        status_label = tk.Label(conn_info_frame, text="Status:")
        status_label.grid(row=2, column=0, sticky="we")
        self.status_var = tk.StringVar()
        self.status_var.set("Not Connected")
        self.label_status_var = tk.Label(conn_info_frame, textvariable=self.status_var, fg="Red")
        self.label_status_var.grid(row=2, column=1, sticky="w", padx=25)

        client_label = tk.Label(conn_info_frame, text="Client:")
        client_label.grid(row=3, column=0, sticky="we")
        self.client_var = tk.StringVar()
        self.client_var.set("Not Connected")
        self.label_client_var = tk.Label(conn_info_frame, textvariable=self.client_var, fg="Red")
        self.label_client_var.grid(row=3, column=1, sticky="w", padx=25)

        active_info_frame = tk.Frame(status_frame)
        active_info_frame.grid(row=0, column=1, sticky="we", padx=0)

        self.active_btn = ttk.Button(active_info_frame, text= "Enable Interaction", command = toggle_activation)
        self.active_btn.grid(row=0, column=0, ipadx=10, ipady=10)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Sensor Data Information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        information_grid = tk.Frame(parent)
        information_grid.grid(row=1, column=0, sticky="nswe")
        information_grid.columnconfigure(0, weight=1)
        information_grid.columnconfigure(1, weight=1)
        information_grid.columnconfigure(2, weight=1)

        information = tk.Label(information_grid, text="Sensor Data", font=("Courier", 24), anchor="w",)
        information.grid(row=0, column=0, sticky="we", columnspan=3)

        # Gyroscope Data
        gyro_data_frame = tk.Frame(information_grid)
        gyro_data_frame.grid(row=1, column=0, sticky="we", padx=0)

        gyro_data_x_label = tk.Label(gyro_data_frame, text="Gyroscope x:")
        gyro_data_x_label.grid(row=0, column=0, sticky="we")
        self.gyro_x = tk.StringVar()
        self.gyro_x.set("N/A")
        label_gyro_x = tk.Label(gyro_data_frame, textvariable=self.gyro_x)
        label_gyro_x.grid(row=0, column=1, sticky="we", padx=25)

        gyro_data_y_label = tk.Label(gyro_data_frame, text="Gyroscope y:")
        gyro_data_y_label.grid(row=1, column=0, sticky="we")
        self.gyro_y = tk.StringVar()
        self.gyro_y.set("N/A")
        label_gyro_y = tk.Label(gyro_data_frame, textvariable=self.gyro_y)
        label_gyro_y.grid(row=1, column=1, sticky="we", padx=25)

        gyro_data_z_label = tk.Label(gyro_data_frame, text="Gyroscope z:")
        gyro_data_z_label.grid(row=2, column=0, sticky="we")
        self.gyro_z = tk.StringVar()
        self.gyro_z.set("N/A")
        label_gyro_z = tk.Label(gyro_data_frame, textvariable=self.gyro_z)
        label_gyro_z.grid(row=2, column=1, sticky="we", padx=25)

        # Positional Data
        acceleration_data_frame = tk.Frame(information_grid)
        acceleration_data_frame.grid(row=1, column=1, sticky="we", padx=0)

        acceleration_data_x_label = tk.Label(acceleration_data_frame, text="Acceleration x:")
        acceleration_data_x_label.grid(row=0, column=0, sticky="we")
        self.acceleration_x = tk.StringVar()
        self.acceleration_x.set("N/A")
        label_acceleration_x = tk.Label(acceleration_data_frame, textvariable=self.acceleration_x)
        label_acceleration_x.grid(row=0, column=1, sticky="we", padx=25)

        acceleration_data_y_label = tk.Label(acceleration_data_frame, text="Acceleration y:")
        acceleration_data_y_label.grid(row=1, column=0, sticky="we")
        self.acceleration_y = tk.StringVar()
        self.acceleration_y.set("N/A")
        label_acceleration_y = tk.Label(acceleration_data_frame, textvariable=self.acceleration_y)
        label_acceleration_y.grid(row=1, column=1, sticky="we", padx=25)

        acceleration_data_z_label = tk.Label(acceleration_data_frame, text="Acceleration z:")
        acceleration_data_z_label.grid(row=2, column=0, sticky="we")
        self.acceleration_z = tk.StringVar()
        self.acceleration_z.set("N/A")
        label_acceleration_z = tk.Label(acceleration_data_frame, textvariable=self.acceleration_z)
        label_acceleration_z.grid(row=2, column=1, sticky="we", padx=25)

        # Rotational Data
        rotation_data_frame = tk.Frame(information_grid)
        rotation_data_frame.grid(row=1, column=2, sticky="we", padx=0)

        rotation_data_x_label = tk.Label(rotation_data_frame, text="Rotation x:")
        rotation_data_x_label.grid(row=0, column=0, sticky="we")
        self.rotation_x = tk.StringVar()
        self.rotation_x.set("N/A")
        label_rotation_x = tk.Label(rotation_data_frame, textvariable=self.rotation_x)
        label_rotation_x.grid(row=0, column=1, sticky="we", padx=25)

        rotation_data_y_label = tk.Label(rotation_data_frame, text="Rotation y:")
        rotation_data_y_label.grid(row=1, column=0, sticky="we")
        self.rotation_y = tk.StringVar()
        self.rotation_y.set("N/A")
        label_rotation_y = tk.Label(rotation_data_frame, textvariable=self.rotation_y)
        label_rotation_y.grid(row=1, column=1, sticky="we", padx=25)

        rotation_data_z_label = tk.Label(rotation_data_frame, text="Rotation z:")
        rotation_data_z_label.grid(row=2, column=0, sticky="we")
        self.rotation_z = tk.StringVar()
        self.rotation_z.set("N/A")
        label_rotation_z = tk.Label(rotation_data_frame, textvariable=self.rotation_z)
        label_rotation_z.grid(row=2, column=1, sticky="we", padx=25)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Phone's Modes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        action_frame = tk.Frame(parent)
        action_frame.grid(row=2, column=0, sticky="nswe", padx=0)

        action_label = tk.Label(action_frame, text="Action Data", font=("Courier", 24), anchor="w",)
        action_label.grid(row=0, column=0, sticky="we", columnspan=2)

        action_data_label = tk.Label(action_frame, text="Active action:")
        action_data_label.grid(row=1, column=0, sticky="we")
        self.current_action_var = tk.StringVar()
        self.current_action_var.set("None")
        label_action = tk.Label(action_frame, textvariable=self.current_action_var)
        label_action.grid(row=1, column=1, sticky="we", padx=25)

    def create_settings(self, parent):

        def create_layout_settings(parent_frame):
            self.settings_widgets = {}

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Left Screen Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            ls_frame = tk.Frame(parent_frame)
            ls_frame.grid(row=0, column=0, sticky="nswe")
            ls_frame.rowconfigure(0, weight=1)
            ls_frame.columnconfigure(1, weight=1)

            self.icon_screen_left  = tk.PhotoImage(file = r"./server/sources/screen_left.png").subsample(3,3)
            lsf_picture = tk.Label(ls_frame, image=self.icon_screen_left)
            lsf_picture.grid(row=0, column=0, sticky="nswe")

            ls_group = tk.Frame(ls_frame)
            ls_group.grid(row=0, column=1, sticky="we")
            ls_group.columnconfigure(1, weight=1)
            ls_group.columnconfigure(2, weight=1)
    
            lstu_label = tk.Label(ls_group, anchor="w", text="Tilt Up:")
            lstu_label.grid(row=0, column=0, sticky="we")

            self.lstu_action_vars = tk.StringVar(ls_group)
            self.lstu_action_vars.set(self.settings['LSTU']['Interaction'])

            self.settings_widgets['LSTU'] = {'action': ttk.OptionMenu(ls_group, self.lstu_action_vars, self.settings['LSTU']['Interaction'], *list(self.ACTIONS), 
                                                                    command= lambda x: modify_setting(self.lstu_action_vars, 'LSTU', 'Interaction'))}
            self.settings_widgets['LSTU']['action'].grid(row=0, column=1, sticky="we")

            self.lstu_type_vars = tk.StringVar(ls_group)
            self.lstu_type_vars.set(self.settings['LSTU']['Type'])

            self.settings_widgets['LSTU']['type'] = ttk.OptionMenu(ls_group, self.lstu_type_vars, self.settings['LSTU']['Type'], *self.TYPES, 
                                                                    command=lambda x: modify_setting(self.lstu_type_vars, 'LSTU', 'Type'))
            self.settings_widgets['LSTU']['type'].grid(row=0, column=2, sticky="we")
            if self.ACTIONS[self.settings['LSTU']['Interaction']]['has_params'] is False: self.settings_widgets['LSTU']['type'].configure(state="disabled")

            lstd_label = tk.Label(ls_group, anchor="w", text="Tilt Down:")
            lstd_label.grid(row=1, column=0, sticky="we")

            self.lstd_action_vars = tk.StringVar(ls_group)
            self.lstd_action_vars.set(self.settings['LSTD']['Interaction'])

            self.settings_widgets['LSTD'] = {'action': ttk.OptionMenu(ls_group, self.lstd_action_vars, self.settings['LSTD']['Interaction'], *list(self.ACTIONS), 
                                                                    command= lambda x: modify_setting(self.lstd_action_vars, 'LSTD', 'Interaction'))}
            self.settings_widgets['LSTD']['action'].grid(row=1, column=1, sticky="we")

            self.lstd_type_vars = tk.StringVar(ls_group)
            self.lstd_type_vars.set(self.settings['LSTD']['Type'])

            self.settings_widgets['LSTD'] = {'type': ttk.OptionMenu(ls_group, self.lstd_type_vars, self.settings['LSTD']['Type'], *self.TYPES, 
                                                                    command=lambda x: modify_setting(self.lstd_type_vars, 'LSTD', 'Type'))}
            self.settings_widgets['LSTD']['type'].grid(row=1, column=2, sticky="we")
            if self.ACTIONS[self.settings['LSTD']['Interaction']]['has_params'] is False: self.settings_widgets['LSTD']['type'].configure(state="disabled")

            lstl_label = tk.Label(ls_group, anchor="w", text="Tilt Left:")
            lstl_label.grid(row=2, column=0, sticky="we")

            self.lstl_action_vars = tk.StringVar(ls_group)
            self.lstl_action_vars.set(self.settings['LSTL']['Interaction'])

            self.settings_widgets['LSTL'] = {'action': ttk.OptionMenu(ls_group, self.lstl_action_vars, self.settings['LSTL']['Interaction'], *list(self.ACTIONS), 
                                                                    command= lambda x: modify_setting(self.lstl_action_vars, 'LSTL', 'Interaction'))}
            self.settings_widgets['LSTL']['action'].grid(row=2, column=1, sticky="we")

            self.lstl_type_vars = tk.StringVar(ls_group)
            self.lstl_type_vars.set(self.settings['LSTL']['Type'])

            self.settings_widgets['LSTL'] = {'type': ttk.OptionMenu(ls_group, self.lstl_type_vars, self.settings['LSTL']['Type'], *self.TYPES, 
                                                                    command=lambda x: modify_setting(self.lstl_type_vars, 'LSTL', 'Type'))}
            self.settings_widgets['LSTL']['type'].grid(row=2, column=2, sticky="we")
            if self.ACTIONS[self.settings['LSTL']['Interaction']]['has_params'] is False: self.settings_widgets['LSTL']['type'].configure(state="disabled")

            lstr_label = tk.Label(ls_group, anchor="w", text="Tilt Right:")
            lstr_label.grid(row=3, column=0, sticky="we")

            self.lstr_action_vars = tk.StringVar(ls_group)
            self.lstr_action_vars.set(self.settings['LSTR']['Interaction'])

            self.settings_widgets['LSTR'] = {'action': ttk.OptionMenu(ls_group, self.lstr_action_vars, self.settings['LSTR']['Interaction'], *list(self.ACTIONS), 
                                                                    command= lambda x: modify_setting(self.lstr_action_vars, 'LSTR', 'Interaction'))}
            self.settings_widgets['LSTR']['action'].grid(row=3, column=1, sticky="we")

            self.lstr_type_vars = tk.StringVar(ls_group)
            self.lstr_type_vars.set(self.settings['LSTR']['Type'])

            self.settings_widgets['LSTR'] = {'type': ttk.OptionMenu(ls_group, self.lstr_type_vars, self.settings['LSTR']['Type'], *self.TYPES, 
                                                                    command=lambda x: modify_setting(self.lstr_type_vars, 'LSTR', 'Type'))}
            self.settings_widgets['LSTR']['type'].grid(row=3, column=2, sticky="we")
            if self.ACTIONS[self.settings['LSTR']['Interaction']]['has_params'] is False: self.settings_widgets['LSTR']['type'].configure(state="disabled")

            tk.Frame(parent_frame, height=1, bg="black").grid(row=0, column=1, sticky="news")

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Screen Right Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            rs_frame = tk.Frame(parent_frame)
            rs_frame.grid(row=0, column=2, sticky="nswe")
            rs_frame.rowconfigure(0, weight=1)
            rs_frame.columnconfigure(1, weight=1)

            self.icon_screen_right  = tk.PhotoImage(file = r"./server/sources/screen_right.png").subsample(3,3)
            rsf_picture = tk.Label(rs_frame, image=self.icon_screen_right)
            rsf_picture.grid(row=0, column=0, sticky="we")

            rs_group = tk.Frame(rs_frame)
            rs_group.grid(row=0, column=1, sticky="we")
            rs_group.columnconfigure(1, weight=1)
            rs_group.columnconfigure(2, weight=1)

            rstu_label = tk.Label(rs_group, anchor="w", text="Tilt Up:")
            rstu_label.grid(row=0, column=0, sticky="we")

            self.rstu_action_vars = tk.StringVar(rs_group)
            self.rstu_action_vars.set(self.settings['RSTU']['Interaction'])

            self.settings_widgets['RSTU'] = {'action': ttk.OptionMenu(rs_group, self.rstu_action_vars, self.settings['RSTU']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.rstu_action_vars, 'RSTU', 'Interaction'))}
            self.settings_widgets['RSTU']['action'].grid(row=0, column=1, sticky="we")

            self.rstu_type_vars = tk.StringVar(rs_group)
            self.rstu_type_vars.set(self.settings['RSTU']['Type'])

            self.settings_widgets['RSTU']['type'] = ttk.OptionMenu(rs_group, self.rstu_type_vars, self.settings['RSTU']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.rstu_type_vars, 'RSTU', 'Type'))
            self.settings_widgets['RSTU']['type'].grid(row=0, column=2, sticky="we")
            if self.ACTIONS[self.settings['RSTU']['Interaction']]['has_params'] is False: self.settings_widgets['RSTU']['type'].configure(state="disabled")

            rstd_label = tk.Label(rs_group, anchor="w", text="Tilt Down:")
            rstd_label.grid(row=1, column=0, sticky="we")

            self.rstd_action_vars = tk.StringVar(rs_group)
            self.rstd_action_vars.set(self.settings['RSTD']['Interaction'])

            self.settings_widgets['RSTD'] = {'action': ttk.OptionMenu(rs_group, self.rstd_action_vars, self.settings['RSTD']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.rstd_action_vars, 'RSTD', 'Interaction'))}
            self.settings_widgets['RSTD']['action'].grid(row=1, column=1, sticky="we")

            self.rstd_type_vars = tk.StringVar(rs_group)
            self.rstd_type_vars.set(self.settings['RSTD']['Type'])

            self.settings_widgets['RSTD']['type'] = ttk.OptionMenu(rs_group, self.rstd_type_vars, self.settings['RSTD']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.rstd_type_vars, 'RSTD', 'Type'))
            self.settings_widgets['RSTD']['type'].grid(row=1, column=2, sticky="we")
            if self.ACTIONS[self.settings['RSTD']['Interaction']]['has_params'] is False: self.settings_widgets['RSTD']['type'].configure(state="disabled")

            rstl_label = tk.Label(rs_group, anchor="w", text="Tilt Left:")
            rstl_label.grid(row=2, column=0, sticky="we")

            self.rstl_action_vars = tk.StringVar(rs_group)
            self.rstl_action_vars.set(self.settings['RSTL']['Interaction'])

            self.settings_widgets['RSTL'] = {'action': ttk.OptionMenu(rs_group, self.rstl_action_vars, self.settings['RSTL']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.rstl_action_vars, 'RSTL', 'Interaction'))}
            self.settings_widgets['RSTL']['action'].grid(row=2, column=1, sticky="we")

            self.rstl_type_vars = tk.StringVar(rs_group)
            self.rstl_type_vars.set(self.settings['RSTL']['Type'])

            self.settings_widgets['RSTL']['type'] = ttk.OptionMenu(rs_group, self.rstl_type_vars, self.settings['RSTL']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.rstl_type_vars, 'RSTL', 'Type'))
            self.settings_widgets['RSTL']['type'].grid(row=2, column=2, sticky="we")
            if self.ACTIONS[self.settings['RSTL']['Interaction']]['has_params'] is False: self.settings_widgets['RSTL']['type'].configure(state="disabled")

            rstr_label = tk.Label(rs_group, anchor="w", text="Tilt Right:")
            rstr_label.grid(row=3, column=0, sticky="we")

            self.rstr_action_vars = tk.StringVar(rs_group)
            self.rstr_action_vars.set(self.settings['RSTR']['Interaction'])

            self.settings_widgets['RSTR'] = {'action': ttk.OptionMenu(rs_group, self.rstr_action_vars, self.settings['RSTR']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.rstr_action_vars, 'RSTR', 'Interaction'))}
            self.settings_widgets['RSTR']['action'].grid(row=3, column=1, sticky="we")

            self.rstr_type_vars = tk.StringVar(rs_group)
            self.rstr_type_vars.set(self.settings['RSTR']['Type'])

            self.settings_widgets['RSTR']['type'] = ttk.OptionMenu(rs_group, self.rstr_type_vars, self.settings['RSTR']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.rstr_type_vars, 'RSTR', 'Type'))
            self.settings_widgets['RSTR']['type'].grid(row=3, column=2, sticky="we")
            if self.ACTIONS[self.settings['RSTR']['Interaction']]['has_params'] is False: self.settings_widgets['RSTR']['type'].configure(state="disabled")

            tk.Frame(parent_frame, height=1, bg="black").grid(row=1, column=0, sticky="news", columnspan=3)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Screen Top Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            ts_frame = tk.Frame(parent_frame)
            ts_frame.grid(row=2, column=0, sticky="nswe")
            ts_frame.rowconfigure(0, weight=1)
            ts_frame.columnconfigure(1, weight=1)

            self.icon_screen_top  = tk.PhotoImage(file = r"./server/sources/screen_top.png").subsample(3,3)
            tsf_picture = tk.Label(ts_frame, image=self.icon_screen_top)
            tsf_picture.grid(row=0, column=0, sticky="we")

            ts_group = tk.Frame(ts_frame)
            ts_group.grid(row=0, column=1, sticky="we")
            ts_group.columnconfigure(1, weight=1)
            ts_group.columnconfigure(2, weight=1)

            tstu_label = tk.Label(ts_group, anchor="w", text="Tilt Up:")
            tstu_label.grid(row=0, column=0, sticky="we")

            self.tstu_action_vars = tk.StringVar(ts_group)
            self.tstu_action_vars.set(self.settings['TSTU']['Interaction'])

            self.settings_widgets['TSTU'] = {'action': ttk.OptionMenu(ts_group, self.tstu_action_vars, self.settings['TSTU']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.tstu_action_vars, 'TSTU', 'Interaction'))}
            self.settings_widgets['TSTU']['action'].grid(row=0, column=1, sticky="we")

            self.tstu_type_vars = tk.StringVar(ts_group)
            self.tstu_type_vars.set(self.settings['TSTU']['Type'])

            self.settings_widgets['TSTU']['type'] = ttk.OptionMenu(ts_group, self.tstu_type_vars, self.settings['TSTU']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.tstu_type_vars, 'TSTU', 'Type'))
            self.settings_widgets['TSTU']['type'].grid(row=0, column=2, sticky="we")
            if self.ACTIONS[self.settings['TSTU']['Interaction']]['has_params'] is False: self.settings_widgets['TSTU']['type'].configure(state="disabled")

            tstd_label = tk.Label(ts_group, anchor="w", text="Tilt Down:")
            tstd_label.grid(row=1, column=0, sticky="we")

            self.tstd_action_vars = tk.StringVar(ts_group)
            self.tstd_action_vars.set(self.settings['TSTD']['Interaction'])

            self.settings_widgets['TSTD'] = {'action': ttk.OptionMenu(ts_group, self.tstd_action_vars, self.settings['TSTD']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.tstd_action_vars, 'TSTD', 'Interaction'))}
            self.settings_widgets['TSTD']['action'].grid(row=1, column=1, sticky="we")

            self.tstd_type_vars = tk.StringVar(ts_group)
            self.tstd_type_vars.set(self.settings['TSTD']['Type'])

            self.settings_widgets['TSTD']['type'] = ttk.OptionMenu(ts_group, self.tstd_type_vars, self.settings['TSTD']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.tstd_type_vars, 'TSTD', 'Type'))
            self.settings_widgets['TSTD']['type'].grid(row=1, column=2, sticky="we")
            if self.ACTIONS[self.settings['TSTD']['Interaction']]['has_params'] is False: self.settings_widgets['TSTD']['type'].configure(state="disabled")

            tstl_label = tk.Label(ts_group, anchor="w", text="Tilt Left:")
            tstl_label.grid(row=2, column=0, sticky="we")

            self.tstl_action_vars = tk.StringVar(ts_group)
            self.tstl_action_vars.set(self.settings['TSTL']['Interaction'])

            self.settings_widgets['TSTL'] = {'action': ttk.OptionMenu(ts_group, self.tstl_action_vars, self.settings['TSTL']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.tstl_action_vars, 'TSTL', 'Interaction'))}
            self.settings_widgets['TSTL']['action'].grid(row=2, column=1, sticky="we")

            self.tstl_type_vars = tk.StringVar(ts_group)
            self.tstl_type_vars.set(self.settings['TSTL']['Type'])

            self.settings_widgets['TSTL']['type'] = ttk.OptionMenu(ts_group, self.tstl_type_vars, self.settings['TSTL']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.tstl_type_vars, 'TSTL', 'Type'))
            self.settings_widgets['TSTL']['type'].grid(row=2, column=2, sticky="we")
            if self.ACTIONS[self.settings['TSTL']['Interaction']]['has_params'] is False: self.settings_widgets['TSTL']['type'].configure(state="disabled")

            tstr_label = tk.Label(ts_group, anchor="w", text="Tilt Right:")
            tstr_label.grid(row=3, column=0, sticky="we")

            self.tstr_action_vars = tk.StringVar(ts_group)
            self.tstr_action_vars.set(self.settings['TSTR']['Interaction'])

            self.settings_widgets['TSTR'] = {'action': ttk.OptionMenu(ts_group, self.tstr_action_vars, self.settings['TSTR']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.tstr_action_vars, 'TSTR', 'Interaction'))}
            self.settings_widgets['TSTR']['action'].grid(row=3, column=1, sticky="we")

            self.tstr_type_vars = tk.StringVar(ts_group)
            self.tstr_type_vars.set(self.settings['TSTR']['Type'])

            self.settings_widgets['TSTR']['type'] = ttk.OptionMenu(ts_group, self.tstr_type_vars, self.settings['TSTR']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.tstr_type_vars, 'TSTR', 'Type'))
            self.settings_widgets['TSTR']['type'].grid(row=3, column=2, sticky="we")
            if self.ACTIONS[self.settings['TSTR']['Interaction']]['has_params'] is False: self.settings_widgets['TSTR']['type'].configure(state="disabled")

            tk.Frame(parent_frame, height=1, width=1, bg="black").grid(row=2, column=1, sticky="news")

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Screen Down Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            bs_frame = tk.Frame(parent_frame)
            bs_frame.grid(row=2, column=2, sticky="nswe")
            bs_frame.rowconfigure(0, weight=1)
            bs_frame.columnconfigure(1, weight=1)

            self.icon_screen_bottom  = tk.PhotoImage(file = r"./server/sources/screen_bottom.png").subsample(3,3)
            bsf_picture = tk.Label(bs_frame, image=self.icon_screen_bottom)
            bsf_picture.grid(row=0, column=0, sticky="we")

            bs_group = tk.Frame(bs_frame)
            bs_group.grid(row=0, column=1, sticky="we")
            bs_group.columnconfigure(1, weight=1)
            bs_group.columnconfigure(2, weight=1)

            bstu_label = tk.Label(bs_group, anchor="w", text="Tilt Up:")
            bstu_label.grid(row=0, column=0, sticky="we")

            self.bstu_action_vars = tk.StringVar(bs_group)
            self.bstu_action_vars.set(self.settings['BSTU']['Interaction'])

            self.settings_widgets['BSTU'] = {'action': ttk.OptionMenu(bs_group, self.bstu_action_vars, self.settings['BSTU']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.bstu_action_vars, 'BSTU', 'Interaction'))}
            self.settings_widgets['BSTU']['action'].grid(row=0, column=1, sticky="we")

            self.bstu_type_vars = tk.StringVar(bs_group)
            self.bstu_type_vars.set(self.settings['BSTU']['Type'])

            self.settings_widgets['BSTU']['type'] = ttk.OptionMenu(bs_group, self.bstu_type_vars, self.settings['BSTU']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.bstu_type_vars, 'BSTU', 'Type'))
            self.settings_widgets['BSTU']['type'].grid(row=0, column=2, sticky="we")
            if self.ACTIONS[self.settings['BSTU']['Interaction']]['has_params'] is False: self.settings_widgets['BSTU']['type'].configure(state="disabled")

            bstd_label = tk.Label(bs_group, anchor="w", text="Tilt Down:")
            bstd_label.grid(row=1, column=0, sticky="we")

            self.bstd_action_vars = tk.StringVar(bs_group)
            self.bstd_action_vars.set(self.settings['BSTD']['Interaction'])

            self.settings_widgets['BSTD'] = {'action': ttk.OptionMenu(bs_group, self.bstd_action_vars, self.settings['BSTD']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.bstd_action_vars, 'BSTD', 'Interaction'))}
            self.settings_widgets['BSTD']['action'].grid(row=1, column=1, sticky="we")

            self.bstd_type_vars = tk.StringVar(bs_group)
            self.bstd_type_vars.set(self.settings['BSTD']['Type'])

            self.settings_widgets['BSTD']['type'] = ttk.OptionMenu(bs_group, self.bstd_type_vars, self.settings['BSTD']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.bstd_type_vars, 'BSTD', 'Type'))
            self.settings_widgets['BSTD']['type'].grid(row=1, column=2, sticky="we")
            if self.ACTIONS[self.settings['BSTD']['Interaction']]['has_params'] is False: self.settings_widgets['BSTD']['type'].configure(state="disabled")

            bstl_label = tk.Label(bs_group, anchor="w", text="Tilt Left:")
            bstl_label.grid(row=2, column=0, sticky="we")

            self.bstl_action_vars = tk.StringVar(bs_group)
            self.bstl_action_vars.set(self.settings['BSTL']['Interaction'])

            self.settings_widgets['BSTL'] = {'action': ttk.OptionMenu(bs_group, self.bstl_action_vars, self.settings['BSTL']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.bstl_action_vars, 'BSTL', 'Interaction'))}
            self.settings_widgets['BSTL']['action'].grid(row=2, column=1, sticky="we")

            self.bstl_type_vars = tk.StringVar(bs_group)
            self.bstl_type_vars.set(self.settings['BSTL']['Type'])

            self.settings_widgets['BSTL']['type'] = ttk.OptionMenu(bs_group, self.bstl_type_vars, self.settings['BSTL']['Type'], *self.TYPES,
                                                                    command=lambda x: modify_setting(self.bstl_type_vars, 'BSTL', 'Type'))
            self.settings_widgets['BSTL']['type'].grid(row=2, column=2, sticky="we")
            if self.ACTIONS[self.settings['BSTL']['Interaction']]['has_params'] is False: self.settings_widgets['BSTL']['type'].configure(state="disabled")

            bstr_label = tk.Label(bs_group, anchor="w", text="Tilt Right:")
            bstr_label.grid(row=3, column=0, sticky="we")

            self.bstr_action_vars = tk.StringVar(bs_group)
            self.bstr_action_vars.set(self.settings['BSTR']['Interaction'])

            self.settings_widgets['BSTR'] = {'action': ttk.OptionMenu(bs_group, self.bstr_action_vars, self.settings['BSTR']['Interaction'], *list(self.ACTIONS),
                                                                    command= lambda x: modify_setting(self.bstr_action_vars, 'BSTR', 'Interaction'))}
            self.settings_widgets['BSTR']['action'].grid(row=3, column=1, sticky="we")

            self.bstr_type_vars = tk.StringVar(bs_group)
            self.bstr_type_vars.set(self.settings['BSTR']['Type'])

            self.settings_widgets['BSTR']['type'] = ttk.OptionMenu(bs_group, self.bstr_type_vars, self.settings['BSTR']['Type'], *self.TYPES,
                                                    command=lambda x: modify_setting(self.bstr_type_vars, 'BSTR', 'Type'))
            self.settings_widgets['BSTR']['type'].grid(row=3, column=2, sticky="we")
            if self.ACTIONS[self.settings['BSTR']['Interaction']]['has_params'] is False: self.settings_widgets['BSTR']['type'].configure(state="disabled")

            tk.Frame(parent_frame, height=1, bg="black").grid(row=3, column=0, sticky="news", columnspan=3)

        def modify_setting(*args):
            self.settings[args[1]][args[2]] = args[0].get()
            if self.ACTIONS[self.settings[args[1]]['Interaction']]['has_params'] is False:
                self.settings_widgets[args[1]]['type'].configure(state="disabled")
            else:
                self.settings_widgets[args[1]]['type'].configure(state="enabled")

        # Settings for Screen layout mode
        self.screen_layout = tk.Frame(parent)
        self.screen_layout.grid(row=0, column=0, sticky="nswe")
        self.screen_layout.rowconfigure(0, weight=1)
        self.screen_layout.rowconfigure(2, weight=1)
        self.screen_layout.columnconfigure(0, weight=1)
        self.screen_layout.columnconfigure(2, weight=1)
        create_layout_settings(self.screen_layout)

        layout_btn_frame = tk.Frame(parent)
        layout_btn_frame.grid(row=4, column=0, sticky="nswe", columnspan=3, pady=5)
        layout_btn_frame.columnconfigure(0, weight=1)
        self.save_settings_btn = ttk.Button(layout_btn_frame, text= "Save Settings", command= self.save_settings)
        self.save_settings_btn.grid(row=0, column=0, ipadx=10, ipady=5)

    def create_interaction_frame(self, parent):
        """
        Create the layout of the interaction frame. The order is the following:
        * Interaction selection frame
        * Test interaction frame
        """
        interaction_selection = tk.Frame(parent, height = self.height/4)
        interaction_selection.grid(row=0, column=0, sticky="nswe", pady=10)
        interaction_selection.rowconfigure(0, weight=1)
        interaction_selection.grid_columnconfigure(0, weight=1)
        interaction_selection.grid_columnconfigure(1, weight=1)
        interaction_selection.grid_columnconfigure(2, weight=1)
        interaction_selection.grid_columnconfigure(3, weight=2)

        interaction_selection_explanation = tk.Message(interaction_selection, width=180 ,text="Please select the type of interaction tests: ")
        interaction_selection_explanation.grid(row=0, column=0, sticky="nswe")

        # Mode Selection RadioButton
        interaction_selection_choice = tk.Frame(interaction_selection)
        interaction_selection_choice.grid(row=0, column=1, sticky="nswe")

        self.interaction_mode = tk.IntVar(value=1)
        self.interaction_choice_1 = tk.Radiobutton(interaction_selection_choice, variable=self.interaction_mode, value=1, tristatevalue=0, text="Speed Mode")
        self.interaction_choice_1.grid(row=0, column=1, sticky="w")
        self.interaction_choice_2 = tk.Radiobutton(interaction_selection_choice, variable=self.interaction_mode, value=2, tristatevalue=0, text="Interactive Mode")
        self.interaction_choice_2.grid(row=1, column=1, sticky="w")

        self.interaction_start = ttk.Button(interaction_selection, text= "Start", command= lambda: threading.Thread(target=self.start_experiment, daemon=True).start())
        self.interaction_start.grid(row=0, column=2, ipady=10)

        experiments_progress = tk.Frame(interaction_selection)
        experiments_progress.grid(row=0, column=3, sticky="nswe")
        experiments_progress.grid_columnconfigure(0, weight=1)
        experiments_progress.grid_rowconfigure(0, weight=1)
        experiments_progress.grid_rowconfigure(1, weight=1)

        self.experiments_progress_bar = ttk.Progressbar(experiments_progress, orient = tk.HORIZONTAL, length = 150, mode = 'determinate')
        self.experiments_progress_bar.grid(row=0, column=0)

        self.progress_value = tk.StringVar()
        self.progress_value.set("Tests completed: 0/10")
        progress_value_label = tk.Label(experiments_progress, textvariable=self.progress_value)
        progress_value_label.grid(row=2, column=0, sticky="we", padx=25)

        tk.Frame(parent, height=1, bg="black").grid(row=1, column=0, sticky="news")

        # Test Interaction Frame
        interaction_test = tk.Frame(parent)
        interaction_test.grid(row=2, column=0, sticky="nswe")
        interaction_test.rowconfigure(0, weight=1)
        interaction_test.columnconfigure(2, weight=1)

        interaction_test_buttons = tk.Frame(interaction_test, bg="lightgray")
        interaction_test_buttons.grid(row=0, column=0, sticky="nswe")
        interaction_test_buttons.grid_columnconfigure(0, weight=1)
        interaction_test_buttons.grid_columnconfigure(1, weight=1)
        interaction_test_buttons.grid_columnconfigure(2, weight=1)
        interaction_test_buttons.grid_rowconfigure(0, weight=1)
        interaction_test_buttons.grid_rowconfigure(1, weight=1)
        interaction_test_buttons.grid_rowconfigure(2, weight=1)
        interaction_test_buttons.grid_rowconfigure(3, weight=1)
        interaction_test_buttons.grid_rowconfigure(4, weight=1)

        self.photo_play = tk.PhotoImage(file = r"./server/sources/play.png").subsample(7,7)
        self.photo_next = tk.PhotoImage(file = r"./server/sources/next.png").subsample(7,7)
        self.photo_prev = tk.PhotoImage(file = r"./server/sources/previous.png").subsample(7,7)
        self.photo_stop = tk.PhotoImage(file = r"./server/sources/stop.png").subsample(7,7)
        self.red_btn    = tk.PhotoImage(file = r"./server/sources/red_btn.png").subsample(7,7)
        self.green_btn  = tk.PhotoImage(file = r"./server/sources/green_btn.png").subsample(7,7)
        self.blue_btn   = tk.PhotoImage(file = r"./server/sources/blue_btn.png").subsample(7,7)

        self.interaction_widgets = {}
        actions = list(self.ACTIONS)
        
        self.interaction_widgets = {actions[1]: ttk.Button(interaction_test_buttons, text= actions[1], image=self.photo_play, compound=tk.LEFT)}
        self.interaction_widgets[actions[1]].grid(row=0, column=1, sticky="we")
        self.interaction_widgets[actions[1]]["state"] = "disabled"

        self.interaction_widgets[actions[3]] = ttk.Button(interaction_test_buttons, text= actions[3], image=self.photo_next, compound=tk.LEFT)
        self.interaction_widgets[actions[3]].grid(row=1, column=2, sticky="we")
        self.interaction_widgets[actions[3]]["state"] = "disabled"

        self.interaction_widgets[actions[2]] = ttk.Button(interaction_test_buttons, text= actions[2], image=self.photo_prev, compound=tk.LEFT)
        self.interaction_widgets[actions[2]].grid(row=1, column=0, sticky="we")
        self.interaction_widgets[actions[2]]["state"] = "disabled"
        
        self.interaction_widgets[actions[4]] = ttk.Button(interaction_test_buttons, text= actions[4], image=self.photo_stop, compound=tk.LEFT)
        self.interaction_widgets[actions[4]].grid(row=2, column=1, sticky="we")
        self.interaction_widgets[actions[4]]["state"] = "disabled"

        self.interaction_widgets[actions[11]] = ttk.Button(interaction_test_buttons, text= actions[11], image=self.red_btn, compound=tk.LEFT)
        self.interaction_widgets[actions[11]].grid(row=4, column=0, sticky="we")
        self.interaction_widgets[actions[11]]["state"] = "disabled"

        self.interaction_widgets['btn2'] = ttk.Button(interaction_test_buttons, text= "Button 2", image=self.green_btn, compound=tk.LEFT)
        self.interaction_widgets['btn2'].grid(row=4, column=1, sticky="we")
        self.interaction_widgets['btn2']["state"] = "disabled"

        self.interaction_widgets['btn3'] = ttk.Button(interaction_test_buttons, text= "Button 3", image=self.blue_btn, compound=tk.LEFT)
        self.interaction_widgets['btn3'].grid(row=4, column=2, sticky="we")
        self.interaction_widgets['btn3']["state"] = "disabled"

        tk.Frame(interaction_test, height=1, bg="black").grid(row=0, column=1, sticky="ns")

        interaction_test_scales = tk.Frame(interaction_test)
        interaction_test_scales.grid(row=0, column=2, sticky="news")
        interaction_test_scales.columnconfigure(0, weight=1)
        interaction_test_scales.rowconfigure(0, weight=1)
        interaction_test_scales.rowconfigure(2, weight=1)

        interaction_test_scales_upper = tk.Frame(interaction_test_scales)
        interaction_test_scales_upper.grid(row=0, column=0, sticky="news", padx=10, pady=10)
        interaction_test_scales_upper.rowconfigure(0, weight=0)
        interaction_test_scales_upper.rowconfigure(1, weight=1)
        interaction_test_scales_upper.columnconfigure(0, weight=1)
        interaction_test_scales_upper.columnconfigure(1, weight=1)

        self.test_volume_user_lb = tk.Label(interaction_test_scales_upper, text="Volume Input")
        self.test_volume_user_lb.grid(row=0, column=0, sticky="news")

        self.experiment_volume_user = ttk.Scale(interaction_test_scales_upper, from_=100, to=0, orient="vertical")
        self.experiment_volume_user.grid(row=1, column=0, sticky="news")
        self.experiment_volume_user["state"] = "disabled"

        self.test_volume_required_lb = tk.Label(interaction_test_scales_upper, text="Volume Required")
        self.test_volume_required_lb.grid(row=0, column=1, sticky="news")

        self.interaction_widgets['Volume'] = ttk.Scale(interaction_test_scales_upper, from_=100, to=0, orient="vertical")
        self.interaction_widgets['Volume'].grid(row=1, column=1, sticky="news")
        self.interaction_widgets['Volume']["state"] = "disabled"

        tk.Frame(interaction_test_scales, height=1, bg="black").grid(row=1, column=0, sticky="news")

        interaction_test_scales_lower = tk.Frame(interaction_test_scales, bg="green")
        interaction_test_scales_lower.grid(row=2, column=0, sticky="news", padx=10)
        interaction_test_scales_lower.rowconfigure(0, weight=1)
        interaction_test_scales_lower.rowconfigure(1, weight=1)
        interaction_test_scales_lower.rowconfigure(2, weight=1)
        interaction_test_scales_lower.rowconfigure(3, weight=1)
        interaction_test_scales_lower.columnconfigure(0, weight=1)

        self.test_seek_user_lb = tk.Label(interaction_test_scales_lower, anchor="w", text="Seek Input")
        self.test_seek_user_lb.grid(row=0, column=0, sticky="news")

        self.experiment_seek_user = ttk.Scale(interaction_test_scales_lower, from_=0, to=100)
        self.experiment_seek_user.grid(row=1, column=0, sticky="news")
        self.experiment_seek_user["state"] = "disabled"

        self.test_seek_required_lb = tk.Label(interaction_test_scales_lower, anchor="w", text="Seek Required")
        self.test_seek_required_lb.grid(row=2, column=0, sticky="news")

        self.interaction_widgets['Seek'] = ttk.Scale(interaction_test_scales_lower, from_=0, to=100)
        self.interaction_widgets['Seek'].grid(row=3, column=0, sticky="news")
        self.interaction_widgets['Seek']["state"] = "disabled"

    def start_experiment(self):
        """
        Starts an experiment cycle consisting of two separate test cases:
        - Speed test:       Compares the speed between the different approaches by holding the phone at all times
        - Interactive test: Compares the speed in a more natural way, like having to pick up the phone each time between each action

        Each experiment requires 10 different random actions to be matched within some time limit.
        """

        self.test_status = True
        mistakes = correct_answers = 0
        experiment_results = []
        self.experiments_progress_bar['value'] = 0

        # Disable experimental controls to prevent unwanted behavior
        self.interaction_start["state"]    = "disabled"
        self.interaction_choice_1["state"] = "disabled"
        self.interaction_choice_2["state"] = "disabled"

        for i in range(0, 10):
            self.progress_value.set("Tests completed: " + str(i+1) + "/10")
            test_interaction, widget = random.choice(list(self.interaction_widgets.items()))
            widget["state"] = "enabled"
            if test_interaction == "Volume" or test_interaction == "Seek":
                if test_interaction == "Volume":
                    self.experiment_volume_user["state"] = "enabled"
                else:
                    self.experiment_seek_user["state"] = "enabled"
                widget.set(random.randint(0, 100))

            start = time.time()
            found = False

            while (time.time()-start) <= 3:
                if self.active_interaction == '':
                    continue
                if self.active_interaction == "Volume":
                    volume_user = self.experiment_volume_user.get()
                    volume_required = self.interaction_widgets['Volume'].get()
                    if volume_user >= volume_required - 10 and volume_user <= volume_required + 10:
                        correct_answers += 1
                        found = True
                        break
                elif self.active_interaction == "Seek":
                    seek_user = self.experiment_seek_user.get()
                    seek_required = self.interaction_widgets['Seek'].get()
                    if seek_user >= seek_required - 10 and seek_user <= seek_required + 10:
                        correct_answers += 1
                        found = True
                        break
                elif self.settings[self.active_interaction]['Interaction'] == test_interaction:
                    correct_answers += 1
                    found = True
                    break
                time.sleep(0.1)

            if not found:
                mistakes += 1

            end = time.time()
            result = end-start
            experiment_results.append((test_interaction, round(result,3), found, self.interaction_mode.get()))
            widget["state"] = "disabled"
            if self.experiment_volume_user["state"] == "enabled": self.experiment_volume_user["state"] = "disabled"
            if self.experiment_seek_user["state"]   == "enabled": self.experiment_seek_user["state"]   = "disabled"
            self.experiments_progress_bar['value'] += 10

            # Check if mode is interactive thus allowing time for the device to be put down
            if self.interaction_mode.get() == 2:
                time.sleep(3)

        self.test_status = False
        
        # Re-enable experimental controls after experiment ended
        self.interaction_start["state"]    = "enabled"
        self.interaction_choice_1["state"] = "normal"
        self.interaction_choice_2["state"] = "normal"

        print('[Debug] Correct answers:', correct_answers, 'Mistakes:', mistakes)

        filename = 'experiments/' + time.strftime("%Y%m%d%H%M%S") + '_experiment.csv'
        with open(filename,'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Required Action', 'Time', 'Correct', 'Mode'])
            writer.writerows(experiment_results)

    def action_controller(self):
        while True:
            if self.connected:
                if time.time()-self.received_time_history >= 0.23:
                    self.active_interaction = ''
                    self.action_compensation = False
                    self.current_action_var.set('None')

                if time.time()-self.received_time_history >= 1:
                    self.status_var.set("Waiting for Data")
                
                if time.time()-self.received_time_history >= 60:
                    self.connected = False
                    self.label_status_var.config(fg='red')
                    self.label_client_var.config(fg='red')
                    self.status_var.set("Not connected")
                    self.client_var.set("Not connected")
            time.sleep(0.1)

    def get_data(self):
        """
        Deserialize the UDP data stream from the Android.
        There are currently two types of sensor data:
        - type `G`: Gyroscope sensor values in x,y,z
        - type `R`: Rotation vector sensor values in x,y,z
        """
        self.connected = False
        self.received_time_history = 0

        self.active_interaction = ''
        self.action_compensation = False

        self.sensor_history = (0, 0, 0) # Past values used for comparisons

        self.action_controller_thread = threading.Thread(target=self.action_controller, daemon=True)
        self.action_controller_thread.start()

        while True:
            try:
                # Buffer size 1024
                message, address = self.s.recvfrom(1024)
                message_string = message.decode("utf-8")

                if message_string:
                    received_time = time.time()
                    self.status_var.set("Receiving Data")

                    if not self.connected:
                        self.label_status_var.config(fg='green')
                        self.label_client_var.config(fg='black')
                        self.status_var.set("Receiving Data")
                        self.client_var.set(address[0])
                        self.connected = True

                    message_string = message_string.replace(' ','').split(",")

                    if len(message_string) != 12:
                        continue

                    data = {}
                    data['Timestep']      = float(message_string[0])
                    data['Action']        = message_string[1]
                    data['Gyroscope']     = {'x': float(message_string[2]), 'y': float(message_string[3]), 'z':  float(message_string[4])}
                    data['Accelerometer'] = {'x': float(message_string[5]), 'y': float(message_string[6]), 'z':  float(message_string[7])}
                    data['Rotation']      = {'x': float(message_string[8]), 'y': float(message_string[9]), 'z':  float(message_string[10])}

                    self.update_sensor_data(data)
                    self.execute_command(data, sensor="Accelerometer")

                    self.received_time_history = received_time
   
            except (KeyboardInterrupt, SystemExit):
                raise traceback.print_exc()

    def update_sensor_data(self, data):
        if not self.active_status and not self.test_status:
            self.gyro_x.set(str(data['Gyroscope']['x']))
            self.gyro_y.set(str(data['Gyroscope']['y']))
            self.gyro_z.set(str(data['Gyroscope']['z']))

            self.acceleration_x.set(str(data['Accelerometer']['x']))
            self.acceleration_y.set(str(data['Accelerometer']['y']))
            self.acceleration_z.set(str(data['Accelerometer']['z']))

            self.rotation_x.set(str(data['Rotation']['x']))
            self.rotation_y.set(str(data['Rotation']['y']))
            self.rotation_z.set(str(data['Rotation']['z']))

    def execute_command(self, data, sensor):
        """
        Executes an action based on sensor data. This function is also responsible for executing\n
        actions depending on active and test statuses.

        Parameters:
        -----------
            data (`dict`): Dictionary containing data from the client's sensors.

        Returns:
        --------
            None
        """

        # Time between dataframes ~ 0.21 sec which means that when this thrueshold is passed a new action should be activated
        if self.active_interaction == '':
            if not self.action_compensation:
                self.sensor_history = (data[sensor]['x'],  data[sensor]['y'],  data[sensor]['z'])
                self.action_compensation = True
                return False
            else:
                self.active_interaction = data['Action'] + self.get_tilt_kind(data[sensor])
                self.current_action_var.set(self.active_interaction + " - (" + self.settings[self.active_interaction]['Interaction'] + ")")
                self.sensor_history = ( data[sensor]['x'],  data[sensor]['y'],  data[sensor]['z'])

        # When active_status is active the application is controlling this device's resources
        if self.active_status:
            if self.ACTIONS[self.settings[self.active_interaction]['Interaction']]['has_params']:
                self.ACTIONS[self.settings[self.active_interaction]['Interaction']]['function'](self.settings[self.active_interaction]['Type'])
            else:
                self.ACTIONS[self.settings[self.active_interaction]['Interaction']]['function']()

        # When test_status is active, an experiment is underway
        if self.test_status:
            if self.experiment_volume_user["state"] == "enabled" and self.active_interaction != '':
                if (self.settings[self.active_interaction]['Interaction']) == "Volume -":
                    self.experiment_volume_user.set(self.experiment_volume_user.get()-10)
                elif (self.settings[self.active_interaction]['Interaction']) == "Volume +":
                    self.experiment_volume_user.set(self.experiment_volume_user.get()+10)
            elif self.experiment_seek_user["state"] == "enabled" and self.active_interaction != '':
                if (self.settings[self.active_interaction]['Interaction']) == "Seek -":
                    self.experiment_seek_user.set(self.experiment_seek_user.get()-10)
                elif (self.settings[self.active_interaction]['Interaction']) == "Seek +":
                    self.experiment_seek_user.set(self.experiment_seek_user.get()+10)

    def get_tilt_kind(self, sensor_data):
        """
        Returns the current phone's tilt gesture.

        Parameters:
        -----------
            rot_vector (`dict`): Data from client's rotation vector in x,y,z

        Returns:
        --------
            tilt (string): String representation of tilt. Possible values are:
            * TU: Tilt Up
            * TD: Tilt Down
            * TR: Tilt Right
            * TL: Tilt Left
        """

        if abs(sensor_data['x']-self.sensor_history[0]) > abs(sensor_data['y']-self.sensor_history[1]):
            if sensor_data['x']-self.sensor_history[0] > 0: return "TL"
            else:                                           return "TR"
        else:
            if sensor_data['y']-self.sensor_history[1] > 0: return "TU"
            else:                                           return "TD"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Action Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def not_used(self):
        pass

    def play_pause(self):
        keyboard.send("space", do_press=True, do_release=True)

    def previous(self):
        keyboard.send("left", do_press=True, do_release=True)

    def next(self):
        keyboard.send("right", do_press=True, do_release=True)

    def stop(self):
        pass

    def increase_vol(self, mode):
        """
        Increase system's volume by specific ammount.
        """
        # Get current volume
        # set_volume = min(1.0, max(0.0, mode))
        currentVolumeDb = self.volume.GetMasterVolumeLevel()
        self.volume.SetMasterVolumeLevel(currentVolumeDb + 2.0, None)

    def decrease_vol(self, mode):
        """
        Increase system's volume by specific ammount.
        """
        # Get current volume
        # set_volume = min(1.0, max(0.0, mode))
        currentVolumeDb = self.volume.GetMasterVolumeLevel()
        self.volume.SetMasterVolumeLevel(currentVolumeDb - 2.0, None)

    def increase_seek(self, arg):
        pass

    def decrease_seek(self, arg):
        pass

    def scroll_up(self, arg):
        keyboard.send("up", do_press=True, do_release=True)

    def scroll_down(self, arg):
        keyboard.send("down", do_press=True, do_release=True)

    def mute(self):
        if self.volume.GetMute() == 0:
            self.volume.SetMute(1, None)
        else:
            self.volume.SetMute(0, None)

    def create_udp_stream(self):
        """
        Create a socket connection and listen to datapackets.
        """

        # TODO We need to check here if we need socket.SOCK_STREAM for TCP connection
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind the IP address and port number to socket instance
        self.s.bind((self.host, self.port))

        print("Success binding: UDP server up and listening")

        self.sensor_data = threading.Thread(target=self.get_data, daemon=True) # Use daemon=True to kill thread when applications exits
        self.sensor_data.start()

if __name__ == "__main__":
    app = Server(host='', port=50000)
    app.window.mainloop()