"""
Registration Module

This module handles user registration and QR code generation.
Users can register as Student, Teacher, or Guest and receive a QR code.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
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
        
        # Title
        title_frame = tk.Frame(self.window, bg="#3498db", pady=20)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="📝 USER REGISTRATION",
            font=("Arial", 24, "bold"),
            bg="#3498db",
            fg="white"
        )
        title_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.window, bg="#ecf0f1")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        # Form frame (left side)
        form_frame = tk.Frame(main_frame, bg="#ecf0f1")
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Inner centered form container with grid
        inner_form = tk.Frame(form_frame, bg="#ecf0f1")
        inner_form.pack(expand=True, anchor=tk.CENTER)
        
        # User Type Selection
        type_label = tk.Label(
            inner_form,
            text="User Type:",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            width=15,
            anchor=tk.W
        )
        type_label.grid(row=0, column=0, sticky=tk.W, pady=(20, 15), padx=(0, 20))
        
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
                command=self.update_fields_based_on_type
            )
            rb.pack(side=tk.LEFT, padx=10)
        
        # Name Field
        name_label = tk.Label(
            inner_form,
            text="Full Name:",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            width=15,
            anchor=tk.W,
            height=1
        )
        name_label.grid(row=1, column=0, sticky=tk.W + tk.E, pady=(30, 8), padx=(0, 20))
        
        self.name_entry = tk.Entry(
            inner_form,
            textvariable=self.name_var,
            font=("Arial", 14),
            width=40
        )
        self.name_entry.grid(row=1, column=1, sticky=tk.W, pady=(30, 25))
        
        # ID Number Field
        self.id_label = tk.Label(
            inner_form,
            text="ID Number:",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            width=15,
            anchor=tk.W,
            height=1
        )
        self.id_label.grid(row=2, column=0, sticky=tk.W + tk.E, pady=(25, 8), padx=(0, 20))
        
        self.id_entry = tk.Entry(
            inner_form,
            textvariable=self.id_var,
            font=("Arial", 14),
            width=40
        )
        self.id_entry.grid(row=2, column=1, sticky=tk.W, pady=(25, 25))
        
        # Department Field
        self.dept_label = tk.Label(
            inner_form,
            text="Department:",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            width=15,
            anchor=tk.W,
            height=1
        )
        self.dept_label.grid(row=3, column=0, sticky=tk.W + tk.E, pady=(25, 8), padx=(0, 20))
        
        self.dept_entry = tk.Entry(
            inner_form,
            textvariable=self.department_var,
            font=("Arial", 14),
            width=40
        )
        self.dept_entry.grid(row=3, column=1, sticky=tk.W, pady=(25, 25))
        
        # Buttons
        button_frame = tk.Frame(inner_form, bg="#ecf0f1")
        button_frame.grid(row=4, column=0, columnspan=2, pady=40)
        
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
        qr_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        qr_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(20, 0))
        
        qr_title = tk.Label(
            qr_frame,
            text="Generated QR Code",
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
            self.department_var.set("Guest")
        else:
            # Show fields for Student/Teacher
            self.id_label.grid()
            self.id_entry.grid()
            self.dept_label.grid()
            self.dept_entry.grid()
            self.id_entry.config(state=tk.NORMAL)
            self.dept_entry.config(state=tk.NORMAL)
            if self.id_var.get() == "Guest":
                self.id_var.set("")
            if self.department_var.get() == "Guest":
                self.department_var.set("")
    
    def validate_input(self):
        """Validate user input before registration"""
        name = self.name_var.get().strip()
        id_number = self.id_var.get().strip()
        department = self.department_var.get().strip()
        user_type = self.user_type_var.get()
        
        if not name:
            messagebox.showerror("Validation Error", "Please enter a name.")
            return False
        
        if user_type != "Guest":
            if not id_number:
                messagebox.showerror("Validation Error", "Please enter an ID number.")
                return False
            
            if not department:
                messagebox.showerror("Validation Error", "Please enter a department.")
                return False
            
            # Check if ID already exists (except for guests)
            if self.db_manager.check_id_exists(id_number):
                messagebox.showerror(
                    "Duplicate ID",
                    f"ID number '{id_number}' is already registered.\nPlease use a different ID."
                )
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
                # Copy the file
                import shutil
                shutil.copy(self.generated_qr_path, save_path)
                messagebox.showinfo("Success", f"QR Code saved to:\n{save_path}", parent=self.window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code:\n{e}", parent=self.window)
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_var.set("")
        self.id_var.set("")
        self.department_var.set("")
        self.user_type_var.set("Student")
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
