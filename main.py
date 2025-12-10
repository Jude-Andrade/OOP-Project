"""
EVSU-OC ALIBLOG - Automated Library Logbook System
Main Entry Point

This is the main application launcher for the library logbook system.
It initializes the database and displays the main menu.
"""

import tkinter as tk
from tkinter import messagebox
from database.db_manager import DatabaseManager
from modules.registration import RegistrationWindow
from modules.scanner import ScannerWindow
from modules.admin_panel import AdminLoginWindow
from PIL import Image, ImageTk
import os


class MainApplication:
    """Main application class that manages the entire system"""
    
    def __init__(self):
        """Initialize the main application"""
        # Initialize database
        self.db_manager = DatabaseManager()
        self.db_manager.initialize_database()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("EVSU-OC ALIBLOG - Library Logbook System")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        bg_path = os.path.join("assets", "makmak1.png")
        if os.path.exists(bg_path):
            # Load original image
            self.bg_orig = Image.open(bg_path)
            
            # Initial resize to window size
            bg_img = self.bg_orig.resize((800, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)

            # Create a Label to hold the background
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Bind resizing
            self.root.bind("<Configure>", self.resize_bg)

                    
        # Maximize main window by default (best-effort)
        self.root.state('zoomed')
        
        self.create_main_menu()
        self.admin_window = None  # Track admin window

        
    def resize_bg(self, event):
        # Avoid very small events
        if event.width < 2 or event.height < 2:
            return
        # Resize original image to new window size
        resized = self.bg_orig.resize((event.width, event.height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_photo)

    
    def center_window(self, window, width, height):
        """Center a window on the screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_main_menu(self):
        """Create the main menu interface"""
        for widget in self.root.winfo_children():
            if widget != self.bg_label:  # skip background
                widget.destroy()    

        # Title frame
        title_frame = tk.Frame(self.root, bg="#6B1F1F", pady=30)
        title_frame.pack(fill=tk.X)
        
        # Create a container frame for logo + title (centered)
        header_container = tk.Frame(title_frame, bg="#6B1F1F")
        header_container.pack()   # CENTER by default
                
        # Load logo image
        logo_path = os.path.join("assets", "ebsulogo2.0.png")  # Example path
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)

            logo_label = tk.Label(
                #title_frame,
                header_container,
                image=self.logo_photo,
                bg="#6B1F1F"
                )
            logo_label.pack(side=tk.LEFT, padx=20)
            
        title_label = tk.Label(
            #title_frame,
            header_container,
            text="EVSU-OC ALIBLOG",
            font=("League Spartan", 35, "bold"),
            bg="#6B1F1F",
            fg="white"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            #title_frame,
            header_container,
            text="Automated Library Logbook System",
            font=("Arial", 16),
            bg="#6B1F1F",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Menu buttons frame
        # menu_frame = tk.Frame(self.root, bg="#2c3e50")
        # menu_frame.pack(expand=True)
        
        menu_frame = tk.Frame(self.root, width=500, height=400)
        menu_frame.pack(expand=True)
    
        # Register button
        register_btn = tk.Button(
            menu_frame,
            text="📝 REGISTER USER",
            font=("Arial", 18, "bold"),
            bg="#00C0EF",
            fg="white",
            activebackground="#00C0EF",
            activeforeground="white",
            width=25,
            height=2,
            cursor="hand2",
            command=self.open_registration
        )
        register_btn.pack(pady=15, padx=20)
        
        # Scanner button
        scanner_btn = tk.Button(
            menu_frame,
            text="📷 QR SCANNER",
            font=("Arial", 18, "bold"),
            bg="#00A65A",
            fg="white",
            activebackground="#00A65A",
            activeforeground="white",
            width=25,
            height=2,
            cursor="hand2",
            command=self.open_scanner
        )
        scanner_btn.pack(pady=15, padx=20)
        
        # Admin button
        admin_btn = tk.Button(
            menu_frame,
            text="🔐 ADMIN PANEL",
            font=("Arial", 18, "bold"),
            bg="#F39C12",
            fg="white",
            activebackground="#F39C12",
            activeforeground="white",
            width=25,
            height=2,
            cursor="hand2",
            command=self.open_admin_login
        )
        admin_btn.pack(pady=15, padx=20) 
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="Eastern Visayas State University - Ormoc Campus Library\n© Information Technology Students 2025",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#000000"
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def open_registration(self):
        """Open the registration window"""
        RegistrationWindow(self.root, self.db_manager)
        self.root.withdraw()
    
    def open_scanner(self):
        """Open the scanner window"""
        ScannerWindow(self.root, self.db_manager)
        self.root.withdraw()
    
    def open_admin_login(self):
        """Open the admin login window (single instance only)"""
        if self.admin_window is None or not tk.Toplevel.winfo_exists(self.admin_window.window):
            self.admin_window = AdminLoginWindow(self.root, self.db_manager)
        else:
            # Optional: bring the existing window to front
            self.admin_window.window.lift()
            self.admin_window.window.focus_force()

        
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.run()
