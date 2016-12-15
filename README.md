# ACM Soda Machine Documentation
This documentation details all of information necessary to start, develop, maintain, and update the Soda Machine in CS 213.

## Dependencies
1. [Pyserial](https://github.com/pyserial/pyserial)
  + ```Pyserial``` handles the serial communication of authorization and logging characters between the Raspberry Pi and Arduino platforms in the soda machine.
2. [Pymysql](https://github.com/PyMySQL/PyMySQL)
  + ```Pymsql``` handles the connection to the SQL-lite database stored locally on the Raspberry Pi machine which stores the currency (i.e. how much money each user has).
3. [Libusb1](https://github.com/vpelletier/python-libusb1)
  + ```Libusb1``` handles the interfacing between the LCD screen and the Raspberry Pi so that the Raspberry Pi can write messages to the LCD.
4. [Evdev](https://python-evdev.readthedocs.io/en/latest/)
  + ```Evdev``` handles Kernel input interfacing for the magnetic strip reader when a user swipes their card.
5. [Nanpy](https://github.com/nanpy/nanpy)
  + ```Nanpy``` handles the direct throughput and communication to the arduino board through python.

## Installation
When migrating or reinstalling the system, please follow the following commands on the Raspberry Pi shell to install the main soda machine files ```NOT DEPENDENCIES```:
```
mkdir ~/pi/Soda-Machine/
cd ~/pi/Soda-Machine/
git init
git clone https://github.com/MST-ACM/ACM_SodaMachine_2.0.git
chmod +x main.py bin/smadmin bin/smdaemon
mv Documentation/sodamachine.init /etc/init.d/sodamachine
sudo update-rc.d sodamachine defaults
sudo service sodamachine restart
```
## Pseudocode Overview
1. The user swipes their Student ID into the magnetic strip reader which the magnetic strip reader translates to a ```Student ID```
2. ```Main.py``` performs a database lookup on the Student ID to determine if the user has the required funds.
3. If the database lookup is successful, the Raspberry Pi sends an authorization character to the Arduino using the serial connection.
  - If the database lookup is not successful the transaction fails and the Raspberry Pi resets it transaction state.
4. After the Arduino receives the authorization character, it waits for the user to press a button on the soda machine
  - If the user does not press a button after a certain amount of seconds, the transaction fails and the Raspberry Pi and Arduino reset their states.
5. After the user presses a button, the Arduino turns on the motor associated with the button until the soda is dispensed.
6. After the soda is dispensed, the Arduino sends a success character back to the Raspberry Pi so that the Raspberry Pi charges the user for the soda
  - The user is charged here instead of step 4 to prevent any errors with a soda failing to be dispensed.
7. Then, the Arduino and Raspberry Pi reset their states for the next transaction.


## Contribute
Please contact [acm@mst.edu](acm@mst.edu) if you would like to contribute to this project.
