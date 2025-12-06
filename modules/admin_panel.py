"""
Admin Panel Module

This module provides admin authentication and a comprehensive dashboard
for viewing, searching, filtering, and exporting log records.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import ctypes
from datetime import datetime
from tkcalendar import DateEntry


class AdminLoginWindow:
    """Admin login window"""
    
    def __init__(self, parent, db_manager):
        """
        Initialize admin login window
        
        Args:
            parent: Parent Tkinter window
            db_manager: DatabaseManager instance
        """
        self.parent = parent
        self.db_manager = db_manager
        
        # Create new window
        self.window = tk.Toplevel(parent)
        self.window.title("Admin Login - EVSU-OC ALIBLOG")
        # make the login window larger to match desired UI and center it
        self.window.geometry("720x520")
        # prevent resizing to keep layout stable
        self.window.resizable(False, False)
        self.window.configure(bg="#34495e")
        
        # Center window
        self.center_window(720, 520)
        
        # Make window overlay everything
        self.window.attributes('-topmost', True)
        self.window.lift()
        self.window.focus_set()
        # Try to remove the minimize button on Windows (non-fatal if it fails)
        try:
            # Remove minimize and maximize buttons but keep close (WS_SYSMENU)
            GWL_STYLE = -16
            WS_MINIMIZEBOX = 0x00020000
            WS_MAXIMIZEBOX = 0x00010000
            hwnd = self.window.winfo_id()
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            style = style & ~WS_MINIMIZEBOX & ~WS_MAXIMIZEBOX
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            # Apply the change so the titlebar updates
            SWP_NOSIZE = 0x1
            SWP_NOMOVE = 0x2
            SWP_NOZORDER = 0x4
            SWP_FRAMECHANGED = 0x20
            flags = SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED
            ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, flags)
        except Exception:
            pass
        
        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        # Guard to avoid repeated error dialogs stacking
        self._login_error_shown = False
        
        self.create_widgets()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create login form widgets"""
        
        # Title
        title_frame = tk.Frame(self.window, bg="#e74c3c", pady=30)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🔐 ADMIN LOGIN",
            font=("Arial", 26, "bold"),
            bg="#e74c3c",
            fg="white"
        )
        title_label.pack()
        
        # Form frame
        form_frame = tk.Frame(self.window, bg="#34495e")
        form_frame.pack(expand=True, pady=30)
        
        # Username
        username_label = tk.Label(
            form_frame,
            text="Username:",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        username_label.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        
        self.username_entry = tk.Entry(
            form_frame,
            textvariable=self.username_var,
            font=("Arial", 14),
            width=25
        )
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        self.username_entry.focus_set()
        # Reset error-flag when user types
        self.username_entry.bind('<Key>', lambda e: self.reset_login_error_flag())
        
        # Password
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        password_label.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        
        self.password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=("Arial", 14),
            width=25,
            show="●"
        )
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        # Reset error-flag when user types
        self.password_entry.bind('<Key>', lambda e: self.reset_login_error_flag())
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = tk.Button(
            form_frame,
            text="✅ LOGIN",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            width=20,
            height=2,
            cursor="hand2",
            command=self.login
        )
        login_btn.grid(row=2, column=0, columnspan=2, pady=30)
        
        # Create Admin button
        create_admin_btn = tk.Button(
            form_frame,
            text="➕ Create Admin",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=20,
            height=1,
            cursor="hand2",
            command=lambda: [self.window.destroy(), CreateAdminWindow(self.parent, self.db_manager)]
        )
        create_admin_btn.grid(row=3, column=0, columnspan=2, pady=(0,10))
        
    
    def login(self):
        """Verify credentials and open admin dashboard"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            # Prevent re-entrant stacking while the modal dialog is open by
            # setting the guard during the showerror call, then reset it
            # once the user dismisses the dialog so it can reappear again.
            if not self._login_error_shown:
                try:
                    self._login_error_shown = True
                    messagebox.showerror("Login Error", "Please enter both username and password.", parent=self.window)
                except Exception:
                    # Fallback if attaching parent fails
                    self._login_error_shown = True
                    messagebox.showerror("Login Error", "Please enter both username and password.")
                finally:
                    self._login_error_shown = False
            return
        
        if self.db_manager.verify_admin(username, password):
            self.window.destroy()
            AdminDashboard(self.parent, self.db_manager)
        else:
            # Prevent stacking while the error dialog is visible; allow it
            # to reappear after the user dismisses it (without forcing typing).
            if not self._login_error_shown:
                try:
                    self._login_error_shown = True
                    messagebox.showerror("Login Failed", "Invalid username or password.", parent=self.window)
                except Exception:
                    self._login_error_shown = True
                    messagebox.showerror("Login Failed", "Invalid username or password.")
                finally:
                    self._login_error_shown = False
            self.password_var.set("")

    def reset_login_error_flag(self):
        """Reset the guard so error dialogs can show again after user input."""
        self._login_error_shown = False


class AdminDashboard:
    """Admin dashboard for viewing and managing logs"""
    
    def __init__(self, parent, db_manager):
        """
        Initialize admin dashboard
        
        Args:
            parent: Parent Tkinter window
            db_manager: DatabaseManager instance
        """
        self.parent = parent
        self.db_manager = db_manager
        
        # Create new window
        self.window = tk.Toplevel(parent)
        self.window.title("Admin Dashboard - EVSU-OC ALIBLOG")
        self.window.configure(bg="#ecf0f1")

        # Try to maximize the dashboard to fill the screen. Use 'zoomed'
        # where supported (Windows), otherwise fall back to setting the
        # geometry to the screen size.
        try:
            self.window.state('zoomed')
        except Exception:
            try:
                sw = self.window.winfo_screenwidth()
                sh = self.window.winfo_screenheight()
                self.window.geometry(f"{sw}x{sh}+0+0")
            except Exception:
                # As a last resort, keep the default size
                self.window.geometry("1400x800")
        
        # Variables
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="name")
        self.user_type_var = tk.StringVar(value="All")
        self.date_from_var = tk.StringVar()
        self.date_to_var = tk.StringVar()
        
        self.current_logs = []
        
        self.create_widgets()
        self.load_today_logs()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create dashboard widgets"""
        
        # Title bar
        title_frame = tk.Frame(self.window, bg="#e74c3c", pady=15)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="📊 ADMIN DASHBOARD",
            font=("Arial", 24, "bold"),
            bg="#e74c3c",
            fg="white"
        )
        title_label.pack()
        
        # Control panel
        control_frame = tk.Frame(self.window, bg="#34495e", pady=15)
        control_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        # Search section
        search_label = tk.Label(
            control_frame,
            text="Search:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        search_entry = tk.Entry(
            control_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            width=30
        )
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Search field selector
        search_field_label = tk.Label(
            control_frame,
            text="Search by:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        search_field_label.grid(row=0, column=2, padx=5, pady=5)
        
        search_field_combo = ttk.Combobox(
            control_frame,
            textvariable=self.search_field_var,
            values=["name", "id_number", "department"],
            state="readonly",
            font=("Arial", 11),
            width=15
        )
        search_field_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # User type filter
        type_label = tk.Label(
            control_frame,
            text="User Type:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        type_label.grid(row=0, column=4, padx=5, pady=5)
        
        type_combo = ttk.Combobox(
            control_frame,
            textvariable=self.user_type_var,
            values=["All", "Student", "Teacher", "Guest"],
            state="readonly",
            font=("Arial", 11),
            width=12
        )
        type_combo.grid(row=0, column=5, padx=5, pady=5)
        
        # Date range filters
        date_label = tk.Label(
            control_frame,
            text="Date From:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        date_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        try:
            self.date_from_picker = DateEntry(
                control_frame,
                textvariable=self.date_from_var,
                font=("Arial", 11),
                width=15,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd'
            )
            self.date_from_picker.grid(row=1, column=1, padx=5, pady=5)
        except:
            # Fallback if tkcalendar is not available
            date_from_entry = tk.Entry(
                control_frame,
                textvariable=self.date_from_var,
                font=("Arial", 11),
                width=18
            )
            date_from_entry.grid(row=1, column=1, padx=5, pady=5)
        
        date_to_label = tk.Label(
            control_frame,
            text="Date To:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        date_to_label.grid(row=1, column=2, padx=5, pady=5)
        
        try:
            self.date_to_picker = DateEntry(
                control_frame,
                textvariable=self.date_to_var,
                font=("Arial", 11),
                width=15,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd'
            )
            self.date_to_picker.grid(row=1, column=3, padx=5, pady=5)
        except:
            # Fallback if tkcalendar is not available
            date_to_entry = tk.Entry(
                control_frame,
                textvariable=self.date_to_var,
                font=("Arial", 11),
                width=18
            )
            date_to_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg="#34495e")
        button_frame.grid(row=1, column=4, columnspan=2, padx=5, pady=5)
        
        search_btn = tk.Button(
            button_frame,
            text="🔍 Search",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.search_logs
        )
        search_btn.pack(side=tk.LEFT, padx=3)
        
        today_btn = tk.Button(
            button_frame,
            text="📅 Today",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.load_today_logs
        )
        today_btn.pack(side=tk.LEFT, padx=3)
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            font=("Arial", 11, "bold"),
            bg="#e67e22",
            fg="white",
            cursor="hand2",
            command=self.refresh_logs
        )
        refresh_btn.pack(side=tk.LEFT, padx=3)
        
        export_btn = tk.Button(
            button_frame,
            text="📄 Export",
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self.export_logs
        )
        export_btn.pack(side=tk.LEFT, padx=3)
        
        # Table frame
        table_frame = tk.Frame(self.window, bg="#ecf0f1")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview (table)
        columns = ("Log ID", "Name", "Dept/Status", "Time In", "Time Out", "Duration", "Date")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            height=20
        )
        
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("Log ID", text="Log ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Dept/Status", text="Department/Status")
        self.tree.heading("Time In", text="Time In")
        self.tree.heading("Time Out", text="Time Out")
        self.tree.heading("Duration", text="Duration")
        self.tree.heading("Date", text="Date")
        
        self.tree.column("Log ID", width=80, anchor=tk.CENTER)
        self.tree.column("Name", width=200, anchor=tk.W)
        self.tree.column("Dept/Status", width=200, anchor=tk.W)
        self.tree.column("Time In", width=100, anchor=tk.CENTER)
        self.tree.column("Time Out", width=100, anchor=tk.CENTER)
        self.tree.column("Duration", width=100, anchor=tk.CENTER)
        self.tree.column("Date", width=120, anchor=tk.CENTER)
        
        # Double-click to view details
        self.tree.bind('<Double-Button-1>', self.view_log_details)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Status bar
        status_frame = tk.Frame(self.window, bg="#34495e", pady=10)
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Arial", 11),
            bg="#34495e",
            fg="white"
        )
        self.status_label.pack()
    
    def clear_table(self):
        """Clear all items from the table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def populate_table(self, logs):
        """Populate table with log data"""
        self.clear_table()
        self.current_logs = logs
        
        for log in logs:
            self.tree.insert("", tk.END, values=(
                log['log_id'],
                log['name'],
                log['department_or_status'],
                log['time_in'],
                log['time_out'],
                log['duration'],
                log['date']
            ))
        
        self.status_label.config(text=f"Showing {len(logs)} record(s)")
    
    def load_today_logs(self):
        """Load today's logs"""
        logs = self.db_manager.get_today_logs()
        self.populate_table(logs)
        self.status_label.config(text=f"Today's logs: {len(logs)} record(s)")
    
    def search_logs(self):
        """Search logs based on filters"""
        search_term = self.search_var.get().strip() if self.search_var.get().strip() else None
        search_field = self.search_field_var.get()
        user_type = self.user_type_var.get()
        date_from = self.date_from_var.get() if self.date_from_var.get() else None
        date_to = self.date_to_var.get() if self.date_to_var.get() else None
        
        logs = self.db_manager.search_logs(
            search_term=search_term,
            date_from=date_from,
            date_to=date_to,
            user_type_filter=user_type,
            search_field=search_field
        )
        
        self.populate_table(logs)
        self.status_label.config(text=f"Search results: {len(logs)} record(s)")
    
    def refresh_logs(self):
        """Refresh the current view"""
        if self.search_var.get() or self.date_from_var.get() or self.date_to_var.get():
            self.search_logs()
        else:
            self.load_today_logs()
    
    def view_log_details(self, event):
        """View detailed information for a selected log"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        log_id = item['values'][0]
        
        log_details = self.db_manager.get_log_details(log_id)
        
        if log_details:
            details_text = (
                f"Log ID: {log_details['log_id']}\n"
                f"Name: {log_details['name']}\n"
                f"ID Number: {log_details['id_number']}\n"
                f"Department/Status: {log_details['department_or_status']}\n"
                f"User Type: {log_details['user_type']}\n"
                f"Date: {log_details['date']}\n"
                f"Time In: {log_details['time_in']}\n"
                f"Time Out: {log_details['time_out']}\n"
                f"Duration: {log_details['duration']}"
            )
            
            try:
                # Attach the dialog to the dashboard window so it appears on top
                messagebox.showinfo("Log Details", details_text, parent=self.window)
            except Exception:
                # Fallback if attaching parent fails
                messagebox.showinfo("Log Details", details_text)
    
    def export_logs(self):
        """Export current logs to a text file"""
        if not self.current_logs:
            messagebox.showwarning("No Data", "No logs to export.")
            return
        
        # Ask for save location
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"ALIBLOG_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            title="Export Logs"
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # Header
                f.write("=" * 80 + "\n")
                f.write("EVSU-OC ALIBLOG - Library Log Records\n")
                f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Total Records: {len(self.current_logs)}\n\n")
                
                # Table header
                f.write(f"{'Log ID':<10} {'Name':<25} {'Department':<20} {'Time In':<12} {'Time Out':<12} {'Duration':<12} {'Date':<15}\n")
                f.write("-" * 120 + "\n")
                
                # Data rows
                for log in self.current_logs:
                    f.write(
                        f"{str(log['log_id']):<10} "
                        f"{log['name']:<25} "
                        f"{log['department_or_status']:<20} "
                        f"{log['time_in']:<12} "
                        f"{log['time_out']:<12} "
                        f"{log['duration']:<12} "
                        f"{log['date']:<15}\n"
                    )
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("End of Report\n")
            
            messagebox.showinfo("Export Successful", f"Logs exported successfully to:\n{filepath}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export logs:\n{e}")


class CreateAdminWindow:
    """Create new admin account window with creator verification"""
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager

        # Create new window
        self.window = tk.Toplevel(parent)
        self.window.title("Create Admin Account - EVSU-OC ALIBLOG")
        self.window.geometry("500x420")
        self.window.configure(bg="#34495e")

        # Center window
        self.center_window(500, 420)

        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var = tk.StringVar()

        self.create_widgets()

        # Make modal-like
        try:
            self.window.transient(self.parent)
            self.window.grab_set()
        except Exception:
            pass

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Back button
        back_btn = tk.Button(
            self.window,
            text="← Back",
            font=("Arial", 11, "bold"),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=lambda: [self.window.destroy(), AdminLoginWindow(self.parent, self.db_manager)]
        )
        back_btn.pack(anchor=tk.NW, padx=10, pady=6)

        title_frame = tk.Frame(self.window, bg="#27ae60", pady=20)
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="➕ CREATE ADMIN ACCOUNT",
            font=("Arial", 20, "bold"),
            bg="#27ae60",
            fg="white"
        )
        title_label.pack()

        form_frame = tk.Frame(self.window, bg="#34495e")
        form_frame.pack(expand=True, pady=20)

        # Username
        username_label = tk.Label(
            form_frame,
            text="New Username:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        username_label.grid(row=0, column=0, sticky=tk.W, pady=8, padx=10)

        username_entry = tk.Entry(
            form_frame,
            textvariable=self.username_var,
            font=("Arial", 12),
            width=28
        )
        username_entry.grid(row=0, column=1, pady=8, padx=10)
        username_entry.focus_set()

        # Password
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        password_label.grid(row=1, column=0, sticky=tk.W, pady=8, padx=10)

        password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=("Arial", 12),
            width=28,
            show="●"
        )
        password_entry.grid(row=1, column=1, pady=8, padx=10)

        # Confirm Password
        confirm_label = tk.Label(
            form_frame,
            text="Confirm Password:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        confirm_label.grid(row=2, column=0, sticky=tk.W, pady=8, padx=10)

        confirm_entry = tk.Entry(
            form_frame,
            textvariable=self.confirm_var,
            font=("Arial", 12),
            width=28,
            show="●"
        )
        confirm_entry.grid(row=2, column=1, pady=8, padx=10)

        # Create button
        create_btn = tk.Button(
            form_frame,
            text="✅ CREATE ACCOUNT",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            width=22,
            height=1,
            cursor="hand2",
            command=self.create_account
        )
        create_btn.grid(row=3, column=0, columnspan=2, pady=18)

        note_label = tk.Label(
            self.window,
            text="Note: Creating a new admin requires verification by an existing admin.",
            font=("Arial", 9),
            bg="#34495e",
            fg="#ecf0f1"
        )
        note_label.pack(side=tk.BOTTOM, pady=10)

    def prompt_creator_credentials(self):
        """Prompt for existing admin credentials and verify them."""
        dialog = tk.Toplevel(self.window)
        dialog.title("Verify Admin - EVSU-OC ALIBLOG")
        dialog.geometry("400x200")
        dialog.configure(bg="#34495e")
        self.center_child(dialog, 400, 200)

        username_var = tk.StringVar()
        password_var = tk.StringVar()

        tk.Label(dialog, text="Verifier Username:", bg="#34495e", fg="white", font=("Arial", 11, "bold")).pack(pady=(20,5))
        u_entry = tk.Entry(dialog, textvariable=username_var, width=30)
        u_entry.pack()

        tk.Label(dialog, text="Verifier Password:", bg="#34495e", fg="white", font=("Arial", 11, "bold")).pack(pady=(10,5))
        p_entry = tk.Entry(dialog, textvariable=password_var, show="●", width=30)
        p_entry.pack()

        result = {'ok': False}

        def on_verify():
            user = username_var.get().strip()
            pwd = password_var.get().strip()
            if not user or not pwd:
                messagebox.showerror("Verification Error", "Please enter verifier credentials.", parent=dialog)
                return
            if self.db_manager.verify_admin(user, pwd):
                result['ok'] = True
                dialog.destroy()
            else:
                messagebox.showerror("Verification Failed", "Invalid verifier credentials.", parent=dialog)
                password_var.set("")

        btn_frame = tk.Frame(dialog, bg="#34495e")
        btn_frame.pack(pady=12)

        verify_btn = tk.Button(btn_frame, text="Verify", bg="#27ae60", fg="white", command=on_verify)
        verify_btn.pack(side=tk.LEFT, padx=6)

        cancel_btn = tk.Button(btn_frame, text="Cancel", bg="#95a5a6", fg="white", command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=6)

        try:
            dialog.transient(self.window)
            dialog.grab_set()
            self.window.wait_window(dialog)
        except Exception:
            # Fallback if modality isn't supported
            pass

        return result['ok']

    def center_child(self, child, width, height):
        screen_width = child.winfo_screenwidth()
        screen_height = child.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        child.geometry(f"{width}x{height}+{x}+{y}")

    def create_account(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        confirm = self.confirm_var.get().strip()

        # Validate input
        if not username:
            messagebox.showerror("Validation Error", "Please enter a username.", parent=self.window)
            return

        if len(username) < 3:
            messagebox.showerror("Validation Error", "Username must be at least 3 characters.", parent=self.window)
            return

        if not password:
            messagebox.showerror("Validation Error", "Please enter a password.", parent=self.window)
            return

        if len(password) < 6:
            messagebox.showerror("Validation Error", "Password must be at least 6 characters.", parent=self.window)
            return

        if password != confirm:
            messagebox.showerror("Validation Error", "Passwords do not match.", parent=self.window)
            return

        # Ask for verification from an existing admin
        verified = self.prompt_creator_credentials()
        if not verified:
            messagebox.showwarning("Not Verified", "Admin creation requires verification by an existing admin.", parent=self.window)
            return

        # Try to create the account
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO admin_accounts (username, password)
                VALUES (?, ?)
            """, (username, password))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Admin account '{username}' created successfully!", parent=self.window)
            self.window.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"Username '{username}' already exists.", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create admin account:\n{e}", parent=self.window)
