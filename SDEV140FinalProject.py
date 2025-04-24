'''
Auther: Gillian Rice
Date: 4/22/2025
This is my final project. It is a restraunt managment system for a coffee shop.
'''

import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Registration")
window.geometry("275x250")
window.resizable(False,False)

# Defines the funtion to control the login form and registration forms
def showlogin():
    loginform()# Showing the login form
    window.withdraw()# Hides the registration form

# Defining a function to hold the log in form to allow it to be called anytime
def loginform():
    loginwindow = tk.Toplevel()
    loginwindow.title("Login")
    loginwindow.geometry("250x130")
    loginwindow.resizable(False,False)

    def login():
        # Validation for login
        username = user_entry.get()
        password = password_entry.get()

        # Checking the file in read mode
        employeesData = open("employees.txt", "r")
        # Reading the lines into a list
        allEmployees = employeesData.readlines()
        employeesData.close()
        for each in range(len(employeesData)):
            if username in allEmployees[each] and password in allEmployees[each]:
                allInfo = allEmployees[each].split(",")
                if allInfo[3] == username and allInfor[4].strip("\n") == password:
                    messagebox.showinfo("Success", "Login completed")
                    break
                else:
                    messaagebox.showerror("Failed", "Login Failed")
                    return
            else:
                messagebox.showerror("Failed", "Login Failed")
                return

def save_infomation():
    # Retreive all entries
    fName = fName_entry.get().strip()
    lName = lName_entry.get().strip()
    email = email_entry.get().strip()
    emailCheck = emailCheck_entry.get().strip()
    username = user_entry.get()
    password = password_entry.get()
    conpass = conpass.entry.get()

    # See if all entries are completed
    if not fName or not lName or not email or not username or not password or not conpass:
        messagebox.showerror("Check Entries", "All fields are required")
    # Ensure that password matches
    elif password != conpass:
        messagebox.showerror("Check Password", "Passwords enterd need to match")
    # Check to ensure password lengh is 8 characters or more
    elif len(password) < 8:
        messagebox.showerror("Check Password", "The Password needs to be at least characters")
    # Checking that the email has the correct formating
    elif "@" not in email or "." not in email:
        messagebox.showerror("Check Email", "The email needs to contain the @ symbol and the . symbol")
    # Checking that the email and the check email match
    elif email != emailCheck:
        messagebox.showerror("Check Email Entries", "Emails need to match")
    else:
        # Saving info in file
        # Create the file object
        regdata = open("employees.txt", "a")
        regdata.write(fName + ",")
        regdata.write(lName + ",")
        regdata.write(email + ",")
        regdata.write(username + ",")
        regdata.write(password + "\n")
        regdata.close()

        messagebox.showinfo("Information", "Employee Registration is Complete")
        # Clearing all fields to prevent mistakes
        fName_entry.delete(0, tk.END)
        lName_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        emailCheck_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        conpass_entry.delete(0, tk.END)

# Creating the labels
fNamelabel = tk.Label(window, text="First Name", justify="left")
fNamelabel.grid(row=0, column=0, padx=10, pady=10)

lNamelabel = tk.Label(window, text="Last Name", justify="left")
lNamelabel.grid(row=1, column=0, padx=10, pady=10)

emaillabel = tk.Label(window, text="Email", justify="left")
emaillabel.grid(row=2, column=0, padx=10, pady=10)

emailChecklabel = tk.Label(window, text="Confirm Email", justify="left")
emailChecklabel.grid(row=3, column=0, padx=10, pady=10)

usernamelabel = tk.Label(window, text="Username", justify="left")
usernamelabel.grid(row=4, column=0, padx=10, pady=10)

passwordlabel = tk.Label(window, text="Password", justify="left")
passwordlabel.grid(row=5, column=0, padx=10, pady=10)

conpasslabel = tk.Label(window, text="Check Password", justify="left")
conpasslabel.grid(row=6, column=0, padx=10, pady=10)

# Creating entry boxes

fName_entry = tk.Entry(window)
fName_entry.grid(row=0, column=1)

lName_entry = tk.Entry(window)
lName_entry.grid(row=1, column=1)

email_entry = tk.Entry(window)
email_entry.grid(row=2, column=1)

emailCheck_entry = tk.Entry(window)
emailCheck_entry.grid(row=3, column=1)

username_entry = tk.Entry(window)
username_entry.grid(row=4, column=1)

password_entry = tk.Entry(window)
password_entry.grid(row=5, column=1)
    
conpass_entry = tk.Entry(window)
conpass_entry.grid(row=6, column=1)

# Creating a submit button
submitButton = tk.Button(window, text="Submit", justify="left", command=save_information)
submit_button.grid(row=7, column=1, columnspan=2)

# Button link to login
login_button = tk.Button(window, text="->", justify="left", command=showlogin)
login_button.grid(row=7, column=2, columnspan=2)

window.mainloop()
    





















                



