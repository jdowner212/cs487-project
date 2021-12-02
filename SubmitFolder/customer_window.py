"""Module contains major customer classes"""
import tkinter as tk
from   tkinter import messagebox
from   tkinter import ttk as ttk
from   tkinter.ttk import Treeview
from   tkinter import OptionMenu

import db_manager
import login_window
import my_config

db = db_manager.appDB('appDB.db')

MY_ORDERS_COLUMNS = ('Id', 'Product name', 'Quantity', 'Total price')
MY_ORDERS_COLUMNS_SIZE = (25, 150, 60, 90)

class CustomerApp:
    """Main customer window."""

    def __init__(self, master):
        """Initializes main customer window."""
        self.master = master
        self.master.geometry("1000x800")
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        # main frames
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame_title = tk.Frame(self.frame, bg=my_config.BACKGROUND)
        self.frame_left  = tk.Frame(self.frame, bg=my_config.BACKGROUND)
        self.frame_right = tk.Frame(self.frame, bg=my_config.BACKGROUND)
        self.frame_top  = tk.Frame(self.frame, bg=my_config.BACKGROUND)
        self.frame_bottom = tk.Frame(self.frame, bg=my_config.BACKGROUND)
        self.function_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame2 = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame3 = tk.Frame(self.master, bg=my_config.BACKGROUND)

        self.error_label      = tk.Label()
        self.product_tree     = None
        self.my_orders_tree   = None
        self.quantity_entry   = None
        self.id_product_entry = None
        self.fg = my_config.FOREGROUND
        self.bg = my_config.BACKGROUND
        
        self.payment_option = None
        self.delivery_option = None
        self.points = 0
        self.shopping_cart_table = None

    def initialize_main_buttons(self):
        """Lists all of the customer products under menu."""  
        for thing in (self.frame,     self.function_frame, self.function_frame2, self.function_frame3, self.frame_title,
                      self.frame_top, self.frame_bottom,   self.frame_left,      self.frame_right,     self.error_label):
            if thing:
                thing.destroy()
            
        self.frame        = tk.Frame(self.master, bg=self.bg, bd=15)        
        frame_title       = tk.Frame(self.frame,  bg=self.bg)
        self.frame_left   = tk.Frame(self.frame,  bg=self.bg, bd=15)
        
        frame_title.grid(row=0, column=0, sticky=tk.N)
        self.frame_left.grid( row=1, column=0, sticky=tk.N)
        
        cart_commands = {'Check Out': self.check_out, 'Add Item': self.add_to_cart, 'Remove Item': self.remove_from_cart}
        
        self.page_options( self.frame_left)
        self.product_page( self.frame_left)
        self.shopping_cart(self.frame_left, cart_commands)
        
        self.frame.pack()

        
    def page_options(self, frame):
        page_title = tk.Label(frame, text="User Page", font="{U.S. 101} 30 bold", bg=self.bg, fg=self.fg)   
        page_title.grid(row=0, column=0, pady=10, sticky = tk.W)

        # Right Side
        points          = tk.Label( frame,  text = 'Points: 183', width = 16)
        button_account  = tk.Button(frame,  text = 'Account Info',command = self.account_edit,  width = 16)
        button_logout   = tk.Button(frame,  text = 'Log Out',     command = self.log_off,       width = 16)
        
        points.grid(         row=2,column=0,  sticky = tk.N + tk.W, padx = 500, pady=(10,0))
        button_account.grid( row=2,column=0,  sticky = tk.N + tk.W, padx = 500, pady=(50,0))
        button_logout.grid(  row=2,column=0,  sticky = tk.N + tk.W, padx = 500, pady=(90,0))
        

    def product_page(self, this_frame):

        label_tree        = tk.Label(    this_frame, text = 'Products',  font="{U.S. 101} 15 bold", bg=self.bg, fg=self.fg)  
        self.product_tree = ttk.Treeview(this_frame, column=("c1", "c2", "c3", "c4"), show='headings', height=10)
        
        label_tree.grid(       row=5,column=0, sticky = tk.W, pady=(30,0))
        self.product_tree.grid(row=6,column=0, sticky = tk.W)
        
        for (k,v) in [('#1',"ID"),('#2',"Product"),('#3',"Price"),('#4',"# in Stock")]:
            num = 100
            if v == "Product":
                num = 150
            self.product_tree.column( k, anchor=tk.CENTER, width=num)
            self.product_tree.heading(k, text=v)
        
        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.product_tree.set)
        self.product_tree.configure(yscrollcommand=scrollbar)
        self.product_tree.bind('<ButtonRelease-1>', self.product_selection)

        records = db.get_all_products()
        for record in records:
            self.product_tree.insert('', tk.END, values=[record[0], record[1], record[2], record[3]])

        # creating entry boxes
        self.id_product_entry = tk.Entry(this_frame, width=30, bg=self.fg, state="readonly")
        self.quantity_entry   = tk.Entry(this_frame, width=30, bg=self.fg)

        self.id_product_entry.grid(row=7, column=0, sticky=tk.W, pady=(10,0))
        self.quantity_entry.grid(  row=8, column=0, sticky=tk.W)
        
        # creating labels
        id_product_label = tk.Label(this_frame, text='Product ID',     bg=self.bg)
        quantity_label   = tk.Label(this_frame, text='Quantity',       bg=self.bg)
       
        id_product_label.grid(row=7, column=0, sticky = tk.W, padx = 300, pady=(10,0))
        quantity_label.grid(  row=8, column=0, sticky = tk.W, padx = 300)

        order_button = tk.Button(  this_frame, text='Place order', bg=self.fg, command=self.place_order,     width=16)
        
        order_button.grid(  row=10, column=0, sticky = tk.W, pady=(10,0))
        
        
        
    def remove_from_cart(self):
        
        try:
            if self.shopping_cart_table.selection():
                item = self.shopping_cart_table.set(self.shopping_cart_table.selection())
                db.remove_order(item[('c1', 'c2', 'c3', 'c4')[0]])
                # db.add_order(my_config.USER_ID, record[('c1', 'c2', 'c3', 'c4')[0]], 1)

        except KeyError:
            pass
        
        self.initialize_main_buttons()


    def add_to_cart(self):
        try:
            if self.product_tree.selection():
                record = self.product_tree.set(self.product_tree.selection())
                if db.get_product(record[('c1', 'c2', 'c3', 'c4')[0]])[3] < 1:
                    messagebox.showinfo("Coffee Shop", 'Out of stock')
                else:
                    db.add_order(my_config.USER_ID, record[('c1', 'c2', 'c3', 'c4')[0]], 1)

        except KeyError:
            pass

        self.initialize_main_buttons()
        
        
    def shopping_cart(self, this_frame, command_d):
        
        shopping_cart_label      = tk.Label(this_frame, text = 'Shopping Cart', font="{U.S. 101} 15 bold", bg=self.bg, fg=self.fg)  
        self.shopping_cart_table = ttk.Treeview(this_frame, column=("c1", "c2", "c3", "c4"), show='headings', height=5)
        
        shopping_cart_label.grid(     row=1,column=0, sticky = tk.W, pady = (10,0))
        self.shopping_cart_table.grid(row=2,column=0, sticky = tk.W)
        
        #R, C = 3, 0
        p = 0
        for (label,action) in command_d.items():
            button = tk.Button(this_frame, text = label, command = action, width=10)
            button.grid(row=3,column=0,sticky=tk.W,padx=p)
            p += 120
       
        self.shopping_cart_table.column( "# 1",    anchor=tk.CENTER, width = 70)
        self.shopping_cart_table.column( "# 2",    anchor=tk.CENTER, width = 150)
        self.shopping_cart_table.column( "# 3",    anchor=tk.CENTER, width = 80)
        self.shopping_cart_table.column( "# 4",    anchor=tk.CENTER, width = 80)
        self.shopping_cart_table.heading("# 1",    text="Order")
        self.shopping_cart_table.heading("# 2",    text="Product")
        self.shopping_cart_table.heading("# 3",    text="Quantity")
        self.shopping_cart_table.heading("# 4",    text="Price")
        # self.shopping_cart_table.insert('', 'end', text="1", values=('Coffee',   '1', '$2'))
        # self.shopping_cart_table.insert('', 'end', text="2", values=('Donut',    '2', '$4'))
        # self.shopping_cart_table.insert('', 'end', text="3", values=('Lemonade', '1', '$3'))

        cart = db.get_all_orders_customer(my_config.USER_ID)
        items_in_cart = []
        for item in cart:
            items_in_cart.append([item[0], db.get_product_name(item[2])[0], 1, db.get_product_price(item[2])[0]])
        
        for item in items_in_cart:
            self.shopping_cart_table.insert('', tk.END, values=item)

        #frame.pack() 


    def place_order(self):
        """Place new order, if all required entries are filled."""
        if self.error_label:
            self.error_label.destroy()
        # checking if all required entries are filled properly
        if not self.id_product_entry.get():
            self.error_message("Product ID missing.")
        elif not my_config.is_integer(self.quantity_entry.get()) or int(self.quantity_entry.get()) < 1:
            self.error_message("Quantity must be a positive integer.")
        elif not self.location_entry.get():
            self.error_message("Location missing.")
        # checking if customer and product exists
        elif not db.is_customer_id_exist(my_config.MY_ID) or not db.is_product_id_exists(
                self.id_product_entry.get()):
            self.error_message("Invalid Product ID or Customer ID.")
        # function itself check if there is enough products, and count total price (quantity*price)
        elif db.add_order(my_config.MY_ID, self.id_product_entry.get(), self.quantity_entry.get(),
                          self.location_entry.get()):
            messagebox.showinfo("Coffee Shop", 'Successfully added.')
            self.page_options()
        else:
            self.error_message("Product out of stock.")
            
    def check_out(self):
        """Place new order, if all required entries are filled."""
        if self.frame:
            self.frame.destroy()
        if self.frame_title:
            self.frame_title.destroy()
        if self.frame_left:
            self.frame_left.destroy()
        if self.frame_right:
            self.frame_right.destroy()
            
        self.frame  = tk.Frame(self.master, bg=self.bg, bd=15)
        self.frame_title = tk.Frame(self.frame,  bg=self.bg, bd=15)
        self.frame_left  = tk.Frame(self.frame,  bg=self.bg, bd=15)
        self.frame_right = tk.Frame(self.frame,  bg=self.bg, bd=15)
        
        self.frame_title.grid(row=0, column=0)
        self.frame_left.grid( row=1, column=0)
        self.frame_right.grid(row=1, column=1)

        page_title = tk.Label(self.frame_title, text="Checkout Page", font="{U.S. 101} 30 bold", bg=self.bg, fg=self.fg)   
        page_title.grid(row=0, column=0, pady=10, sticky = tk.W)

        cart_commands = {'Remove Item': self.remove_from_cart,
                         'Place Order': self.place_order,
                         'Go Back':     self.initialize_main_buttons}
        self.shopping_cart(self.frame_left, cart_commands)
        
        
        options_payment  = ["<select option>","Credit Card","Points","Cash (Pick-up only)"]
        options_delivery = ["<select option>","Pick-up","Delivery"]
        
        
        variable_payment  = tk.StringVar(self.frame_right)
        variable_delivery = tk.StringVar(self.frame_right)
        variable_payment.set( options_payment [0])
        variable_delivery.set(options_delivery[0])
        
        menu_payment  = tk.OptionMenu(self.frame_right, variable_payment,  *options_payment)
        menu_delivery = tk.OptionMenu(self.frame_right, variable_delivery, *options_delivery)
        menu_payment.config( width=30, height=3,bg=self.bg,fg=self.fg)
        menu_delivery.config(width=30, height=2,bg=self.bg, fg=self.fg)
        
        
        points_avail_label = tk.Label(self.frame_right, text = 'Points available: ',            bg=self.bg,fg=self.fg)
        points_avail       = tk.Label(self.frame_right,text = str(self.points),                 bg=self.bg,fg=self.fg, width=20)
        points_used        = tk.Label(self.frame_right, text = 'Points used toward purchase: ', bg=self.bg,fg=self.fg)
        points_used_entry  = tk.Entry(self.frame_right, bg=self.bg, width=20, show='*')


        points_avail_label.grid(row=0,column=0,ipadx=5,sticky=tk.E)
        points_avail.grid(      row=0,column=1,ipadx=5,sticky=tk.E)
        points_used.grid(       row=1,column=0,ipadx=5,sticky=tk.E)
        points_used_entry.grid( row=1,column=1,ipadx=5,sticky=tk.E)
        menu_payment.grid(      row=2,column=0,ipadx=5,sticky=tk.E)
        menu_delivery.grid(     row=3,column=0,ipadx=5,sticky=tk.E)

        def ok():
            self.payment_option = variable_payment.get()
            self.delivery_option = variable_delivery.get()
            ok = tk.Label(self.frame_right,text = "Choices saved.")
            ok.grid(row=5,column=0,ipadx=5,ipady=5,sticky=tk.E)

        button = tk.Button(self.frame_right, text="OK", command=ok)
        button.grid(row=4,column=0,ipadx=5,ipady=5,sticky=tk.E)
        
        self.frame.pack()
        

    def product_selection(self, event):
        """Adds id of selected product to designated entry."""
        self.clear_entries()
        if self.error_label:
            self.error_label.destroy()
        try:
            if self.product_tree.selection():
                record = self.product_tree.set(self.product_tree.selection())
                self.id_product_entry.insert(tk.END, record[('c1', 'c2', 'c3', 'c4')[0]])

        except KeyError:
            pass

    def order_selection(self, event):
        """Shows details of selected order."""
        if self.my_orders_tree.selection():
            record = self.my_orders_tree.set(self.my_orders_tree.selection())
            record = db.return_order(record[('Id', 'Product name', 'Price', 'In stock')[0]])

            if self.function_frame2:
                self.function_frame2.destroy()

            self.function_frame2 = tk.Frame(self.master, bg=self.bg)
            self.function_frame2.pack(side=tk.TOP)

            # creating Message instead of Label (might be long)
            order_info = ("quantity: \t{}\ntotal_price: \t{}\npayment_status: \t{}\n"
                          "send_status: \t{}\noder_date: \t{}\nlocation: \t{}\n"
                          ).format(record[3], record[4], record[5], record[6], record[7], record[8])

            self.error_label = tk.Message(self.function_frame2, text=order_info,
                                          bg=self.bg, width=300)
            self.error_label.grid(row=0, column=0)

    def account_edit(self):
        """Runs new window for editing account."""
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()
        # AccountEdit(self.master)

    def my_orders(self):
        """Creates menu with list of user orders."""
        self.initialize_main_buttons()

        self.function_frame = tk.Frame(self.master, bg=self.bg)
        self.function_frame.pack()

        # creating listbox for customers
        list_label = tk.Label(self.function_frame, text='My Orders:', width=100, bg=my_config.BACKGROUND)
        list_label.grid(row=0, column=0, pady=(10, 0))

        # creating treeview for customers
        self.my_orders_tree = Treeview(self.function_frame, columns=MY_ORDERS_COLUMNS,
                                       show='headings', height=10)
        self.my_orders_tree.grid(row=1, column=0)

        for column_name, width in zip(MY_ORDERS_COLUMNS, MY_ORDERS_COLUMNS_SIZE):
            self.my_orders_tree.column( column_name, width=width, anchor=tk.CENTER)
            self.my_orders_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.function_frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.my_orders_tree.set)
        self.my_orders_tree.configure(yscrollcommand=scrollbar)
        self.my_orders_tree.bind('<ButtonRelease-1>', self.order_selection)

        # adding records from DB to treeview
        records = db.orders_product_info(my_config.MY_ID)
        for record in records:
            self.my_orders_tree.insert('', tk.END, values=[record[0], record[1], record[2], record[3]])

    def error_message(self, name):
        """Shows passed message in designated place

        Used to clear code and make it more readable as it is
        called multiple times."""
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.function_frame2, text=name, bg=my_config.BACKGROUND,
                                    fg=my_config.ERROR_FOREGROUND)
        self.error_label.grid(row=3, column=1)

    def log_off(self):
        """Returns User to log-in window."""
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()

    def clear_entries(self):
        if self.error_label:
            self.error_label.destroy()
        
        self.quantity_entry.delete(0, tk.END)
        self.id_product_entry.delete(0, tk.END)
        