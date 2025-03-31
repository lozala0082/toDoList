from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
import sqlite3


# Function for login attempts
# -------------------------------------------------------------------------
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if either of the fields is empty
    if not username or not password:
        messagebox.showerror("ERROR", "Both fields are required!")
        return

    # Connect to database
    conn = sqlite3.connect('toDoDesktop.db')
    cursor = conn.cursor()

    # Query the database to check if the username exist
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user is None:
        messagebox.showerror("ERROR", "USERNAME NOT FOUND")  # If username is not found
    elif user[4] != password:
        messagebox.showerror("ERROR",
                             f"INCORRECT PASSWORD FOR {username}!")  # If password is wrong but username is correct
    else:
        messagebox.showinfo("SUCCESS!", f"Welcome {username}")  # If correct credentials were entered

    conn.close()
# -------------------------------------------------------------------------


# Function for login attempts
# -------------------------------------------------------------------------
def create_accounts():
    firstname = first_name_entry.get()
    lastname = last_name_entry.get()
    create_username = create_user_entry.get()
    create_password = create_psswrd_entry.get()

    # Check if either of the fields is empty
    if not firstname or not lastname or not create_username or not create_password:
        messagebox.showerror("ERROR", "All fields are required!")
        return

    # Connect to the database
    conn = sqlite3.connect("toDoDesktop.db")
    cursor = conn.cursor()

    try:
        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (create_username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("ERROR", "Username already exists! Choose a different one.")
            return

        # Insert the new user into the user table
        cursor.execute("INSERT INTO users (firstname, lastname, username, password) VALUES (?, ?, ?, ?)",
                   (firstname, lastname, create_username, create_password))
        conn.commit()  # Save the changes

        messagebox.showinfo("SUCCESS!", f"Account created successfully for {create_username}!")

        # Clear the input fields after successful registration
        first_name_entry.delete(0, 'end')
        last_name_entry.delete(0, 'end')
        create_user_entry.delete(0, 'end')
        create_psswrd_entry.delete(0, 'end')

        # Go back to the login
        show_login()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        conn.close()  # Close the connection

# Function to display the labels and entries to create a new user
# -------------------------------------------------------------------------
def create_labels():
    # Hide existing login widgets
    username_label.place_forget()
    username_entry.place_forget()
    password_label.place_forget()
    password_entry.place_forget()
    login_button.place_forget()
    create_button.place_forget()

    # Create new user fields
    global new_user_widgets  # Store new widgets for later reference
    new_user_widgets = []

    global first_name_entry, last_name_entry, create_user_entry, create_psswrd_entry  # Declare as global


    create_message_label = Label(root, text="Enter Your Information Below:", font=("Arial", 14, "bold"))
    create_message_label.place(x=500, y=300)
    new_user_widgets.append(create_message_label)


    firstname_label = Label(root, text="First Name:", font=("Arial", 14))
    firstname_label.place(x=500, y=350)
    new_user_widgets.append(firstname_label)

    first_name_entry = Entry(root, font=("Arial", 14), width=20)
    first_name_entry.place(x=660, y=350)
    new_user_widgets.append(first_name_entry)

    lastname_label = Label(root, text="Last Name:", font=("Arial", 14))
    lastname_label.place(x=500, y=400)
    new_user_widgets.append(lastname_label)

    last_name_entry = Entry(root, font=("Arial", 14), width=20)
    last_name_entry.place(x=660, y=400)
    new_user_widgets.append(last_name_entry)

    create_user_label = Label(root, text="Create Username:", font=("Arial", 14))
    create_user_label.place(x=500, y=450)
    new_user_widgets.append(create_user_label)

    create_user_entry = Entry(root, font=("Arial", 14), width=20)
    create_user_entry.place(x=660, y=450)
    new_user_widgets.append(create_user_entry)


    create_psswrd_label = Label(root, text="Create Password:", font=("Arial", 14))
    create_psswrd_label.place(x=500, y=500)
    new_user_widgets.append(create_psswrd_label)

    create_psswrd_entry = Entry(root, font=("Arial", 14), width=20, show='*')
    create_psswrd_entry.place(x=660, y=500)
    new_user_widgets.append(create_psswrd_entry)

    # Button to go back to login screen
    back_button = Button(root, text="Back to Login", font=("Arial", 14), command=show_login)
    back_button.place(x=550, y=550)
    new_user_widgets.append(back_button)

    # Send the info to create_accounts function so it can append the info to the sql database
    create_account_button = Button(root, text="Create Account", font=("Arial", 14), command=create_accounts)
    create_account_button.place(x=650, y=600)
    new_user_widgets.append(create_account_button)

# -------------------------------------------------------------------------


# Function to bring back login widgets
# -------------------------------------------------------------------------
def show_login():
    # Hide new user widgets
    for widget in new_user_widgets:
        widget.place_forget()

    # Show login widgets again
    username_label.place(x=500, y=300)
    username_entry.place(x=600, y=300)
    password_label.place(x=500, y=350)
    password_entry.place(x=600, y=350)
    login_button.place(x=500, y=400)
    create_button.place(x=600, y=400)
# -------------------------------------------------------------------------


# Creating the main window widget
root = Tk()

# Brings the window to fullscreen
root.state('zoomed')
# Set the window title
root.title("To Do List")


# Name of Application Widget
#-------------------------------------------------------------------------
name_label = Label(root, text="The To Do List", font=("Comic Sans MS", 40, "bold"))
name_label.place(x=400, y=200)
#-------------------------------------------------------------------------


# Logo Image Widget
#-------------------------------------------------------------------------
logoimage = Image.open("todolist.png")
logoimage = logoimage.resize((100, 100), Image.Resampling.LANCZOS)

# Convert the image to a Tkinter-compatible format
logophoto = ImageTk.PhotoImage(logoimage)

# Create a Label widget to hold the image
logo_pic_label = Label(root, image=logophoto)
logo_pic_label.place(x=800, y=188)
#-------------------------------------------------------------------------


# Boss Image Widget
#-------------------------------------------------------------------------
bossimage = Image.open("bosscat.png")

# Convert the image to a Tkinter-compatible format
bossphoto = ImageTk.PhotoImage(bossimage)

# Create a Label widget to hold the image
boss_pic_label = Label(root, image=bossphoto)
boss_pic_label.place(x=-5, y=470)
#-------------------------------------------------------------------------


# Textbox Image Widget
#-------------------------------------------------------------------------
textboximage = Image.open("textbox.png")
textboximage = textboximage.resize((200, 200), Image.Resampling.LANCZOS)

# Convert the image to a Tkinter-compatible format
textphoto = ImageTk.PhotoImage(textboximage)

# Create a Label widget to hold the image
text_pic_label = Label(root, image=textphoto)
text_pic_label.place(x=200, y=380)
#-------------------------------------------------------------------------



# Username and password login
#-------------------------------------------------------------------------
username_label = Label(root, text="Username:", font=("Arial", 14))
username_label.place(x=500, y=300)

username_entry = Entry(root, font=("Arial", 14), width=20)
username_entry.place(x=600, y=300)

password_label = Label(root, text="Password:", font=("Arial", 14))
password_label.place(x=500, y=350)

password_entry = Entry(root, font=("Arial", 14), width=20, show="*")  # 'show' hides the password
password_entry.place(x=600, y=350)

#Create the Login button
login_button = Button(root, text="Login", font=("Arial", 14), command=login)
login_button.place(x=500, y=400)
#-------------------------------------------------------------------------


# Create user account
#-------------------------------------------------------------------------
#Create the create button
create_button = Button(root, text="Create New Account", font=("Arial", 14), command=create_labels)
create_button.place(x=600, y=400)


#-------------------------------------------------------------------------

# Run the code
root.mainloop()
