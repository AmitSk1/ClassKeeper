"""
Client GUI
Amit Skarbin

A GUI for the student client to enter their name and start streaming.
"""
import os
import sys
from tkinter import Tk, StringVar, messagebox, filedialog, ttk
from Client_Modules.client import Client

class ClientGUI:
    def __init__(self, host, port):
        self.start_stream_button = None
        self.client = Client(host, port)
        self.window = Tk()
        self.window.title("Student GUI for Academic Interface")
        self.username_var = StringVar()
        self.stream_started = False
        self.setup_gui()

    def setup_gui(self):
        style = ttk.Style()
        style.configure('TButton', font=('Verdana', 10), padding=10, background='lightgray')
        style.configure('TLabel', font=('Verdana', 12), padding=5, background='lightgray')
        style.configure('TEntry', font=('Verdana', 12), padding=5)

        main_frame = ttk.Frame(self.window, padding="20 20 20 20", style='New.TFrame')
        main_frame.grid(row=0, column=0, sticky="EWNS")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky='W')
        name_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        name_entry.grid(row=1, column=1, sticky='EW')

        self.start_stream_button = ttk.Button(main_frame, text="Begin Test", command=self.start_streaming)
        self.start_stream_button.grid(row=2, column=0, sticky='EW', columnspan=2)

        ttk.Button(main_frame, text="End Test", command=self.finish_test).grid(row=3, column=0, sticky='EW')
        ttk.Button(main_frame, text="Send Test", command=self.select_file_to_upload).grid(row=3, column=1, sticky='EW')
        ttk.Button(main_frame, text="Receive Test", command=self.download_file).grid(row=4, column=0, columnspan=2, sticky='EW')

        self.window.resizable(True, True)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        style.configure('New.TFrame', background='lightblue')
        self.window.resizable(True, True)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def is_english_name(self, name):
        for char in name:
            if not char.isalpha() or not char.isascii():
                return False
        return True

    def start_streaming(self):
        username = self.username_var.get()
        if not username:
            messagebox.showerror("Error", "Please enter your name.")
        elif not self.is_english_name(username):
            messagebox.showerror("Error", "Please enter an English name.")
        else:
            self.client.begin_video_stream(username)
            self.stream_started = True
            self.start_stream_button.configure(text="Streaming...", state='disabled', style='Streaming.TButton')
            messagebox.showinfo("Streaming", "You are now streaming. Good luck!")
            self.check_test_over_flag()

    def check_test_over_flag(self):
        if self.client.test_over:
            self.handle_test_over()
        else:
            self.window.after(1000, self.check_test_over_flag)

    def handle_file_upload(self):
        messagebox.showinfo("Upload file", "The teacher uploaded file")

    def handle_test_over(self):
        messagebox.showinfo("TEST OVER", "The test will be over in one minute, submit the test")
        self.window.after(60000, self.stop_test)

    def stop_test(self):
        self.client.terminate_client()
        self.window.destroy()
        messagebox.showinfo("Test Over", "The test is over. The application will now close.")
        sys.exit()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to exit?"):
            self.window.destroy()
            self.client.terminate_client()
            sys.exit()

    def finish_test(self):
        if messagebox.askokcancel("Quit", "Do you want to finish the test"):
            self.window.destroy()
            self.client.terminate_client()
            sys.exit()

    def check_stream_started(self):
        if not self.stream_started:
            messagebox.showerror("Error", "Please enter the name and then start the stream.")
            return False
        return True

    def select_file_to_upload(self):
        if self.check_stream_started():
            username = self.username_var.get()
            file_path = filedialog.askopenfilename()
            if file_path:
                self.client.file_management_module.transmit_file_to_server(file_path, username)
                messagebox.showinfo("Upload", "File successfully uploaded to the teacher.")

    def download_file(self):
        if self.check_stream_started():
            directory = "C:/classKeeper"
            if not os.path.exists(directory):
                os.makedirs(directory)

            self.client.file_management_module.fetch_latest_file()
            check = self.client.file_management_module.verify_file_upload()
            if not check:
                messagebox.showinfo("Download", "No file available for download.")
            else:
                self.client.file_management_module.download_file_from_server(directory)
                messagebox.showinfo("Download Complete", f"File saved to {directory}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = ClientGUI('127.0.0.1', 5471)
    gui.run()