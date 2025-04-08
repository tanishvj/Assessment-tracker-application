# Tanishka Vijay, 21048, Creating an app for the yr 13 physics students to help them keep track of their assessments
# Prototype 3
# Changes/ additions:
#   Notifiaction of due date popup (adding functionality)
#   Placement of logout button (observation)
#   Switch the new assessment button to an icon (feedback)

import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

# Standard details dictionary
standard_details = {
    "91521": {"Name": "Carry out a practical investigation to test a physics theory relating two variables in a non-linear relationship",
               "Credits": 4,
               "Type": "Internal"},
    "91522": {"Name": "Demonstrate understanding of the application of physics to a selected context",
               "Credits": 3,
               "Type": "Internal"},
    "91523": {"Name": "Demonstrate understanding of wave systems", 
              "Credits": 4, 
              "Type": "External"},
    "91524": {"Name": "Demonstrate understanding of mechanical systems", 
              "Credits": 6, 
              "Type": "External"},
    "91525": {"Name": "Demonstrate understanding of modern physics", 
              "Credits": 3, 
              "Type": "Internal"},
    "91526": {"Name": "Demonstrate understanding of electrical systems", 
              "Credits": 6, 
              "Type": "External"},
    "91527": {"Name": "Use physics knowledge to develop an informed response to a socio-scientific issue", 
              "Credits": 3, 
              "Type": "Internal"},
}


assessments_list = []  
toggle_menu = None
logged_in_user = None 
as_name_to_number = {details["Name"]: as_number for as_number, details in standard_details.items()} 

def register():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Registration Failed", "Username and password cannot be empty.")
        return

    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                stored_username, _ = user.split(',')
                if stored_username.strip() == username:
                    messagebox.showwarning("Registration Failed", "Username already exists!")
                    return

    with open('users.txt', 'a') as file:
        file.write(f"{username},{password}\n")

    messagebox.showinfo("Registration Success", "Registration successful! You can now log in.")


def login():
    global logged_in_user, assessments_list
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Login Failed", "Please fill all fields")
        return

    if not os.path.exists('users.txt'):
        messagebox.showerror("Login Failed", "No users registered yet.")
        return

    with open('users.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            stored_username, stored_password = user.strip().split(',')
            if stored_username == username and stored_password == password:
                logged_in_user = username
                messagebox.showinfo("Login Success", "Login successful!")
                load_user_assessments()
                show_assessment_page()
                check_due_dates() # Check for due dates
                return

    messagebox.showerror("Login Failed", "Invalid username or password.")


def load_user_assessments():
    global assessments_list
    assessments_list = []
    user_file = f"{logged_in_user}_assessments.txt"
    
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            for line in file:
                as_number, as_name, as_credits, as_type, due_date, test_type = line.strip().split('|')
                assessments_list.append({
                    "AS Number": as_number,
                    "Name": as_name,
                    "Credits": as_credits,
                    "Type": as_type,
                    "Due Date": due_date,
                    "Test Type": test_type
                })


def save_user_assessments():

    if not logged_in_user:
        return

    user_file = f"{logged_in_user}_assessments.txt"
    with open(user_file, "w") as file:
        for assessment in assessments_list:
            file.write(f'{assessment["AS Number"]}|{assessment["Name"]}|{assessment["Credits"]}|{assessment["Type"]}|{assessment["Due Date"]}|{assessment["Test Type"]}\n')


def create_login_frame():
    global entry_username, entry_password, login_frame


    login_frame = tk.Frame(root)
    login_frame.pack(expand=True)
    login_frame.configure(background= '#B02324')


    app_title = tk.Label(login_frame, text="Assessment Manager", font=("Arial", 30, "bold"), fg='#E6E6E6', bg='#B02324')
    app_title.pack(pady=50)

    label_username = tk.Label(login_frame, text="Username:", font=(24), fg='#E6E6E6')
    label_username.pack()
    label_username.configure(background= '#B02324')


    entry_username = tk.Entry(login_frame, bg="#B02324", fg='#E6E6E6', relief="flat", font=(24))
    entry_username.pack(fill="x", padx=20)

    username_underline = tk.Frame(login_frame, height=2, bg="#E6E6E6")
    username_underline.pack(fill="x", padx=20, pady=(0, 10))

    label_password = tk.Label(login_frame, text="Password:", font=(24), fg='#E6E6E6')
    label_password.pack()
    label_password.configure(background= '#B02324')

    entry_password = tk.Entry(login_frame, show="*", bg="#B02324", fg='#E6E6E6', relief="flat", font=(24))
    entry_password.pack(fill="x", padx=20)

    password_underline = tk.Frame(login_frame, height=2, bg="#E6E6E6")
    password_underline.pack(fill="x", padx=20, pady=(0, 10))

    button_frame = tk.Frame(login_frame, bg='#B02324')
    button_frame.pack(pady=10)

    btn_login = tk.Button(button_frame, text="Login", command=login, bg='#B02324', fg='#253B80', width=8, relief="flat", font=(24))
    btn_login.pack(side=tk.LEFT, padx=10)

    btn_register = tk.Button(button_frame, text="Register", command=register, bg='#B02324', fg='#253B80', width=8, relief="flat", font=(24))
    btn_register.pack(side=tk.LEFT, padx=10)


def show_assessment_page():
    global assessment_frame

    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    login_frame.pack_forget()

    side_bar()

    assessment_frame = tk.Frame(root, background='#B02324', highlightthickness=0, bd=0)
    assessment_frame.pack(fill='both', expand=True)

    columns = ("AS Number", "Name", "Credits", "Type", "Due Date", "Test Type")

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", background="#B02324", fieldbackground="#B02324",
                    foreground="white", borderwidth=0, relief="flat", font=("Arial", 18, "bold"), rowheight=30)  
    style.configure("Treeview.Heading", background="#253B80", foreground="white", font=("Arial", 18, "bold"))
    
    style.map("Treeview", background=[('selected', '#B02324')])  
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  

    tree_frame = tk.Frame(assessment_frame, bg='#B02324', highlightthickness=0, bd=0)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")
    tree.pack(fill="both", expand=True)

    column_widths = [100, 600, 100, 100, 150, 150]
    for col, width in zip(columns, column_widths):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=width, stretch=True)

    for assessment in assessments_list:
        tree.insert("", "end", values=(
            assessment["AS Number"],
            assessment["Name"],
            assessment["Credits"],
            assessment["Type"],
            assessment["Due Date"],
            assessment["Test Type"]
        ))

    # Create a canvas to draw the circle
    canvas = tk.Canvas(assessment_frame, width=120, height=120, bg="#B02324", bd=0, highlightthickness=0)
    canvas.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Positioning the canvas at the bottom-right corner

# Draw a circle on the canvas
    canvas.create_oval(10, 10, 110, 110, outline="#253B80", width=5, fill="#253B80")  # Circle outline

# Create a button and place it in the center of the circle
    circle_button = tk.Button(canvas, text="+", font=('Arial', 30), fg='white', bg='#253B80', relief='flat', command=new_assessment)
    circle_button.place(relx=0.5, rely=0.5, anchor='center')  # Center the button within the circle


def check_due_dates():
    if not assessments_list:
        return

    upcoming = []
    today = datetime.today()

    for assessment in assessments_list:
        try:
            due_date = datetime.strptime(assessment["Due Date"], "%d-%m-%Y")
            days_left = (due_date - today).days
            if 0 <= days_left <= 1:
                upcoming.append(f"{assessment['Name']} is due in {days_left} day(s) on {assessment['Due Date']}")
        except Exception as e:
            print("Error parsing date:", assessment["Due Date"], e)

    if upcoming:
        messagebox.showwarning("Upcoming Assessments", "\n".join(upcoming))


def new_assessment():
    global new_assessment_frame, name_var, number_var, credits_var, type_var

    assessment_frame.pack_forget()

    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    side_bar()

    new_assessment_frame = tk.Frame(root)
    new_assessment_frame.pack(expand=True)
    new_assessment_frame.configure(background='#B02324')

    label_welcome = tk.Label(new_assessment_frame, text="Enter New Assessment", font=("Arial", 16,))
    label_welcome.pack(pady=20)
    label_welcome.configure(background='#B02324')


    tk.Label(new_assessment_frame, text="AS Number:", background= '#B02324').pack(pady=5)
    number_var = tk.StringVar()
    number_dropdown = ttk.Combobox(new_assessment_frame, textvariable=number_var, values=list(standard_details.keys()), state="readonly")
    number_dropdown.set("Select AS Number")
    number_dropdown.pack(pady=5)

    max_length = max(len(details["Name"]) for details in standard_details.values())

    tk.Label(new_assessment_frame, text="AS Name:", background= '#B02324').pack(pady=5)
    name_var = tk.StringVar()
    name_dropdown = ttk.Combobox(new_assessment_frame, textvariable=name_var, values=[details["Name"] for details in standard_details.values()], state="readonly", width=max_length)
    name_dropdown.set("Select AS Name")
    name_dropdown.pack(pady=5)

    name_dropdown.bind("<<ComboboxSelected>>", lambda event: update_categories(event, name_var, number_var, name_var, credits_var, type_var))
    number_dropdown.bind("<<ComboboxSelected>>", lambda event: update_categories(event, number_var, number_var, name_var, credits_var, type_var))

    tk.Label(new_assessment_frame, text="Type:", background= '#B02324').pack(pady=5)
    global type_var
    type_var = tk.StringVar()
    type_entry = tk.Entry(new_assessment_frame, textvariable=type_var, state="readonly")
    type_entry.pack(pady=5)

    tk.Label(new_assessment_frame, text="Credits:", background= '#B02324').pack(pady=5)
    global credits_var
    credits_var = tk.StringVar()
    credit_entry = tk.Entry(new_assessment_frame, textvariable=credits_var, state="readonly")
    credit_entry.pack(pady=5)
     
    tk.Label(new_assessment_frame, text="Due Date:", background= '#B02324').pack(pady=5)
    global due_date_var
    due_date_var = tk.StringVar()
    due_date_entry = DateEntry(new_assessment_frame, textvariable=due_date_var, date_pattern='dd-mm-yyyy')  # Calendar Picker
    due_date_entry.pack(pady=5)

    tk.Label(new_assessment_frame, text="Test Type:", background= '#B02324').pack(pady=5)
    test_var = tk.StringVar(value="Test")
    radio_written = tk.Radiobutton(new_assessment_frame, text="Test", variable=test_var, value="Test", background= '#B02324')
    radio_written.pack(side=tk.TOP, padx=10, pady=5)

    radio_practical = tk.Radiobutton(new_assessment_frame, text="Essay", variable=test_var, value="Essay", background= '#B02324')
    radio_practical.pack(side=tk.TOP, padx=10, pady=5)


    submit_button = tk.Button(new_assessment_frame, text="Submit", command=lambda: add_assessment(number_var, name_var, credits_var, type_var, test_var))
    submit_button.pack(pady=20)


def update_categories_by_number(event, number_var):
    global name_var, credits_var, type_var

    selected_standard = number_var.get()
    if selected_standard in standard_details:
        details = standard_details[selected_standard]
        name_var.set(details["Name"])
        credits_var.set(details["Credits"])
        type_var.set(details["Type"])


def update_categories(event, selection_var, number_var, name_var, credits_var, type_var):

    selected_value = selection_var.get()
    details = None 

    if selected_value in standard_details:  
        details = standard_details[selected_value]
        number_var.set(selected_value)
        name_var.set(details["Name"])
    elif selected_value in as_name_to_number: 
        as_number = as_name_to_number[selected_value]
        details = standard_details[as_number]
        number_var.set(as_number)
        name_var.set(selected_value)

    if details:
        credits_var.set(details["Credits"])
        type_var.set(details["Type"])


def add_assessment(number_var, name_var, credits_var,type_var, test_var):
    global assessments_list

    as_number = number_var.get()
    as_name = name_var.get()
    as_credits = credits_var.get()
    as_type = type_var.get()
    due_date = due_date_var.get()
    test_type = test_var.get()
    
    if not as_number or not as_name or not due_date or not test_type:
        messagebox.showwarning("Input Error", "Please find your assessment first")
        return

    updated = False

    for assessment in assessments_list:
        if assessment["AS Number"] == as_number:
            update = messagebox.askyesno("Update Assessment", "This assessment already exists! Do you want to update the due date and test type?")
            if update:
                assessment["Due Date"] = due_date
                assessment["Test Type"] = test_type
                updated = True  
            break  

    if not updated:
        assessments_list.append({
            "AS Number": as_number,
            "Name": as_name,
            "Credits": as_credits,
            "Type": as_type,
            "Due Date": due_date,
            "Test Type": test_type
        })

    save_user_assessments() 
    messagebox.showinfo("Success", "Assessment saved!")
    show_assessment_page()    


def page_menu():


    def collapse_menu():
        global toggle_menu
        toggle_menu.place_forget()  
        toggle_button.config(text='☰')  
        toggle_button.config(command=expand_menu)  


    def expand_menu():
        global toggle_menu
        
        if toggle_menu is None:
            toggle_menu = tk.Frame(root, bg='#253B80')

        toggle_menu = tk.Frame(root, bg='#253B80')


        main_btn = tk.Button(toggle_menu, text='Home', font=('Bold', 20), bg='#253B80', fg='white', command=show_assessment_page, relief="flat")
        main_btn.place(x=20, y=20)
        
        as_btn = tk.Button(toggle_menu, text='New Assessment', font=('Bold', 20), bg='#253B80', fg='white', command=new_assessment, relief="flat")
        as_btn.place(x=20, y=140)

        # Frame to put logout button in
        bottom_bar = tk.Frame(toggle_menu, bg='#EB9435', height=80)
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Logout button
        logout_btn = tk.Button(bottom_bar, text='Logout', font=('Bold', 20), bg='#EB9435', fg='white', command=logout, relief="flat")
        logout_btn.place(relx=0.5, rely=0.5, anchor='center')

        window_height = root.winfo_height()
        window_width = root.winfo_width()
        toggle_menu.place(x=0, y=50, height=window_height-50, width=window_width * 0.25)

        toggle_button.config(text="X")
        toggle_button.config(command=collapse_menu)  

    expand_menu()
    toggle_button.config(command=collapse_menu)


def side_bar():

    global toggle_button
    head_frame = tk.Frame(root, bg='#253B80', highlightbackground='#253B80', highlightthickness=10,)

    toggle_button = tk.Button(head_frame, text='☰', fg="white", bg="#253B80", font=20, command=page_menu, relief="flat")
    toggle_button.pack(side=tk.LEFT)
   
    head_frame.pack(side=tk.TOP, fill=tk.X)
    head_frame.pack_propagate(False)
   
    head_frame.configure(height=50)


def logout():
    for widget in root.winfo_children():
        widget.destroy()

    create_login_frame()


def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not is_fullscreen)


root = tk.Tk()
root.title("Assessment Manager App")
root.attributes('-fullscreen', True)
root.configure(background= '#B02324')
root.bind("<Escape>", toggle_fullscreen)

create_login_frame()

root.mainloop()