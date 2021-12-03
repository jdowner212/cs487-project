"""Module contains major customer classes"""
import tkinter as tk
from   tkinter import messagebox
from   tkinter import ttk as ttk
from   tkinter.ttk import Treeview
from   tkinter import OptionMenu
import numpy as np

import db_manager
import login_window
#from login_window import LoginWindow as LW
import my_config

db = db_manager.appDB('appDB.db')

PRODUCT_COLUMNS = ('Id', 'Product name', 'Price', 'In stock')
PRODUCT_COLUMNS_SIZE = (25, 150, 50, 50)

MY_ORDERS_COLUMNS = ('Id', 'Product name')
MY_ORDERS_COLUMNS_SIZE = (50,50)


CUSTOMER_WINDOW_SIZE = '1200x1000'

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

        # it contains error messages, for example not all entry are filled.
        self.error_label      = tk.Label()

        self.shopping_cart_table = None
        self.product_tree     = None
        self.my_orders_tree   = None
        self.quantity_entry   = None
        self.id_product_entry = None
        self.fg = my_config.FOREGROUND
        self.bg = my_config.BACKGROUND
        self.points = 100


    def destroy_all(self):
        for thing in self.frame, self.frame_title, self.frame_left, self.frame_right, self.error_label:
            if thing:
                thing.destroy()
    def destroy_error(self):
        if self.error:
            self.error.destroy()
    
    def initialize_main_buttons(self):
        self.destroy_all()
            
        self.frame        = tk.Frame(self.master, bg=self.bg, bd=15)        
        frame_title       = tk.Frame(self.frame,  bg=self.bg)
        self.frame_left   = tk.Frame(self.frame,  bg=self.bg, bd=15)
        self.frame_right  = tk.Frame(self.frame,  bg=self.bg, bd=15)
        frame_bottom      = tk.Frame(self.frame,  bg=self.bg, bd=15)

        frame_title.grid(     row=0, column=0, sticky=tk.N+tk.W)
        self.frame_left.grid( row=1, column=0, sticky=tk.N+tk.W)
        self.frame_right.grid(row=1, column=1, sticky=tk.N)   
        frame_bottom.grid(row=2, column=0)
        
        page_title  = tk.Label(frame_title, text='User Page', font="{U.S. 101} 30 bold", bg=self.bg, fg=self.fg) 
        page_title.grid( row=0, column=0, sticky=tk.W,      pady=10)
        cart_commands = {'Remove from cart': self.remove_from_cart}
        
        self.shopping_cart(self.frame_left, cart_commands)
        self.product_page( self.frame_left)
        self.page_options( self.frame_right)

        
        refresh_button = tk.Button(frame_bottom, text='Refresh Page', bg=self.fg, command=self.initialize_main_buttons, width=20)
        refresh_button.grid(row=0, column=0, pady=(20,0))
        
        self.frame.pack()

        
    def page_options(self, frame):
        inner_frame = tk.Frame(frame, bg=self.bg, bd=15)
        inner_frame.grid(row=1, column=0, sticky=tk.N+tk.W)

        # Right Side
        button_edit      = tk.Button(inner_frame,  text = 'Edit Account', command = self.account_edit,  width = 16)
        button_orders    = tk.Button(inner_frame,  text = 'Order History',command = self.my_orders,     width = 16)
        button_check_out = tk.Button(inner_frame,  text = 'Check Out',    command = self.check_out,     width = 16)
        button_logout    = tk.Button(inner_frame,  text = 'Log Out',      command = self.log_off,       width = 16)
        button_account   = tk.Button(inner_frame,  text = 'Account Info', command = self.show_account,  width = 16)


        button_edit.      grid(row=0,column=0, sticky=tk.N+tk.W,pady=(20,0))
        button_orders.    grid(row=1,column=0, sticky=tk.N+tk.W)
        button_check_out. grid(row=2,column=0, sticky=tk.N+tk.W)
        button_logout.    grid(row=4,column=0, sticky=tk.N+tk.W)
        button_account.   grid(row=3,column=0, sticky=tk.N+tk.W)



    def product_page(self, this_frame):

        label_tree        = tk.Label(    this_frame, text = 'Products',  font="{U.S. 101} 15 bold", bg=self.bg, fg=self.fg)  
        self.product_tree = ttk.Treeview(this_frame, column=("c1", "c2", "c3", "c4"), show='headings', height=10)
        
        label_tree.        grid(row=3,column=0, sticky = tk.W, pady=(30,0))
        self.product_tree. grid(row=4,column=0, sticky = tk.W)
        
        for (k,v) in [('#1',"ID"),('#2',"Product"),('#3',"Price"),('#4',"# in Stock")]:
            num = 100
            if v == "Product":
                num = 150
            self.product_tree.column( k, anchor=tk.CENTER, width=num)
            self.product_tree.heading(k, text=v)
        
        records = db.get_all_products()
        for record in records:
            self.product_tree.insert('', tk.END, values=[record[0], record[1], record[2], record[3]])

        # creating labels
        id_product_label = tk.Label(this_frame, text='Product ID',     bg=self.bg)
        quantity_label   = tk.Label(this_frame, text='Quantity',       bg=self.bg)
       
        id_product_label.grid(row=5, column=0, sticky = tk.W, pady=(10,0))
        quantity_label.grid(  row=6, column=0, sticky = tk.W, )
        # creating entry boxes
        p = self.id_product_entry = tk.Entry(this_frame, width=30, bg=self.fg)
        q = self.quantity_entry   = tk.Entry(this_frame, width=30, bg=self.fg)

        self.id_product_entry.grid(row=5, column=0, padx=100, pady=(10,0))
        self.quantity_entry.grid(  row=6, column=0, padx=100)
        # creating buttons
                
        order_button = tk.Button(this_frame, text='Add to cart', command=self.add_to_cart, bg=self.fg, width=15)
        order_button.grid(row=10, column=0, sticky = tk.W, pady=(10,0))

    def show_account(self):
        
        self.destroy_all()
            
        self.frame        = tk.Frame(self.master, bg=self.bg, bd=15)        
        frame_title       = tk.Frame(self.frame,  bg=self.bg)
        frame_middle      = tk.Frame(self.frame,  bg=self.bg)
        frame_bottom      = tk.Frame(self.frame,  bg=self.bg, bd=15)

        frame_title. grid(row=0, column=0, sticky=tk.N+tk.W)
        frame_middle.grid(row=1, column=0)
        frame_bottom.grid(row=2, column=0)
        
        page_title = tk.Label(frame_title, text='Account Information', font="{U.S. 101} 30 bold", bg=self.bg, fg=self.fg) 
        page_title.grid( row=0, column=0, sticky=tk.W,      pady=10)
        
        info = db.get_one_user(my_config.USER_ID) # info[5] is the permsion id (Int type)
        # 0 - customer, 1 - employee, 2 - manager
        if info[5] == 0:
            user_type = 'Customer'
        elif info[5] == 1:
            user_type = 'Employee'
        elif info[5] == 2:
            user_type = 'Manager'
        else:
            user_type = 'Error'

        name = info[3]
        email = info[1]
        phone = info[4]
        cust_id = info[0]
        
        label_name      = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = 'Name: ', font="{U.S. 101} 15 bold")
        label_email     = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = 'Email: ', font="{U.S. 101} 15 bold")
        label_phone     = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = 'Phone: ', font="{U.S. 101} 15 bold")
        label_user_type = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = 'User Type: ', font="{U.S. 101} 15 bold")
        label_id        = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = 'User Id: ', font="{U.S. 101} 15 bold")

        label_name      .grid(row=0,column=0, sticky=tk.E, pady=(20,0))        
        label_email     .grid(row=1,column=0, sticky=tk.E)
        label_phone     .grid(row=2,column=0, sticky=tk.E)
        label_user_type .grid(row=3,column=0, sticky=tk.E)
        label_id        .grid(row=5,column=0, sticky=tk.E)
        
        label_name_actual      = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = name, font="{U.S. 101} 15 bold")
        label_email_actual     = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = email, font="{U.S. 101} 15 bold")
        label_phone_actual     = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = phone, font="{U.S. 101} 15 bold")
        label_user_type_actual = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = user_type, font="{U.S. 101} 15 bold")
        label_id_actual        = tk.Label(frame_middle,bg=self.bg,fg=self.fg,text = cust_id, font="{U.S. 101} 15 bold")

        label_name_actual      .grid(row=0,column=1, sticky=tk.W,pady=(20,0))        
        label_email_actual     .grid(row=1,column=1, sticky=tk.W)
        label_phone_actual     .grid(row=2,column=1, sticky=tk.W)
        label_user_type_actual .grid(row=3,column=1, sticky=tk.W)
        label_id_actual        .grid(row=5,column=1, sticky=tk.W)

        button_go_back = tk.Button(frame_bottom,text='Go Back',command=self.initialize_main_buttons)
        button_go_back.grid(row=0,column=0,sticky=tk.W,pady=(20,0))

        self.frame.pack()


        
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
                # print(record)
                if db.get_product(record[('c1', 'c2', 'c3', 'c4')[0]])[3] < 1:
                    messagebox.showinfo("Coffee Shop", 'Out of stock')
                else:
                    db.add_order(my_config.USER_ID, record[('c1', 'c2', 'c3', 'c4')[0]], 1)

        except KeyError:
            pass

        self.initialize_main_buttons()
        
    def shopping_cart(self, this_frame, command_d):
        label_SC      = tk.Label(    this_frame, text = 'Shopping Cart', font="{U.S. 101} 15 bold", bg=self.bg, fg=self.fg) 
        self.shopping_cart_table = ttk.Treeview(this_frame, column=("c1", "c2", "c3", "c4"), show='headings', height=5)
        
        label_SC.grid(     row=0,column=0, sticky = tk.W, pady = (10,0))
        self.shopping_cart_table.grid(row=1,column=0, sticky = tk.W)
        
        R=2
        for (label,action) in command_d.items():
            button = tk.Button(this_frame, text = label, command = action, width=15)
            p = (10,0) if R == 2 else (0,0)
            button.grid(row=R,column=0,sticky=tk.W,pady=p)
            R+=1
       
        self.shopping_cart_table.column( "# 1",    anchor=tk.CENTER, width = 70)
        self.shopping_cart_table.column( "# 2",    anchor=tk.CENTER, width = 150)
        self.shopping_cart_table.column( "# 3",    anchor=tk.CENTER, width = 80)
        self.shopping_cart_table.column( "# 4",    anchor=tk.CENTER, width = 80)
        self.shopping_cart_table.heading("# 1",    text="Order")
        self.shopping_cart_table.heading("# 2",    text="Product")
        self.shopping_cart_table.heading("# 3",    text="Quantity")
        self.shopping_cart_table.heading("# 4",    text="Price")

                
        cart = db.get_all_orders_customer(my_config.USER_ID)
        items_in_cart=[]
        for item in cart:
            items_in_cart.append([item[0], db.get_product_name(item[2])[0], 1, db.get_product_price(item[2])[0]])
        for item in items_in_cart:
            self.shopping_cart_table.insert('', tk.END, values=item)

        #frame.pack() 


    def place_order(self):
#         """Place new order, if all required entries are filled."""
        
        selected = self.shopping_cart_table.selection()
        try:
#            self.id_product.entry = selected[
            p, q = selected[1,2]
                
#             q = self.chosen_q.get()
#             p = self.chosen_p.get()


            if self.error_label:
                self.error_label.destroy()
            #if not self.id_product_entry.get():
            if not p:
                self.error_message("Product ID missing.")
            elif not my_config.is_integer(q) or int(q) < 1:
                self.error_message("Quantity must be a positive integer.")
    #         elif not self.location_entry.get():
    #             self.error_message("Location missing.")
            elif not db.is_customer_id_exist(my_config.USER_ID) or not db.is_product_id_exists(q):
                self.error_message("Invalid Product ID or Customer ID.")
            elif db.add_order(my_config.USER_ID, p, q):
                messagebox.showinfo("Coffee Shop", 'Successfully added.')
                self.page_options()
            else:
                self.error_message("Product out of stock.")
        except:
            pass
            
    def check_out(self):
#         """Place new order, if all required entries are filled."""
        self.destroy_all()
                            
        self.frame       = tk.Frame(self.master, bg=self.bg, bd=15)
        self.frame_title = tk.Frame(self.frame,  bg=self.bg, bd=15)
        self.frame_cart  = tk.Frame(self.frame,  bg=self.bg, bd=15)

        self.frame_inner = tk.Frame(self.frame,  bg=self.bg, bd=15)
        
        self.frame_title.grid(row=0, column=0, sticky=tk.W)
        self.frame_cart.grid( row=1, column=0, sticky=tk.W)
        self.frame_inner.grid(row=2, column=0, sticky=tk.W)
            
            

        cart_commands = {'Remove Item': self.remove_from_cart,
                         'Place Order': self.place_order,
                         'Go Back':     self.initialize_main_buttons}

        
        options_payment   = ["<select option>","Credit Card","Points","Cash (Pick-up only)"]
        options_service   = ["<select option>","Pick-up",    "Delivery"]
        variable_payment  = tk.StringVar(self.frame_inner)
        variable_service  = tk.StringVar(self.frame_inner)
        variable_payment.set( options_payment[0])
        variable_service.set( options_service[0])
 
        self.shopping_cart(self.frame_cart, cart_commands)
        
        page_title = tk.Label(self.frame_title, text="Checkout Page", font="{U.S. 101} 30 bold", bg=self.bg, fg=self.fg)   
        label_points_avail  = tk.Label(self.frame_inner, text = 'Points available: ',            bg=self.bg,fg=self.fg)
        label_points_used   = tk.Label(self.frame_inner, text = 'Points used toward purchase: ', bg=self.bg,fg=self.fg)
        label_payment       = tk.Label(self.frame_inner, text = 'Payment method: ',              bg=self.bg,fg=self.fg)
        label_service       = tk.Label(self.frame_inner, text = 'Service method: ',              bg=self.bg,fg=self.fg)

        page_title.grid(        row=0,column=0,ipady=10, sticky = tk.W)
        label_points_avail.grid(row=0,column=0,ipadx=5,sticky=tk.E)
        label_points_used.grid( row=1,column=0,ipadx=5,sticky=tk.E)
        label_payment.grid(     row=2,column=0,ipadx=5,sticky=tk.E)
        label_service.grid(     row=3,column=0,ipadx=5,sticky=tk.E)
        
        label_points_db   = tk.Label(     self.frame_inner, text=str(self.points), bg=self.bg, fg=self.fg, width=15)
        points_used_entry = tk.Entry(     self.frame_inner,                        bg=self.fg,             width=15)
        menu_payment      = tk.OptionMenu(self.frame_inner, variable_payment, *options_payment)
        menu_service      = tk.OptionMenu(self.frame_inner, variable_service, *options_service)
        

        label_points_db.grid(   row=0,column=1,ipadx=5,sticky=tk.W)
        points_used_entry.grid( row=1,column=1,ipadx=5,sticky=tk.W)
        menu_payment.grid(      row=2,column=1,ipadx=5,sticky=tk.W+tk.N)
        menu_service.grid(      row=3,column=1,ipadx=5,sticky=tk.W+tk.N)
        menu_payment.config( height=3,bg=self.bg,fg=self.fg,width=15)
        menu_service.config( height=2,bg=self.bg,fg=self.fg,width=15)
        
        self.frame.pack()

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
            this_row = self.my_orders_tree.set(self.my_orders_tree.selection())
            cust_id = my_config.USER_ID
            records = db.get_all_orders_customer(cust_id)
            records = [r for r in records if (int(r[0]) == int(this_row['Id']))][0]
            
            #creating Message instead of Label (might be long)
            order_info = ("Order ID:       {}\nProduct ID:     {}\nOrder Quantity: {}\nOrder Date:     {}\n"
                          ).format(records[0], records[2], records[3], records[4])

            self.error_label = tk.Message(self.frame_left, text=order_info,
                                          bg=self.bg, fg=self.fg,width=300, font="{U.S. 101} 15 bold")
            self.error_label.grid(row=1, column=0, sticky=tk.W)

    def account_edit(self):
        """Runs new window for editing account."""
#         if self.frame:
#             self.frame.destroy()
#         if self.function_frame:
#             self.function_frame.destroy()
#         if self.function_frame2:
#             self.function_frame2.destroy()
#         if self.function_frame3:
#             self.function_frame3.destroy()
        self.destroy_all()
        #self.destroy_error()
        AccountEdit(self.master)

    def my_orders(self):
        """Creates menu with list of user orders."""
        self.destroy_all()
        self.frame        = tk.Frame(self.master, bg=self.bg, bd=15)        
        frame_title       = tk.Frame(self.frame,  bg=self.bg)
        self.frame_left   = tk.Frame(self.frame,  bg=self.bg, bd=15)
        self.frame_right  = tk.Frame(self.frame,  bg=self.bg, bd=15)
        frame_bottom      = tk.Frame(self.frame,  bg=self.bg, bd=15)

        frame_title.      grid(row=0, column=0, sticky=tk.N+tk.W)
        self.frame_left.  grid(row=1, column=0, sticky=tk.N+tk.W)
        self.frame_right .grid(row=1, column=1, sticky=tk.N)    
        frame_bottom     .grid(row=2, column=0, sticky=tk.N+tk.W)            

        
        page_title  = tk.Label(frame_title, text='Order History', font="{U.S. 101} 30 bold", bg=self.bg, fg=self.fg) 
        page_title.grid( row=0, column=0, sticky=tk.W,      pady=10)
        self.page_options( self.frame_right)
        button_go_back = tk.Button(frame_bottom,text='Go Back',command=self.initialize_main_buttons)
        button_go_back.grid(row=0,column=0,sticky=tk.W,pady=(20,0))
        
        # creating treeview for customers
        self.my_orders_tree = Treeview(self.frame_left, columns=MY_ORDERS_COLUMNS, show='headings', height=10)
        self.my_orders_tree.grid(row=0, column=0, sticky=tk.W)

        for column_name, width in zip(MY_ORDERS_COLUMNS, MY_ORDERS_COLUMNS_SIZE):
            self.my_orders_tree.column( column_name, width=150, anchor=tk.CENTER)
            self.my_orders_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.frame_left, orient=tk.VERTICAL)
        scrollbar.configure(command=self.my_orders_tree.set)
        self.my_orders_tree.configure(yscrollcommand=scrollbar)
        self.my_orders_tree.bind('<ButtonRelease-1>', self.order_selection)

        
        # adding records from DB to treeview
        records = db.get_all_orders_customer(my_config.USER_ID)
        for record in records:
            product_name = str(db.get_product_name(record[2]))[2]
            self.my_orders_tree.insert('', tk.END, values=[record[0],product_name])# record[1], record[2], record[3]])
        self.frame.pack()


    def error_message(self, name):
        """Shows passed message in designated place

        Used to clear code and make it more readable as it is
        called multiple times."""
        self.destroy_error()
        self.error_label = tk.Label(self.function_frame2, text=name, bg=my_config.BACKGROUND,
                                    fg=my_config.ERROR_FOREGROUND)
        self.error_label.grid(row=3, column=1)

    def log_off(self):
        self.destroy_all()
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
        self.bg = my_config.BACKGROUND
        self.fg = my_config.FOREGROUND
        
        self.frame       = tk.Frame(self.master, bg=self.bg)      
        self.frame_inner = tk.Frame(self.frame,  bg=self.bg) 
        self.error       = tk.Label()

        

        def destroy_all(self):
            for thing in (self.frame, self.frame_inner, self.error):
                if thing:
                    thing.destroy()
        
        self.error_label = tk.Label()
        self.frame  = tk.Frame(self.master, bg=my_config.BACKGROUND)

        
        frame_title = tk.Frame(self.frame, bg=self.bg)
        frame_inner = tk.Frame(self.frame, bg=self.bg)      
        frame_title.grid(row=0,column=0,sticky=tk.N+tk.W,pady=(10,0))
        frame_inner.grid(row=1,column=0,sticky=tk.N+tk.W)

        
        page_title  = tk.Label(frame_title, text='Edit', font="{U.S. 101} 30 bold", bg=self.bg, fg=self.fg) 
        page_title.grid( row=0, column=0, sticky=tk.N+tk.W, pady=10)
        
            
        label_password =tk.Label(frame_inner,bg=self.bg,text='Password')
        label_name     =tk.Label(frame_inner,bg=self.bg,text='Name')
        label_phone    =tk.Label(frame_inner,bg=self.bg,text='Phone')
        label_email    =tk.Label(frame_inner,bg=self.bg,text='Email')


        label_password.grid(row=2,column=0,sticky=tk. E,pady=(4,0))  
        label_name.    grid(row=3,column=0,sticky=tk.E)
        label_phone.   grid(row=4,column=0,sticky=tk.E)
        label_email.   grid(row=5,column=0,sticky=tk.E)

        self.password = tk.Entry(frame_inner,width=22, bg=self.fg, show='*')
        self.name     = tk.Entry(frame_inner,width=22, bg=self.fg)
        self.phone    = tk.Entry(frame_inner,width=22, bg=self.fg)
        self.email    = tk.Entry(frame_inner,width=22, bg=self.fg)
                            
        self.password.grid(row=2,column=1, sticky=tk.E,pady=(4,0))
        self.name .   grid(row=3,column=1, sticky=tk.E)   
        self.phone.   grid(row=4,column=1, sticky=tk.E) 
        self.email.   grid(row=5,column=1, sticky=tk.E)



            
        self.change_button = tk.Button(frame_inner, text='Save Changes', command=self.set_change, width=15, bg=self.bg)
        button_exit = tk.Button(       frame_inner, text='Exit',         command=self.exit,       width=15, bg=self.bg)
        self.change_button.grid(row=12, column=1, pady=(10, 0))
        button_exit.grid(       row=13, column=1)
            
            
            
            

#         self.change_button = tk.Button(frame_inner, text='Save Changes', bg=my_config.FOREGROUND,
#                                        command=self.set_change, width=16)
#         self.change_button.grid(row=9, column=1, pady=(10, 0))
#         self.cancel_button = tk.Button(frame_inner, text='Cancel', bg=my_config.FOREGROUND,
#                                        command=self.exit, width=16)
#         self.cancel_button.grid(row=10, column=1)

        
        
        # getting customer info from DB
#         customer_info = db.return_customer(my_config.MY_ID)
#         if customer_info:
#             self.name_entry.insert(tk.END, customer_info[3])
#             self.phone_entry.insert(tk.END, customer_info[4])
#             self.email_entry.insert(tk.END, customer_info[5])
#             self.cc_entry.insert(tk.END, customer_info[7])
#             self.exp_date_entry.insert(tk.END, customer_info[8] )
#             self.ccv_entry.insert(tk.END, customer_info[9])
#         else:
#             messagebox.showinfo("Coffee Shop", 'Error: Invalid ID')
#             self.exit()
            
        self.frame.pack()

        

 
        

    def set_change(self):
        """Changes customer account details if all required entries are filled properly."""
        if self.error_label:
            self.error_label.destroy()

        if 0 < len(self.password.get()) < 6:
            self.error_message('Password must be at least 6 characters')
#         if 0 < len(self.cc.get()) < 16:
#             self.error_message('Credit card must be at least 16 characters')
#         if 0 < len(self.exp_date.get()) < 5:
#             self.error_message('Invalid expiration date')
#             self.error_message('Credit card must be at least 16 characters')
#         if 0 < len(self.ccv.get()) < 3:
#             self.error_message('Invalid CCV')

        elif self.name.get() and self.password.get() != db.get_user_password(self.email.get()):
            self.error_message('Invalid password.')
        elif not self.password.get():
            self.error_message('Password missing.')
        elif not self.name.get():
            self.error_message('Name missing.')
        elif self.phone.get() and not my_config.is_integer(self.phone.get()):
            self.error_message("Phone number missing.")
        elif not self.email.get():
            self.error_message('Email missing.')

#             if self.cc:
#                 cc = self.cc.get()
#             else:
#                 cc = db.return_customer(my_config.USER_ID)[7]
#             if self.exp_date:
#                 exp_date = self.exp_date.get()
#             else:
#                 exp_date = db.return_customer(my_config.USER_ID)[8]  
#             if self.ccv:
#                 ccv = self.ccv.get()
#             else:
#                 ccv = db.return_customer(my_config.USER_ID)[9]  
            
            # if all entries are filled correctly
        else:
            db.update_customer(my_config.USER_ID, self.password.get(), self.name.get(), self.email.get(), self.phone.get())
            self.error_message("Account has been updated.")

    def error_message(self, name):
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.frame, fg=my_config.ERROR_FOREGROUND,
                                    text=name, bg=my_config.BACKGROUND)
        self.error_label.grid(row=6, column=2)

    def exit(self):
        self.frame.destroy()

        application = CustomerApp(self.master)
        application.initialize_main_buttons()
