import tkinter as tk
from tkinter import ttk
import socket, traceback
import threading
import json

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class Server:
    """
    Main server class. It initializes the variables needed to display the graphical user interface
    and opens a UDP socket which listens to a user-defined port.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.pos_vector_y = 0

        self.settings = {}
        self.populate_settings()

        # Get default audio device using PyCAW
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

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
            self.settings['LSTU'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['LSTD'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['LSTL'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['LSTR'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['RSTU'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['RSTD'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['RSTL'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['RSTR'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['TSTU'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['TSTD'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['TSTL'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['TSTR'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['BSTU'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['BSTD'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['BSTL'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}
            self.settings['BSTR'] = {'Interaction' : 'Stop', 'Type' : 'Instant'}

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

    def create_general(self, parent):

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Connection Information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        status_frame = tk.Frame(parent)
        status_frame.grid(row=0, column=0, sticky="we", padx=0)

        conn_info = tk.Label(status_frame, text="Connection", font=("Courier", 24), anchor="w",)
        conn_info.grid(row=0, column=0, sticky="we", columnspan=2)

        status_label = tk.Label(status_frame, text="Status:")
        status_label.grid(row=1, column=0, sticky="we")
        self.status_var = tk.StringVar()
        self.status_var.set("Not Connected")
        self.label_status_var = tk.Label(status_frame, textvariable=self.status_var, fg="Red")
        self.label_status_var.grid(row=1, column=1, sticky="we", padx=25)

        client_label = tk.Label(status_frame, text="Client:")
        client_label.grid(row=2, column=0, sticky="we")
        self.client_var = tk.StringVar()
        self.client_var.set("Not Connected")
        self.label_client_var = tk.Label(status_frame, textvariable=self.client_var, fg="Red")
        self.label_client_var.grid(row=2, column=1, sticky="we", padx=25)

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
        position_data_frame = tk.Frame(information_grid)
        position_data_frame.grid(row=1, column=1, sticky="we", padx=0)

        position_data_x_label = tk.Label(position_data_frame, text="Acceleration x:")
        position_data_x_label.grid(row=0, column=0, sticky="we")
        self.position_x = tk.StringVar()
        self.position_x.set("N/A")
        label_position_x = tk.Label(position_data_frame, textvariable=self.position_x)
        label_position_x.grid(row=0, column=1, sticky="we", padx=25)

        position_data_y_label = tk.Label(position_data_frame, text="Acceleration y:")
        position_data_y_label.grid(row=1, column=0, sticky="we")
        self.position_y = tk.StringVar()
        self.position_y.set("N/A")
        label_position_y = tk.Label(position_data_frame, textvariable=self.position_y)
        label_position_y.grid(row=1, column=1, sticky="we", padx=25)

        position_data_z_label = tk.Label(position_data_frame, text="Acceleration z:")
        position_data_z_label.grid(row=2, column=0, sticky="we")
        self.position_z = tk.StringVar()
        self.position_z.set("N/A")
        label_position_z = tk.Label(position_data_frame, textvariable=self.position_z)
        label_position_z.grid(row=2, column=1, sticky="we", padx=25)

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
        modes_frame = tk.Frame(parent)
        modes_frame.grid(row=2, column=0, sticky="nswe", padx=0)

        modes = tk.Label(modes_frame, text="Mode Data", font=("Courier", 24), anchor="w",)
        modes.grid(row=0, column=0, sticky="we", columnspan=2)

        mode_data_label = tk.Label(modes_frame, text="Current Mode:")
        mode_data_label.grid(row=1, column=0, sticky="we")
        self.mode_var = tk.StringVar()
        self.mode_var.set("N/A")
        label_mode = tk.Label(modes_frame, textvariable=self.mode_var)
        label_mode.grid(row=1, column=1, sticky="we", padx=25)

    def create_settings(self, parent):

        ACTIONS = [
            "Play/Pause",
            "Previous",
            "Next",
            "Stop",
            "Volume +",
            "Volume -",
            "Seek +",
            "Seek -",
            "Scroll UP",
            "Scroll DOWN"
        ]

        TYPES = [
            "Constant",
            "Incremental",
            "Steps"
        ]

        def create_layout_settings(parent_frame):
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

            self.lstu_action = ttk.OptionMenu(ls_group, self.lstu_action_vars, self.settings['LSTU']['Interaction'], *ACTIONS, 
                                                    command= lambda x: modify_setting(self.lstu_action_vars, 'LSTU', 'Interaction'))
            self.lstu_action.grid(row=0, column=1, sticky="we")

            self.lstu_type_vars = tk.StringVar(ls_group)
            self.lstu_type_vars.set(self.settings['LSTU']['Type'])

            self.lstu_type = ttk.OptionMenu(ls_group, self.lstu_type_vars, self.settings['LSTU']['Type'], *TYPES, 
                                                    command=lambda x: modify_setting(self.lstu_type_vars, 'LSTU', 'Type'))
            self.lstu_type.grid(row=0, column=2, sticky="we")

            lstd_label = tk.Label(ls_group, anchor="w", text="Tilt Down:")
            lstd_label.grid(row=1, column=0, sticky="we")

            self.lstd_action_vars = tk.StringVar(ls_group)
            self.lstd_action_vars.set(self.settings['LSTD']['Interaction'])

            self.lstd_action = ttk.OptionMenu(ls_group, self.lstd_action_vars, self.settings['LSTD']['Interaction'], *ACTIONS, 
                                                    command= lambda x: modify_setting(self.lstd_action_vars, 'LSTD', 'Interaction'))
            self.lstd_action.grid(row=1, column=1, sticky="we")

            self.lstd_type_vars = tk.StringVar(ls_group)
            self.lstd_type_vars.set(self.settings['LSTD']['Type'])

            self.lstd_type = ttk.OptionMenu(ls_group, self.lstd_type_vars, self.settings['LSTD']['Type'], *TYPES, 
                                                    command=lambda x: modify_setting(self.lstd_type_vars, 'LSTD', 'Type'))
            self.lstd_type.grid(row=1, column=2, sticky="we")

            lstl_label = tk.Label(ls_group, anchor="w", text="Tilt Left:")
            lstl_label.grid(row=2, column=0, sticky="we")

            self.lstl_action_vars = tk.StringVar(ls_group)
            self.lstl_action_vars.set(self.settings['LSTL']['Interaction'])

            self.lstl_action = ttk.OptionMenu(ls_group, self.lstl_action_vars, self.settings['LSTL']['Interaction'], *ACTIONS, 
                                                    command= lambda x: modify_setting(self.lstl_action_vars, 'LSTL', 'Interaction'))
            self.lstl_action.grid(row=2, column=1, sticky="we")

            self.lstl_type_vars = tk.StringVar(ls_group)
            self.lstl_type_vars.set(self.settings['LSTL']['Type'])

            self.lstl_type = ttk.OptionMenu(ls_group, self.lstl_type_vars, self.settings['LSTL']['Type'], *TYPES, 
                                                    command=lambda x: modify_setting(self.lstl_type_vars, 'LSTL', 'Type'))
            self.lstl_type.grid(row=2, column=2, sticky="we")

            lstr_label = tk.Label(ls_group, anchor="w", text="Tilt Right:")
            lstr_label.grid(row=3, column=0, sticky="we")

            self.lstr_action_vars = tk.StringVar(ls_group)
            self.lstr_action_vars.set(self.settings['LSTR']['Interaction'])

            self.lstr_action = ttk.OptionMenu(ls_group, self.lstr_action_vars, self.settings['LSTR']['Interaction'], *ACTIONS, 
                                                    command= lambda x: modify_setting(self.lstr_action_vars, 'LSTR', 'Interaction'))
            self.lstr_action.grid(row=3, column=1, sticky="we")

            self.lstr_type_vars = tk.StringVar(ls_group)
            self.lstr_type_vars.set(self.settings['LSTR']['Type'])

            self.lstr_type = ttk.OptionMenu(ls_group, self.lstr_type_vars, self.settings['LSTR']['Type'], *TYPES, 
                                                    command=lambda x: modify_setting(self.lstr_type_vars, 'LSTR', 'Type'))
            self.lstr_type.grid(row=3, column=2, sticky="we")

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

            self.rstu_action = ttk.OptionMenu(rs_group, self.rstu_action_vars, self.settings['RSTU']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.rstu_action_vars, 'RSTU', 'Interaction'))
            self.rstu_action.grid(row=0, column=1, sticky="we")

            self.rstu_type_vars = tk.StringVar(rs_group)
            self.rstu_type_vars.set(self.settings['RSTU']['Type'])

            self.rstu_type = ttk.OptionMenu(rs_group, self.rstu_type_vars, self.settings['RSTU']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.rstu_type_vars, 'RSTU', 'Type'))
            self.rstu_type.grid(row=0, column=2, sticky="we")

            rstd_label = tk.Label(rs_group, anchor="w", text="Tilt Down:")
            rstd_label.grid(row=1, column=0, sticky="we")

            self.rstd_action_vars = tk.StringVar(rs_group)
            self.rstd_action_vars.set(self.settings['RSTD']['Interaction'])

            self.rstd_action = ttk.OptionMenu(rs_group, self.rstd_action_vars, self.settings['RSTD']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.rstd_action_vars, 'RSTD', 'Interaction'))
            self.rstd_action.grid(row=1, column=1, sticky="we")

            self.rstd_type_vars = tk.StringVar(rs_group)
            self.rstd_type_vars.set(self.settings['RSTD']['Type'])

            self.rstd_type = ttk.OptionMenu(rs_group, self.rstd_type_vars, self.settings['RSTD']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.rstd_type_vars, 'RSTD', 'Type'))
            self.rstd_type.grid(row=1, column=2, sticky="we")

            rstl_label = tk.Label(rs_group, anchor="w", text="Tilt Left:")
            rstl_label.grid(row=2, column=0, sticky="we")

            self.rstl_action_vars = tk.StringVar(rs_group)
            self.rstl_action_vars.set(self.settings['RSTL']['Interaction'])

            self.rstl_action = ttk.OptionMenu(rs_group, self.rstl_action_vars, self.settings['RSTL']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.rstl_action_vars, 'RSTL', 'Interaction'))
            self.rstl_action.grid(row=2, column=1, sticky="we")

            self.rstl_type_vars = tk.StringVar(rs_group)
            self.rstl_type_vars.set(self.settings['RSTL']['Type'])

            self.rstl_type = ttk.OptionMenu(rs_group, self.rstl_type_vars, self.settings['RSTL']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.rstl_type_vars, 'RSTL', 'Type'))
            self.rstl_type.grid(row=2, column=2, sticky="we")

            rstr_label = tk.Label(rs_group, anchor="w", text="Tilt Right:")
            rstr_label.grid(row=3, column=0, sticky="we")

            self.rstr_action_vars = tk.StringVar(rs_group)
            self.rstr_action_vars.set(self.settings['RSTR']['Interaction'])

            self.rstr_action = ttk.OptionMenu(rs_group, self.rstr_action_vars, self.settings['RSTR']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.rstr_action_vars, 'RSTR', 'Interaction'))
            self.rstr_action.grid(row=3, column=1, sticky="we")

            self.rstr_type_vars = tk.StringVar(rs_group)
            self.rstr_type_vars.set(self.settings['RSTR']['Type'])

            self.rstr_type = ttk.OptionMenu(rs_group, self.rstr_type_vars, self.settings['RSTR']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.rstr_type_vars, 'RSTR', 'Type'))
            self.rstr_type.grid(row=3, column=2, sticky="we")

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

            self.tstu_action = ttk.OptionMenu(ts_group, self.tstu_action_vars, self.settings['TSTU']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.tstu_action_vars, 'TSTU', 'Interaction'))
            self.tstu_action.grid(row=0, column=1, sticky="we")

            self.tstu_type_vars = tk.StringVar(ts_group)
            self.tstu_type_vars.set(self.settings['TSTU']['Type'])

            self.tstu_type = ttk.OptionMenu(ts_group, self.tstu_type_vars, self.settings['TSTU']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.tstu_type_vars, 'TSTU', 'Type'))
            self.tstu_type.grid(row=0, column=2, sticky="we")

            tstd_label = tk.Label(ts_group, anchor="w", text="Tilt Down:")
            tstd_label.grid(row=1, column=0, sticky="we")

            self.tstd_action_vars = tk.StringVar(ts_group)
            self.tstd_action_vars.set(self.settings['TSTD']['Interaction'])

            self.tstd_action = ttk.OptionMenu(ts_group, self.tstd_action_vars, self.settings['TSTD']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.tstd_action_vars, 'TSTD', 'Interaction'))
            self.tstd_action.grid(row=1, column=1, sticky="we")

            self.tstd_type_vars = tk.StringVar(ts_group)
            self.tstd_type_vars.set(self.settings['TSTD']['Type'])

            self.tstd_type = ttk.OptionMenu(ts_group, self.tstd_type_vars, self.settings['TSTD']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.tstd_type_vars, 'TSTD', 'Type'))
            self.tstd_type.grid(row=1, column=2, sticky="we")

            tstl_label = tk.Label(ts_group, anchor="w", text="Tilt Left:")
            tstl_label.grid(row=2, column=0, sticky="we")

            self.tstl_action_vars = tk.StringVar(ts_group)
            self.tstl_action_vars.set(self.settings['TSTL']['Interaction'])

            self.tstl_action = ttk.OptionMenu(ts_group, self.tstl_action_vars, self.settings['TSTL']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.tstl_action_vars, 'TSTL', 'Interaction'))
            self.tstl_action.grid(row=2, column=1, sticky="we")

            self.tstl_type_vars = tk.StringVar(ts_group)
            self.tstl_type_vars.set(self.settings['TSTL']['Type'])

            self.tstl_type = ttk.OptionMenu(ts_group, self.tstl_type_vars, self.settings['TSTL']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.tstl_type_vars, 'TSTL', 'Type'))
            self.tstl_type.grid(row=2, column=2, sticky="we")

            tstr_label = tk.Label(ts_group, anchor="w", text="Tilt Right:")
            tstr_label.grid(row=3, column=0, sticky="we")

            self.tstr_action_vars = tk.StringVar(ts_group)
            self.tstr_action_vars.set(self.settings['TSTR']['Interaction'])

            self.tstr_action = ttk.OptionMenu(ts_group, self.tstr_action_vars, self.settings['TSTR']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.tstr_action_vars, 'TSTR', 'Interaction'))
            self.tstr_action.grid(row=3, column=1, sticky="we")

            self.tstr_type_vars = tk.StringVar(ts_group)
            self.tstr_type_vars.set(self.settings['TSTR']['Type'])

            self.tstr_type = ttk.OptionMenu(ts_group, self.tstr_type_vars, self.settings['TSTR']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.tstr_type_vars, 'TSTR', 'Type'))
            self.tstr_type.grid(row=3, column=2, sticky="we")

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

            self.bstu_action = ttk.OptionMenu(bs_group, self.bstu_action_vars, self.settings['BSTU']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.bstu_action_vars, 'BSTU', 'Interaction'))
            self.bstu_action.grid(row=0, column=1, sticky="we")

            self.bstu_type_vars = tk.StringVar(bs_group)
            self.bstu_type_vars.set(self.settings['BSTU']['Type'])

            self.bstu_type = ttk.OptionMenu(bs_group, self.bstu_type_vars, self.settings['BSTU']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.bstu_type_vars, 'BSTU', 'Type'))
            self.bstu_type.grid(row=0, column=2, sticky="we")

            bstd_label = tk.Label(bs_group, anchor="w", text="Tilt Down:")
            bstd_label.grid(row=1, column=0, sticky="we")

            self.bstd_action_vars = tk.StringVar(bs_group)
            self.bstd_action_vars.set(self.settings['BSTD']['Interaction'])

            self.bstd_action = ttk.OptionMenu(bs_group, self.bstd_action_vars, self.settings['BSTD']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.bstd_action_vars, 'BSTD', 'Interaction'))
            self.bstd_action.grid(row=1, column=1, sticky="we")

            self.bstd_type_vars = tk.StringVar(bs_group)
            self.bstd_type_vars.set(self.settings['BSTD']['Type'])

            self.bstd_type = ttk.OptionMenu(bs_group, self.bstd_type_vars, self.settings['BSTD']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.bstd_type_vars, 'BSTD', 'Type'))
            self.bstd_type.grid(row=1, column=2, sticky="we")

            bstl_label = tk.Label(bs_group, anchor="w", text="Tilt Left:")
            bstl_label.grid(row=2, column=0, sticky="we")

            self.bstl_action_vars = tk.StringVar(bs_group)
            self.bstl_action_vars.set(self.settings['BSTL']['Interaction'])

            self.bstl_action = ttk.OptionMenu(bs_group, self.bstl_action_vars, self.settings['BSTL']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.bstl_action_vars, 'BSTL', 'Interaction'))
            self.bstl_action.grid(row=2, column=1, sticky="we")

            self.bstl_type_vars = tk.StringVar(bs_group)
            self.bstl_type_vars.set(self.settings['BSTL']['Type'])

            self.bstl_type = ttk.OptionMenu(bs_group, self.bstl_type_vars, self.settings['BSTL']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.bstl_type_vars, 'BSTL', 'Type'))
            self.bstl_type.grid(row=2, column=2, sticky="we")

            bstr_label = tk.Label(bs_group, anchor="w", text="Tilt Right:")
            bstr_label.grid(row=3, column=0, sticky="we")

            self.bstr_action_vars = tk.StringVar(bs_group)
            self.bstr_action_vars.set(self.settings['BSTR']['Interaction'])

            self.bstr_action = ttk.OptionMenu(bs_group, self.bstr_action_vars, self.settings['BSTR']['Interaction'], *ACTIONS,
                                                    command= lambda x: modify_setting(self.bstr_action_vars, 'BSTR', 'Interaction'))
            self.bstr_action.grid(row=3, column=1, sticky="we")

            self.bstr_type_vars = tk.StringVar(bs_group)
            self.bstr_type_vars.set(self.settings['BSTR']['Type'])

            self.bstr_type = ttk.OptionMenu(bs_group, self.bstr_type_vars, self.settings['BSTR']['Type'], *TYPES,
                                                    command=lambda x: modify_setting(self.bstr_type_vars, 'BSTR', 'Type'))
            self.bstr_type.grid(row=3, column=2, sticky="we")

            tk.Frame(parent_frame, height=1, bg="black").grid(row=3, column=0, sticky="news", columnspan=3)

        def modify_setting(*args):
            self.settings[args[1]][args[2]] = args[0].get()

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
        self.save_settings_btn.grid(row=0, column=0)

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

        interaction_selection_explanation = tk.Message(interaction_selection, width=180 ,text="Please select the type of interaction tests: ")
        interaction_selection_explanation.grid(row=0, column=0, sticky="nswe")

        # Mode Selection RadioButton
        interaction_selection_choice = tk.Frame(interaction_selection)
        interaction_selection_choice.grid(row=0, column=1, sticky="nswe")

        interaction_mode = tk.IntVar(value=1)
        interaction_choice_1 = tk.Radiobutton(interaction_selection_choice, variable=interaction_mode, value=1, tristatevalue=0, text="Speed Test")
        interaction_choice_1.grid(row=0, column=1, sticky="w")
        interaction_choice_2 = tk.Radiobutton(interaction_selection_choice, variable=interaction_mode, value=2, tristatevalue=0, text="Interactive Test")
        interaction_choice_2.grid(row=1, column=1, sticky="w")

        interaction_start = ttk.Button(interaction_selection, text= "Start")
        interaction_start.grid(row=0, column=2)

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

        def test():
            print("It works!")

        self.photo_play  = tk.PhotoImage(file = r"./server/sources/play.png").subsample(7,7)
        self.photo_next  = tk.PhotoImage(file = r"./server/sources/next.png").subsample(7,7)
        self.photo_prev  = tk.PhotoImage(file = r"./server/sources/previous.png").subsample(7,7)
        self.photo_stop  = tk.PhotoImage(file = r"./server/sources/stop.png").subsample(7,7)
        self.red_btn     = tk.PhotoImage(file = r"./server/sources/red_btn.png").subsample(7,7)
        self.green_btn   = tk.PhotoImage(file = r"./server/sources/green_btn.png").subsample(7,7)
        self.blue_btn    = tk.PhotoImage(file = r"./server/sources/blue_btn.png").subsample(7,7)

        self.interaction_button = ttk.Button(interaction_test_buttons, text= "Play/Pause", image=self.photo_play, compound=tk.LEFT, command= test)
        self.interaction_button.grid(row=0, column=1, sticky="we")
        self.interaction_button["state"] = "disabled"

        self.interaction_button_next = ttk.Button(interaction_test_buttons, text= "Next", image=self.photo_next, compound=tk.LEFT, command= test)
        self.interaction_button_next.grid(row=1, column=2, sticky="we")

        self.interaction_button_prev = ttk.Button(interaction_test_buttons, text= "Previous", image=self.photo_prev, compound=tk.LEFT, command= test)
        self.interaction_button_prev.grid(row=1, column=0, sticky="we")
        
        self.interaction_button_stop = ttk.Button(interaction_test_buttons, text= "Stop", image=self.photo_stop, compound=tk.LEFT, command= test)
        self.interaction_button_stop.grid(row=2, column=1, sticky="we")

        tk.Frame(interaction_test, height=1, bg="black").grid(row=3, column=0, sticky="we")

        self.interaction_button_1 = ttk.Button(interaction_test_buttons, text= "Button 1", image=self.red_btn, compound=tk.LEFT, command= test)
        self.interaction_button_1.grid(row=4, column=0, sticky="we")

        self.interaction_button_2 = ttk.Button(interaction_test_buttons, text= "Button 2", image=self.green_btn, compound=tk.LEFT, command= test)
        self.interaction_button_2.grid(row=4, column=1, sticky="we")

        self.interaction_button_3 = ttk.Button(interaction_test_buttons, text= "Button 3", image=self.blue_btn, compound=tk.LEFT, command= test)
        self.interaction_button_3.grid(row=4, column=2, sticky="we")  

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

        self.test_volume_user = ttk.Scale(interaction_test_scales_upper, from_=0, to=100, orient="vertical")
        self.test_volume_user.grid(row=1, column=0, sticky="news")

        self.test_volume_required_lb = tk.Label(interaction_test_scales_upper, text="Volume Required")
        self.test_volume_required_lb.grid(row=0, column=1, sticky="news")

        self.test_volume_required = ttk.Scale(interaction_test_scales_upper, from_=0, to=100, orient="vertical")
        self.test_volume_required.grid(row=1, column=1, sticky="news")

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

        self.test_seek_user = ttk.Scale(interaction_test_scales_lower, from_=0, to=100)
        self.test_seek_user.grid(row=1, column=0, sticky="news")

        self.test_seek_required_lb = tk.Label(interaction_test_scales_lower, anchor="w", text="Seek Required")
        self.test_seek_required_lb.grid(row=2, column=0, sticky="news")

        self.test_seek_required = ttk.Scale(interaction_test_scales_lower, from_=0, to=100)
        self.test_seek_required.grid(row=3, column=0, sticky="news")

    def get_data(self):
        """
        Deserialize the UDP data stream from the Android.
        There are currently two types of sensor data:
        - type `G`: Gyroscope sensor values in x,y,z
        - type `R`: Rotation vector sensor values in x,y,z
        """
        connected = False
        while True:
            try:
                # Buffer size 1024
                message, address = self.s.recvfrom(1024)
                message_string = message.decode("utf-8")

                if message_string:
                    if not connected:
                        self.label_status_var.config(fg='green')
                        self.label_client_var.config(fg='black')
                        self.status_var.set("Receiving Data")
                        self.client_var.set(address[0])
                        connected = True

                    message_string = message_string.replace(' ','').split("?")

                    data = {}

                    for item in message_string:
                        temp_item = item.split(",")
                        data[temp_item[0]] = {'x': temp_item[1], 'y': temp_item[2], 'z': temp_item[3]}

                    old_vector = self.pos_vector_y

                    self.gyro_x.set(data['G']['x'])
                    self.gyro_y.set(data['G']['y'])
                    self.gyro_z.set(data['G']['z'])

                    self.position_x.set(data['R']['x'])
                    self.position_y.set(data['R']['y'])
                    self.position_z.set(data['R']['z'])

                    self.pos_vector_y = float(data['R']['y'])

                    if self.pos_vector_y - old_vector > 0:
                        self.increase_vol(self.pos_vector_y)
   
            except (KeyboardInterrupt, SystemExit):
                raise traceback.print_exc()

    def increase_vol(self, vol):
        """
        Increase System's volume by specific ammount.

        Todo:
            * Make this work with Db
            * Find ways to make this constant, incremental and exponential
        """
        # Get current volume
        set_volume = min(1.0, max(0.0, vol))
        currentVolumeDb = self.volume.GetMasterVolumeLevel()
        self.volume.SetMasterVolumeLevel(currentVolumeDb - 1.0, None)

    def create_udp_stream(self):
        """
        Create a socket connection and listen to datapackets.
        """

        # TODO We need to check here ifwe need socket.SOCK_STREAM for TCP connection
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind the IP address and port number to socket instance
        self.s.bind((self.host, self.port))

        print("Success binding: UDP server up and listening")

        self.sensor_data = threading.Thread(target=self.get_data, daemon=True) # Use daemon=True to kill thread when applications exits
        self.sensor_data.start()

if __name__ == "__main__":
    app = Server(host='', port=50000)
    app.window.mainloop()