"""Module contains major customer classes"""
import tkinter as tk
from   tkinter import messagebox
from   tkinter import ttk as ttk
from   tkinter.ttk import Treeview
from   tkinter import OptionMenu

import db_manager as db
import login_window
import my_config

# Module Constants:
CUSTOMER_WINDOW_SIZE = "1000x1500"

PRODUCT_COLUMNS = ('Id', 'Product name', 'Price', 'In stock')
PRODUCT_COLUMNS_SIZE = (25, 150, 50, 50)

MY_ORDERS_COLUMNS = ('Id', 'Product name', 'Quantity', 'Total price')
MY_ORDERS_COLUMNS_SIZE = (25, 150, 60, 90)


class CustomerApp:
    """Main customer window."""

    def __init__(self, master):
        """Initializes main customer window."""
        self.master = master
        self.master.geometry(CUSTOMER_WINDOW_SIZE)
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

        # it contains error messages, for example not all entry are filled.
        self.error_label      = tk.Label()
        self.product_tree     = None
        self.my_orders_tree   = None
        self.location_entry   = None
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
        
        #frame.pack() 
        

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
            
            
            
        # IDK why this is not working:
        
#         records = db.get_products()
#         for record in records:
#             self.product_tree.insert('', tk.END, values=[record[0], record[1], record[2], record[3]])
            
            
        
        self.product_tree.insert('', 'end', text="1", values=(1,'Coffee',   '$2.00',50))
        self.product_tree.insert('', 'end', text="2", values=(2,'Donut',    '$1.00',29))
        self.product_tree.insert('', 'end', text="3", values=(3,'Lemonade', '$3.00',32))
        self.product_tree.insert('', 'end', text="4", values=(4,'Banana',   '$0.50',10))


        # creating entry boxes
        self.id_product_entry = tk.Entry(this_frame, width=30, bg=self.fg)
        self.quantity_entry   = tk.Entry(this_frame, width=30, bg=self.fg)
        self.location_entry   = tk.Entry(this_frame, width=30, bg=self.fg)

        self.id_product_entry.grid(row=7, column=0, sticky=tk.W, pady=(10,0))
        self.quantity_entry.grid(  row=8, column=0, sticky=tk.W)
        self.location_entry.grid(  row=9, column=0, sticky=tk.W)
        
        # creating labels
        id_product_label = tk.Label(this_frame, text='Product ID',     bg=self.bg)
        quantity_label   = tk.Label(this_frame, text='Quantity',       bg=self.bg)
        location_label   = tk.Label(this_frame, text='Order location', bg=self.bg)
       
        id_product_label.grid(row=7, column=0, sticky = tk.W, padx = 300, pady=(10,0))
        quantity_label.grid(  row=8, column=0, sticky = tk.W, padx = 300)
        location_label.grid  (row=9, column=0, sticky = tk.W, padx = 300)

        # buttons
        order_button = tk.Button(  this_frame, text='Place order', bg=self.fg, command=self.place_order,     width=16)
        details_button = tk.Button(this_frame, text='Details',     bg=self.fg, command=self.product_details, width=16)
        
        order_button.grid(  row=10, column=0, sticky = tk.W, pady=(10,0))
        details_button.grid(row=11, column=0, sticky = tk.W)
        
        #frame.pack()
        
        
    def remove_from_cart(self):
        table = self.shopping_cart_table
        selected_item = table.selection()[0]
        table.delete(selected_item)
        
    def add_to_cart(self):
        table = self.product_tree
        selected_item = table.selection()[0]
        self.shopping_cart_table.insert('','end',text='',values=(str(selected_item[1]),'1',str(selected_item[2])))
        
        
    def shopping_cart(self, this_frame, command_d):
        
        shopping_cart_label      = tk.Label(this_frame, text = 'Shopping Cart', font="{U.S. 101} 15 bold", bg=self.bg, fg=self.fg)  
        self.shopping_cart_table = ttk.Treeview(this_frame, column=("c1", "c2", "c3"), show='headings', height=5)
        
        shopping_cart_label.grid(     row=1,column=0, sticky = tk.W, pady = (10,0))
        self.shopping_cart_table.grid(row=2,column=0, sticky = tk.W)
        
        #R, C = 3, 0
        p = 0
        for (label,action) in command_d.items():
            button = tk.Button(this_frame, text = label, command = action, width=10)
            button.grid(row=3,column=0,sticky=tk.W,padx=p)
            p += 120
       
        self.shopping_cart_table.column( "# 1",    anchor=tk.CENTER, width = 150)
        self.shopping_cart_table.column( "# 2",    anchor=tk.CENTER, width = 150)
        self.shopping_cart_table.column( "# 3",    anchor=tk.CENTER, width = 150)
        self.shopping_cart_table.heading("# 1",    text="Product")
        self.shopping_cart_table.heading("# 2",    text="Quantity")
        self.shopping_cart_table.heading("# 3",    text="Price")
        self.shopping_cart_table.insert('', 'end', text="1", values=('Coffee',   '1', '$2'))
        self.shopping_cart_table.insert('', 'end', text="2", values=('Donut',    '2', '$4'))
        self.shopping_cart_table.insert('', 'end', text="3", values=('Lemonade', '1', '$3'))

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
        
      

    def product_details(self):
        """show details of selected product."""
        if self.error_label:
            self.error_label.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        if not self.id_product_entry.get():
            self.error_message("Select product.")

        elif db.is_product_id_exists(self.id_product_entry.get()):

            self.function_frame3 = tk.Frame(self.master, bg = self.bg)
            self.function_frame3.pack(side=tk.TOP)

            # creating Message instead of Label (description might be long)
            description = db.get_product(self.id_product_entry.get())[4]
            self.error_label = tk.Message(self.function_frame3, text="Description: {}".format(description), bg=self.bg, width=300)
            self.error_label.grid(row=5, column=0)
        else:
            self.error_message("Invalid product.")

    def product_selection(self, event):
        """Adds id of selected product to designated entry."""
        try:
            if self.product_tree.selection():
                record = self.product_tree.set(self.product_tree.selection())
                self.id_product_entry.delete(0, tk.END)
                self.id_product_entry.insert(tk.END, record[PRODUCT_COLUMNS[0]])

        except KeyError:
            pass

    def order_selection(self, event):
        """Shows details of selected order."""
        if self.my_orders_tree.selection():
            record = self.my_orders_tree.set(self.my_orders_tree.selection())
            record = db.return_order(record[PRODUCT_COLUMNS[0]])

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
        AccountEdit(self.master)

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


class AccountEdit:
    """Customer window for editing account."""

    def __init__(self, master):
        """Initializes editing account window."""
        self.master = master
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)
        self.master.geometry(CUSTOMER_WINDOW_SIZE)

        # label that need to be defined in __init__ so functions can check if it exist and delete it
        self.error_label = tk.Label()

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()

        # Create text box labels
        new_password_label = tk.Label(self.frame, text='New Password (optional):', bg=my_config.BACKGROUND)
        new_password_label.grid(row=1, column=0, pady=(10, 0), sticky=tk.E)
        password_label = tk.Label(self.frame, text='Password:', bg=my_config.BACKGROUND)
        password_label.grid(row=2, column=0, sticky=tk.E)
        name_label = tk.Label(self.frame, text='Name:', bg=my_config.BACKGROUND)
        name_label.grid(row=3, column=0, pady=(4, 0), sticky=tk.E)
        phone_label = tk.Label(self.frame, text='Phone:', bg=my_config.BACKGROUND)
        phone_label.grid(row=4, column=0, pady=(4, 0), sticky=tk.E)
        email_label = tk.Label(self.frame, text='Email:', bg=my_config.BACKGROUND)
        email_label.grid(row=5, column=0, pady=(4, 0), sticky=tk.E)
        cc_label = tk.Label(self.frame, text='Credit Card Number:', bg=my_config.BACKGROUND)
        cc_label.grid(row=6, column=0, pady=(4, 0), sticky=tk.E)
        exp_date_label = tk.Label(self.frame, text='Expiration Date:', bg=my_config.BACKGROUND)
        exp_date_label.grid(row=7, column=0, pady=(4, 0), sticky=tk.E)
        ccv_label = tk.Label(self.frame, text='CCV:', bg=my_config.BACKGROUND)
        ccv_label.grid(row=8, column=0, pady=(4, 0), sticky=tk.E)

        # Create Entry box
        self.new_password_entry = tk.Entry(self.frame, width=22, show='*', bg=my_config.FOREGROUND)
        self.new_password_entry.grid(row=1, column=1, pady=(10, 0))
        self.password_entry = tk.Entry(self.frame, width=22, show='*', bg=my_config.FOREGROUND)
        self.password_entry.grid(row=2, column=1)
        self.name_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.name_entry.grid(row=3, column=1)
        self.phone_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.phone_entry.grid(row=4, column=1)
        self.email_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.email_entry.grid(row=5, column=1)
        self.cc_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.cc_entry.grid(row=6, column=1)
        self.exp_date_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.exp_date_entry.grid(row=7, column=1)
        self.ccv_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.ccv_entry.grid(row=8, column=1)

        # Create Buttons
        self.change_button = tk.Button(self.frame, text='Save Changes', bg=my_config.FOREGROUND,
                                       command=self.set_change, width=16)
        self.change_button.grid(row=9, column=1, pady=(10, 0))
        self.cancel_button = tk.Button(self.frame, text='Cancel', bg=my_config.FOREGROUND,
                                       command=self.exit, width=16)
        self.cancel_button.grid(row=10, column=1)

        # getting customer info from DB
        customer_info = db.return_customer(my_config.MY_ID)
        if customer_info:
            self.name_entry.insert(tk.END, customer_info[3])
            self.phone_entry.insert(tk.END, customer_info[4])
            self.email_entry.insert(tk.END, customer_info[5])
            #self.perm_entry.insert(tk.END, customer_info[6])
            self.cc_entry.insert(tk.END, customer_info[7])
            self.exp_date_entry.insert(tk.END, customer_info[8])
            self.ccv_entry.insert(tk.END, customer_info[9])
        else:
            messagebox.showinfo("Coffee Shop", 'Error: Invalid ID')
            self.exit()

    def set_change(self):
        """Changes customer account details if all required entries are filled properly."""
        if self.error_label:
            self.error_label.destroy()

        # update password if field is not left blank
        if 0 < len(self.new_password_entry.get()) < 6:
            self.error_message('Password must be at least 6 characters')
        # update credit card if field is not left blank
        if 0 < len(self.cc_entry.get()) < 16:
            self.error_message('Credit card must be at least 16 characters')
        # update expiration date if field is not left blank
        if 0 < len(self.exp_date_entry.get()) < 5:
            self.error_message('Invalid expiration date')
            self.error_message('Credit card must be at least 16 characters')
        # update ccv if field is not left blank
        if 0 < len(self.ccv_entry.get()) < 3:
            self.error_message('Invalid CCV')

        # checking if all required entries are filled properly
        elif self.password_entry.get() != db.return_customer(my_config.MY_ID)[2]:
            self.error_message('Invalid password.')
        elif not self.name_entry.get():
            self.error_message('Name missing.')
        elif self.phone_entry.get() and not my_config.is_integer(self.phone_entry.get()):
            self.error_message("Phone number missing.")
        elif not self.email_entry.get():
            self.error_message('Email missing.')

        else:
            if self.new_password_entry:
                pw = self.new_password_entry.get()
            else:
                pw = db.return_customer(my_config.MY_ID)[2]
            if self.cc_entry:
                cc = self.cc_entry.get()
            else:
                cc = db.return_customer(my_config.MY_ID)[7]
            if self.exp_date_entry:
                exp_date = self.exp_date_entry.get()
            else:
                exp_date = db.return_customer(my_config.MY_ID)[8]  
            if self.ccv_entry:
                ccv = self.ccv_entry.get()
            else:
                ccv = db.return_customer(my_config.MY_ID)[9]  
            
            # if all entries are filled correctly

            db.edit_customer(my_config.MY_ID, pwd, self.name_entry.get(),
                             self.email_entry.get(), self.phone_entry.get(),
                             cc, exp_date, ccv)
                

            self.error_message("Account has been updated.")

    def error_message(self, name):
        """Shows passed message in designated place

        Used to clear code and make it more readable as it is
        called multiple times."""
        # deleting missing label from last add_order call if it exists
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.frame, fg=my_config.ERROR_FOREGROUND,
                                    text=name, bg=my_config.BACKGROUND)
        self.error_label.grid(row=6, column=1)

    def exit(self):
        """Runs back main customer window."""
        self.frame.destroy()
        application = CustomerApp(self.master)
        application.initialize_main_buttons()
