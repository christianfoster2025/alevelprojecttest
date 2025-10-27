import os.path
import sqlite3
from hashtest import hashtext

def dbcheck() -> None:
    if os.path.exists('users.db'):
        return True
    else:
        connection = sqlite3.connect('users.db')
        connection = connection.cursor()
        connection.execute('''create table users( 
                    userID integer,
                    username text,
                    password text
                    )''')
        connection.commit()
        connection.close()
        return False

def makedummyrecords() -> None:
    connect = sqlite3.connect('users.db')
    connect.execute(f"INSERT INTO users (userID,username,password) \
        VALUES (1,'testuser','{hashtext('monkey')}') ")
    connect.execute(f"INSERT INTO users (userID,username,password) \
        VALUES (2,'david','{hashtext('david')}') ")
    connect.execute(f"INSERT INTO users (userID,username,password) \
        VALUES (3,'banana','{hashtext('fruit')}') ")
    connect.commit()
    connect.close()   

def enterrecord(id:any,username:str,password:str) -> None: #not sure if id is going to stay around, may just use username as primary key
    dbcheck()
    connect = sqlite3.connect('users.db')
    connect.execute(f"INSERT INTO users (userID,username,password) \
        VALUES ({int(id)},'{username}','{hashtext(password)}') ")
    connect.commit()
    connect.close() 

def checkcredentials(username:str,password:str) -> bool:
    if not(dbcheck()):
        return False
    else:
        
        connect = sqlite3.connect('users.db')
        connect = connect.cursor()
        connect.execute(f"SElECT * FROM users WHERE username LIKE'{username}' AND password LIKE '{hashtext(password)}'")
        if not connect.fetchone():  # An empty result evaluates to False.
            print('User error ', 'Invalid user name'+chr(13)+'or password' )
        else:
           print('Logged on ', 'Welcome to the database')
        connect.close() 
        



if __name__ == '__main__':
    #enterrecord(input('enterid'),input('enter user'),input('enterpassword'))
    checkcredentials(input('enter user'),input('enterpassword'))
    #makedummyrecords()