from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Treeview

import my_config
import login_window

CUSTOMER_WINDOW_SIZE = "650x600"

class AdminApp:
    """Main customer window."""

    def __init__(self, master):
        self.master = master
        self.master.geometry(CUSTOMER_WINDOW_SIZE)
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        # main frames
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)

        # it contains error messages, for example not all entry are filled.
        self.error_label = tk.Label()
    
    def initialize_admin_menu(self):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)

        test_label = tk.Label(self.frame, text='Admin Menu', bg=my_config.BACKGROUND)
        test_label.grid(row=0, column=0, pady=(10, 0))

        logoff_button = tk.Button(self.frame, text='Log off', bg=my_config.FOREGROUND,
                                  command=self.log_off, width=16)
        logoff_button.grid(row=3, column=0, pady=(0, 3))

        self.frame.pack()

    def log_off(self):
        if self.frame:
            self.frame.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()