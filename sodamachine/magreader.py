# Import Struct and evdev modules
import struct
from evdev import InputDevice, categorize, ecodes

# Magstrip Class
class MagStrip(object):
    # Initialize values
    def __init__(self, device = '/dev/input/event0'):
        # Define input device
        self.device = InputDevice(device)
        # Define raw and studentID
        self.rawStudentID = ""
        self.studentID = ""

    # Read from the magstrip
    def read(self):
        # Get input and convert codes to actual key representations
        for event in self.device.read_loop():
            # Only read when we don't have a finished studentID
            if not self.studentID:
                # Key down event
                if event.value == 1:
                    # Event codes, represents keys 0 to 9
                    if event.code == 2:
                        self.rawStudentID += "1"
                    elif event.code == 3:
                        self.rawStudentID += "2"
                    elif event.code == 4:
                        self.rawStudentID += "3"
                    elif event.code == 5:
                        self.rawStudentID += "4"
                    elif event.code == 6:
                        self.rawStudentID += "5"
                    elif event.code == 7:
                        self.rawStudentID += "6"
                    elif event.code == 8:
                        self.rawStudentID += "7"
                    elif event.code == 9:
                        self.rawStudentID += "8"
                    elif event.code == 10:
                        self.rawStudentID += "9"
                    elif event.code == 11:
                        self.rawStudentID += "0"

                # Set Student ID when rawStudentID is 0xxxxxxxx1
                if len(self.rawStudentID) == 10:
                    self.studentID = self.rawStudentID[1:9]
                    self.rawStudentID = ""
        
