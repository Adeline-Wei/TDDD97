__author__ = 'linwe991'

from flask import g
import sqlite3


DB = None


def init_db(db_name):
    global DB
    DB = get_db(db_name)
    with open('database.schema', mode='r') as f:
        try:
            DB.cursor().executescript(f.read())
            DB.commit()
        except:
            print("Database Initialization Failed.")
    return None


def get_db(db_name):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name, check_same_thread=False)
    return db



def add_user(email,password,firstname,familyname,gender,city,country):
    global DB
    try:
        DB.cursor().execute('INSERT INTO Users VALUES (?,?,?,?,?,?,?,?);', [None,email,password,firstname,familyname,gender,city,country])
        DB.commit()
        return True
    except Exception:
        print ('An Exception Occurs In ADD_USER Function. ')
        return False


def find_user(email,password=None,status=None):
    global DB
    if status == 'LOGIN':
        result = DB.cursor().execute("SELECT * FROM Users WHERE email = ? AND password = ?;", [email,password]).fetchall()
        DB.commit()
        if result:
            return result[0]
        else:
            print ('An Exception Occurs In FIND_USER Function. ')
            return False
    else:
        result = DB.cursor().execute("SELECT * FROM Users WHERE email = ?;", [email]).fetchall()
        DB.commit()
        if result:
            return result[0]
        else:
            print ('An Exception Occurs In FIND_USER Function. ')
            return False


def add_sign_in_user(uid, email, token):
    global DB
    try:
        DB.cursor().execute("INSERT INTO Logins VALUES (?,?,?,?);", [None,uid,email,token])
        DB.commit()
        return True
    except:
        print ('An Exception Occurs In ADD_SIGN_IN_USER Function. ')
        return False


def remove_sign_in_user(token):
    global DB
    try:
        DB.cursor().execute("DELETE FROM Logins WHERE token = ?;", [token])
        DB.commit()
        return True
    except:
        print ('An Exception Occurs In REMOVE_SIGN_IN_USER Function. ')
        return False


def change_password(token, old_pw, new_pw):
    global DB
    # Format: [(2, u'123', u'BfK3nE71lA3YsPdWRp9SJ315gL5U9gwGZSkP')]
    result = DB.cursor().execute("SELECT email FROM Logins WHERE token = ?;", [token]).fetchall()
    if result:
        email = result[0][0]
        DB.cursor().execute("UPDATE Users SET password = ? WHERE email = ? AND password = ?;", [new_pw,email,old_pw])
        DB.commit()
        return True
    else:
        print ('An Exception Occurs In CHANGE PASSWORD Function.')
        return False



def find_sign_in_user(token):
    global DB
    result = DB.cursor().execute("SELECT email FROM Logins WHERE token = ?;", [token]).fetchall()
    if result:
        email = result[0][0]
        result = DB.cursor().execute("SELECT uid,email,firstname,familyname,gender,city,country FROM Users WHERE email = ?;", [email]).fetchall()
        DB.commit()
        return result[0]
    else:
        print ('An Exception Occurs In FIND_SIGN_IN_USER.')
        return False


def find_user_message(token, email=None):
    global DB
    result = DB.cursor().execute("SELECT uid FROM Logins WHERE token = ?;", [token]).fetchall()
    if result and email:
        result = DB.cursor().execute("SELECT uid FROM Users WHERE email = ?;", [email]).fetchall()
        if result:
            result = DB.cursor().execute("SELECT mid, content FROM Messages WHERE uid = ?;", [result[0][0]]).fetchall()
            return True, result
        else:
            print ('FIND_USER_MESSAGE: No corresponding email.')
            return False
    elif result:
        result = DB.cursor().execute("SELECT mid, content FROM Messages WHERE uid = ?;", [result[0][0]]).fetchall()
        return True, result
    else:
        print ('An Exception Occurs In FIND_USER_MESSAGE')
        return False


def add_message(token, message, email):
    global DB
    result1 = DB.cursor().execute("SELECT uid FROM Logins WHERE token = ?;", [token]).fetchall()
    result2 = DB.cursor().execute("SELECT uid FROM Users WHERE email = ?;", [email]).fetchall()
    if result1 and result2:
        DB.cursor().execute("INSERT INTO Messages VALUES (?,?,?,?);", [None,result2[0][0],result1[0][0],message])
        DB.commit()
        return True
    else:
        print ('ADD_MESSAGE: No corresponding email.')
        return False


def close():
    global DB
    DB.close()
    return None