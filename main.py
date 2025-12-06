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
        self.root.configure(bg="#2c3e50")
        
        # Maximize main window by default (best-effort)
        try:
            self.root.state('zoomed')
        except Exception:
            # Fall back to manual centering if state() is not supported
            self.center_window(self.root, 800, 600)
        
        self.create_main_menu()
    
    def center_window(self, window, width, height):
        """Center a window on the screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_main_menu(self):
        """Create the main menu interface"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title frame
        title_frame = tk.Frame(self.root, bg="#34495e", pady=30)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="EVSU-OC ALIBLOG",
            font=("Arial", 32, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Automated Library Logbook System",
            font=("Arial", 16),
            bg="#34495e",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Menu buttons frame
        menu_frame = tk.Frame(self.root, bg="#2c3e50")
        menu_frame.pack(expand=True)
        
        # Register button
        register_btn = tk.Button(
            menu_frame,
            text="📝 REGISTER NEW USER",
            font=("Arial", 18, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=25,
            height=2,
            cursor="hand2",
            command=self.open_registration
        )
        register_btn.pack(pady=15)
        
        # Scanner button
        scanner_btn = tk.Button(
            menu_frame,
            text="📷 QR SCANNER (TIME-IN/OUT)",
            font=("Arial", 18, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            activeforeground="white",
            width=25,
            height=2,
            cursor="hand2",
            command=self.open_scanner
        )
        scanner_btn.pack(pady=15)
        
        # Admin button
        admin_btn = tk.Button(
            menu_frame,
            text="🔐 ADMIN PANEL",
            font=("Arial", 18, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            width=25,
            height=2,
            cursor="hand2",
            command=self.open_admin_login
        )
        admin_btn.pack(pady=15) 
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="Eastern Visayas State University - Ormoc Campus Library",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def open_registration(self):
        """Open the registration window"""
        RegistrationWindow(self.root, self.db_manager)
    
    def open_scanner(self):
        """Open the scanner window"""
        ScannerWindow(self.root, self.db_manager)
    
    def open_admin_login(self):
        """Open the admin login window"""
        AdminLoginWindow(self.root, self.db_manager)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.run()
