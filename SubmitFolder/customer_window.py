from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Treeview

import login_window
import my_config

CUSTOMER_WINDOW_SIZE = "650x600"

class CustomerApp:
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
    
    def initialize_main_menu(self):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)

        test_label = tk.Label(self.frame, text='Customer Menu', bg=my_config.BACKGROUND)
        test_label.grid(row=0, column=0, pady=(10, 0))

        self.frame.pack()