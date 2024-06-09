import os
import shutil
import threading
import tkinter as tk
from tkinter import Label, messagebox, filedialog, Toplevel, ttk
from PIL import Image, ImageTk
import math
from Server_Modules.server import Server
import cv2

class ServerGUI:
    def __init__(self, host, port, resolution=(640, 480)):
        self.server = Server(host, port, self.new_frame_received)
        self.window = tk.Tk()
        self.window.title("Teacher's Dashboard")
        self.resolution = resolution
        self.aspect_ratio = resolution[1] / resolution[0]
        self.student_frames = {}
        self.filename = None
        self.fullscreen_student_id = None
        self.setup_gui()

    def setup_gui(self):
        style = ttk.Style()
        style.configure('TButton', font=('Verdana', 10), padding=10, background='lightgray')
        style.configure('TLabel', font=('Verdana', 12), padding=5, background='lightgray')

        self.streams_frame = ttk.Frame(self.window, padding="30 30 30 30", style='New.TFrame')
        self.streams_frame.pack(fill=tk.BOTH, expand=True)
        self.streams_frame.columnconfigure(0, weight=1)
        self.streams_frame.rowconfigure(0, weight=1)

        logo_image = Image.open("background.png")
        logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = ttk.Label(self.streams_frame, image=logo_photo, background='lightblue')
        self.logo_label.image = logo_photo
        self.logo_label.pack(side=tk.TOP, pady=10)

        self.placeholder_label = ttk.Label(self.streams_frame, text="Awaiting student connections...", font=('Verdana', 16), background='lightblue')
        self.placeholder_label.pack(fill=tk.BOTH, expand=True)

        self.open_control_panel()

        style.configure('New.TFrame', background='lightblue')

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.bind('<Configure>', self.on_window_resize)
        self.window.resizable(True, True)
        self.start_server()

    def on_window_resize(self, event=None):
        self.update_layout()

    def open_control_panel(self):
        self.control_panel = Toplevel(self.window)
        self.control_panel.title("Actions Panel")
        self.control_panel.resizable(False, False)

        control_frame = ttk.Frame(self.control_panel, padding="10 10 10 10", style='New.TFrame')
        control_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(control_frame, text="Upload Test file", command=self.upload_file).pack(pady=5)
        ttk.Button(control_frame, text="Download All Files", command=self.download_all_files).pack(pady=5)
        ttk.Button(control_frame, text="Finish test", command=self.finish_test).pack(pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        self.filename = os.path.basename(file_path)
        print(self.filename)
        self.server.file_management_module.register_uploaded_file(file_path)  # Updated function name
        messagebox.showinfo("Upload", "File upload started.")

    def finish_test(self):
        print("finish test, sending notification for clients")
        self.server.network_module.alert_clients_test_ended()

    def download_all_files(self):
        source_directory = "C:\\client_files"
        destination_directory = f"C:/test/{self.filename}"
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        for file_name in os.listdir(source_directory):
            source_file = os.path.join(source_directory, file_name)
            destination_file = os.path.join(destination_directory, file_name)
            shutil.move(source_file, destination_file)
        messagebox.showinfo("Download Complete", f"File saved to {destination_directory}")

    def start_server(self):
        threading.Thread(target=self.server.initiate_server, daemon=True).start()
        messagebox.showinfo("Server", "Streaming server started.")

    def add_student_stream(self, student_id):
        self.placeholder_label.pack_forget()
        self.logo_label.pack_forget()
        frame_label = Label(self.streams_frame)
        frame_label.bind('<Double-Button-1>', lambda e, sid=student_id: self.toggle_fullscreen(sid))
        frame_label.grid(row=999, column=999)
        self.student_frames[student_id] = frame_label
        self.update_layout()

    def toggle_fullscreen(self, student_id):
        if self.fullscreen_student_id:
            self.fullscreen_student_id = None
            self.window.attributes('-fullscreen', False)
            self.update_layout()
        else:
            self.fullscreen_student_id = student_id
            self.maximize_student_stream(student_id)

    def maximize_student_stream(self, student_id):
        for sid, frame_label in self.student_frames.items():
            frame_label.grid_forget()

        frame_label = self.student_frames[student_id]
        frame_label.grid(row=0, column=0, sticky='nsew')
        self.streams_frame.grid_rowconfigure(0, weight=1)
        self.streams_frame.grid_columnconfigure(0, weight=1)
        self.streams_frame.update_idletasks()

        window_width = self.streams_frame.winfo_width()
        window_height = self.streams_frame.winfo_height()
        frame_label.config(width=window_width, height=window_height)

    def new_frame_received(self, client_address, frame, username):
        student_id = f"{client_address[0]}:{client_address[1]}"
        if frame is None:
            self.remove_student_stream(student_id)
            if self.fullscreen_student_id == student_id:
                self.fullscreen_student_id = None
                self.window.attributes('-fullscreen', False)
        else:
            self.window.after(0, self.update_video_display, student_id, frame, username)

    def remove_student_stream(self, student_id):
        if student_id in self.student_frames:
            frame_label = self.student_frames[student_id]
            frame_label.grid_forget()
            frame_label.destroy()
            del self.student_frames[student_id]
            self.update_layout()
        if not self.student_frames:
            self.placeholder_label.pack(fill=tk.BOTH, expand=True)

    def update_video_display(self, student_id, frame, username):
        if frame is not None and student_id in self.student_frames:
            if self.fullscreen_student_id == student_id:
                frame = cv2.resize(frame, (self.streams_frame.winfo_width(), self.streams_frame.winfo_height()))

        if frame is not None:
            cv2.putText(frame, username, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame)
            frame_photo = ImageTk.PhotoImage(image=frame_image)

            if student_id not in self.student_frames:
                self.add_student_stream(student_id)

            self.student_frames[student_id].configure(image=frame_photo)
            self.student_frames[student_id].image = frame_photo

    def update_layout(self):
        if self.fullscreen_student_id:
            self.maximize_student_stream(self.fullscreen_student_id)
            return

        num_students = len(self.student_frames)
        if num_students == 0:
            return

        window_width = self.streams_frame.winfo_width()
        window_height = self.streams_frame.winfo_height()
        cols = int(math.sqrt(num_students))
        rows = math.ceil(num_students / cols)
        frame_width = window_width // cols
        frame_height = window_height // rows

        for i, (student_id, frame_label) in enumerate(sorted(self.student_frames.items())):
            row = i // cols
            col = i % cols
            frame_label.grid(row=row, column=col, sticky='nsew')
            frame_label.config(width=frame_width, height=frame_height)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to shut down the server?"):
            self.server.shutdown_server()
            self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = ServerGUI('127.0.0.1', 5471)
    gui.run()