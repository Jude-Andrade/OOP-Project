"""
Admin Panel Module

This module provides admin authentication and a comprehensive dashboard
for viewing, searching, filtering, and exporting log records.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.window.geometry("500x400")
        self.window.configure(bg="#34495e")
        
        # Center window
        self.center_window(500, 400)
        
        # Make window overlay everything
        self.window.attributes('-topmost', True)
        self.window.lift()
        self.window.focus_set()
        
        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
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
        
        username_entry = tk.Entry(
            form_frame,
            textvariable=self.username_var,
            font=("Arial", 14),
            width=25
        )
        username_entry.grid(row=0, column=1, pady=10, padx=10)
        username_entry.focus_set()
        
        # Password
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        password_label.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        
        password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=("Arial", 14),
            width=25,
            show="●"
        )
        password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Bind Enter key
        password_entry.bind('<Return>', lambda e: self.login())
        
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
        
        # Info label
        info_label = tk.Label(
            self.window,
            text="Default credentials: admin / admin123",
            font=("Arial", 10, "italic"),
            bg="#34495e",
            fg="#95a5a6"
        )
        info_label.pack(side=tk.BOTTOM, pady=10)
    
    def login(self):
        """Verify credentials and open admin dashboard"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return
        
        if self.db_manager.verify_admin(username, password):
            self.window.destroy()
            AdminDashboard(self.parent, self.db_manager)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.password_var.set("")


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
        self.window.geometry("1400x800")
        self.window.configure(bg="#ecf0f1")
        
        # Center window
        self.center_window(1400, 800)
        
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
        
        # Close button
        close_btn = tk.Button(
            self.window,
            text="❌ Close Dashboard",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            cursor="hand2",
            command=self.window.destroy
        )
        close_btn.pack(pady=10)
    
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
