import sys
sys.path.append('/home/pi/sodamachine')
import pymysql
from sodamachine import database

def printHeader():
  print('+----------+------------+---------+-----------------+-----------------+')
  print('|       ID |       RFID |  Amount | First Name      | Last Name       |')
  print('+----------+------------+---------+-----------------+-----------------+')

def printFooter():
  print('+----------+------------+---------+-----------------+-----------------+')

def printRecord(record):
  (id, rfid, amnt, fname, lname) = record
  if id is None:
    id = 0
  if rfid is None:
    rfid = 0
  if amnt is None:
    anmt = 0
  if fname is None:
    fname = "null"
  if lname is None:
    lname = "null"
  
  print('| %08i | %10i | $%6.2f | %-15s | %-15s |' % (int(id), int(rfid), amnt / 100.0, fname, lname))

def main(args):
  # input
  if args == "":
    ID = None
  else:
    ID = int(args)
  try:
    # connect to MySQL database
    con = database.connect()
    cur = con.cursor()
    
    try:
      if ID is not None:
        record = database.getRecord(cur, ID)
        
        if record is None:
          print("Error: could not retrieve record")
          return
        
        printHeader()
        printRecord(record)
        printFooter()
        
      else:
        records = database.getAll(cur)
        
        printHeader()
        for record in records:
          printRecord(record)
        printFooter()
        
    except pymysql.Error as e:
      print("Error: could not retrieve record(s)")
  except pymysql.Error as e:
    print("Error: could not connect to database")
