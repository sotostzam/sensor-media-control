import tkinter as tk
from tkinter import ttk
import socket, traceback
import threading

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
        self.create_gui()
        self.create_udp_stream()

    def create_gui(self):
        self.pos_vector_y = 0

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
        self.settings_frame.rowconfigure(2, weight=1)
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

        self.mode = 0  # Mode selection: 0 for screen-layout mode and 1 for orientation mode

        mode_info_frame = tk.Frame(parent)
        mode_info_frame.grid(row=0, column=0, sticky="we", pady=10)
        mode_info_frame.rowconfigure(1, weight=1)
        mode_info_frame.columnconfigure(0, weight=1)
        mode_info_frame.columnconfigure(1, weight=1)

        mode_info_label = tk.Label(mode_info_frame, font=("Courier", 12), text="Please select your preferred mode:")
        mode_info_label.grid(row=0, column=0, sticky="we")

        mode_btn_group = tk.Frame(mode_info_frame)
        mode_btn_group.grid(row=0, column=1, sticky="nswe")

        self.mode_1_button = ttk.Button(mode_btn_group, text= "Screen Layout Mode", command=lambda: show_frame(0))
        self.mode_1_button.grid(row=0, column=0, sticky="we")

        self.mode_2_button = ttk.Button(mode_btn_group, text= "Orientation Mode", command=lambda: show_frame(1))
        self.mode_2_button.grid(row=1, column=0, sticky="we")

        tk.Frame(parent, height=1, bg="black").grid(row=1, column=0, sticky="ew")

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
            "Exponential",
            "Instant"
        ]

        def create_slm_settings(parent_frame):
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Screen Left Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            slm_left = tk.Frame(parent_frame)
            slm_left.grid(row=0, column=0, sticky="nswe")
            slm_left.rowconfigure(0, weight=1)

            self.icon_screen_left  = tk.PhotoImage(file = r"./server/sources/screen_left.png").subsample(3,3)
            slml_picture = tk.Label(slm_left, image=self.icon_screen_left)
            slml_picture.grid(row=0, column=0, sticky="nswe")

            slml_group = tk.Frame(slm_left)
            slml_group.grid(row=0, column=1, sticky="we")

            slml_tu = tk.Label(slml_group, anchor="w", text="Tilt Up:")
            slml_tu.grid(row=0, column=0, sticky="we")

            self.slml_tu_action_vars = tk.StringVar(slml_group)
            self.slml_tu_action_vars.set(ACTIONS[2])

            self.slml_tu_action = ttk.OptionMenu(slml_group, self.slml_tu_action_vars, ACTIONS[2], *ACTIONS, command=save_setting)
            self.slml_tu_action.grid(row=0, column=1, sticky="we")

            self.slml_tu_type_vars = tk.StringVar(slml_group)
            self.slml_tu_type_vars.set(TYPES[2])

            self.slml_tu_type = ttk.OptionMenu(slml_group, self.slml_tu_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slml_tu_type.grid(row=0, column=2, sticky="we")

            slml_td = tk.Label(slml_group, anchor="w", text="Tilt Down:")
            slml_td.grid(row=1, column=0, sticky="we")

            self.slml_td_action_vars = tk.StringVar(slml_group)
            self.slml_td_action_vars.set(ACTIONS[0])

            self.slml_td_action = ttk.OptionMenu(slml_group, self.slml_td_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slml_td_action.grid(row=1, column=1, sticky="we")

            self.slml_td_type_vars = tk.StringVar(slml_group)
            self.slml_td_type_vars.set(TYPES[2])

            self.slml_td_type = ttk.OptionMenu(slml_group, self.slml_td_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slml_td_type.grid(row=1, column=2, sticky="we")

            slml_tl = tk.Label(slml_group, anchor="w", text="Tilt Left:")
            slml_tl.grid(row=2, column=0, sticky="we")

            self.slml_tl_action_vars = tk.StringVar(slml_group)
            self.slml_tl_action_vars.set(ACTIONS[0])

            self.slml_tl_action = ttk.OptionMenu(slml_group, self.slml_tl_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slml_tl_action.grid(row=2, column=1, sticky="we")

            self.slml_tl_type_vars = tk.StringVar(slml_group)
            self.slml_tl_type_vars.set(TYPES[2])

            self.slml_tl_type = ttk.OptionMenu(slml_group, self.slml_tl_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slml_tl_type.grid(row=2, column=2, sticky="we")

            slml_tr = tk.Label(slml_group, anchor="w", text="Tilt Right:")
            slml_tr.grid(row=3, column=0, sticky="we")

            self.slml_tr_action_vars = tk.StringVar(slml_group)
            self.slml_tr_action_vars.set(ACTIONS[0])

            self.slml_tr_action = ttk.OptionMenu(slml_group, self.slml_tr_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slml_tr_action.grid(row=3, column=1, sticky="we")

            self.slml_tr_type_vars = tk.StringVar(slml_group)
            self.slml_tr_type_vars.set(TYPES[2])

            self.slml_tr_type = ttk.OptionMenu(slml_group, self.slml_tr_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slml_tr_type.grid(row=3, column=2, sticky="we")

            tk.Frame(parent_frame, height=1, bg="black").grid(row=0, column=1, sticky="news")
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Screen Right Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            slm_right = tk.Frame(parent_frame)
            slm_right.grid(row=0, column=2, sticky="nswe")
            slm_right.rowconfigure(0, weight=1)

            self.icon_screen_right  = tk.PhotoImage(file = r"./server/sources/screen_right.png").subsample(3,3)
            slmr_picture = tk.Label(slm_right, image=self.icon_screen_right)
            slmr_picture.grid(row=0, column=0, sticky="we")

            slmr_group = tk.Frame(slm_right)
            slmr_group.grid(row=0, column=1, sticky="we")

            slmr_tu = tk.Label(slmr_group, anchor="w", text="Tilt Up:")
            slmr_tu.grid(row=0, column=0, sticky="we")

            self.slmr_tu_action_vars = tk.StringVar(slmr_group)
            self.slmr_tu_action_vars.set(ACTIONS[2])

            self.slmr_tu_action = ttk.OptionMenu(slmr_group, self.slmr_tu_action_vars, ACTIONS[2], *ACTIONS, command=save_setting)
            self.slmr_tu_action.grid(row=0, column=1, sticky="we")

            self.slmr_tu_type_vars = tk.StringVar(slmr_group)
            self.slmr_tu_type_vars.set(TYPES[2])

            self.slmr_tu_type = ttk.OptionMenu(slmr_group, self.slmr_tu_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmr_tu_type.grid(row=0, column=2, sticky="we")

            slmr_td = tk.Label(slmr_group, anchor="w", text="Tilt Down:")
            slmr_td.grid(row=1, column=0, sticky="we")

            self.slmr_td_action_vars = tk.StringVar(slmr_group)
            self.slmr_td_action_vars.set(ACTIONS[0])

            self.slmr_td_action = ttk.OptionMenu(slmr_group, self.slmr_td_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmr_td_action.grid(row=1, column=1, sticky="we")

            self.slmr_td_type_vars = tk.StringVar(slmr_group)
            self.slmr_td_type_vars.set(TYPES[2])

            self.slmr_td_type = ttk.OptionMenu(slmr_group, self.slmr_td_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmr_td_type.grid(row=1, column=2, sticky="we")

            slmr_tl = tk.Label(slmr_group, anchor="w", text="Tilt Left:")
            slmr_tl.grid(row=2, column=0, sticky="we")

            self.slmr_tl_action_vars = tk.StringVar(slmr_group)
            self.slmr_tl_action_vars.set(ACTIONS[0])

            self.slmr_tl_action = ttk.OptionMenu(slmr_group, self.slmr_tl_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmr_tl_action.grid(row=2, column=1, sticky="we")

            self.slmr_tl_type_vars = tk.StringVar(slmr_group)
            self.slmr_tl_type_vars.set(TYPES[2])

            self.slmr_tl_type = ttk.OptionMenu(slmr_group, self.slmr_tl_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmr_tl_type.grid(row=2, column=2, sticky="we")

            slmr_tr = tk.Label(slmr_group, anchor="w", text="Tilt Right:")
            slmr_tr.grid(row=3, column=0, sticky="we")

            self.slmr_tr_action_vars = tk.StringVar(slmr_group)
            self.slmr_tr_action_vars.set(ACTIONS[0])

            self.slmr_tr_action = ttk.OptionMenu(slmr_group, self.slmr_tr_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmr_tr_action.grid(row=3, column=1, sticky="we")

            self.slmr_tr_type_vars = tk.StringVar(slmr_group)
            self.slmr_tr_type_vars.set(TYPES[2])

            self.slmr_tr_type = ttk.OptionMenu(slmr_group, self.slmr_tr_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmr_tr_type.grid(row=3, column=2, sticky="we")

            tk.Frame(parent_frame, height=1, bg="black").grid(row=1, column=0, sticky="news", columnspan=3)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Screen Top Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            slm_top = tk.Frame(parent_frame)
            slm_top.grid(row=2, column=0, sticky="nswe")
            slm_top.rowconfigure(0, weight=1)

            self.icon_screen_top  = tk.PhotoImage(file = r"./server/sources/screen_top.png").subsample(3,3)
            slmt_picture = tk.Label(slm_top, image=self.icon_screen_top)
            slmt_picture.grid(row=0, column=0, sticky="we")

            slmt_group = tk.Frame(slm_top)
            slmt_group.grid(row=0, column=1, sticky="we")

            slmt_tu = tk.Label(slmt_group, anchor="w", text="Tilt Up:")
            slmt_tu.grid(row=0, column=0, sticky="we")

            self.slmt_tu_action_vars = tk.StringVar(slmt_group)
            self.slmt_tu_action_vars.set(ACTIONS[2])

            self.slmt_tu_action = ttk.OptionMenu(slmt_group, self.slmt_tu_action_vars, ACTIONS[2], *ACTIONS, command=save_setting)
            self.slmt_tu_action.grid(row=0, column=1, sticky="we")

            self.slmt_tu_type_vars = tk.StringVar(slmt_group)
            self.slmt_tu_type_vars.set(TYPES[2])

            self.slmt_tu_type = ttk.OptionMenu(slmt_group, self.slmt_tu_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmt_tu_type.grid(row=0, column=2, sticky="we")

            slmt_td = tk.Label(slmt_group, anchor="w", text="Tilt Down:")
            slmt_td.grid(row=1, column=0, sticky="we")

            self.slmt_td_action_vars = tk.StringVar(slmt_group)
            self.slmt_td_action_vars.set(ACTIONS[0])

            self.slmt_td_action = ttk.OptionMenu(slmt_group, self.slmt_td_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmt_td_action.grid(row=1, column=1, sticky="we")

            self.slmt_td_type_vars = tk.StringVar(slmt_group)
            self.slmt_td_type_vars.set(TYPES[2])

            self.slmt_td_type = ttk.OptionMenu(slmt_group, self.slmt_td_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmt_td_type.grid(row=1, column=2, sticky="we")

            slmt_tl = tk.Label(slmt_group, anchor="w", text="Tilt Left:")
            slmt_tl.grid(row=2, column=0, sticky="we")

            self.slmt_tl_action_vars = tk.StringVar(slmt_group)
            self.slmt_tl_action_vars.set(ACTIONS[0])

            self.slmt_tl_action = ttk.OptionMenu(slmt_group, self.slmt_tl_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmt_tl_action.grid(row=2, column=1, sticky="we")

            self.slmt_tl_type_vars = tk.StringVar(slmt_group)
            self.slmt_tl_type_vars.set(TYPES[2])

            self.slmt_tl_type = ttk.OptionMenu(slmt_group, self.slmt_tl_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmt_tl_type.grid(row=2, column=2, sticky="we")

            slmt_tr = tk.Label(slmt_group, anchor="w", text="Tilt Right:")
            slmt_tr.grid(row=3, column=0, sticky="we")

            self.slmt_tr_action_vars = tk.StringVar(slmt_group)
            self.slmt_tr_action_vars.set(ACTIONS[0])

            self.slmt_tr_action = ttk.OptionMenu(slmt_group, self.slmt_tr_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmt_tr_action.grid(row=3, column=1, sticky="we")

            self.slmt_tr_type_vars = tk.StringVar(slmt_group)
            self.slmt_tr_type_vars.set(TYPES[2])

            self.slmt_tr_type = ttk.OptionMenu(slmt_group, self.slmt_tr_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmt_tr_type.grid(row=3, column=2, sticky="we")

            tk.Frame(parent_frame, height=1, width=1, bg="black").grid(row=2, column=1, sticky="news")
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Screen Down Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            slm_bottom = tk.Frame(parent_frame)
            slm_bottom.grid(row=2, column=2, sticky="nswe")
            slm_bottom.rowconfigure(0, weight=1)

            self.icon_screen_bottom  = tk.PhotoImage(file = r"./server/sources/screen_bottom.png").subsample(3,3)
            slmb_picture = tk.Label(slm_bottom, image=self.icon_screen_bottom)
            slmb_picture.grid(row=0, column=0, sticky="we")

            slmb_group = tk.Frame(slm_bottom)
            slmb_group.grid(row=0, column=1, sticky="we")

            slmb_tu = tk.Label(slmb_group, anchor="w", text="Tilt Up:")
            slmb_tu.grid(row=0, column=0, sticky="we")

            self.slmb_tu_action_vars = tk.StringVar(slmb_group)
            self.slmb_tu_action_vars.set(ACTIONS[2])

            self.slmb_tu_action = ttk.OptionMenu(slmb_group, self.slmb_tu_action_vars, ACTIONS[2], *ACTIONS, command=save_setting)
            self.slmb_tu_action.grid(row=0, column=1, sticky="we")

            self.slmb_tu_type_vars = tk.StringVar(slmb_group)
            self.slmb_tu_type_vars.set(TYPES[2])

            self.slmb_tu_type = ttk.OptionMenu(slmb_group, self.slmb_tu_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmb_tu_type.grid(row=0, column=2, sticky="we")

            slmb_td = tk.Label(slmb_group, anchor="w", text="Tilt Down:")
            slmb_td.grid(row=1, column=0, sticky="we")

            self.slmb_td_action_vars = tk.StringVar(slmb_group)
            self.slmb_td_action_vars.set(ACTIONS[0])

            self.slmb_td_action = ttk.OptionMenu(slmb_group, self.slmb_td_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmb_td_action.grid(row=1, column=1, sticky="we")

            self.slmb_td_type_vars = tk.StringVar(slmb_group)
            self.slmb_td_type_vars.set(TYPES[2])

            self.slmb_td_type = ttk.OptionMenu(slmb_group, self.slmb_td_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmb_td_type.grid(row=1, column=2, sticky="we")

            slmb_tl = tk.Label(slmb_group, anchor="w", text="Tilt Left:")
            slmb_tl.grid(row=2, column=0, sticky="we")

            self.slmb_tl_action_vars = tk.StringVar(slmb_group)
            self.slmb_tl_action_vars.set(ACTIONS[0])

            self.slmb_tl_action = ttk.OptionMenu(slmb_group, self.slmb_tl_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmb_tl_action.grid(row=2, column=1, sticky="we")

            self.slmb_tl_type_vars = tk.StringVar(slmb_group)
            self.slmb_tl_type_vars.set(TYPES[2])

            self.slmb_tl_type = ttk.OptionMenu(slmb_group, self.slmb_tl_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmb_tl_type.grid(row=2, column=2, sticky="we")

            slmb_tr = tk.Label(slmb_group, anchor="w", text="Tilt Right:")
            slmb_tr.grid(row=3, column=0, sticky="we")

            self.slmb_tr_action_vars = tk.StringVar(slmb_group)
            self.slmb_tr_action_vars.set(ACTIONS[0])

            self.slmb_tr_action = ttk.OptionMenu(slmb_group, self.slmb_tr_action_vars, ACTIONS[0], *ACTIONS, command=save_setting)
            self.slmb_tr_action.grid(row=3, column=1, sticky="we")

            self.slmb_tr_type_vars = tk.StringVar(slmb_group)
            self.slmb_tr_type_vars.set(TYPES[2])

            self.slmb_tr_type = ttk.OptionMenu(slmb_group, self.slmb_tr_type_vars, TYPES[2], *TYPES, command=save_setting)
            self.slmb_tr_type.grid(row=3, column=2, sticky="we")

        def create_om_settings(parent_frame):
            bbbtestlabel = tk.Label(parent_frame, text="Frame 2", bg="lightgreen")
            bbbtestlabel.grid(row=0, column=0, sticky="nswe")

        def save_setting(*args):
            print ("Implement function save_setting for option: " + self.slmr_tr_action_vars.get())

        # Settings for Screen layout mode
        self.screen_layout_mode = tk.Frame(parent)
        self.screen_layout_mode.grid(row=2, column=0, sticky="nswe")
        self.screen_layout_mode.rowconfigure(0, weight=1)
        self.screen_layout_mode.rowconfigure(2, weight=1)
        self.screen_layout_mode.columnconfigure(0, weight=1)
        self.screen_layout_mode.columnconfigure(2, weight=1)
        create_slm_settings(self.screen_layout_mode)

        # Settings for orientation mode
        self.orientation_mode = tk.Frame(parent)
        self.orientation_mode.grid(row=2, column=0, sticky="nswe")
        self.orientation_mode.rowconfigure(0, weight=1)
        self.orientation_mode.columnconfigure(0, weight=1)
        create_om_settings(self.orientation_mode)

        def show_frame(id):
            if id==0:
                self.screen_layout_mode.tkraise()
                self.mode = 0
            else:
                self.orientation_mode.tkraise()
                self.mode = 1

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