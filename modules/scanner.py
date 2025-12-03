"""
QR Scanner Module

This module handles QR code scanning and automatic Time-In/Time-Out logging.
The scanner accepts input from a QR code reader (which acts as keyboard input).
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from utils.qr_generator import QRCodeGenerator


class ScannerWindow:
    """QR Scanner window for logging Time-In and Time-Out"""
    
    def __init__(self, parent, db_manager):
        """
        Initialize scanner window
        
        Args:
            parent: Parent Tkinter window
            db_manager: DatabaseManager instance
        """
        self.parent = parent
        self.db_manager = db_manager
        self.qr_generator = QRCodeGenerator()
        
        # Create new window
        self.window = tk.Toplevel(parent)
        self.window.title("QR Scanner - EVSU-OC ALIBLOG")
        self.window.geometry("800x600")
        self.window.configure(bg="#2c3e50")
        
        # Maximize window on popup
        try:
            self.window.state('zoomed')
        except Exception:
            pass
        
        # Center window
        self.center_window(800, 600)
        
        # Variables
        self.qr_input_var = tk.StringVar()
        
        self.create_widgets()
        
        # Focus on input field
        self.qr_entry.focus_set()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create all widgets for the scanner interface"""
        
        # Title
        title_frame = tk.Frame(self.window, bg="#27ae60", pady=25)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="📷 QR CODE SCANNER",
            font=("Arial", 28, "bold"),
            bg="#27ae60",
            fg="white"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Scan your QR code to log Time-In or Time-Out",
            font=("Arial", 14),
            bg="#27ae60",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)
        
        # Current time display
        self.time_frame = tk.Frame(main_frame, bg="#34495e", relief=tk.RIDGE, bd=2)
        self.time_frame.pack(fill=tk.X, pady=(0, 30))
        
        time_label_text = tk.Label(
            self.time_frame,
            text="Current Time:",
            font=("Arial", 14),
            bg="#34495e",
            fg="#bdc3c7"
        )
        time_label_text.pack(pady=(10, 0))
        
        self.time_display = tk.Label(
            self.time_frame,
            text="",
            font=("Arial", 32, "bold"),
            bg="#34495e",
            fg="#2ecc71"
        )
        self.time_display.pack(pady=(0, 10))
        
        # Start time update
        self.update_time()
        
        # Scanner instruction
        instruction_label = tk.Label(
            main_frame,
            text="Place QR code in front of scanner or paste scanned data below:",
            font=("Arial", 13),
            bg="#2c3e50",
            fg="white"
        )
        instruction_label.pack(pady=(0, 15))
        
        # QR Input field (where scanner inputs data)
        input_frame = tk.Frame(main_frame, bg="#2c3e50")
        input_frame.pack(pady=10)
        
        self.qr_entry = tk.Entry(
            input_frame,
            textvariable=self.qr_input_var,
            font=("Arial", 16),
            width=50,
            justify=tk.CENTER
        )
        self.qr_entry.pack()
        
        # Bind Enter key to process QR code
        self.qr_entry.bind('<Return>', lambda e: self.process_qr_scan())
        
        scan_btn = tk.Button(
            input_frame,
            text="✅ Process Scan",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=20,
            height=2,
            cursor="hand2",
            command=self.process_qr_scan
        )
        scan_btn.pack(pady=20)
        
        # Status display
        self.status_frame = tk.Frame(main_frame, bg="#34495e", relief=tk.RIDGE, bd=2)
        self.status_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        status_title = tk.Label(
            self.status_frame,
            text="Scan Status",
            font=("Arial", 16, "bold"),
            bg="#34495e",
            fg="white"
        )
        status_title.pack(pady=10)
        
        self.status_text = tk.Text(
            self.status_frame,
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#ecf0f1",
            height=8,
            width=70,
            state=tk.DISABLED,
            relief=tk.FLAT
        )
        self.status_text.pack(padx=20, pady=(0, 20))
        
        # Initial status message
        self.update_status("Ready to scan. Waiting for QR code...", "info")
        
        # Close button
        close_btn = tk.Button(
            self.window,
            text="❌ Close Scanner",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            width=20,
            cursor="hand2",
            command=self.window.destroy
        )
        close_btn.pack(pady=10)
    
    def update_time(self):
        """Update the current time display"""
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        date_str = now.strftime("%B %d, %Y")
        self.time_display.config(text=f"{time_str}\n{date_str}")
        
        # Schedule next update
        self.window.after(1000, self.update_time)
    
    def update_status(self, message, status_type="info"):
        """
        Update the status display
        
        Args:
            message: Status message to display
            status_type: Type of status (info, success, error)
        """
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%I:%M:%S %p")
        
        # Color coding
        if status_type == "success":
            color = "#2ecc71"
            prefix = "✅ SUCCESS"
        elif status_type == "error":
            color = "#e74c3c"
            prefix = "❌ ERROR"
        else:
            color = "#3498db"
            prefix = "ℹ INFO"
        
        self.status_text.insert(tk.END, f"[{timestamp}] {prefix}\n\n", "header")
        self.status_text.insert(tk.END, message, "message")
        
        self.status_text.tag_config("header", foreground=color, font=("Arial", 12, "bold"))
        self.status_text.tag_config("message", foreground="#ecf0f1", font=("Arial", 12))
        
        self.status_text.config(state=tk.DISABLED)
    
    def process_qr_scan(self):
        """Process the scanned QR code and log Time-In or Time-Out"""
        qr_data = self.qr_input_var.get().strip()
        
        if not qr_data:
            self.update_status("No QR code data detected. Please scan a valid QR code.", "error")
            return
        
        # Parse QR data
        parsed_data = self.qr_generator.parse_qr_data(qr_data)
        
        if not parsed_data:
            self.update_status(
                f"Invalid QR code format.\n\nScanned data: {qr_data}\n\n"
                "Please scan a valid ALIBLOG QR code.",
                "error"
            )
            self.qr_input_var.set("")
            self.qr_entry.focus_set()
            return
        
        # Get user from database
        user = self.db_manager.get_user_by_qr_data(
            parsed_data['name'],
            parsed_data['id_number']
        )
        
        if not user:
            self.update_status(
                f"User not found in database.\n\n"
                f"Name: {parsed_data['name']}\n"
                f"ID: {parsed_data['id_number']}\n\n"
                "Please register first.",
                "error"
            )
            self.qr_input_var.set("")
            self.qr_entry.focus_set()
            return
        
        # Check if user has an active log (no Time-Out)
        active_log = self.db_manager.get_active_log(user['user_id'])
        
        if active_log:
            # User is logging OUT
            success = self.db_manager.create_time_out(active_log['log_id'])
            
            if success:
                # Get the updated log to show duration
                log_details = self.db_manager.get_log_details(active_log['log_id'])
                
                self.update_status(
                    f"TIME-OUT recorded successfully!\n\n"
                    f"Name: {user['name']}\n"
                    f"ID: {user['id_number']}\n"
                    f"Department: {user['department']}\n"
                    f"User Type: {user['user_type']}\n\n"
                    f"Time-In: {active_log['time_in']}\n"
                    f"Time-Out: {datetime.now().strftime('%H:%M:%S')}\n"
                    f"Duration: {log_details['duration']}\n\n"
                    f"Thank you for visiting the library!",
                    "success"
                )
                
                # Play success sound or visual feedback (optional)
                self.window.bell()
            else:
                self.update_status("Failed to record Time-Out. Please try again.", "error")
        else:
            # User is logging IN
            log_id = self.db_manager.create_time_in(
                user['user_id'],
                user['name'],
                user['department']
            )
            
            if log_id:
                self.update_status(
                    f"TIME-IN recorded successfully!\n\n"
                    f"Name: {user['name']}\n"
                    f"ID: {user['id_number']}\n"
                    f"Department: {user['department']}\n"
                    f"User Type: {user['user_type']}\n\n"
                    f"Time-In: {datetime.now().strftime('%H:%M:%S')}\n"
                    f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
                    f"Welcome to the library!",
                    "success"
                )
                
                # Play success sound or visual feedback (optional)
                self.window.bell()
            else:
                self.update_status("Failed to record Time-In. Please try again.", "error")
        
        # Clear input field and refocus
        self.qr_input_var.set("")
        self.qr_entry.focus_set()
