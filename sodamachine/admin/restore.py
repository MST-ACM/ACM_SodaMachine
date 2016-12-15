from sodamachine import database
import pymysql
import sys
import os

def getFiles(directory):
  a = [s for s in os.listdir(directory)
      if os.path.isfile(os.path.join(directory, s))]
  a.sort(key=lambda s: os.path.getmtime(os.path.join(directory, s)))
  return a


def chooseFile(files):
  max = len(files)
  if max == 0:
    print("No backup files found")
    sys.exit()

  for i in range(len(files)):
    print("[" + str(i) + "]", files[i])

  while True:
    x = int(input("Enter a file number: "))
    if x >= 0 and x < max:
      break

  return files[x]


def executeSqlFromFile(filename):

  con = database.connect()
  cur = con.cursor()

  fd = open(filename, 'r')

  sqlFile = fd.read()
  fd.close()

  commands = sqlFile.split(';')
  commands = filter(None, commands)

  for command in commands:
    try:
      command = command.strip().replace("None", "NULL")
      cur.execute(command)
      con.commit()
    except (pymysql.Error, e):
      print(e)
      print("Command skipped:", command)
  print("Database restored from: ", filename)

def main():
  file = chooseFile(getFiles(DATABASE_BACKUP_PATH))
  executeSqlFromFile(backupPath + file)
