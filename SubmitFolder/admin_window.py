from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Treeview

import my_config
import login_window
import db_manager

db = db_manager.appDB('appDB.db')

class AdminApp:
    """Main customer window."""

    def __init__(self, master):
        self.master = master
        self.master.geometry("650x600")
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        # main frames
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)

        # it contains error messages, for example not all entry are filled.
        self.error_label = tk.Label()

        self.product_tree = None
        self.in_stock_entry = None
        self.product_name_entry = None
        self.product_price_entry = None
    
    def initialize_admin_menu(self):

        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)

        # test_label = tk.Label(self.frame, text='Admin Menu', bg=my_config.BACKGROUND)
        # test_label.grid(row=0, column=0, pady=(10, 0))

        product_name_label = tk.Label(self.frame, text='Product name:', bg=my_config.BACKGROUND)
        product_name_label.grid(row=0, column=0, sticky=tk.NE)
        product_price_label = tk.Label(self.frame, text='Product price:', bg=my_config.BACKGROUND)
        product_price_label.grid(row=1, column=0, sticky=tk.NE)
        in_stock_label = tk.Label(self.frame, text='In stock:', bg=my_config.BACKGROUND)
        in_stock_label.grid(row=2, column=0, sticky=tk.NE)

        self.product_name_entry = tk.Entry(self.frame, width=30, bg=my_config.FOREGROUND)
        self.product_name_entry.grid(row=0, column=1, sticky=tk.NE)
        self.product_price_entry = tk.Entry(self.frame, width=30, bg=my_config.FOREGROUND)
        self.product_price_entry.grid(row=1, column=1, sticky=tk.NE)
        self.in_stock_entry = tk.Entry(self.frame, width=30, bg=my_config.FOREGROUND)
        self.in_stock_entry.grid(row=2, column=1, sticky=tk.NE)

        add_button = tk.Button(self.frame, text='Add', command=self.add_product,
                               width=20, bg=my_config.FOREGROUND)
        add_button.grid(row=0, column=3, sticky=tk.SE, padx=10)
        search_button = tk.Button(self.frame, text='Search',
                                  width=20, bg=my_config.FOREGROUND)
        search_button.grid(row=1, column=3, sticky=tk.SE, padx=10)
        update_button = tk.Button(self.frame, text='Update',
                                  width=20, bg=my_config.FOREGROUND)
        update_button.grid(row=2, column=3, sticky=tk.SE, padx=10)
        clear_button = tk.Button(self.frame, text='Clear',
                                 width=20, bg=my_config.FOREGROUND)
        clear_button.grid(row=3, column=3, sticky=tk.SE, padx=10)
        delete_button = tk.Button(self.frame, text='Delete', command=self.delete_product,
                                  width=20, bg=my_config.FOREGROUND)
        delete_button.grid(row=4, column=3,sticky=tk.SE, padx=10)
        exit_button = tk.Button(self.frame, text='Log off', command=self.log_off,
                                width=20, bg=my_config.FOREGROUND)
        exit_button.grid(row=5, column=3, sticky=tk.SE, padx=10)

        list_label = tk.Label(self.frame, text='Products',
                              bg=my_config.BACKGROUND, font= 'bold')
        list_label.grid(row=7, column=0, sticky=tk.NW, padx = 30)

        self.product_tree = Treeview(self.frame, columns=('Id', 'Product name', 'Price', 'Stock'),
                                     show='headings', height=10)
        self.product_tree.grid(row=8, column=0, sticky=tk.NW, padx = 30)

        for column_name, width in zip(('Id', 'Product name', 'Price', 'Stock'), (25, 120, 50, 50)):
            self.product_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.product_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.product_tree.set)
        self.product_tree.configure(yscrollcommand=scrollbar)
        self.product_tree.bind('<ButtonRelease-1>', self.get_selected_product)

        records = db.get_all_products()
        for record in records:
            # [record[0], record[1], record[2], record[3], record[4]])
            self.product_tree.insert('', tk.END, values=record)

        self.frame.pack()

    def log_off(self):
        if self.frame:
            self.frame.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()

    def get_selected_product(self, event):
        """Inserts selected product data into entries."""
        self.clear_product_entries()
        if self.error_label:
            self.error_label.destroy()
        try:
            if self.product_tree.selection():
                record = self.product_tree.set(self.product_tree.selection())
                self.product_name_entry.insert(tk.END, record[('Id', 'Product name', 'Price', 'Stock')[1]])
                self.product_price_entry.insert(tk.END, record[('Id', 'Product name', 'Price', 'Stock')[2]])
                self.in_stock_entry.insert(tk.END, record[('Id', 'Product name', 'Price', 'Stock')[3]])

        except KeyError:
            pass

    def clear_product_entries(self):
        """Clears all entries."""
        if self.error_label:
            self.error_label.destroy()

        self.product_name_entry.delete(0, tk.END)
        self.product_price_entry.delete(0, tk.END)
        self.in_stock_entry.delete(0, tk.END)

    def add_product(self):
        if self.error_label:
            self.error_label.destroy()
        if not self.product_name_entry.get():
            print("Product name missing.")
        elif not my_config.is_float(self.product_price_entry.get()) or float(
                self.product_price_entry.get()) < 1.0:
                    print("Price must be a positive integer.")
        elif not my_config.is_integer(self.in_stock_entry.get()) or int(
                self.in_stock_entry.get()) < 0:
                    print("'In stock' value must be a non-negative integer.")

        else:
            # if product exists -> print error ELSE add
            if db.is_product_exists(self.product_name_entry.get()):
                print("'{}' Exists".format(self.product_name_entry.get()))

            else:
                db.add_product(self.product_name_entry.get(), self.product_price_entry.get(),
                               self.in_stock_entry.get())

                # showing clear new window
                self.initialize_admin_menu()

    def delete_product(self):
        if self.error_label:
            self.error_label.destroy()

        # checking if anything is selected
        if not self.product_tree.selection():
            print("product not selected")
            return

        # finding selected product
        selected_record = self.product_tree.set(self.product_tree.selection())
        record = db.get_product(selected_record[('Id', 'Product name', 'Price', 'Stock')[0]])

        # if there is record in DB with such id
        if record:
            product_info = "Product: {}\nPrice: {}\nStock: {}".format(record[1], record[2], record[3])

            # window asking to delete
            answer = messagebox.askquestion('Coffee Shop', "Delete:\n{}".format(product_info))
            if answer == 'yes':
                db.delete_product(selected_record[('Id', 'Product name', 'Price', 'Stock')[0]])
                # refreshing all
                self.initialize_admin_menu()

        # if there was no record with such id
        else:
            print("record not exists in database.")