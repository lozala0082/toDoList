import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from datetime import datetime
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the DJANGO_SETTINGS_MODULE environment variable to a placeholder to make Django happy
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shared_db.django_settings')

# Import from shared database
from shared_db.db_manager import DatabaseManager, ASSIGNMENT_STATUSES

# App configuration
APP_TITLE = "Task Management System"
APP_VERSION = "1.0.5"
MAIN_WINDOW_SIZE = "800x600"
ASSIGNMENT_WINDOW_SIZE = "600x400"

class TaskManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_TITLE} v{APP_VERSION}")
        self.db = DatabaseManager()
        self.current_user = None
        self.show_login()

    def show_login(self):
        # Clears anything before getting into this new function
        self.clear_window()
        # Brings the window to fullscreen
        self.root.state('zoomed')  # This simulates the maximize button being clicked

        # Name of Application Widget
        # -------------------------------------------------------------------------
        name_label = Label(self.root, text="The To Do List", font=("Comic Sans MS", 40, "bold"))
        name_label.place(x=400, y=200)
        # -------------------------------------------------------------------------

        # Logo Image Widget
        # -------------------------------------------------------------------------

        self.logoimage = Image.open(os.path.join(os.path.dirname(__file__), "todolist.png"))  # Using correct path
        self.logoimage = self.logoimage.resize((100, 100), Image.Resampling.LANCZOS)

        # Convert the image to a Tkinter-compatible format
        self.logophoto = ImageTk.PhotoImage(self.logoimage)

        # Create a Label widget to hold the image
        logo_pic_label = Label(self.root, image=self.logophoto)
        logo_pic_label.place(x=800, y=188)
        # -------------------------------------------------------------------------

        # Boss Image Widget
        # -------------------------------------------------------------------------
        self.bossimage = Image.open(os.path.join(os.path.dirname(__file__), "bosscat.png"))
        self.bossimage = self.bossimage.resize((200, 200), Image.Resampling.LANCZOS)

        # Convert the image to a Tkinter-compatible format
        self.bossphoto = ImageTk.PhotoImage(self.bossimage)

        # Create a Label widget to hold the image
        boss_pic_label = Label(self.root, image=self.bossphoto)
        boss_pic_label.place(x=-5, y=470)
        # -------------------------------------------------------------------------

        # Textbox Image Widget
        # -------------------------------------------------------------------------
        self.textboximage = Image.open(os.path.join(os.path.dirname(__file__), "textbox.png"))
        self.textboximage = self.textboximage.resize((200, 200), Image.Resampling.LANCZOS)

        # Convert the image to a Tkinter-compatible format
        self.textphoto = ImageTk.PhotoImage(self.textboximage)

        # Create a Label widget to hold the image
        text_pic_label = Label(self.root, image=self.textphoto)
        text_pic_label.place(x=200, y=380)
        # -------------------------------------------------------------------------

        # Username and password login
        # -------------------------------------------------------------------------
        username_label = Label(self.root, text="Username:", font=("Arial", 14))
        username_label.place(x=500, y=300)

        username_entry = Entry(self.root, font=("Arial", 14), width=20)
        username_entry.place(x=600, y=300)

        password_label = Label(self.root, text="Password:", font=("Arial", 14))
        password_label.place(x=500, y=350)

        password_entry = Entry(self.root, font=("Arial", 14), width=20, show="*")  # 'show' hides the password
        password_entry.place(x=600, y=350)


        # Create the Login button
        # -------------------------------------------------------------------------
        login_button = Button(self.root, text="Login", font=("Arial", 14), command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.place(x=500, y=400)
        # -------------------------------------------------------------------------


        # Create user account
        # -------------------------------------------------------------------------
        # Create the create button
        create_button = Button(self.root, text="Create New Account", font=("Arial", 14), command=self.show_register)
        create_button.place(x=600, y=400)
        # -------------------------------------------------------------------------

    def show_register(self):
        self.clear_window()
        # Brings the window to fullscreen
        self.root.state('zoomed')  # This simulates the maximize button being clicked

        create_message_label = Label(self.root, text="Enter Your Information Below:", font=("Comic Sans MS", 30, "bold"))
        create_message_label.place(x=380, y=200)

        #firstname_label = Label(self.root, text="First Name:", font=("Arial", 14))
        #firstname_label.place(x=500, y=350)

        #first_name_entry = Entry(self.root, font=("Arial", 14), width=20)
        #first_name_entry.place(x=660, y=350)

        #lastname_label = Label(self.root, text="Last Name:", font=("Arial", 14))
        #lastname_label.place(x=500, y=400)

        #last_name_entry = Entry(self.root, font=("Arial", 14), width=20)
        #last_name_entry.place(x=660, y=400)

        create_user_label = Label(self.root, text="Create Username:", font=("Arial", 14))
        create_user_label.place(x=480, y=300)

        create_user_entry = Entry(self.root, font=("Arial", 14), width=20)
        create_user_entry.place(x=650, y=300)

        create_psswrd_label = Label(self.root, text="Create Password:", font=("Arial", 14))
        create_psswrd_label.place(x=480, y=350)

        create_psswrd_entry = Entry(self.root, font=("Arial", 14), width=20, show='*')
        create_psswrd_entry.place(x=650, y=350)

        confirm_psswrd_label = Label(self.root, text="Confirm Password:", font=("Arial", 14))
        confirm_psswrd_label.place(x=480, y=400)

        confirm_psswrd_entry = Entry(self.root, font=("Arial", 14), width=20, show='*')
        confirm_psswrd_entry.place(x=650, y=400)

        # Send the info to create_accounts function so it can append the info to the sql database
        register_account_button = Button(self.root, text="Register Account", font=("Arial", 14), command=lambda: self.register(create_user_entry.get(), create_psswrd_entry.get(), confirm_psswrd_entry.get()))
        register_account_button.place(x=710, y=450)

        # Go Back to the main log in
        go_back_button = Button(self.root, text="Go Back", font=("Arial", 14),command=self.show_login)
        go_back_button.place(x=600, y=450)


    def show_main_window(self):
        self.clear_window()
        self.root.geometry(MAIN_WINDOW_SIZE)

        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(header_frame, text=f"Welcome, {self.current_user['username']}!", font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Logout", command=self.show_login).pack(side=tk.RIGHT)

        # Assignment List
        list_frame = ttk.LabelFrame(main_frame, text="Assignments", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Create Treeview
        columns = ('ID', 'Name', 'Due Date', 'Status', 'Creator')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')

        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        if self.current_user['is_admin']:
            ttk.Button(button_frame, text="Create Assignment", command=self.show_create_assignment).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Manage Users", command=self.show_user_management).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="View Details", command=self.show_assignment_details).pack(side=tk.LEFT, padx=5)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Load assignments
        self.load_assignments()

    def show_create_assignment(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Assignment")
        dialog.geometry(ASSIGNMENT_WINDOW_SIZE)

        # Create Frame
        create_frame = ttk.Frame(dialog, padding="10")
        create_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Name
        ttk.Label(create_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(create_frame, width=40)
        name_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Due Date
        ttk.Label(create_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        due_date_entry = ttk.Entry(create_frame, width=40)
        due_date_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Description
        ttk.Label(create_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        description_text = tk.Text(create_frame, width=40, height=5)
        description_text.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Status
        ttk.Label(create_frame, text="Status:").grid(row=3, column=0, sticky=tk.W, pady=5)
        status_var = tk.StringVar(value=ASSIGNMENT_STATUSES[0])
        status_combo = ttk.Combobox(create_frame, textvariable=status_var, values=ASSIGNMENT_STATUSES, state="readonly")
        status_combo.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Assignees
        ttk.Label(create_frame, text="Assignees:").grid(row=4, column=0, sticky=tk.W, pady=5)
        assignees_listbox = tk.Listbox(create_frame, selectmode=tk.MULTIPLE, width=40, height=5)
        assignees_listbox.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Load users into listbox
        users = self.db.get_all_users()
        for user in users:
            assignees_listbox.insert(tk.END, f"{user[1]} (ID: {user[0]})")

        def save_assignment():
            try:
                name = name_entry.get()
                due_date = datetime.strptime(due_date_entry.get(), "%Y-%m-%d")
                description = description_text.get("1.0", tk.END).strip()
                status = status_var.get()
                selected_indices = assignees_listbox.curselection()
                assignee_ids = [users[i][0] for i in selected_indices]

                if not name or not due_date_entry.get():
                    messagebox.showerror("Error", "Name and due date are required!")
                    return

                self.db.create_assignment(name, due_date, description, status, self.current_user['user_id'], assignee_ids)
                self.load_assignments()
                dialog.destroy()
                messagebox.showinfo("Success", "Assignment created successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create assignment: {str(e)}")

        ttk.Button(create_frame, text="Save", command=save_assignment).grid(row=5, column=0, columnspan=3, pady=10)

    def show_assignment_details(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select an assignment to view details!")
            return

        assignment_id = self.tree.item(selected_items[0])['values'][0]
        assignment, assignees = self.db.get_assignment_details(assignment_id)

        dialog = tk.Toplevel(self.root)
        dialog.title("Assignment Details")
        dialog.geometry(ASSIGNMENT_WINDOW_SIZE)

        # Details Frame
        details_frame = ttk.Frame(dialog, padding="10")
        details_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Display assignment details
        ttk.Label(details_frame, text="Name:", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=assignment[1]).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(details_frame, text="Due Date:", font=('Helvetica', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=assignment[2].strftime("%Y-%m-%d")).grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(details_frame, text="Description:", font=('Helvetica', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=assignment[3] or "No description").grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(details_frame, text="Status:", font=('Helvetica', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        status_var = tk.StringVar(value=assignment[4])
        status_combo = ttk.Combobox(details_frame, textvariable=status_var, values=ASSIGNMENT_STATUSES, state="readonly")
        status_combo.grid(row=3, column=1, sticky=tk.W, pady=5)

        ttk.Label(details_frame, text="Creator:", font=('Helvetica', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=assignment[-1]).grid(row=4, column=1, sticky=tk.W, pady=5)

        ttk.Label(details_frame, text="Assignees:", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=5)
        assignees_text = "\n".join([assignee[1] for assignee in assignees])
        ttk.Label(details_frame, text=assignees_text or "No assignees").grid(row=5, column=1, sticky=tk.W, pady=5)

        def update_status():
            try:
                self.db.update_assignment_status(assignment_id, status_var.get())
                self.load_assignments()
                dialog.destroy()
                messagebox.showinfo("Success", "Status updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update status: {str(e)}")

        ttk.Button(details_frame, text="Update Status", command=update_status).grid(row=6, column=0, columnspan=2, pady=10)

    def show_user_management(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("User Management")
        dialog.geometry("400x300")

        # User Management Frame
        user_frame = ttk.Frame(dialog, padding="10")
        user_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create Treeview
        columns = ('ID', 'Username', 'Role')
        user_tree = ttk.Treeview(user_frame, columns=columns, show='headings')

        # Set column headings
        for col in columns:
            user_tree.heading(col, text=col)
            user_tree.column(col, width=100)

        user_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(user_frame, orient=tk.VERTICAL, command=user_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        user_tree.configure(yscrollcommand=scrollbar.set)

        # Buttons Frame
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=1, column=0, pady=5)

        def promote_user():
            selected_items = user_tree.selection()
            if not selected_items:
                messagebox.showwarning("Warning", "Please select a user to promote!")
                return

            user_id = user_tree.item(selected_items[0])['values'][0]
            try:
                self.db.promote_user(user_id)
                self.load_users()
                messagebox.showinfo("Success", "User promoted to admin successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to promote user: {str(e)}")

        ttk.Button(button_frame, text="Promote to Admin", command=promote_user).pack(side=tk.LEFT, padx=5)

        def load_users():
            # Clear existing items
            for item in user_tree.get_children():
                user_tree.delete(item)

            # Load users from database
            users = self.db.get_all_users()
            for user in users:
                role = "Admin" if user[2] else "User"
                user_tree.insert('', tk.END, values=(user[0], user[1], role))

        # Load users
        load_users()

        # Configure grid weights
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        user_frame.columnconfigure(0, weight=1)
        user_frame.rowconfigure(0, weight=1)

    def load_assignments(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load assignments from database
        assignments = self.db.get_assignments(self.current_user['user_id'], self.current_user['is_admin'])
        for assignment in assignments:
            # Extract the specific fields we want
            assignment_id = assignment[0]  # id is the first column
            name = assignment[1]           # name is the second column
            due_date = assignment[2].strftime('%Y-%m-%d')  # due date is the third column
            status = assignment[4]         # status is the fifth column
            creator_name = assignment[-1]  # creator_name is the last column added in the query

            self.tree.insert('', tk.END, values=(assignment_id, name, due_date, status, creator_name))

    def login(self, username, password):
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        user_data = self.db.verify_user(username, password)
        if user_data:
            self.current_user = {
                'user_id': user_data['user_id'],
                'username': username,
                'is_admin': user_data['is_staff']
            }
            self.show_main_window()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def register(self, username, password, confirm_password):
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            self.db.create_user(username, password)
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.show_login()
        except Exception as e:
            if "unique" in str(e).lower():
                messagebox.showerror("Error", "Username already exists!")
            else:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")


    # This function removes any previous windows
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TaskManagementApp()
    app.run()