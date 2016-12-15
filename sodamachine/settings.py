##########
# Initilzation of consants responsible for holding price values of different
# soda types
##########
PRICE_OF_CAN = .50
PRICE_OF_BOTTLE = .75

##########
# Initilization of the list which contains the dictionaries that contains
# all of the data we need for each of the slots,
##########

slotData = [{"name":"Mountain Dew", "isBottle": False, "price": PRICE_OF_CAN},
            {"name":"Dr. Pepper", "isBottle": False, "price": PRICE_OF_CAN},
            {"name":"Diet Coke", "isBottle": True, "price": PRICE_OF_CAN},
            {"name":"Coca Cola", "isBottle": True, "price": PRICE_OF_CAN},
            {"name":"Sprite", "isBottle": True, "price": PRICE_OF_CAN},
            {"name":"Minute Maid Lemonade", "isBottle": True, "price": PRICE_OF_CAN},
            {"name":"A&W Root Beer", "isBottle": False, "price": PRICE_OF_CAN},
            {"name":"Random Slot", "isBottle": False, "price": PRICE_OF_CAN},]

##########
# Time (in seconds) it takes for the transaction to timeout once the user
# is authorized.
##########
TIMEOUT_TIME = 12


##########
# Locations of each of the log files in absolute path
##########
TRANSACTION_LOG_PATH = "/home/pi/Soda-Machine/sodamachine/logs/transactions.log"
SYSTEM_LOG_PATH = "/home/pi/Soda-Machine/sodamachine/logs/system.log"
DAEMON_LOG_PATH = "/home/pi/Soda-Machine/sodamachine/logs/daemon.log"

##########
# How long the LCD will break between commands/writes (in seconds)
##########
LCD_BREAK_TIME = 4


##########
# Magnetic Strip Reader Settings
##########
MAGSTRIP_PATH = '/dev/cardreader'

##########
# Serial Connection Settings
##########
SERIAL_PATH = '/dev/arduino'
