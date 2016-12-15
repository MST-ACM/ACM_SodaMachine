import pymysql
from sodamachine import database
from sodamachine.admin import restore
import os
from datetime import datetime

backupPath = '/home/pi/Soda-Machine/sodamachine/backups/'
maxBackups = 10

def shrinkDir():
  y = restore.getFiles(backupPath)
  if(len(y) >= maxBackups):
    total = len(y) - maxBackups
    for i in range(total):
      os.remove(backupPath + y[i])
      print(y[i], "deleted")

def genName():
  return "{:%m-%d-%Y-%H-%M}".format(datetime.now())

def printBackup():
  name = genName() + ".sql"
  f1 = open(backupPath + name, "w+")

  default = """DROP TABLE IF EXISTS `users`;

  CREATE TABLE `users`(
    `id` int(11) NOT NULL,
    `rfid` varchar(11) DEFAULT NULL,
    `balance` int(10) unsigned DEFAULT '0',
    `firstname` varchar(25) DEFAULT NULL,
    `lastname` varchar(40) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id` (`id`),
    UNIQUE KEY `rfid` (`rfid`)
  ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

  LOCK TABLES `users` WRITE;
  """

  con = database.connect()
  cur = con.cursor()
  cur.execute("SELECT * FROM users")
  results = cur.fetchall()

  s = ""

  for x in results:
    s += str(x) + ","

  s = s[:-1]

  insert = "INSERT INTO `users` VALUES "
  insert += s + ";"

  f1.write(default)

  insert.replace('None', 'NULL')

  f1.write(insert)

  unlock = "UNLOCK TABLES;"

  f1.write(unlock)
  f1.write("")
  f1.close()
  print("Database backed up to: ", backupPath + name)

def main():
  shrinkDir()
  printBackup()

