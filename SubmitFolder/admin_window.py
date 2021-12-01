from tkinter import messagebox
import tkinter as tk
from tkinter.constants import COMMAND
from tkinter.ttk import Treeview

import my_config
import login_window
import db_manager

db = db_manager.appDB('appDB.db')

class AdminApp:
    """Main customer window."""

    def __init__(self, master):
        self.master = master
        self.master.geometry("750x500")
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)

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
        product_name_label.grid(row=1, column=1)
        product_price_label = tk.Label(self.frame, text='Product price:', bg=my_config.BACKGROUND)
        product_price_label.grid(row=2, column=1)
        in_stock_label = tk.Label(self.frame, text='In stock:', bg=my_config.BACKGROUND)
        in_stock_label.grid(row=3, column=1)

        # entries
        self.product_name_entry = tk.Entry(self.frame, width=20, bg=my_config.FOREGROUND)
        self.product_name_entry.grid(row=1, column=2)
        self.product_price_entry = tk.Entry(self.frame, width=20, bg=my_config.FOREGROUND)
        self.product_price_entry.grid(row=2, column=2)
        self.in_stock_entry = tk.Entry(self.frame, width=20, bg=my_config.FOREGROUND)
        self.in_stock_entry.grid(row=3, column=2)

        # buttons
        add_button = tk.Button(self.frame, text='Add', command=self.add_product,
                               width=20, bg=my_config.FOREGROUND)
        add_button.grid(row=1, column=3, padx=10)
        search_button = tk.Button(self.frame, text='Search',
                                  width=20, bg=my_config.FOREGROUND)
        search_button.grid(row=2, column=3,  padx=10)
        update_button = tk.Button(self.frame, text='Update', command=self.update_product,
                                  width=20, bg=my_config.FOREGROUND)
        update_button.grid(row=3, column=3,  padx=10)
        clear_button = tk.Button(self.frame, text='Clear',
                                 width=20, bg=my_config.FOREGROUND, command=self.clear_entries)
        clear_button.grid(row=4, column=3,  padx=10)
        delete_button = tk.Button(self.frame, text='Delete', command=self.delete_product,
                                  width=20, bg=my_config.FOREGROUND)
        delete_button.grid(row=5, column=3, padx=10)
        exit_button = tk.Button(self.frame, text='Log off', command=self.log_off,
                                width=20, bg=my_config.FOREGROUND)
        exit_button.grid(row=6, column=3,  padx=10)

        list_label = tk.Label(self.frame, text='Products',
                              bg=my_config.BACKGROUND, font= 'bold')
        list_label.grid(row=0, column=0, sticky=tk.NW, padx = 10)

        self.product_tree = Treeview(self.frame, columns=('Id', 'Product name', 'Price', 'Stock'),
                                     show='headings', height=10)
        self.product_tree.grid(row=1, column=0, sticky=tk.W, padx=10, rowspan=6)

        for column_name, width in zip(('Id', 'Product name', 'Price', 'Stock'), (25, 120, 50, 50)):
            self.product_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.product_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.product_tree.set)
        self.product_tree.configure(yscrollcommand=scrollbar)
        self.product_tree.bind('<ButtonRelease-1>', self.get_selected_product)

        records = db.get_all_products()
        for record in records:
            # [record[0], record[1], record[2], record[3]])
            self.product_tree.insert('', tk.END, values=record)

        self.frame.pack()

    def log_off(self):
        if self.frame:
            self.frame.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()

    def get_selected_product(self, event):
        """Inserts selected product data into entries."""
        self.clear_entries()
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

    def add_product(self):
        if self.error_label:
            self.error_label.destroy()
        if not self.product_name_entry.get():
            messagebox.showwarning(title="Coffee Shop", message="Product name missing")
        elif not my_config.is_float(self.product_price_entry.get()) or float(
                self.product_price_entry.get()) < 1.0:
                    messagebox.showwarning(title="Coffee Shop", message="Price must be positive")
        elif not my_config.is_integer(self.in_stock_entry.get()) or int(
                self.in_stock_entry.get()) < 0:
                    messagebox.showwarning(title="Coffee Shop", message="Stock value must be positive")

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


    def clear_entries(self):
        """Clears all entries."""
        if self.error_label:
            self.error_label.destroy()

        self.product_name_entry.delete(0, tk.END)
        self.product_price_entry.delete(0, tk.END)
        self.in_stock_entry.delete(0, tk.END)

    def update_product(self):
        """Updates product, if all required entries are filled properly."""
        try:
            if self.error_label:
                self.error_label.destroy()

            # checking if any record from LISTBOX is selected
            if not self.product_tree.selection():
                messagebox.showwarning(title="Coffee Shop", message="Select a product")
                return

            # checking if all required entries are filled correctly
            if not self.product_name_entry.get():
                messagebox.showwarning(title="Coffee Shop", message="Product name missing")
            elif not my_config.is_float(self.product_price_entry.get()) or float(
                    self.product_price_entry.get()) < 0.0:
                messagebox.showwarning(title="Coffee Shop", message="Wrong price format")
            elif not my_config.is_integer(self.in_stock_entry.get()) or int(
                    self.in_stock_entry.get()) < 0:
                messagebox.showwarning(title="Coffee Shop", message="Number of products must be an interger")

            else:
                # everything is filled updating
                record = self.product_tree.set(self.product_tree.selection())
                db.update_product(record[('Id', 'Product name', 'Price', 'Stock')[0]], self.product_name_entry.get(),
                                  self.product_price_entry.get(),
                                  self.in_stock_entry.get())

                # refresh all
                self.initialize_admin_menu()
        except KeyError:
            pass