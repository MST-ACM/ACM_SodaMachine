import sys
import pymysql
from sodamachine import database

def main(id, balance, fname, lname, rfid=0):
    con = database.connect()
    cur = con.cursor()

    try:
        database.addUser(con, cur, id, rfid, balance, fname, lname)
    except pymysql.Error as e:
        print("Error, The user could not be added")

