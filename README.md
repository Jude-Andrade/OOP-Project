qr_attendance_system/
├── database.py
├── qr_generator.py
├── scanner.py
├── admin_panel.py
├── main.py
├── logs/
└── qr_codes/

# Project Folder: qr_attendance_system/

$ database.py
Contains all SQLite database logic:
Creates three tables (admins, registered users, attendance logs)
Initializes the database with a default admin account
Handles logging Time-In and Time-Out with automatic duration calculation

$ qr_generator.py
Responsible for user registration:
Takes name and role (Student/Teacher/Guest)
Generates a unique ID
Creates and saves a printable QR code image in the qr_codes/ folder

$ scanner.py
The live QR code scanner:
Opens the webcam
Detects and reads QR codes in real time
Checks if the person is already timed in/out today
Records Time-In or Time-Out automatically
Prevents duplicate scans on the same day

$ admin_panel.py
The real-time administrator dashboard (Tkinter GUI):
Shows today’s and past attendance logs in a big, easy-to-read table
Live updates when someone scans their QR
Search and filter by name or ID
Large fonts for use on a monitor at the entrance
Print/report button (ready for date-range reports)

$ main.py
The launcher:
Initializes everything
Opens the admin panel window
Starts the QR scanner in the background at the same time


# Additional folders created automatically:

# qr_codes/ → Stores all generated QR code images (.png)
# attendance.db → Single SQLite file that holds all data (works completely offline)
