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

    def __init__(self):
        self.create_gui()
        self.create_udp_stream()

    def create_gui(self):

        self.host = ''
        self.port = 50000

        self.pos_vector_y = 0

        # Get default audio device using PyCAW
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

        # Window and canvas initialization parameters
        self.width  = 800
        self.height = 600
        self.window = tk.Tk()
        self.window.title("Android's Sensors")

        self.create_sensor_frame()
        self.create_tabs_frame()

    def create_sensor_frame(self):
        
        # Main sensor Frame
        self.sensor_frame = tk.Frame(self.window)
        self.sensor_frame.grid(row=0, column=0, sticky="nswe")
        self.sensor_frame.rowconfigure(0, minsize=100, weight=0)

        # Gyroscope Data
        self.gyro_data_frame = tk.Frame(self.sensor_frame)
        self.gyro_data_frame.grid(row=0, column=0, sticky="we", padx=0)

        self.gyro_data_x_label = tk.Label(self.gyro_data_frame, text="Gyroscope x:")
        self.gyro_data_x_label.grid(row=0, column=0, sticky="we")
        self.gyro_x = tk.StringVar()
        self.gyro_x.set("N/A")
        self.label_gyro_x = tk.Label(self.gyro_data_frame, textvariable=self.gyro_x)
        self.label_gyro_x.grid(row=0, column=1, sticky="we", padx=25)

        self.gyro_data_y_label = tk.Label(self.gyro_data_frame, text="Gyroscope y:")
        self.gyro_data_y_label.grid(row=1, column=0, sticky="we")
        self.gyro_y = tk.StringVar()
        self.gyro_y.set("N/A")
        self.label_gyro_y = tk.Label(self.gyro_data_frame, textvariable=self.gyro_y)
        self.label_gyro_y.grid(row=1, column=1, sticky="we", padx=25)

        self.gyro_data_z_label = tk.Label(self.gyro_data_frame, text="Gyroscope z:")
        self.gyro_data_z_label.grid(row=2, column=0, sticky="we")
        self.gyro_z = tk.StringVar()
        self.gyro_z.set("N/A")
        self.label_gyro_z = tk.Label(self.gyro_data_frame, textvariable=self.gyro_z)
        self.label_gyro_z.grid(row=2, column=1, sticky="we", padx=25)

        # Positional Data
        self.position_data_frame = tk.Frame(self.sensor_frame)
        self.position_data_frame.grid(row=1, column=0, sticky="we", padx=0)

        self.position_data_x_label = tk.Label(self.position_data_frame, text="Acceleration x:")
        self.position_data_x_label.grid(row=0, column=0, sticky="we")
        self.position_x = tk.StringVar()
        self.position_x.set("N/A")
        self.label_position_x = tk.Label(self.position_data_frame, textvariable=self.position_x)
        self.label_position_x.grid(row=0, column=1, sticky="we", padx=25)

        self.position_data_y_label = tk.Label(self.position_data_frame, text="Acceleration y:")
        self.position_data_y_label.grid(row=1, column=0, sticky="we")
        self.position_y = tk.StringVar()
        self.position_y.set("N/A")
        self.label_position_y = tk.Label(self.position_data_frame, textvariable=self.position_y)
        self.label_position_y.grid(row=1, column=1, sticky="we", padx=25)

        self.position_data_z_label = tk.Label(self.position_data_frame, text="Acceleration z:")
        self.position_data_z_label.grid(row=2, column=0, sticky="we")
        self.position_z = tk.StringVar()
        self.position_z.set("N/A")
        self.label_position_z = tk.Label(self.position_data_frame, textvariable=self.position_z)
        self.label_position_z.grid(row=2, column=1, sticky="we", padx=25)

    def create_tabs_frame(self):
        # Right Frame
        self.right_frame = tk.Frame(self.window, width = self.width, height = self.height, bg="lightblue")
        self.right_frame.grid(row=0, column=1, sticky="nswe")
        self.right_frame.rowconfigure(0, minsize=400, weight=1)

        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.grid(row=0, column=0, sticky="nswe")

        self.frame1 = tk.Frame(self.notebook, width=self.width, height=self.height)
        self.create_settings(self.frame1)

        self.canvas_interaction = tk.Canvas(master = self.window, width = self.width, height = self.height, bg="grey")
        self.create_interaction_frame(self.canvas_interaction)

        self.notebook.add(self.frame1, text='Settings')
        self.notebook.add(self.canvas_interaction, text='Interaction Testing')

    def create_settings(self, parent):

        def ok(*args):
            print ("value is:" + self.variable.get())

        OPTIONS = [
        "Left Gesture",
        "Right Gesture",
        "Up Gesture",
        "Down Gesture"
        ]

        gestures = tk.Label(parent, text="GESTURES")
        gestures.grid(row=0, column=0, sticky="we")

        self.testlabel = tk.Label(parent, text="Play/Pause: ")
        self.testlabel.grid(row=1, column=0, sticky="we")

        self.variable = tk.StringVar(parent)
        self.variable.set(OPTIONS[2]) # default value

        self.w = ttk.OptionMenu(parent, self.variable, OPTIONS[2], *OPTIONS, command=ok)
        self.w.grid(row=1, column=1, sticky="we")

        self.testlabel1 = tk.Label(parent, text="Previous: ")
        self.testlabel1.grid(row=2, column=0, sticky="we")

        self.variable1 = tk.StringVar(parent)
        self.variable1.set(OPTIONS[0]) # default value

        self.w1 = ttk.OptionMenu(parent, self.variable1, OPTIONS[0], *OPTIONS, command=ok)
        self.w1.grid(row=2, column=1, sticky="we")

    def create_interaction_frame(self, parent):

        def test():
            print("It works!")

        self.photo_play  = tk.PhotoImage(file = r"./server/sources/play.png").subsample(5,5)
        self.photo_pause = tk.PhotoImage(file = r"./server/sources/pause.png").subsample(5,5)
        self.photo_next  = tk.PhotoImage(file = r"./server/sources/next.png").subsample(5,5)
        self.photo_prev  = tk.PhotoImage(file = r"./server/sources/previous.png").subsample(5,5)
        self.photo_stop  = tk.PhotoImage(file = r"./server/sources/stop.png").subsample(5,5)

        self.interaction_button = ttk.Button(parent, text= "Play", image=self.photo_play, compound=tk.LEFT, command= test)
        self.interaction_button.grid(row=0, column=0, sticky="we")

        self.interaction_button_pause = ttk.Button(parent, text= "Pause", image=self.photo_pause, compound=tk.LEFT, command= test)
        self.interaction_button_pause.grid(row=0, column=3, sticky="we")

        self.interaction_button_next = ttk.Button(parent, text= "Next", image=self.photo_next, compound=tk.LEFT, command= test)
        self.interaction_button_next.grid(row=1, column=3, sticky="we")

        self.interaction_button_prev = ttk.Button(parent, text= "Previous", image=self.photo_prev, compound=tk.LEFT, command= test)
        self.interaction_button_prev.grid(row=1, column=0, sticky="we")
        
        self.interaction_button_stop = ttk.Button(parent, text= "Stop", image=self.photo_stop, compound=tk.LEFT, command= test)
        self.interaction_button_stop.grid(row=2, column=1, sticky="we")

        self.interaction_volume = ttk.Scale(parent, from_=0, to=100, orient="vertical")
        self.interaction_volume.grid(row=3, column=1, sticky="w")

        self.interaction_seek = ttk.Scale(parent, from_=0, to=100)
        self.interaction_seek.grid(row=4, column=1, sticky="we")

    def set_udp(self, host, port):
        """
        Set the host's IP and port to the UDP socket.

        Args:
            host (int): IP adress of current machine
            port (int): Port of connected device
        """
        self.host = host
        self.port = port

    def get_data(self):
        """
        Deserialize the UDP data stream from the Android.
        There are currently two types of sensor data:
        - type `G`: Gyroscope sensor values in x,y,z
        - type `R`: Rotation vector sensor values in x,y,z
        """
        while True:
            try:
                # Buffer size 1024
                message, address = self.s.recvfrom(1024)
                message_string = message.decode("utf-8")

                if message_string:
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

        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind the IP address and port number to socket instance
        self.s.bind((self.host, self.port))

        print("Success binding: UDP server up and listening")

        self.sensor_data = threading.Thread(target=self.get_data, daemon=True)
        self.sensor_data.start()

if __name__ == "__main__":
    app = Server()
    app.set_udp('', 50000)
    app.window.mainloop()