import re
import MySQLdb
import MySQLdb.cursors
import config

def connect_to_database():
    options = {
        'host': 'localhost',
        'user': config.env['user'],
        'passwd': config.env['password'],
        'db': config.env['db'],
        'cursorclass' : MySQLdb.cursors.DictCursor
    }
    db = MySQLdb.connect(**options)
    db.autocommit(True)
    return db

def isStrLengthLessThanN(str, length):
    if len(str) <= length:
        return True
    else: 
        return False

def isStrAllLDU(str):#all may only contain letters, digits, and underscores
    '''if re.match("^[A-Za-z0-9_-]*$", str):
        return True'''
    if all(ch.isalnum() or ch == '_' for ch in str):
        return True
    else:
        return False

def ifStrHasDL(str):# must contain at least one letter and one number
    '''if re.match("^(?=.*[A-Za-z])(?=.*\d).+$",str):
        return True'''
    if any(ch.isdigit() for ch in str) and any(ch.isalpha() for ch in str):
        return True
    else:
        return False

def isEmailValid(str):
    if re.match(r"[^@]+@[^@]+\.[^@]+", str):
        return True
    else:
        return False


