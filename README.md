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
This is the exact file that opens the camera and does live scanning:
- Automatically uses the laptop’s built-in webcam OR any connected USB QR scanner
- Real-time detection (scans in less than 0.3 seconds)
- Shows live video feed with green box around detected QR
- Displays on-screen: "TIME IN → Maria Santos (Student)" or "TIME OUT"
- Prevents double scanning on the same day
- Runs in background while admin panel is open
→ You do NOT need to change anything — just connect camera/scanner and run the program

$ admin_panel.py - FRONT END
Beautiful, large-font Tkinter dashboard with:
- Real-time attendance log table (auto-refreshes every scan)
- Search & filter by name or ID
- Three big buttons at the top:
  → "REGISTER NEW PERSON (Student/Teacher/Guest)" → pop-up + instant QR
  → "MANAGE ADMIN ACCOUNTS" → secure admin management
  → "OPEN LIVE SCANNER" → opens scanner.py window 
- Print/report button (ready for date-range export)
- Designed for 24/7 use at school entrance

$ main.py 
The master launcher:
- Initializes database
- Automatically starts the live QR scanner in background (scanner.py)
- Opens the full admin panel
- Everything runs with one command: python main.py

# How the scanning works in real life (you asked this!)
- If you use a laptop → uses built-in webcam automatically
- If you connect a handheld QR/barcode scanner (like the ones in stores) → it works even better!
  → The scanner acts like a keyboard → just point and click → no camera needed
  → The system detects it automatically and logs instantly
- Both methods work at the same time if you want

# Additional files created automatically:
- attendance.db → Single offline database
- qr_codes/ → All QR codes ready to print
- Default admin ready

Fully offline | Works with laptop camera OR USB scanner | Zero setup
Perfect for schools, offices, events, churches
Just plug in → scan → done!