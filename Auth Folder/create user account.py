import sqlite3
from database import get_connection, create_table_if_not_exists, init_db
import hashlib


class Account_Creator:
    def __init__(self):
        init_db()
    
    @staticmethod
    def add_account(userId, username, hashedpassword):
        
        create_table_if_not_exists()
        
        try:
            with get_connection() as connection:
                connection.execute("INSERT INTO Credentials (userId, username, password) VALUES (?,?,?)",
                                   (userId, username, hashedpassword)
                                   )
                connection.commit()
                
        except sqlite3.IntegrityError as error:
            raise print(f'Account Creation Error: UserId or Username is already taken!')  
                
        except sqlite3.OperationalError as error:
            raise print(f'Database Error: {error}')
        
        except Exception as error:
            raise(f'Account Creation Error: {error}')
        
create_account = Account_Creator()  

while True:
    while True:
        userId = input('Enter your User Identification: ').strip()
        
        if userId == '':
            print('Field Should not be left blank!')
            continue
        else:
            break
    
    while True:
        username = input('Enter your Username: ').strip()
        
        if username.strip() == '':
            print('Field Should not be left blank!')
            continue
        elif len(username) < 5:
            print('Username should be atleast 5 characters long!')
            continue
        else:
            break
        
    while True:
        password = input('Enter your Password: ').strip()
        
        if password == '':
            print('Field Should not be left blank!')
            continue
        elif len(password) < 8:
            print('Password should be atleast 8 characters long!')
            continue
        else:
            break
        
    hashedpassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    create_account.add_account(userId, username, hashedpassword)
    print('Account Successfully Created!')
    break
    
