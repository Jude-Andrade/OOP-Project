"""
Registration Module

This module handles user registration and QR code generation.
Users can register as Student, Teacher, or Guest and receive a QR code.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from utils.qr_generator import QRCodeGenerator



class RegistrationWindow:
    """Registration window for new users"""
    
    def __init__(self, parent, db_manager):
        """
        Initialize registration window
        
        Args:
            parent: Parent Tkinter window
            db_manager: DatabaseManager instance
        """
        self.parent = parent
        self.db_manager = db_manager
        self.qr_generator = QRCodeGenerator()
        
        # Predefined list of departments for dropdown
        self.departments = [
        "Dept. of Education",
        "Dept. of Technology",
        "Dept. of Engineering",
        "Dept. of Information Technology",
        ]
        
        # Create new window
        self.window = tk.Toplevel(parent)
        self.window.title("User Registration - EVSU-OC ALIBLOG")
        self.window.geometry("900x700")
        self.window.configure(bg="#ecf0f1")
        
        # Maximize window on popup
        try:
            self.window.state('zoomed')
        except Exception:
            pass
        
        # Center window
        self.center_window(900, 700)
        
        # Variables
        self.name_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.user_type_var = tk.StringVar(value="Student")
        
        self.generated_qr_path = None
        self.qr_image_label = None
        
        self.create_widgets()
        self.update_fields_based_on_type()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create all widgets for the registration form"""
        
        # Title frame with back button
        title_frame = tk.Frame(self.window, bg="#6B1F1F", pady=20)
        title_frame.pack(fill=tk.X)
        
        # # Back button (left side)
        # back_btn = tk.Button(
        #     title_frame,
        #     text="← BACK",
        #     font=("Arial", 12, "bold"),
        #     bg="#e74c3c",
        #     fg="white",
        #     activebackground="#c0392b",
        #     activeforeground="white",
        #     cursor="hand2",
        #     command=self.go_back
        # )
        # back_btn.pack(side=tk.LEFT, padx=20)
        
        # # Title (center)
        # title_label = tk.Label(
        #     title_frame,
        #     text="📝 USER REGISTRATION",
        #     font=("League Spartan", 28, "bold"),
        #     bg="#6B1F1F",
        #     fg="white"
        # )
        # title_label.pack(expand=True)
        
        # Title frame with back button
        # Title Frame
        title_frame = tk.Frame(self.window, bg="#6B1F1F", height=170)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        # Configure 3 equal-weight columns
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=1)
        title_frame.grid_columnconfigure(2, weight=1)

        # Back Button (Left)
        back_btn = tk.Button(
            title_frame,
            text="BACK",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            cursor="hand2",
            command=self.go_back
        )
        back_btn.grid(row=0, column=0, sticky="w", padx=40)

        # Title (Center)
        title_label = tk.Label(
            title_frame,
            text="USER REGISTRATION",
            font=("League Spartan", 30, "bold"),
            bg="#6B1F1F",
            fg="white",
            pady=20
        )
        title_label.grid(row=0, column=1)   # <-- always centered PERFECTLY

        # Empty placeholder so the title stays centered even with left button
        placeholder = tk.Label(title_frame, bg="#6B1F1F")
        placeholder.grid(row=0, column=2, sticky="e", padx=40)


        # Main content frame
        main_frame = tk.Frame(self.window, bg="#ecf0f1")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=120)
        
        # Form frame (left side)
        form_frame = tk.Frame(main_frame, bg="#ecf0f1")
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Inner centered form container with grid
        inner_form = tk.Frame(form_frame, bg="#ecf0f1")
        inner_form.pack(expand=True, anchor=tk.CENTER, pady=10)
        
        # Ensure consistent grid columns so labels and entries align
        inner_form.grid_columnconfigure(0, weight=0, minsize=180)  # label column (fixed width)
        inner_form.grid_columnconfigure(1, weight=1)               # entry column (expandable)
        
        # User Type Selection
        type_label = tk.Label(
            inner_form,
            text="User Type:",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            anchor=tk.W
        )
        type_label.grid(row=0, column=0, sticky=tk.W, pady=(20, 15), padx=(10, 10))
        
        type_frame = tk.Frame(inner_form, bg="#ecf0f1")
        type_frame.grid(row=0, column=1, sticky=tk.W, pady=(20, 15))
        
        for user_type in ["Student", "Teacher", "Guest"]:
            rb = tk.Radiobutton(
                type_frame,
                text=user_type,
                variable=self.user_type_var,
                value=user_type,
                font=("Arial", 12),
                bg="#ecf0f1",
                anchor=tk.W,
                command=self.update_fields_based_on_type
            )
            rb.pack(side=tk.LEFT, padx=8)
        
        # Name Field
        name_label = tk.Label(
            inner_form,
            text="Full Name:",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            anchor=tk.W
        )
        name_label.grid(row=1, column=0, sticky=tk.W, pady=(12, 8), padx=(10, 10))
        
        self.name_entry = tk.Entry(
            inner_form,
            textvariable=self.name_var,
            font=("Arial", 14)
        )
        self.name_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=(12, 8))
        
        # ID Number Field
        self.id_label = tk.Label(
            inner_form,
            text="ID Number:",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            anchor=tk.W
        )
        self.id_label.grid(row=2, column=0, sticky=tk.W, pady=(12, 8), padx=(10, 10))
        
        self.id_entry = tk.Entry(
            inner_form,
            textvariable=self.id_var,
            font=("Arial", 14)
        )
        self.id_entry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=(12, 8))
        
        # # Department Field
        # self.dept_label = tk.Label(
        #     inner_form,
        #     text="Department:",
        #     font=("Arial", 14, "bold"),
        #     bg="#ecf0f1",
        #     anchor=tk.W
        # )
        # self.dept_label.grid(row=3, column=0, sticky=tk.W, pady=(12, 8), padx=(10, 10))
        
        # self.dept_entry = tk.Entry(
        #     inner_form,
        #     textvariable=self.department_var,
        #     font=("Arial", 14)
        # )
        # self.dept_entry.grid(row=3, column=1, sticky=tk.W+tk.E, pady=(12, 8))
        
        self.dept_label = tk.Label(
        inner_form,
        text="Department:",
        font=("Arial", 14, "bold"),
        bg="#ecf0f1",
        anchor=tk.W
    )
        self.dept_label.grid(row=3, column=0, sticky=tk.W, pady=(12, 8), padx=(10, 10))

    #     self.dept_entry = ttk.Combobox(
    #     inner_form,
    #     textvariable=self.department_var,
    #     font=("Arial", 14),
    #     values=self.departments,
    #     state="readonly"
    # )
    
        self.dept_entry = ttk.Combobox(
        inner_form,
        textvariable=self.department_var,
        font=("Arial", 14),
        values=self.departments,
        state="readonly"
    )
        self.dept_entry.grid(row=3, column=1, sticky=tk.W+tk.E, pady=(12, 8))
        self.dept_entry.set("Select Department")

    # Change dropdown list font
        self.window.option_add("*TCombobox*Listbox.font",   ("Arial", 14))
    
        self.window.option_add("*TCombobox*Listbox.font", ("Arial", 14))
        self.dept_entry.grid(row=3, column=1, sticky=tk.W+tk.E, pady=(12, 8))
        self.dept_entry.set("Select Department")

        # Contact Number Field
        self.contact_label = tk.Label(
            inner_form,
            text="Contact Number:",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            anchor=tk.W
        )
        self.contact_label.grid(row=4, column=0, sticky=tk.W, pady=(12, 8), padx=(10, 10))

        self.contact_entry = tk.Entry(
            inner_form,
            textvariable=self.contact_var,
            font=("Arial", 14)
        )
        self.contact_entry.grid(row=4, column=1, sticky=tk.W+tk.E, pady=(12, 8))
        
        # Buttons
        button_frame = tk.Frame(inner_form, bg="#ecf0f1")
        button_frame.grid(row=5, column=0, columnspan=2, pady=30)
        
        register_btn = tk.Button(
            button_frame,
            text="✅ REGISTER & GENERATE QR",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            width=25,
            height=2,
            cursor="hand2",
            command=self.register_user
        )
        register_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="🔄 CLEAR",
            font=("Arial", 14, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            activeforeground="white",
            width=12,
            height=2,
            cursor="hand2",
            command=self.clear_form
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # QR Code Display Frame (right side)
        qr_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2, width=320)
        qr_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False, padx=(20, 0))
        qr_frame.pack_propagate(False)
        
        qr_title = tk.Label(
            qr_frame,
            text="GENERATE QR CODE",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        qr_title.pack(pady=10)
        
        self.qr_display_frame = tk.Frame(qr_frame, bg="white", width=300, height=300)
        self.qr_display_frame.pack(padx=20, pady=10)
        self.qr_display_frame.pack_propagate(False)
        
        placeholder_label = tk.Label(
            self.qr_display_frame,
            text="QR Code will appear here\nafter registration",
            font=("Arial", 12),
            bg="white",
            fg="#7f8c8d"
        )
        placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        save_btn = tk.Button(
            qr_frame,
            text="💾 Save QR Code",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=20,
            cursor="hand2",
            command=self.save_qr_code,
            state=tk.DISABLED
        )
        save_btn.pack(pady=10)
        self.save_qr_btn = save_btn
    
    def update_fields_based_on_type(self):
        """Update form fields based on selected user type"""
        user_type = self.user_type_var.get()
        
        if user_type == "Guest":
            # Hide ID and Department fields for guests
            self.id_label.grid_remove()
            self.id_entry.grid_remove()
            self.dept_label.grid_remove()
            self.dept_entry.grid_remove()
            self.id_var.set("Guest")
            # self.department_var.set("Guest")
            self.dept_entry.config(state="disabled")
            self.department_var.set("Guest")
        else:
            # Show fields for Student/Teacher
            self.id_label.grid()
            self.id_entry.grid()
            self.dept_label.grid()
            # self.dept_entry.grid()
            # self.id_entry.config(state=tk.NORMAL)
            self.dept_entry.grid()
            self.dept_entry.config(state="readonly")
            self.dept_entry.config(state=tk.NORMAL)
            if self.id_var.get() == "Guest":
                self.id_var.set("")
            if self.department_var.get() == "Guest":
                self.department_var.set("")

        # Contact number should always be visible for all user types
        try:
            self.contact_label.grid()
            self.contact_entry.grid()
        except Exception:
            pass
    
    def validate_input(self):
        """Validate user input before registration"""
        name = self.name_var.get().strip()
        id_number = self.id_var.get().strip()
        department = self.department_var.get().strip()
        contact_number = self.contact_var.get().strip()
        user_type = self.user_type_var.get()
        
        if not name:
            messagebox.showerror("Validation Error", "Please enter a name.", parent=self.window)
            return False
        
        if user_type != "Guest":
            if not id_number:
                messagebox.showerror("Validation Error", "Please enter an ID number.", parent=self.window)
                return False
            
            if not department:
                messagebox.showerror("Validation Error", "Please enter a department.", parent=self.window)
                return False
            
            # Check if ID already exists (except for guests)
            if self.db_manager.check_id_exists(id_number):
                messagebox.showwarning(
                    "Duplicate ID",
                    f"ID number '{id_number}' is already registered.\nPlease use a different ID.",
                    parent=self.window
                )
                return False

        # Contact number is required for all user types
        if not contact_number:
            messagebox.showerror("Validation Error", "Please enter a contact number.", parent=self.window)
            return False
        
        return True
    
    def register_user(self):
        """Register a new user and generate QR code"""
        if not self.validate_input():
            return
        
        # Get values
        name = self.name_var.get().strip()
        id_number = self.id_var.get().strip()
        department = self.department_var.get().strip()
        contact_number = self.contact_var.get().strip()
        user_type = self.user_type_var.get()
        
        # Generate QR code first
        qr_path = self.qr_generator.generate_qr_code(
            name=name,
            id_number=id_number,
            department=department,
            user_type=user_type
        )
        
        if not qr_path:
            messagebox.showerror("Error", "Failed to generate QR code.")
            return
        
        # Register user in database
        user_id = self.db_manager.register_user(
            name=name,
            id_number=id_number,
            department=department,
            user_type=user_type,
            contact_number=contact_number,
            qr_path=qr_path
        )
        
        if user_id:
            self.generated_qr_path = qr_path
            self.display_qr_code(qr_path)
            self.save_qr_btn.config(state=tk.NORMAL)
            
            # Keep window on top and focused
            self.window.attributes('-topmost', True)
            self.window.lift()
            self.window.focus_set()
            
            messagebox.showinfo(
                "Registration Successful",
                f"User registered successfully!\n\n"
                f"Name: {name}\n"
                f"ID: {id_number}\n"
                f"Department: {department}\n"
                f"Contact: {contact_number}\n"
                f"Type: {user_type}\n\n"
                f"QR Code has been generated and displayed.",
                parent=self.window
            )
            # Window stays open, QR code is displayed in the frame
        else:
            messagebox.showerror("Error", "Failed to register user in database.")
    
    def display_qr_code(self, qr_path):
        """Display the generated QR code in the window"""
        try:
            # Clear previous content
            for widget in self.qr_display_frame.winfo_children():
                widget.destroy()
            
            # Load and resize image
            img = Image.open(qr_path)
            img = img.resize((280, 280), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Display image
            label = tk.Label(self.qr_display_frame, image=photo, bg="white")
            label.image = photo  # Keep a reference
            label.pack()
            
            self.qr_image_label = label
        except Exception as e:
            print(f"Error displaying QR code: {e}")
    
    def save_qr_code(self):
        """Save the QR code to a user-selected location"""
        if not self.generated_qr_path or not os.path.exists(self.generated_qr_path):
            messagebox.showerror("Error", "No QR code to save.", parent=self.window)
            return
        
        # Ask user where to save
        filename = os.path.basename(self.generated_qr_path)
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=filename,
            title="Save QR Code",
            parent=self.window
        )
        
        if save_path:
            try:
                import shutil
                shutil.copy(self.generated_qr_path, save_path)
                messagebox.showinfo("Success", f"QR code saved to:\n{save_path}", parent=self.window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {e}", parent=self.window)
    
    def go_back(self):
        """Close the registration window and return to main menu"""
        self.window.destroy()
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_var.set("")
        self.id_var.set("")
        self.department_var.set("")
        self.user_type_var.set("Student")
        self.contact_var.set("")
        self.generated_qr_path = None
        self.save_qr_btn.config(state=tk.DISABLED)
        
        # Clear QR display
        for widget in self.qr_display_frame.winfo_children():
            widget.destroy()
        
        placeholder_label = tk.Label(
            self.qr_display_frame,
            text="QR Code will appear here\nafter registration",
            font=("Arial", 12),
            bg="white",
            fg="#7f8c8d"
        )
        placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.update_fields_based_on_type()
