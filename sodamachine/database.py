# MYSQL library
import pymysql

# default connect information
def_host = "127.0.0.1"
def_user = "root"
def_psw  = "pi cs acm"
def_db   = "soda"

# connect with params
def connect(host, user, password, database):
  return pymysql.connect(host, user, password, database)

# connect with defaults
def connect():
  return pymysql.connect(def_host, def_user, def_psw, def_db)

# retrieve record
def getRecord(cursor, id):
  cursor.execute("SELECT * FROM users WHERE id=\'" + str(id) + "\'")
  return cursor.fetchone()

# get all records
def getAll(cursor):
  cursor.execute("SELECT * FROM users")
  return cursor.fetchall()

# add user
def addUser(connection, cursor, id, rfid, balance, fname, lname):
  id = "\'" + str(id) + "\'"
  if rfid is None:
    rfid = "NULL"
  else:
    rfid = "\'" + str(rfid) + "\'"
  balance = "\'" + str(balance) + "\'"
  if fname is None:
    fname = "NULL"
  else:
    fname = "\'" + fname + "\'"
  if lname is None:
    lname = "NULL"
  else:
    lname = "\'" + lname + "\'"
  
  values = id + "," + rfid + "," + balance + "," + fname + "," + lname
  cursor.execute("INSERT INTO users VALUES(" + values + ");")
  connection.commit()

# deduct from balance
def deductFromBalance(connection, cursor, ID, amount):
  record = getRecord(cursor, ID)
  balance = int(record[2])
  if (balance < amount):
    return False
  else:
    cursor.execute("UPDATE users SET balance=\'" + str(balance-amount) + "\' WHERE id=\'" + str(ID) + "\'")
    connection.commit()
    return True
    
# add to balance
def addToBalance(connection, cursor, ID, amount):
  record = getRecord(cursor, ID)
  balance = int(record[2])

  cursor.execute("UPDATE users SET balance=\'" + str(balance+amount) + "\' WHERE id=\'" + str(ID) + "\'")
  connection.commit()
  return balance+amount

# Output the balance of a user
def checkBalance(connection, cursor, id):
  cursor.execute("Select balance FROM users WHERE id = \'" + str(id) + "\'")
  result = cursor.fetchone()
  print("The balance for the id = \'" + str(id) + "\' is: " + result)
  return result

# remove user
def removeUser(connection, cursor, id):
  try:
    cursor.execute("DELETE FROM users WHERE id = \'" + str(id) + "\'")
    connection.commit()
    print("User: " + str(id) + " has been deleted.")
  except pymysql.Error as e:
    print(e);
