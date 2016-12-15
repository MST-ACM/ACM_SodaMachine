import sys
import pymysql
from sodamachine import database

def main(args):
  # input checking
  if len(args) < 1:
    print("Usage: python remove_users.py <ID>")
    return

  ID = int(args)
  #print(ID) 
  try:
    # connect to MySQL database
    con = database.connect()
    cur = con.cursor()
    
    try:
      # test for user
      rec = database.getRecord(cur, ID)
      
      try:
        # remove user
        database.removeUser(con, cur, ID)
        #con.commit()
      except pymysql.Error as e:
        print("Error: could not remove user")
    except pymysql.Error as e:
      print("Error: could not find user")
  except pymysql.Error as e:
    print("Error: could not connect to database")
