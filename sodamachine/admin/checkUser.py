import sys
import pymysql
from sodamachine import database

def main(*args):
  if len(args) < 1:
    print("Usage: <ID>")
    return

  ID = int(args[0])
  
  try:
    # cnnect to MySQL database
    con = database.connect()
    cur = con.cursor()
    
    try:
      # get record
      record = database.getRecord(cur, ID)
      if record is None:
        return None
      else:
        return record
      
    except pymysql.Error as e:
      print("Error: could not retrieve record")
  except pymysql.Error as e:
    print("Error: could not connect to database")
