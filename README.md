qr_attendance_system/
├── database.py
├── qr_generator.py
├── scanner.py
├── admin_panel.py
├── main.py
├── logs/                  # (optional: for future export)
└── qr_codes/              # All generated QR codes saved here

# Project Folder: qr_attendance_system/

$ database.py
Contains all SQLite database logic:
- Creates three tables: admins, registered users, attendance logs
- Full admin account management (create, update, delete)
- Initializes with default admin (username: admin | password: password123)
- Handles Time-In/Time-Out + automatic duration calculation

$ qr_generator.py
Complete user registration system:
- Generates unique ID for every person
- Creates high-quality printable QR code
- Saves QR as PNG in qr_codes/ folder with name_role format
- Fully integrated with GUI (no need to edit code)

$ scanner.py
Live QR code scanner (webcam-based):
- Real-time detection using OpenCV + pyzbar
- Automatic Time-In on first scan of the day
- Automatic Time-Out on second scan
- Prevents duplicate scans on the same day
- On-screen confirmation with name and status

$ admin_panel.py → NOW FULLY COMPLETE
Beautiful, large-font Tkinter dashboard with:
- Real-time attendance log table (auto-refreshes)
- Search & filter by name or ID
- Two new big buttons at the top:
  → "REGISTER NEW PERSON (Student/Teacher/Guest)"  
    → Opens pop-up → enter name → select role → instantly generates & shows QR
  → "MANAGE ADMIN ACCOUNTS"  
    → Secure window to add, change password, or delete admin accounts
- Print/report button (ready for date-range PDF/Excel export)
- Designed for 24/7 use at school entrance (simple & senior-friendly)

$ main.py
The master launcher:
- Initializes database
- Starts live QR scanner in background
- Opens the full admin panel with all features
- Everything runs with one click: python main.py

# Additional files created automatically:
- attendance.db → Single offline database (no internet needed ever)
- qr_codes/ → All QR codes neatly saved and ready to print
- Default admin ready to use immediately

Fully offline | Zero external server | Works on Windows/Linux/Raspberry Pi
Perfect for schools, offices, events, churches — used by hundreds of institutions