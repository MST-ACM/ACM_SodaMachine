# Import struct and USB modules
import struct
import time
from settings import LCD_BREAK_TIME
import libusb1
import usb1

# Vendor and Product ID of lcd2usb device
# Determined from lsusb
VID = 0x0403
PID = 0xc630

# Define commands to communicate with LCD
LCD_CTRL = 1 << 3
LCD_CMD = 1 << 5
LCD_DATA = 2 << 5

# USB vendor type
TYPE_VENDOR = libusb1.LIBUSB_TYPE_VENDOR

# Unable to connect to LCD
class LCDError(Exception):
    def __str__(self):
        return('Unable to connect to LCD')

# LCD Object
class LCD(object):
    # Open connection
    def __init__(self, vendor_id = VID, product_id = PID):
        # Open a connection to LCD
        self.open(vendor_id, product_id)

        # Set buffer default variables
        self.buffer_command = -1
        self.buffer_size = 0
        self.buffer = bytearray(4)

    # Open connection
    def open(self, vendor_id, product_id):
        # Connect to LCD device
        context = usb1.USBContext()
        self.device = context.openByVendorIDAndProductID(vendor_id, product_id)
        # Error if unable to connect to LCD
        if not self.device:
            raise LCDError()

    # Close connection
    def close(self):
        self.device.close()

    # Send data
    def send(self, request, value, index):
        # Send the data to the LCD
        try:
            self.device.controlWrite(TYPE_VENDOR, request, value, index, '', 1000)
        # Error if unable to send data
        except libusb1.USBError:
            print('Unable to send data to LCD')
            return -1
        return 0

    # Flush queue buffer
    def flush(self):
        # Flush only if buffer has data
        if self.buffer_command == -1:
            return

        # Arrange bitmap for data to be sent
        request = self.buffer_command | self.buffer_size - 1
        value = self.buffer[0] | self.buffer[1] << 8
        index = self.buffer[2] | self.buffer[3] << 8

        # Send data
        self.send(request, value, index)

        # Reset buffer variables to defaults
        self.buffer_command = -1
        self.buffer_size = 0

    # Load command into the buffer
    def enqueue(self, command, value):
        # Send if anything is still in the buffer
        if(self.buffer_command >= 0 and self.buffer_command != command):
            self.flush()

        # Add to buffer
        self.buffer_command = command
        if(not isinstance(value, int)):
            value = ord(value)
        self.buffer[self.buffer_size] = value
        self.buffer_size += 1

        # Flush if buffer is full
        if (self.buffer_size == 4):
            self.flush()

    # Enqueue commands into buffer
    def command(self, command):
        self.enqueue(LCD_CMD | LCD_CTRL, command)

    # Clear display
    def clear(self):
        self.command(0x01)
        self.command(0x03)

    # Move to next line
    def newline(self):
        self.command(0xc0)

    # Write to LCD
    def write(self, data, waitTime = LCD_BREAK_TIME):
        #Ensure there is no data on screen
        self.clear()
        # Queue for each char
        for char in data:
            # If \n escape character, move to newline
            if char == '\n':
                self.newline()
            # Queue the char to LCD
            else:
                self.enqueue(LCD_DATA | LCD_CTRL, char)
        # Send remaining in buffer to LCD
        self.flush()
        time.sleep(waitTime)
