#!/usr/bin/python
## Built-in modules
import os
import sys
import time
import pymysql
import serial
import settings
import log
from nanpy import ArduinoApi
from decimal import Decimal
from threading import Thread
##

## SodaMachine modules
# To import from the admin directory
from sodamachine.admin import *
# To import LCD object from the lcd module
from sodamachine.lcd import LCD
# To import Magstrip object from sodamag module
from sodamachine.magreader import MagStrip
##

def main():
    sysLog = log.createSystemLogger()
    ## Variables
    # Default account balance
    accountBalance = 0
    # Default char received data
    charReceived = ""
    # Cost of one soda
    sodaCost = .50 # 50 cents
    # Flow control variable for main program loop
    shouldContinueTrans = True
    ##

    ## Serial/USB connections
    # Initialize and connect to Arduino
    ser = serial.Serial(settings.SERIAL_PATH, 9600, timeout=10)

    # Initialize and connect to LCD
    lcd = LCD(0x0403, 0xc630)

    # Initialize and connect to Magstrip
    mag = MagStrip(settings.MAGSTRIP_PATH)
    ##
    
    try:
        ## Threaded processes
        # Start magstrip thread
        p = Thread(target=mag.read, args=())
        p.daemon = True
        p.start()
        sysLog.info('[SUCCESS] Magnetic Stripe thread successfully connected.')
        ##
    except:
        sysLog.error('[FAILURE] Failed to connect magnetic stripe thread.', exc_info=True)

    sysLog.info('[SUCCESS] Program initialization occured sucessfully.')

    # Main program loop
    while shouldContinueTrans:
        ####
        # @If: Integrity check to make sure the Serial port still active.
        #      If check fails, display error and attempt to reconnect
        #      every 10 seconds.
        # @Elif: Integrity check for LCD connection.
        #        If check fails, attempts to reconnect LCD once. Shuts down
        #        on failure.
        # @Else: Displays normal user time message on the LCD to show LCD working.
        ####
        if(not ser):
            try:
                ser = serial.Serial('/dev/arduino', 9600, timeout=10)
                lcd.write('Error Code: ARD\nContact Admin.')
            finally:
                time.sleep(10)
        elif(not lcd):
            try:
                lcd = LCD(0x0403, 0xc630)
            except:
                sys.exit("Unrecoverable LCD error.")
        else:
            # Display main message and current time
            ct = time.strftime("%I:%M %P")
            lcd.write('ACM Soda Machine\n    %s' % ct, 1)

        # Only process when card swiped
        if mag.studentID:
            sysLog.debug('Magnetic Stripe Reader read student ID: {0}'.format(mag.studentID))
            transactionHandler(ser, mag, lcd, sodaCost)
            # Reset IDs that were read
            mag.rawStudentID = ""
            mag.studentID = ""
            ser.reset_input_buffer()
            ser.reset_output_buffer()

def transactionHandler(ser, mag, lcd, sodaCost):
    transLogger = log.createTransactionLogger()
    ####
    # Creating a fresh transaction state for the user to ensure
    # no residual data is left over from previous transaction.
    ####
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    ####
    # charReceived - stores the serial communication characters
    #                from raspberry pi
    # transFinished - Describes current transcation state
    ####
    charReceived = ""
    transFinished = False

    result = authorizeTransaction(mag, lcd)

    # If result is null then not valid user
    if not result:
        # Output invalid user to LCD
        lcd.write('No account found\nfor ID %s' % mag.studentID)
        transLogger.error('[FAIL] Failed to find account information for student ID: {0}'.format(mag.studentID))
    else:
        # Valid user
        transLogger.info('[SUCCESS] Sucessfully processed user {0} {1}'.format(str(result[3]),str(result[4])))
        transLogger.debug('Current Transaction results: {0}'.format(result))
        processTransaction(result, ser, mag, lcd, sodaCost, transLogger)

def authorizeTransaction(mag, lcd):
        lcd.write('Authorizing ...', 1)
        ####
        # Attempt to check for user
        ####
        try:
            result = checkUser.main(mag.studentID)
            return(result)
        except:
            print("[Error] Cannot check User in main.py.")
            return(False)

def processTransaction(result, ser, mag, lcd, sodaCost, logger):
    accountBalance = int(result[2]) # third record is account balance
    fname = str(result[3]) # fourth record is first name

    # Check accountBalance
    # Low balance
    if accountBalance < sodaCost:
        # Output low balance to LCD
        lcd.write('Sorry %s' % fname)
        lcd.write('Not enough funds\nfor transaction')

        errmsg = ('[NO FUNDS] the user {fname} {lname} currently has'
                  ' {curmoney} which is not enough for the soda price,'
                  '{price}').format(fname = fname, lname = str(result[4]),
                                    curmoney = accountBalance,
                                    price = sodaCost)
        logger.error(errmsg)
    # Sufficient Balance
    else:
        sucmsg = ('[HAS FUNDS] the user {fname} {lname} currently has'
                  ' {curmoney} which is enough for the soda price,'
                  '{price}').format(fname = fname, lname = str(result[4]),
                                    curmoney = accountBalance,
                                    price = sodaCost)

        logger.debug(sucmsg)
        # Output Make Selection to LCD
        lcd.write('Hello %s' % fname, 1)
        lcd.write('Please make\na selection', .1)
        try:
            # Send authorized to Arduino
            ser.write('a')
            logger.info('[SUCCESS] The \'a\' authorization character'
                         ' was succesfully written to the Arduino')
        except:
            logger.error('[FAILURE] The \'a\' authorization character'
                         ' failed to be written to the Arduino')

        finalizeTransaction(ser, mag, lcd, sodaCost, fname, accountBalance, logger)

def finalizeTransaction(ser, mag, lcd, sodaCost, fname, accountBalance, logger):
    ####
    # Start timeout clock if no serial transaction happens
    ####
    timeout = time.time() + settings.TIMEOUT_TIME
    transFinished = False
    logger.debug(('Timeout has been set to {0} and the Pi is waiting for'
                 'Arduino response.').format(timeout))

    while(not transFinished):
        charReceived = ser.read(1)
        if charReceived == 's':
            logger.info('[Success] Arduino has been succesful in dispensing'
                        ' soda')
            #####
            # If the transaction successfully completes, the
            # Arduino sends the index of the bottle they ordered
            # which corresponds with sloteData in settings.
            #####
            time.sleep(2)
            bottleOrdered = int(ser.read())
            while(not isinstance(bottleOrdered, int)):
               if(time.time() >= timeout):
                   print('BREAK')
                   break
               bottleOrdered = int(ser.read())

            print(bottleOrdered)
            logger.info(('[SUCCESS] {ID} has received the soda {soda}'
                         ' which has data of'
                         ' {data}').format(ID = mag.studentID,
                                           soda = settings.slotData[bottleOrdered]["name"],
                                           data = settings.slotData[bottleOrdered]))
            # Deduct sodaCost from amount
            # NOTE: change for modular prices
            changeAmount.main(mag.studentID, -sodaCost)
            logger.debug('{ID} has been charged {cost}'.format(ID = mag.studentID,
                                                               cost = sodaCost))
            # Output success & new balance to LCD
            lcd.write('Thank you, %s' % fname)
            ###
            # Normalizing account balance for user
            ###
            accountBalance = ((Decimal(accountBalance))/100-Decimal(.5))
            lcd.write('Remaining\nBalance: ${0:.2f}'.format(accountBalance)) #Temporary
            logger.debug(('{ID} has a remaning balance of'
                          ' {bal}').format(ID = mag.studentID,
                                           bal = accountBalance))

            transFinished = True


        # Vending error from Arduino
        elif charReceived == 'e':
            # Output error to LCD
            logger.error('There was an error dispensing the Soda')
            lcd.write('Error dispensing\nPlease try again')
            transFinished = True
        elif charReceived == 'o':
            # Output error to LCD
            lcd.write('Out of Stock.')
            logger.error('The soda machine is out of stock of the soda'
                         ' the user ordered.')
            transFinished = True
        # Took too long to make a selection
        elif(time.time() >= timeout):
            logger.info('The transaction timed out.')
            ser.write("t")
            lcd.write('Transaction\ntimed out')
            transFinished = True


if __name__ == "__main__":
    # Call main function
    main()
