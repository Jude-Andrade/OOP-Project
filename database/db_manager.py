"""
Database Manager Module

This module handles all database operations for the ALIBLOG system.
It manages three main tables: admin_accounts, registered_users, and log_records.
"""

import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    """Manages all database operations for the library logbook system"""
    
    def __init__(self, db_path="database/aliblog.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.ensure_database_directory()
    
    def ensure_database_directory(self):
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self):
        """
        Get a database connection
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        return sqlite3.connect(self.db_path)
    
    def initialize_database(self):
        """Create all necessary tables and insert default admin account"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create admin_accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_accounts (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        
        # Create registered_users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registered_users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                id_number TEXT NOT NULL,
                department TEXT NOT NULL,
                user_type TEXT NOT NULL CHECK(user_type IN ('Student', 'Teacher', 'Guest')),
                qr_path TEXT,
                registration_date TEXT NOT NULL
            )
        """)
        
        # Create log_records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_records (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                department_or_status TEXT NOT NULL,
                time_in TEXT NOT NULL,
                time_out TEXT,
                duration TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES registered_users(user_id)
            )
        """)
        
        # Insert default admin account (username: admin, password: admin123)
        try:
            cursor.execute("""
                INSERT INTO admin_accounts (username, password)
                VALUES (?, ?)
            """, ("admin", "admin123"))
        except sqlite3.IntegrityError:
            # Admin already exists
            pass
        
        conn.commit()
        conn.close()
    
    # ==================== ADMIN OPERATIONS ====================
    
    def verify_admin(self, username, password):
        """
        Verify admin credentials
        
        Args:
            username: Admin username
            password: Admin password
            
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT admin_id FROM admin_accounts
            WHERE username = ? AND password = ?
        """, (username, password))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    # ==================== USER REGISTRATION OPERATIONS ====================
    
    def register_user(self, name, id_number, department, user_type, qr_path):
        """
        Register a new user
        
        Args:
            name: User's full name
            id_number: Student/Teacher ID or "Guest"
            department: Department name or "Guest"
            user_type: Student, Teacher, or Guest
            qr_path: Path to generated QR code image
            
        Returns:
            int: The new user's ID, or None if registration failed
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            cursor.execute("""
                INSERT INTO registered_users 
                (name, id_number, department, user_type, qr_path, registration_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, id_number, department, user_type, qr_path, registration_date))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.close()
            return None
    
    def get_user_by_qr_data(self, name, id_number):
        """
        Find a user by their QR code data
        
        Args:
            name: User's name
            id_number: User's ID number
            
        Returns:
            dict: User data or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, name, id_number, department, user_type
            FROM registered_users
            WHERE name = ? AND id_number = ?
        """, (name, id_number))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'user_id': row[0],
                'name': row[1],
                'id_number': row[2],
                'department': row[3],
                'user_type': row[4]
            }
        return None
    
    def check_id_exists(self, id_number):
        """
        Check if an ID number is already registered
        
        Args:
            id_number: ID number to check
            
        Returns:
            bool: True if ID exists, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id FROM registered_users
            WHERE id_number = ?
        """, (id_number,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    # ==================== LOG OPERATIONS ====================
    
    def get_active_log(self, user_id):
        """
        Get the active log entry (no time-out) for a user
        
        Args:
            user_id: User's ID
            
        Returns:
            dict: Log data or None if no active log
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT log_id, time_in, date
            FROM log_records
            WHERE user_id = ? AND time_out IS NULL
            ORDER BY log_id DESC
            LIMIT 1
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'log_id': row[0],
                'time_in': row[1],
                'date': row[2]
            }
        return None
    
    def create_time_in(self, user_id, name, department_or_status):
        """
        Create a new Time-In log entry
        
        Args:
            user_id: User's ID
            name: User's name
            department_or_status: Department name or "Guest"
            
        Returns:
            int: Log ID or None if failed
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now()
        time_in = now.strftime("%H:%M:%S")
        date = now.strftime("%Y-%m-%d")
        
        try:
            cursor.execute("""
                INSERT INTO log_records 
                (user_id, name, department_or_status, time_in, date)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, department_or_status, time_in, date))
            
            conn.commit()
            log_id = cursor.lastrowid
            conn.close()
            return log_id
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.close()
            return None
    
    def create_time_out(self, log_id):
        """
        Update a log entry with Time-Out and calculate duration
        
        Args:
            log_id: Log entry ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get the time_in value
        cursor.execute("SELECT time_in FROM log_records WHERE log_id = ?", (log_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        time_in_str = row[0]
        time_out_str = datetime.now().strftime("%H:%M:%S")
        
        # Calculate duration
        time_in = datetime.strptime(time_in_str, "%H:%M:%S")
        time_out = datetime.strptime(time_out_str, "%H:%M:%S")
        duration_seconds = int((time_out - time_in).total_seconds())
        
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        try:
            cursor.execute("""
                UPDATE log_records
                SET time_out = ?, duration = ?
                WHERE log_id = ?
            """, (time_out_str, duration_str, log_id))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.close()
            return False
    
    # ==================== ADMIN QUERY OPERATIONS ====================
    
    def get_today_logs(self):
        """
        Get all logs for today
        
        Returns:
            list: List of log dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute("""
            SELECT log_id, name, department_or_status, time_in, time_out, duration, date
            FROM log_records
            WHERE date = ?
            ORDER BY log_id DESC
        """, (today,))
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                'log_id': row[0],
                'name': row[1],
                'department_or_status': row[2],
                'time_in': row[3],
                'time_out': row[4] if row[4] else "---",
                'duration': row[5] if row[5] else "---",
                'date': row[6]
            })
        
        conn.close()
        return logs
    
    def search_logs(self, search_term=None, date_from=None, date_to=None, 
                    user_type_filter=None, search_field="name"):
        """
        Search and filter log records
        
        Args:
            search_term: Term to search for
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            user_type_filter: Filter by user type
            search_field: Field to search in (name, id_number, department)
            
        Returns:
            list: List of matching log dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build query dynamically
        query = """
            SELECT l.log_id, l.name, l.department_or_status, l.time_in, 
                   l.time_out, l.duration, l.date, u.user_type, u.id_number
            FROM log_records l
            LEFT JOIN registered_users u ON l.user_id = u.user_id
            WHERE 1=1
        """
        params = []
        
        # Add search term filter
        if search_term:
            if search_field == "name":
                query += " AND l.name LIKE ?"
                params.append(f"%{search_term}%")
            elif search_field == "id_number":
                query += " AND u.id_number LIKE ?"
                params.append(f"%{search_term}%")
            elif search_field == "department":
                query += " AND l.department_or_status LIKE ?"
                params.append(f"%{search_term}%")
        
        # Add date range filter
        if date_from:
            query += " AND l.date >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND l.date <= ?"
            params.append(date_to)
        
        # Add user type filter
        if user_type_filter and user_type_filter != "All":
            query += " AND u.user_type = ?"
            params.append(user_type_filter)
        
        query += " ORDER BY l.log_id DESC"
        
        cursor.execute(query, params)
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                'log_id': row[0],
                'name': row[1],
                'department_or_status': row[2],
                'time_in': row[3],
                'time_out': row[4] if row[4] else "---",
                'duration': row[5] if row[5] else "---",
                'date': row[6],
                'user_type': row[7] if row[7] else "N/A",
                'id_number': row[8] if row[8] else "N/A"
            })
        
        conn.close()
        return logs
    
    def get_log_details(self, log_id):
        """
        Get detailed information for a specific log entry
        
        Args:
            log_id: Log entry ID
            
        Returns:
            dict: Detailed log information or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT l.log_id, l.name, l.department_or_status, l.time_in,
                   l.time_out, l.duration, l.date, u.user_id, u.user_type, u.id_number
            FROM log_records l
            LEFT JOIN registered_users u ON l.user_id = u.user_id
            WHERE l.log_id = ?
        """, (log_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'log_id': row[0],
                'name': row[1],
                'department_or_status': row[2],
                'time_in': row[3],
                'time_out': row[4] if row[4] else "Not yet",
                'duration': row[5] if row[5] else "Not yet",
                'date': row[6],
                'user_id': row[7],
                'user_type': row[8] if row[8] else "N/A",
                'id_number': row[9] if row[9] else "N/A"
            }
        return None

    def delete_user(self, user_id):
        """
        Delete a registered user and all associated log records.

        Args:
            user_id: ID of the registered user to delete

        Returns:
            bool: True if deletion succeeded, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Get qr_path so we can remove the QR image file if present
            cursor.execute("SELECT qr_path FROM registered_users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            qr_path = row[0] if row else None

            # Delete log records for this user
            cursor.execute("DELETE FROM log_records WHERE user_id = ?", (user_id,))

            # Delete the user record
            cursor.execute("DELETE FROM registered_users WHERE user_id = ?", (user_id,))

            conn.commit()
            conn.close()

            # Remove QR file from disk if it exists
            if qr_path and os.path.exists(qr_path):
                try:
                    os.remove(qr_path)
                except Exception:
                    # Non-fatal if file removal fails
                    pass

            return True
        except sqlite3.Error as e:
            print(f"Database error while deleting user: {e}")
            conn.close()
            return False
