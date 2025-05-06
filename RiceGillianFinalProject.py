'''
File: 
Auther: Gillian Rice
Date: 4/22/2025
Description: It is a restraunt managment system for a coffee shop. Employees
can be added tothe software and them used to login. Once loged in the items
can be added tocart and checkedout. This will print a reciet and store the
information in aunique file.
'''
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, PhotoImage
from datetime import datetime

# Creating the main window
window = tk.Tk()
window.title("Registration")
window.geometry("400x300")
window.resizable(False,False)

# Setting a cleaner theme
style = ttk.Style()
style.theme_use("vista")

def showlogin():
    # Defines the funtion to control the login form and registration forms
    loginform()# Showing the login form
    window.withdraw()# Hides the registration form

def loginform():
    # Defining a function to hold the log in form to allow it to be called anytime
    # Creating the window
    loginwindow = tk.Toplevel()
    loginwindow.title("Login")
    loginwindow.geometry("250x130")
    loginwindow.resizable(False,False)

    # Creating a label and entry for the username
    user_label = ttk.Label(loginwindow, text="Username").grid(row=0, column=0)
    user_entry = ttk.Entry(loginwindow)
    user_entry.grid(row=0, column=1)

    # Creating a label and entry for the password
    ttk.Label(loginwindow, text="Password").grid(row=1, column=0)
    password_entry = ttk.Entry(loginwindow, show="*")
    password_entry.grid(row=1, column=1)

    def login():
        # Validation for login
        username = user_entry.get().strip()
        password = password_entry.get().strip()
        
        # Checking the file (open in read mode)
        try:
            with open("employees.txt", "r") as employeesData:
                allEmployees = employeesData.readlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "Employee data file not found.")
            return

        # Testing if the information is stored in the list
        for each in allEmployees:
            allInfo = each.strip().split(",")
            if len(allInfo) >= 5 and allInfo[3] == username and allInfo[4] == password:
                messagebox.showinfo("Success", "Login completed")
                ordermenu(username)
                return
            
        messagebox.showerror("Failed", "Login Failed")# Letting them know they failed

    ttk.Button(loginwindow, text="Login", command=login).grid(row=2, column=1)# A button to login

def save_information():
    # Saves all information and test it to ensure all of the data meets the criteria
    
    # Retreive all entries
    fName = fName_entry.get().strip()
    lName = lName_entry.get().strip()
    email = email_entry.get().strip()
    emailCheck = emailCheck_entry.get().strip()
    username = username_entry.get()
    password = password_entry.get()
    conpass = conpass_entry.get()

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

def ordermenu(username):
    # Window settings
    orderwindow = tk.Toplevel()
    orderwindow.title("Order Menu")
    orderwindow.geometry("425x650")
    orderwindow.resizable(False,False)

    # Dictonary to hold the items with there prices
    cart = {}

    # Frame to hold text and the scrollbar
    textframe = tk.Frame(orderwindow)
    textframe.grid(row=6, column=0, columnspan=3, pady=10)

    # Scrollbar
    scrollbar = tk.Scrollbar(textframe)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Text widget
    cartdisplay = tk.Text(textframe, height=10, width=50, state="disabled", yscrollcommand=scrollbar.set)
    cartdisplay.pack(side=tk.LEFT)

    # Configure scrollbar
    scrollbar.config(command=cartdisplay.yview)
    
    # This updates the cart display listed above when items are added
    def updateCartDisplay():
        cartdisplay.config(state="normal") # Enables editing in the cartdisplay text widget
        cartdisplay.delete("1.0", tk.END) # Clears any existing text from the widget
        total = 0 # Initializing total and setting it to 0
        for item, details in cart.items(): # iterates over each item in the cart dicionary
            line = f"{item}: ${details['price']} x {details['quantity']} = ${details['price'] * details['quantity']:.2f}\n"
            cartdisplay.insert(tk.END, line) # Inserts the line into the cart display widget
            total += details['price'] * details['quantity'] # Adds everything
        cartdisplay.insert(tk.END, f"\nTotal: ${total:.2f}") # Adds the final total price to the bottom of the display
        cartdisplay.config(state='disabled') # Makes the cartdisplay text widget read-only agian
        
    def addcart(itemName, price):
        # If more than one item is added the if statement will catch it and add it
        if itemName in cart:
            cart[itemName]['quantity'] += 1
        else:
            cart[itemName] = {"price": price, "quantity": 1}
        updateCartDisplay() # Calls the funtion 

    def checkout():
        
        if not cart: #Checks if the cart is empty 
            tk.messagebox.showinfo("Checkout", 'The cart is empty.')
            return
        
        print("Final Order:") # Displays the final order in the console
        total = 0 # Initializing total as 0
        orderlines = [] # Creating a list to store information in the file

        # Get the current time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Initalizes the time when the order was made
        filename = f"order-{username}_{timestamp}.txt" # Creates a unique file and initializes it
        orderlines.append(f"--- Order by {username} on {timestamp} ---\n")# Appends the username and the timestamp into the file
        
        for item, details in cart.items(): # Loops through each item in the cart, prints item details to th econsole and adds the price * quantiy to the total
            orderlines.append(f"{item}: ${details['price']} x {details['quantity']}")
            total += details['price'] * details['quantity']
        print(f"Total: ${total:.2f}")

        # Appending this information into the text file
        orderlines.append(f"Total: ${total:.2f}\n")
        orderlines.append("-" * 40 + "\n")

        # Write to file
        with open(filename, "w") as f:
            f.writelines(orderlines)

        tk.messagebox.showinfo("Checkout", f"Total: ${total:.2f}\nThank you for your order!") # Informs you that the checkout is complete along with the total price

    def clearCart():
        # Clear the cart and the display
        cart.clear()
        updateCartDisplay()
        tk.messagebox.showinfo("Cart Cleared", "Your cart has been emptied.")

    # Creating all of the buttons with photos
    # The first one is broken down to show how it works

    # Creating the latte button with an image
    latte_img = tk.PhotoImage(file="latteimage.png") # Loads the image file into a PhotoImage object, this will display the image on the button
    latteButton = ttk.Button(orderwindow, text="Latte", image=latte_img, compound='top', command=lambda: addcart("Latte", 6.75)) # Creates a ttk.Button, sets the button label, displays the image on the button, places the image above the text, when clicked it will call the addcart function with the "Latte" and a price of 6.65
    latteButton.image = latte_img # Stores teh image in the button object to prevent it from being garbage collected
    latteButton.grid(row=0, column=0) # Places the button in the top-left cell of the window layout using the grid geometry manager

    americano_img = tk.PhotoImage(file="americanoimage.png")
    americanoButton = ttk.Button(orderwindow, text="Americano", image=americano_img, compound='top', command=lambda: addcart("Americano", 5.25))
    americanoButton.image = americano_img
    americanoButton.grid(row=0, column=1)

    expresso_img = tk.PhotoImage(file="expressoimage.png")
    expressoButton = ttk.Button(orderwindow, text="Expresso", image=expresso_img, compound='top', command=lambda: addcart("Expresso", 5.25))
    expressoButton.image = expresso_img
    expressoButton.grid(row=0, column=2)

    mocha_img = tk.PhotoImage(file="mochaimage.png")
    mochaButton = ttk.Button(orderwindow, text="Mocha", image=mocha_img, compound='top', command=lambda: addcart("Mocha", 6.75))
    mochaButton.image = mocha_img
    mochaButton.grid(row=1, column=0)

    dirty_img = tk.PhotoImage(file="dirtyimage.png")
    dirtyButton = ttk.Button(orderwindow, text="Dirty", image=dirty_img, compound='top', command=lambda: addcart("Dirty", 6.75))
    dirtyButton.image = dirty_img
    dirtyButton.grid(row=1, column=1)

    coldbrew_img = tk.PhotoImage(file="coldbrewimage.png")
    coldbrewButton = ttk.Button(orderwindow, text="Cold Brew", image=coldbrew_img, compound='top', command=lambda: addcart("Cold Brew", 6.75))
    coldbrewButton.image = coldbrew_img
    coldbrewButton.grid(row=1, column=2)

    cappuccino_img = tk.PhotoImage(file="cappuccinoimage.png")
    cappuccinoButton = ttk.Button(orderwindow, text="Cappuccino", image=cappuccino_img, compound='top', command=lambda: addcart("Cappuccino", 7.00))
    cappuccinoButton.image = cappuccino_img
    cappuccinoButton.grid(row=2, column=0)

    cocoa_img = PhotoImage(file='cocoaimage.png')
    cocoaButton = ttk.Button(orderwindow, text="Cocoa", image=cocoa_img, compound='top', command=lambda: addcart("Cocoa", 5.25))
    cocoaButton.image = cocoa_img
    cocoaButton.grid(row=2, column=1)

    blacktea_img = PhotoImage(file='blackteaimage.png')
    blackteaButton = ttk.Button(orderwindow, text="Black Tea", image=blacktea_img, compound='top',  command=lambda: addcart("Black Tea", 5.25))
    blackteaButton.image = blacktea_img
    blackteaButton.grid(row=2, column=2)

    greentea_img = PhotoImage(file='greenteaimage.png')
    greenteaButton = ttk.Button(orderwindow, text="Green Tea", image=greentea_img, compound='top', command=lambda: addcart("Green Tea", 5.75))
    greenteaButton.image = greentea_img
    greenteaButton.grid(row=3, column=0)

    herbaltea_img = PhotoImage(file='herbalteaimage.png')
    herbalteaButton = ttk.Button(orderwindow, text="Herbal Tea", image=herbaltea_img, compound='top', command=lambda: addcart("Herbal Tea", 6.75))
    herbalteaButton.image = herbaltea_img
    herbalteaButton.grid(row=3, column=1)

    chaitea_img = PhotoImage(file='chaiteaimage.png')
    chaiteaButton = ttk.Button(orderwindow, text="Chai Tea", image=chaitea_img, compound='top', command=lambda: addcart("Chai Tea", 7.75))
    chaiteaButton.image = chaitea_img
    chaiteaButton.grid(row=3, column=2)

    brownie_img = PhotoImage(file='brownieimage.png')
    brownieButton = ttk.Button(orderwindow, text="Brownie", image=brownie_img, compound='top', command=lambda: addcart("Brownie", 5.25))
    brownieButton.image = brownie_img
    brownieButton.grid(row=4, column=0)

    muffin_img = PhotoImage(file='muffinimage.png')
    muffinButton = ttk.Button(orderwindow, text="Muffin", image=muffin_img, compound='top', command=lambda: addcart("Muffin", 6.75))
    muffinButton.image = muffin_img
    muffinButton.grid(row=4, column=1)

    cookie_img = PhotoImage(file='cookieimage.png')
    cookieButton = ttk.Button(orderwindow, text="Cookie", image=cookie_img, compound='top', command=lambda: addcart("Cookie", 4.75))
    cookieButton.image = cookie_img
    cookieButton.grid(row=4, column=2)

    # This button uses the command clearCart to clear the cart and dicionary
    clearButton = ttk.Button(orderwindow, text="Clear Cart", command=clearCart)
    clearButton.grid(row=5, column=0, padx=5, pady=5) # Places it within the grid

    # A button that uses the command checkout to function
    checkoutButton = ttk.Button(orderwindow, text="Checkout", command=checkout)
    checkoutButton.grid(row=5, column=1, padx=5, pady=5) # Places it within the grid

    # The exit button destroys the orderwindow when pressed
    exitButton = ttk.Button(orderwindow, text="Exit", command=orderwindow.destroy)
    exitButton.grid(row=5, column=2, padx=5, pady=5) # Places it within the grid

# Creating the labels
fNamelabel = ttk.Label(window, text="First Name", justify="left")
fNamelabel.grid(row=0, column=0, padx=10, pady=10)

lNamelabel = ttk.Label(window, text="Last Name", justify="left")
lNamelabel.grid(row=1, column=0, padx=10, pady=10)

emaillabel = ttk.Label(window, text="Email", justify="left")
emaillabel.grid(row=2, column=0, padx=10, pady=10)

emailChecklabel = ttk.Label(window, text="Confirm Email", justify="left")
emailChecklabel.grid(row=3, column=0, padx=10, pady=10)

usernamelabel = ttk.Label(window, text="Username", justify="left")
usernamelabel.grid(row=4, column=0, padx=10, pady=10)

passwordlabel = ttk.Label(window, text="Password", justify="left")
passwordlabel.grid(row=5, column=0, padx=10, pady=10)

conpasslabel = ttk.Label(window, text="Check Password", justify="left")
conpasslabel.grid(row=6, column=0, padx=10, pady=10)

# Creating entry boxes

fName_entry = ttk.Entry(window)
fName_entry.grid(row=0, column=1)

lName_entry = ttk.Entry(window)
lName_entry.grid(row=1, column=1)

email_entry = ttk.Entry(window)
email_entry.grid(row=2, column=1)

emailCheck_entry = ttk.Entry(window)
emailCheck_entry.grid(row=3, column=1)

username_entry = ttk.Entry(window)
username_entry.grid(row=4, column=1)

password_entry = ttk.Entry(window)
password_entry.grid(row=5, column=1)
    
conpass_entry = ttk.Entry(window)
conpass_entry.grid(row=6, column=1)

# Creating a submit button
submitButton = ttk.Button(window, text="Submit", command=save_information)
submitButton.grid(row=7, column=1, columnspan=2)

# Button link to login
login_button = ttk.Button(window, text="->", command=showlogin)
login_button.grid(row=7, column=2, columnspan=2)

window.mainloop() # Starts the main loop for the application
