import sqlite3

DB_PATH = 'data.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table_if_not_exists():
    with get_connection() as connection:
        connection.execute("""
                           CREATE TABLE IF NOT EXISTS Credentials (
                               userId TEXT PRIMARY KEY NOT NULL,
                               username TEXT NOT NULL,
                               password TEXT NOT NULL,
                               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )
                           """)
        connection.commit()

def init_db():
    create_table_if_not_exists()



