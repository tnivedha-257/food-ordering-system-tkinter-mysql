# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:25:08 2024

@author:T.NIVEDHA
"""
# V48 final version - working well

import mysql.connector
from tkinter import  *
import tkinter.messagebox  #provides message box
from tkinter import ttk  #needed for combo box


mydb_con = mysql.connector.connect(host="localhost", user="root", password="your_mysql_password")

#Creating DB

cur = mydb_con.cursor()
cur.execute("create database if not exists food1")
cur.execute("use food1")


'''
#If you make any changes in the table column names delete the database and enter the details again
#deleting database
sql = "DROP DATABASE food1"
#sql = "DROP TABLE Customer"
cur.execute(sql)
'''

Window = Tk()

# Define the Employee table
cur.execute("""
CREATE TABLE IF NOT EXISTS Employee (
    Emp_id INT PRIMARY KEY,
    ename VARCHAR(255) NOT NULL,
    emp_g VARCHAR(10),
    eage INT,
    emp_phone BIGINT,
    pwd VARCHAR(255)
)
""")

# Define the Customer table
cur.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    c_id INT PRIMARY KEY,
    c_name VARCHAR(255) NOT NULL,
    cphone BIGINT,
    payment INT,
    pstatus VARCHAR(20),
    email VARCHAR(255),
    orderid INT,
    date DATE
)
""")


# Define the Food table    Food_id, Food_name, Food_quantity, Price_per_item
cur.execute("""
CREATE TABLE IF NOT EXISTS Food_list (
    Food_id INT AUTO_INCREMENT PRIMARY KEY,
    Food_name VARCHAR(255),
    Food_quantity INT,
    Price_per_item INT
)
""")

# Define the Rest_viewOrder table 
cur.execute("""
CREATE TABLE IF NOT EXISTS Rest_manageOrder (
    orderid INT AUTO_INCREMENT PRIMARY KEY,
    c_id INT,
    c_name VARCHAR(255) NOT NULL,
    cphone BIGINT,
    email VARCHAR(255),
    Food_id INT,
    Food_name VARCHAR(255),
    Food_qty INT,
    Price INT,
    Emp_id INT, 
    ename VARCHAR(255),
    emp_phone BIGINT
)
""")


# Define the Cust_order table 
cur.execute("""
CREATE TABLE IF NOT EXISTS Cust_order (
    c_id INT,
    Food_name VARCHAR(255),
    Food_qty INT,
    Address VARCHAR(255),
    cphone BIGINT
)
""")

# Store last order id.
cur.execute("""
CREATE TABLE IF NOT EXISTS Customer_orders (
    Order_index INT AUTO_INCREMENT PRIMARY KEY,
    Ordered_cust_ids INT    #only one customer id per index not ids
)
""")
   

#Generate a 6 digit customer ID that is not already in the table and return it as customer_id
def generate_unique_customer_id():
    import random
    #import string

    while True:
        # Generate a random 6-character ID
        customer_id = random.randint(100000, 999999)

        # Check if the ID exists in the database
        sql = "SELECT * FROM Customer WHERE c_id = %s"
        cur.execute(sql, (customer_id,))
        result = cur.fetchone()

        if not result:
            return customer_id     #returns unique ID
        
#Generate a 6 digit Employee ID that is not already in the table and return it as customer_id
#Note that for each table different function names and table names are to be used
def generate_unique_employee_id():
    import random
    #import string

    while True:
        # Generate a random 6-character ID
        employer_id = random.randint(100000, 999999)

        # Check if the ID exists in the database
        sql = "SELECT * FROM Employee WHERE Emp_id = %s"
        cur.execute(sql, (employer_id,))
        result = cur.fetchone()

        if not result:
            return employer_id #returns unique ID


def Employee_Register_OR_Show():
  
    def Register_emp_details():
        # Generate a unique employer ID
        employer_id = generate_unique_employee_id()
        #Insert the record for  employer_id 
        Emp_data_insert = employer_id, e2.get(), e3.get(), e4.get(), e5.get(), e6.get()  #get all entries
        emp_sql = "INSERT INTO Employee (Emp_id, ename, emp_g, eage, emp_phone, pwd) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(emp_sql, Emp_data_insert)
        mydb_con.commit()
        lbl_emp_added=Label(employee_frame,text="SUCCESSFULLY ADDED")
        lbl_emp_added.pack()
       

    def Show_emp_details():
        e1_combo.config(state='normal') 
        cur.execute("SELECT Emp_id FROM Employee")  
        All_Employee_Ids = [row[0] for row in cur.fetchall()]  #feteches all records and takes only the first value in each record and puts in a list
        e1_combo.config(values=All_Employee_Ids)          # Populate the combobox                      
            
        def on_Emp_id_selected(event):
            selected_Emp_id = e1_combo.get()
            sql = "SELECT * FROM Employee WHERE Emp_id = %s"
            cur.execute(sql, (selected_Emp_id,))
            Employee_record = cur.fetchone()
            e2.delete(0,END) #blank the input widgets
            e3.delete(0,END)
            e4.delete(0,END) 
            e5.delete(0,END)
            e6.delete(0,END)                
            # Populate the other fields with the retrieved result data
            e2.insert(0, Employee_record[1])  # Food name
            e3.insert(0, Employee_record[2])  # Food quantity
            e4.insert(0, Employee_record[3])  # Price per item
            e5.insert(0, Employee_record[4])  # Food name
            e6.insert(0, Employee_record[5])  # Food quantity

             
        e1_combo.bind("<<ComboboxSelected>>", on_Emp_id_selected)  
        # should be put only after defining the event function. But may not be moved out of Show_emp_details()
        
#function code starts
    employee_frame = Toplevel(Window)
    label1=Label(employee_frame,text="EMPLOYEE DETAILS",font='arial 15 bold', bg='light blue')
    label1.pack(pady=(5,10))
     
    label_instruction1=Label(employee_frame,text="Press Ctrl and v keys simultaneously",font='arial 8 bold', fg='red')
    label_instruction1.pack() 
    label_instruction2=Label(employee_frame,text="to change to view mode",font='arial 8 bold', fg='red')
    label_instruction2.pack()
    
    l1=Label(employee_frame,text="EMPLOYEE ID")
    l1.pack()

    # Create a hidden combobox
    e1_combo = ttk.Combobox(employee_frame)
    e1_combo.pack(pady=(0,15))
    e1_combo.config(state='disabled') 
    
    
    l2=Label(employee_frame,text="EMPLOYEE NAME")
    l2.pack()
    e2=tkinter.Entry(employee_frame)
    e2.pack()
    l3=Label(employee_frame,text="EMPLOYEE GENDER")
    l3.pack()
    e3=tkinter.Entry(employee_frame)
    e3.pack()
    l4=Label(employee_frame,text="EMPLOYEE AGE")
    l4.pack()
    e4=tkinter.Entry(employee_frame)
    e4.pack()
    l5=Label(employee_frame,text="EMPLOYEE PHONE NO:")
    l5.pack()
    e5=tkinter.Entry(employee_frame)
    e5.pack()
    l6=Label(employee_frame,text="ENTER PASS WORD")
    l6.pack()
    e6=tkinter.Entry(employee_frame)
    e6.pack()


    but_emp_register=Button(employee_frame,text="Register",font="arial 20 bold",bg='cyan',command=lambda: Register_emp_details())
    but_emp_register.pack(pady=20)
    #but_emp_show=Button(employee_frame,text="View",font="arial 20 bold",bg='cyan',command=lambda: Show_emp_details())
    #but_emp_show.pack(side=RIGHT, pady=10)
    def activate_view_mode(event):     #Ctrl+v i.e on_ctrl_v event is attached to the Add_food_frame
        but_emp_register.config(state='disabled')
        #lbl_successfully_added.destroy()
        Show_emp_details()
       
    employee_frame.bind("<Control-v>", activate_view_mode)
    

    
def Customer_Register_ShowDetails(Cutomer_OR_Manager):
          
    def Register_cust_details():
        # Generate a unique customer ID
        customer_id = generate_unique_customer_id()      
        but_cust_store['state'] = DISABLED  
        #c1 & c7 widgets are not used while registration
        Cust_data_insert = customer_id, c2.get(), c3.get(), c4.get(), c5.get(), c6.get(), c8.get()
        cust_sql = "INSERT INTO Customer (c_id, c_name, cphone, payment, pstatus, email, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(cust_sql, Cust_data_insert)
        mydb_con.commit()
        lbl_cust_added=Label(customer_frame,text="SUCCESSFULLY ADDED")
        lbl_cust_added.pack() 
        c1['state'] = NORMAL
        c1.insert(0,customer_id)
        c1['state'] = DISABLED
        custID_str= "Your Cutomer ID is    "+ str(customer_id) + "   Please Store it Safely"
        #lbl_cust_added=Label(customer_frame,text=custID_str)
        #lbl_cust_added.pack() 
        messagebox.showinfo("Customer Registration", custID_str, parent=customer_frame)
        Window.destroy()
        
          
    def Show_cust_details(Cust_rec): #Pass the customer record retrived based on customer ID or phone number       
            c2['state'] = NORMAL
            c4['state'] = NORMAL
            c5['state'] = NORMAL
            c6['state'] = NORMAL
            c8['state'] = NORMAL
            #c1.insert(0, Cust_rec[0][0])  # even c_id is the primary key it is to be inserted in the entry widget
            c2.insert(0, Cust_rec[1]) #inserts the text in the input widget, first index is the record number and the second index is the item
            c4.insert(0, Cust_rec[3])
            c5.insert(0, Cust_rec[4])
            c6.insert(0, Cust_rec[5])
            c8.insert(0, Cust_rec[7]) # date is inserted and then order_id is checked for availability



# function code starts
    customer_frame = Toplevel(Window)
    labelc=Label(customer_frame,text="CUSTOMER REGISTRATION DETAILS",font='arial 8 bold', bg='light green')
    labelc.pack(pady=(5,10))
    
    l1=Label(customer_frame,text="CUSTOMER ID (INT)")
    l1.pack()
    c1=tkinter.Entry(customer_frame)
    c1.pack()
    c1.config(state='disabled')
    
    
    l2=Label(customer_frame,text="NAME")
    l2.pack()
    c2=tkinter.Entry(customer_frame)
    c2.pack()
    l3=Label(customer_frame,text="CELL PHONE NO.")
    l3.pack()
    c3=tkinter.Entry(customer_frame)
    c3.pack()
    l4=Label(customer_frame,text="ADVANCE AMOUNT PAID IN Rs", font='arial 6 bold')
    l4.pack(pady=(10,0))
    c4=tkinter.Entry(customer_frame)
    c4.pack()
    l5=Label(customer_frame,text="PAYMENT STATUS", font='arial 6 bold')
    l5.pack()
    c5=tkinter.Entry(customer_frame)
    c5.pack()
    c5['state'] = DISABLED
    l6=Label(customer_frame,text="EMAIL")
    l6.pack()
    c6=tkinter.Entry(customer_frame)
    c6.pack()
    l7=Label(customer_frame,text="ORDER ID")   
    # disable orderid during registartion and show while viewing,  7th item created  in Rest_view_order table
    l7.pack()
    c7=tkinter.Entry(customer_frame)
    c7.pack()
    l8=Label(customer_frame,text="DATE yyyy-mm-dd")
    l8.pack()
    c8=tkinter.Entry(customer_frame)
    c8.pack()
      
    
    def check_entry_c1_and_process():
        #This event function gets the customer ID from the Entry Widget and displays other details
        Cust_id=c1.get()
        c1["state"]=DISABLED        
        sql = "SELECT * FROM Customer WHERE c_id = %s"
        cur.execute(sql, (Cust_id,))
        Cust_rec = cur.fetchone()
        
        if Cust_rec:
            # Proceed with fetching the order ID only if customer record exists
            accepted_order_id_sql = "SELECT orderid FROM Rest_manageOrder WHERE c_id = %s"
            cur.execute(accepted_order_id_sql, (Cust_id,))
            order_id_fetched = cur.fetchone()        
            # Check if an order ID was found
            if order_id_fetched:
                # Process the order_id_fetched if available
                c3['state'] = NORMAL
                c3.insert(0, Cust_rec[2]) #Display the phone number 
                c7['state'] = NORMAL
                c7.insert(0, order_id_fetched[0]) 
                #if orderid 7th item is created by the Manager in the Cust_rect_view_order table then show it
                Show_cust_details(Cust_rec)  #Display other other
            else:
                messagebox.showerror("Restarant Manager - Error", "No order found for this customer")
                Window.destroy()
        else:
            messagebox.showerror("Restarant Manager - Error", "No Such Customer ID Exists")
            Window.destroy()
                        
                
        
        
    def check_entry_c3_and_process(event):
        #This event function gets the customer Phone number from the Entry Widget and displays other details
        Phone_no=c3.get()
        c3["state"]=DISABLED
        sql = "SELECT * FROM Customer WHERE cphone = %s"
        cur.execute(sql,  (Phone_no,))
        Cust_rec = cur.fetchone()  #'None' data type will be returned when the table is empty. Causes error
        
        if Cust_rec:
            # Proceed with fetching the order ID only if customer record exists
            accepted_order_phone_sql = "SELECT orderid FROM Rest_manageOrder WHERE cphone = %s"
            cur.execute(accepted_order_phone_sql, (Phone_no,))
            order_phone_id_fetched = cur.fetchone()        
            # Check if an order ID was found
            if order_phone_id_fetched:
                # Process the order_id_fetched if available
                c1['state'] = NORMAL
                c1.insert(0, Cust_rec[0]) #Display the customer id 
                c7['state'] = NORMAL
                c7.insert(0,order_phone_id_fetched[0]) 
                #if orderid 7th item is order_phone_id_fetchedted by the Manager in the Cust_rect_view_order table then show it
                Show_cust_details(Cust_rec)  #Display other other
            else:
                messagebox.showerror("Restarant Manager - Error", "No order found for this customer")
                Window.destroy()
        else:
            messagebox.showerror("Restarant Manager - Error", "No Such Phone Number Exists")
            Window.destroy()
        
    
    # Bind the Enter key to the check_entry_and_process function
    #Two ways to use event function. The label event should be passed to check_entry_c3_and_process() function in the second case
    c1.bind('<Return>', lambda event: check_entry_c1_and_process())   #retrives details using customer ID
    c3.bind('<Return>', check_entry_c3_and_process)   #retrieves details using customer phone number   
                
            
    if Cutomer_OR_Manager ==1:    #Register
        but_cust_store=Button(customer_frame,text="Register",font="arial 20 bold",bg='cyan',command=lambda: Register_cust_details())
        but_cust_store.pack(pady=20)
        # disable orderid during registartion and bring while viewing from orderid 7th item created  in Rest_view_order table
        c7['state'] = DISABLED
    elif Cutomer_OR_Manager == 2:  # View Customer Details
        c1['state'] = NORMAL  
        c1.delete(0,END) 
        c2.delete(0,END)
        c3['state'] = NORMAL
        c3.delete(0,END)  #phone number
        c4.delete(0,END)
        c5.delete(0,END)
        c6.delete(0,END)
        #c7['state'] = NORMAL
        c7.delete(0,END) 
        c8.delete(0,END) 
        
        c2['state'] = DISABLED
        #c3['state'] = DISABLED
        c4['state'] = DISABLED
        c5['state'] = DISABLED
        c6['state'] = DISABLED
        c7['state'] = DISABLED
        c8['state'] = DISABLED
        
        
        cust_l1=Label(customer_frame,text="Enter Customer ID or Phone Number &", font="arial 7 bold", fg='red')
        #Pad 10 pixels above and 5 pixels below
        cust_l1.pack(pady=(10,1))
        cust_l2=Label(customer_frame,text="Press <Enter> Key to View Details", font="arial 7 bold", fg='red')
        cust_l2.pack()
       

def Add_food_list(): 
    
  def Store_food_details():
        # disable orderid during registration and bring while viewing from orderid 7th item created  in Rest_view_order table
        #Instead of fe1 a combo button is used for food-id and it is the Primary key & auto incremented, need not be included
        Food_data =fe2.get(), fe3.get(), fe4.get()
        #food_sql = "INSERT INTO Food_list (Food_id, Food_name, Food_quantity, Price_per_item) VALUES (%s, %s, %s, %s)"
        food_sql = "INSERT INTO Food_list (Food_name, Food_quantity, Price_per_item) VALUES (%s, %s, %s)"
        cur.execute(food_sql, Food_data)
        mydb_con.commit()
        lbl_successfully_added=Label(Add_food_frame,text="SUCCESSFULLY ADDED")
        lbl_successfully_added.pack()
        
  def Show_food_details():
        food_id_combo.config(state='normal') 
        cur.execute("SELECT Food_id FROM Food_list")
        food_ids = [row[0] for row in cur.fetchall()]  #feteches all records and takes only the first value in each record and puts in a list
        food_id_combo.config(values=food_ids)          # Populate the combobox                       
            
        def on_food_id_selected(event):
            selected_food_id = food_id_combo.get()
            sql = "SELECT Food_name, Food_quantity, Price_per_item FROM Food_list WHERE Food_id = %s"
            cur.execute(sql, (selected_food_id,))
            Food_record = cur.fetchone()
            fe2.delete(0,END) #blank the input widgets otherwise contents will be concatenated
            fe3.delete(0,END)
            fe4.delete(0,END)                
            # Populate the other fields with the retrieved result data
            fe2.insert(0, Food_record[0])  # Food name
            fe3.insert(0, Food_record[1])  # Food quantity
            fe4.insert(0, Food_record[2])  # Price per item
       
        food_id_combo.bind("<<ComboboxSelected>>", on_food_id_selected)    
        
        
  Add_food_frame = Toplevel(Window)  # Add_food_frame is an instance of window assosciated with the main window
  

  def activate_view_mode(event):     #Ctrl+v i.e on_ctrl_v event is attached to the Add_food_frame
      b1.config(state='disabled')
      fe2.delete(0,END) #blank the input widgets. Otherwise contents will be concatenated
      fe3.delete(0,END)
      fe4.delete(0,END) 
      Show_food_details()
     
  Add_food_frame.bind("<Control-v>", activate_view_mode)


  frame_lbl = Label(Add_food_frame, text="ADD FOOD TO THE LIST", font="arial 15 bold", bg='light blue')
  frame_lbl.pack()
  
  instruction_label = Label(Add_food_frame, text="Click on the Window & Press Ctrl and v", font='arial 8 bold', fg='red')
  instruction_label.pack(pady=(10,0))
  instruction_labe2 = Label(Add_food_frame, text="together to change to View mode", font='arial 8 bold', fg='red')
  instruction_labe2.pack(pady=(0,0))
  
  flbl1 = Label(Add_food_frame, text="FOOD ID")
  flbl1.pack()
   
  # Create a hidden combobox
  food_id_combo = ttk.Combobox(Add_food_frame)
  food_id_combo.pack(pady=(0,10))
  food_id_combo.config(state='disabled')  
  
  flbl2 = Label(Add_food_frame, text="FOOD NAME")
  flbl2.pack()
  fe2 = tkinter.Entry(Add_food_frame)
  fe2.pack()
  flbl3 = Label(Add_food_frame, text="FOOD QUANTITY")
  flbl3.pack()
  fe3 = tkinter.Entry(Add_food_frame)
  fe3.pack()
  flbl4 = Label(Add_food_frame, text="PRICE PER ITEM")
  flbl4.pack()
  fe4 = tkinter.Entry(Add_food_frame)
  fe4.pack()
  
  b1=Button(Add_food_frame, text="Store",font="arial 20 bold",bg='cyan',command=lambda: Store_food_details())
  b1.pack(pady=30)
  


def Cust_order():        
  def populate_combo():
      combolbl = Label(Cust_order_frame, text=" Use Arrow Button & Select Food Item ", font="arial 10 bold", fg='red')
      combolbl.pack(pady=(10,0))  #pad from previous widget
      food_combo = ttk.Combobox(Cust_order_frame)
      food_combo.pack(pady=(0,10))  
      # Bind the add_food_item function to the Enter key press in the entry widget (using fentry)
      #fe1.bind("<Return>", lambda event: add_food_item(fe1, food_combo))
      # Retrieve food names
      sql = "SELECT Food_name FROM Food_list"
      cur.execute(sql)
      food_names = [row[0] for row in cur.fetchall()]  # Get food names from results

      # Clear existing items (optional)
      food_combo.set("")
      food_combo['values'] = food_names
      # Bind selection event to update oe2 entry
      food_combo.bind("<<ComboboxSelected>>", lambda event: update_oe2(food_combo.get()))   
     
  def update_oe2(selected_food):
        oe2.delete(0, END)  # Clear existing text in oe2 entry
        oe2.insert(0, selected_food)  # Insert the selected food item

  def Submit_food_order():     
    # Get customer ID and phone number from entry widgets
    customer_id = oe1.get()
    customer_phone = oe5.get()
    # Validate customer ID by checking against Customer table
    sql = "SELECT cphone FROM Customer WHERE c_id = %s"
    cur.execute(sql, (customer_id,))
    registered_phone = cur.fetchone()  # Fetch first row (if exists). This will return 0 if the record does not exist for the c_id

    if not registered_phone:    #This is not checking the phone no. It checks wether ther record exists. if record does not exists for the c_id
        # Display error message for invalid customer ID
        lbl_error = Label(Cust_order_frame, text="Invalid Customer ID. Please enter a valid ID.", fg='red')
        lbl_error.pack()
        return  # Exit the function without submitting the order

    # Validate phone number by comparing with registered phone
    if int(customer_phone) != registered_phone[0]: #customer_phone is astring and registered_phone[0] is an integer
        # Display error message for mismatched phone number
        lbl_error = Label(Cust_order_frame, text="Enter registered cell phone number.", fg='red')
        lbl_error.pack()
        return  # Exit the function without submitting the order  
      
      
    # disable orderid during registration and bring while viewing from orderid 7th item created  in Rest_view_order table
    Food_data =oe1.get(), oe2.get(), oe3.get(), oe4.get(), oe5.get()   #fe1.get(), is Primary key & auto incremented, need not be included
    food_sql = "INSERT INTO Cust_order (c_id, Food_name, Food_qty, Address, cphone) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(food_sql, Food_data)
    mydb_con.commit()
    lbl_successfully_added=Label(Cust_order_frame,text="SUCCESSFULLY ADDED")
    lbl_successfully_added.pack()
    custID_from_order = oe1.get()  # custID_from_order - set by  Cust_order() function is saved
    order_sql = "INSERT INTO Customer_orders (Ordered_cust_ids) VALUES (%s)"
    cur.execute(order_sql, (custID_from_order,))
    mydb_con.commit()
        
  def Show_food_order():  
        
        Co_id = int(oe1.get())
        sql = "SELECT * FROM Cust_order WHERE c_id = %s"
        cur.execute(sql,  (Co_id ,)) #c_id_from_order received from the Customer Order window widget
        res = cur.fetchall()  #'None' data type will be returned when the table is empty. Causes error
        oe1.delete(0,END)
        oe2.delete(0,END) #inserts the text in the input widget
        oe3.delete(0,END)
        oe4.delete(0,END)
        oe5.delete(0,END)
        oe1.insert(0, res[0][0])  # even c_id is the primary key it is to be inserted in the entry widget
        oe2.insert(0, res[0][1]) #inserts the text in the input widget, first index is the record number and the second index is the item
        oe3.insert(0, res[0][2])
        oe4.insert(0, res[0][3])    
        oe5.insert(0, res[0][4]) 
        
  Cust_order_frame = Toplevel(Window)
  frame_lbl = Label(Cust_order_frame, text="   PLACE ORDER   ", font="arial 20 bold", bg='light green')
  frame_lbl.pack(pady=(5,10))
  
  olb1 = Label(Cust_order_frame, text="CUSTOMER ID")
  olb1.pack()
  oe1 = tkinter.Entry(Cust_order_frame)
  oe1.pack()
  olb2 = Label(Cust_order_frame, text="Use Combobox to Select the Food Item", font="arial 8 bold", fg='red')
  olb2.pack(pady=(5,0))
  oe2 = tkinter.Entry(Cust_order_frame)
  oe2.pack()
  olb3 = Label(Cust_order_frame, text="FOOD QUANTITY")
  olb3.pack(pady=(10,0))
  oe3 = tkinter.Entry(Cust_order_frame)
  oe3.pack()
  olb4 = Label(Cust_order_frame, text="ADDRESS")
  olb4.pack()
  oe4 = tkinter.Entry(Cust_order_frame)
  oe4.pack()
  olb5 = Label(Cust_order_frame, text="PHONE NUMBER")
  olb5.pack()
  oe5 = tkinter.Entry(Cust_order_frame)
  oe5.pack()

  populate_combo()

  b1=Button(Cust_order_frame, text="Submit",font="arial 20 bold",bg='cyan',command=lambda: Submit_food_order())
  b1.pack(pady=(15,5)) #Provides 15 pixels padding above the button to display combobox content 
      
     
def Rest_manageOrder():

    def populate_combo_employee():
        # Get all employee names
        sql = "SELECT ename FROM Employee"
        cur.execute(sql)
        employee_names = [row[0] for row in cur.fetchall()]  # Check if index is ename (row[0])
        # Clear existing items (optional)
        assign_emp_combo.set("")
        assign_emp_combo['values'] = employee_names

    def select_employee(event):  #called when an item is selected in the combo box
        selected_emp = assign_emp_combo.get()
        # Get employee details based on selected name
        sql = "SELECT Emp_id, emp_phone FROM Employee WHERE ename = %s"
        cur.execute(sql, (selected_emp,))
        emp_data = cur.fetchone()

        if emp_data:
            emp_id_entry.delete(0, END)
            emp_id_entry.insert(0, emp_data[0])
            emp_phone_entry.delete(0, END)
            emp_phone_entry.insert(0, emp_data[1])
        
        
    def poulate_orderCombo():
        order_sql = "SELECT Ordered_cust_ids FROM Customer_orders"
        cur.execute(order_sql)
        all_orders_cust_ids= [row[0] for row in cur.fetchall()]
        # Clear existing items (optional)
        orders_combo.set("")
        orders_combo['values'] = all_orders_cust_ids


    def assign_selected_value(orders_cust_id_selected):  #event function called when an item is selected on  the orders_combo
        global selected_order_cust_id  # Use global keyword to modify the variable outside the function
        selected_order_cust_id = orders_cust_id_selected
        select_order_andAccept()  # get the values for other widgets from the tables and enter into the widgets 
        

    def select_order_andAccept():  
        
        sql = "SELECT c_name,cphone, email FROM Customer WHERE c_id = %s"
        cur.execute(sql, (selected_order_cust_id,))  
        # selected_order_cust_id  defined as global in assign_selected_value() event function of orders_combo
        customer_data = cur.fetchone()
        if customer_data:
            c_id_entry.delete(0, END)
            c_id_entry.insert(0,selected_order_cust_id)  #customer id brought from the order combo box
            c_name_entry.delete(0, END)
            c_name_entry.insert(0, customer_data[0])
            c_phone_entry.delete(0, END)
            c_phone_entry.insert(0, customer_data[1])
            email_entry.delete(0, END)
            email_entry.insert(0, customer_data[2])
            
        
        sql = "SELECT Food_name, Food_qty FROM Cust_order WHERE c_id = %s"
        cur.execute(sql, (selected_order_cust_id,))  
        # selected_order_cust_id  defined as global in assign_selected_value() event function of orders_combo
        order_details = cur.fetchone()
        
        if  order_details:
            # Set retrieved order details 
            food_name_entry.delete(0, END)
            food_name_entry.insert(0, order_details[0])
            food_qty_entry.delete(0, END)
            food_qty_entry.insert(0, order_details[1])          
            
        #From the above Food_name order_details[0], get Food_id, price from Food_list table (Primary key)

        sql = "SELECT Food_id, price_per_item FROM Food_list WHERE Food_name = %s"
        cur.execute(sql, (order_details[0],))  # order_details[0] = Food_id
        Food_id_price = cur.fetchone()
            
        if  Food_id_price:
            Total_price=Food_id_price[1]*order_details[1]  # order_details[2] = Food_qty
            price_entry.delete(0,END)
            price_entry.insert(0,Total_price)
            food_id_entry.delete(0, END)
            food_id_entry.insert(0, Food_id_price[0])

    def Accept_order():
        
        manager_data = (
        c_id_entry.get(),
        c_name_entry.get(),
        c_phone_entry.get(),
        email_entry.get(),
        food_id_entry.get(),
        food_name_entry.get(),
        food_qty_entry.get(),
        price_entry.get(),
        emp_id_entry.get(),
        assign_emp_combo.get(),  #employee name assigned by the manager
        emp_phone_entry.get(),
        )
                                              
        manager_sql = "INSERT INTO Rest_manageOrder (c_id,c_name,cphone,email,Food_id,Food_name,Food_qty,Price,Emp_id,ename,emp_phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(manager_sql, manager_data)
        mydb_con.commit()
        #orderAccept_lbl = Label(Manage_order_frame, text="ORDER ACCEPTED", font="arial 10 bold", bg='light blue')
        #orderAccept.pack()
        messagebox.showinfo("Restaurant Manager", "Order Accepted", parent=Manage_order_frame)
        
    # Create the window and frame
    Manage_order_window = Toplevel()
    Manage_order_window.title("Manage Order")
    Manage_order_frame = Frame(Manage_order_window)
    Manage_order_frame.pack(padx=10, pady=10)
    frame_lbl = Label(Manage_order_frame, text="  MANAGE ORDERS  ", font="arial 15 bold", bg='light blue')
    frame_lbl.pack(pady=(5,10))
    combolbl = Label(Manage_order_frame, text="SELECT Cutomer ID of Order Received", font='arial 7 bold', fg='red')
    combolbl.pack(pady=(5,0))  #pad from previous widget
    orders_combo = ttk.Combobox(Manage_order_frame)
    orders_combo.bind("<<ComboboxSelected>>", lambda event: assign_selected_value(orders_combo.get())) 
    orders_combo.pack() 



# Customer Details
    c_id_lbl = Label(Manage_order_frame, text="Customer ID:")
    c_id_lbl.pack()
    c_id_entry = Entry(Manage_order_frame)
    c_id_entry.pack()

    c_name_lbl = Label(Manage_order_frame, text="Customer Name:")
    c_name_lbl.pack()
    c_name_entry = Entry(Manage_order_frame)
    c_name_entry.pack()
    
    c_phone_lbl = Label(Manage_order_frame, text="Customer Phone:")
    c_phone_lbl.pack()
    c_phone_entry = Entry(Manage_order_frame)
    c_phone_entry.pack()

    email_lbl = Label(Manage_order_frame, text="Email:")
    email_lbl.pack()
    email_entry = Entry(Manage_order_frame)
    email_entry.pack()

    # Order Details
    food_id_lbl = Label(Manage_order_frame, text="Food ID:")
    food_id_lbl.pack()
    food_id_entry = Entry(Manage_order_frame)
    food_id_entry.pack()

    food_name_lbl = Label(Manage_order_frame, text="Food Name:")
    food_name_lbl.pack()
    food_name_entry = Entry(Manage_order_frame)
    food_name_entry.pack()

    food_qty_lbl = Label(Manage_order_frame, text="Food Qty:")
    food_qty_lbl.pack()
    food_qty_entry = Entry(Manage_order_frame)
    food_qty_entry.pack()

    price_lbl = Label(Manage_order_frame, text="Price:")
    price_lbl.pack()
    price_entry = Entry(Manage_order_frame)
    price_entry.pack()

    # Employee Details
    emp_id_lbl = Label(Manage_order_frame, text="Employee ID:")
    emp_id_lbl.pack()
    emp_id_entry = Entry(Manage_order_frame)
    emp_id_entry.pack()

    emp_phone_lbl = Label(Manage_order_frame, text="Employee Phone:")
    emp_phone_lbl.pack()
    emp_phone_entry = Entry(Manage_order_frame)
    emp_phone_entry.pack()

    ename_lbl = Label(Manage_order_frame, text="Assign an Employee")
    ename_lbl.pack()
    emp_name_entry = Entry(Manage_order_frame)
    emp_phone_entry.pack()
       
    # Create combo button for employee selection
    assign_emp_combo = ttk.Combobox(Manage_order_frame)
    assign_emp_combo.bind("<<ComboboxSelected>>", select_employee)
    assign_emp_combo.pack()
    
    b3=Button(Manage_order_frame, text="Accept Order",font="arial 20 bold",bg='cyan',command=lambda: Accept_order())
    b3.pack(pady=10)
    
    poulate_orderCombo()
    populate_combo_employee()  #called in the Rest_manageOrder() function
  

    
def CustomerView_AcceptedOrder():            
    # Create the window and frame
    View_Accepted_order_window = Toplevel()
    View_Accepted_order_window.title("CUSTOMER ORDER ACCEPTED")
    View_Accepted_order_frame = Frame(View_Accepted_order_window)
    View_Accepted_order_frame.pack(padx=10, pady=10)
    frame_lbl = Label(View_Accepted_order_frame, text="  ORDER ACCEPTED  ", font="arial 15 bold", bg='light green')
    frame_lbl.pack(pady=(5,10))
    
    
    def get_c_id_entry(event):
        """
        This function is called when the Enter key is pressed in the c_id_entry field.
        It retrieves the entered value and (you can replace this with your desired action)
        prints it to the console.
        """
        customer_id = c_id_entry.get()
        sql = "SELECT c_name,cphone,email,Food_id,Food_name,Food_qty,Price,Emp_id,ename,emp_phone FROM  Rest_manageOrder WHERE c_id = %s"
        cur.execute(sql, (customer_id,))  
            # selected_order_cust_id  defined as global in assign_selected_value() event function of orders_combo
        accepted_order_details = cur.fetchone()
        
        if accepted_order_details:
            #Enable the widgets and clear the contents
            c_name_entry['state']= NORMAL
            c_phone_entry['state']= NORMAL
            email_entry['state']= NORMAL
            food_id_entry['state']= NORMAL
            food_name_entry['state']= NORMAL
            food_qty_entry['state']= NORMAL
            price_entry['state']= NORMAL
            emp_id_entry['state']= NORMAL
            emp_name_entry['state']= NORMAL
            emp_phone_entry['state']= NORMAL
            
            #clear all widgets
            c_name_entry.delete(0, END)
            c_phone_entry.delete(0, END)
            email_entry.delete(0, END)
            food_id_entry.delete(0, END)
            food_name_entry.delete(0, END)
            food_qty_entry.delete(0, END)
            price_entry.delete(0,END)
            emp_id_entry.delete(0, END)
            emp_name_entry.delete(0, END)
            emp_phone_entry.delete(0, END)
            #Insert / display details retrived from the database into the widgeta
            c_name_entry.insert(0, accepted_order_details[0])
            c_phone_entry.insert(0, accepted_order_details[1])
            email_entry.insert(0, accepted_order_details[2])
            food_id_entry.insert(0, accepted_order_details[3])
            food_name_entry.insert(0, accepted_order_details[4])
            food_qty_entry.insert(0, accepted_order_details[5]) 
            price_entry.insert(0,accepted_order_details[6])
            emp_id_entry.insert(0, accepted_order_details[7])
            emp_name_entry.insert(0, accepted_order_details[8])
            emp_phone_entry.insert(0, accepted_order_details[9])
            #Disable the widgets to avoid entering details into those widgets
            c_name_entry['state']= DISABLED
            c_phone_entry['state']= DISABLED
            email_entry['state']= DISABLED
            food_id_entry['state']= DISABLED
            food_name_entry['state']= DISABLED
            food_qty_entry['state']= DISABLED
            price_entry['state']= DISABLED
            emp_id_entry['state']= DISABLED
            emp_name_entry['state']= DISABLED
            emp_phone_entry['state']= DISABLED
            
        else:
            #Enable the widgets and clear the contes
            c_name_entry['state']= NORMAL
            c_phone_entry['state']= NORMAL
            email_entry['state']= NORMAL
            food_id_entry['state']= NORMAL
            food_name_entry['state']= NORMAL
            food_qty_entry['state']= NORMAL
            price_entry['state']= NORMAL
            emp_id_entry['state']= NORMAL
            emp_name_entry['state']= NORMAL
            emp_phone_entry['state']= NORMAL
            
            #clear the contents
            c_name_entry.delete(0, END)
            c_phone_entry.delete(0, END)
            email_entry.delete(0, END)
            food_id_entry.delete(0, END)
            food_name_entry.delete(0, END)
            food_qty_entry.delete(0, END)
            price_entry.delete(0,END)
            emp_id_entry.delete(0, END)
            emp_name_entry.delete(0, END)
            emp_phone_entry.delete(0, END)
            
            #Disbale the widgets
            c_name_entry['state']= DISABLED
            c_phone_entry['state']= DISABLED
            email_entry['state']= DISABLED
            food_id_entry['state']= DISABLED
            food_name_entry['state']= DISABLED
            food_qty_entry['state']= DISABLED
            price_entry['state']= DISABLED
            emp_id_entry['state']= DISABLED
            emp_name_entry['state']= DISABLED
            emp_phone_entry['state']= DISABLED
            
            messagebox.showinfo("Customer-Error", "The ID you Entered Does not Exists / Your Order has not been accepted. Please Contact the Restaurant Manager")
            Window.destroy()

    
    c_id_lbl = Label(View_Accepted_order_frame, text="Enter Customer ID & Press Enter Key", font="arial 7 bold",fg='red')
    c_id_lbl.pack()
    c_id_entry = Entry(View_Accepted_order_frame)
    # Bind the <Return> key event to the get_customer_id function
    c_id_entry.bind("<Return>", get_c_id_entry)
    c_id_entry.pack()

    c_name_lbl = Label(View_Accepted_order_frame, text="Customer Name:")
    c_name_lbl.pack()
    c_name_entry = Entry(View_Accepted_order_frame)
    c_name_entry.pack()
    
    c_phone_lbl = Label(View_Accepted_order_frame, text="Customer Phone:")
    c_phone_lbl.pack()
    c_phone_entry = Entry(View_Accepted_order_frame)
    c_phone_entry.pack()

    email_lbl = Label(View_Accepted_order_frame, text="Email:")
    email_lbl.pack()
    email_entry = Entry(View_Accepted_order_frame)
    email_entry.pack()

    # Order Details
    food_id_lbl = Label(View_Accepted_order_frame, text="Food ID:")
    food_id_lbl.pack()
    food_id_entry = Entry(View_Accepted_order_frame)
    food_id_entry.pack()

    food_name_lbl = Label(View_Accepted_order_frame, text="Food Name:")
    food_name_lbl.pack()
    food_name_entry = Entry(View_Accepted_order_frame)
    food_name_entry.pack()

    food_qty_lbl = Label(View_Accepted_order_frame, text="Food Qty:")
    food_qty_lbl.pack()
    food_qty_entry = Entry(View_Accepted_order_frame)
    food_qty_entry.pack()

    price_lbl = Label(View_Accepted_order_frame, text="Total Price:")
    price_lbl.pack()
    price_entry = Entry(View_Accepted_order_frame)
    price_entry.pack()

    # Employee Details
    emp_id_lbl = Label(View_Accepted_order_frame, text="Employee ID:")
    emp_id_lbl.pack()
    emp_id_entry = Entry(View_Accepted_order_frame)
    emp_id_entry.pack()

    ename_lbl = Label(View_Accepted_order_frame, text="Assign an Employee")
    ename_lbl.pack()
    emp_name_entry = Entry(View_Accepted_order_frame)
    emp_name_entry.pack() 
    
    emp_phone_lbl = Label(View_Accepted_order_frame, text="Employee Phone:")
    emp_phone_lbl.pack()
    emp_phone_entry = Entry(View_Accepted_order_frame)
    emp_phone_entry.pack()     

   
def Customer_window():
    Window.title("CUSTOMER WINDOW - T. NIVEDHA")
    Customer_window_frame=Toplevel(Window) #define a frame for placing the widgets,but top level object does not have pack() method
    labelC=Label(Customer_window_frame,text=" CUSTOMER REGISTER / VIEW ",font='arial 20 bold', bg='light green')
    labelC.pack(pady=30)
    b1=Button(Customer_window_frame, text="Customer Registration",font="arial 20 bold",bg='cyan',command=lambda: Customer_Register_ShowDetails(1))
    #store button will be disabled if 0 is passed, enabled if 1 is passed
    b2=Button(Customer_window_frame, text="     Place Order     ",font="arial 20 bold",bg='cyan',command=lambda: Cust_order())
    b3=Button(Customer_window_frame, text="View Accepted Order",font="arial 20 bold",bg='cyan',command=lambda: CustomerView_AcceptedOrder())
    b4=Button(Customer_window_frame, text="Exit",font='arial 20 bold',command=Customer_window_frame.destroy,bg='violet')
   
    # Buttons on the left side, fill vertical space
    for button in (b1, b2, b3):
        button.pack(pady=10)  # Pack to left, fill vertically with padding
  
def Restaurant_window():
    Window.title("RESTAURANT WINDOW - T. NIVEDHA")
    Restaurant_window_frame = Toplevel(Window) #define a frame for placing the widgets,but top level object does not have pack() method 
    ###This frame will be displayed at the top of the Window instance. should not use pack()
    labelR=Label(Restaurant_window_frame,text="  RESTAURANT MANAGER SYSYEM  ",font='arial 25 bold', bg='light blue')
    labelR.pack(pady=20)
    rest_but1=Button(Restaurant_window_frame,text="Add / View List of Foods Available",font="arial 20 bold",bg='cyan',command=lambda: Add_food_list())
    rest_but2=Button(Restaurant_window_frame,text=" Register / View Employee Details ",font="arial 20 bold",bg='cyan',command=lambda: Employee_Register_OR_Show()) 
    rest_but3=Button(Restaurant_window_frame,text="          Manage Orders           ",font="arial 20 bold",bg='cyan',command=lambda: Rest_manageOrder())
    rest_but4=Button(Restaurant_window_frame,text="View Customer Registration Details",font="arial 20 bold",bg='cyan',command=lambda: Customer_Register_ShowDetails(2))
    rest_but5=Button(Restaurant_window_frame,text="Exit",font='arial 20 bold',command=Restaurant_window_frame.destroy,bg='violet')
    
    # Buttons on the left side, fill vertical space
    for button in (rest_but1,rest_but2, rest_but3, rest_but4,rest_but5):
        button.pack(pady=10)  # Pack to left, fill vertically with padding


def Main_window():
    Window.title("MAIN WINDOW - T. NIVEDHA")
    #Label for the main window should use only Window instance i.e it will be displayed in main window tilte
    Window_label=Label(Window,text="   FOOD ORDERING SYSTEM   ",font="arial 40 bold",bg='light blue')
    Window_label.pack(pady=40) 
    #This frame also uses Windows instance i.e. it will be displayed in the Main window
    Main_window_frame=Frame(Window) #define a frame for looping
    
    ###b1=Button(Main_window_frame,text="Restaurant",font="arial 20 bold",bg='cyan',command=lambda: Restaurant_window()) 
    ###Frame name should not be given in button class for this menu window because they are to be placed in Window instance    
    b1=Button(text="Restaurant",font="arial 20 bold",bg='cyan',command=lambda: Restaurant_window()) 
    b2=Button(text="Customer",font="arial 20 bold",bg='cyan',command=lambda: Customer_window())
    b3=Button(text="Exit",font='arial 20 bold',command=Window.destroy,bg='violet')
   
    # Buttons on the left side, fill vertical space
    for button in (b1, b2, b3):
        button.pack(pady=10)  # Pack to left, fill vertically with padding

    Main_window_frame.mainloop()   ###This should not be removed

Main_window()









