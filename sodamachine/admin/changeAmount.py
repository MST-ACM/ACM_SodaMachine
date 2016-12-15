import sys
import pymysql
from sodamachine import database

def main(*args):
  if len(args) < 2:
    print("Usage: python change_user_amount.py <ID> <Amount>")
    return

  ID = int(args[0])
  Amount = float(args[1])
  
  try:
    # cnnect to MySQL database
    con = database.connect()
    cur = con.cursor()
    
    try:
      # get record
      record = database.getRecord(cur, ID)
      if record is None:
        print("Error: could not retrieve record")
      elif record[2] is None:
        print("Error: record balance is NULL")
      else:
        print("doing stuff")
        try:
          if Amount < 0:
            result = database.addToBalance(con, cur, ID, int(Amount * 100))
            if not result:
              print("Error: balance cannot be negative")
          else:
            database.addToBalance(con, cur, ID, int(Amount * 100))
        except pymysql.Error as e:
          print("Error: could not update amount")
    except pymysql.Error as e:
      print("Error: could not retrieve record")
  except pymysql.Error as e:
    print("Error: could not connect to database")
