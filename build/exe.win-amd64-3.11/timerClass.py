#####################################################
### Start a 5 min timer if network drops to 0MB/s ###
#####################################################

import time

class timer():
    def __init__(self, timeLength, timerType):
        # Setting the time and type relative to parameter #
        self.time = 0
        if timerType == "Seconds":
            self.time = float(timeLength)
        elif timerType == "Minutes":
            self.time = float(timeLength)*60
        elif timerType == "Hours":
            self.time = float(timeLength)*3600
        
        # Setting the type of stored time i.e minutes #
        self.timerType = timerType
            
        # Setting the starting and ending time to DNE for the moment. These are defined correctly in the _resetTimer() function #
        self.startTime = None
        self.endTime = None
        
        # This variable will be used to hold the current time left --> Should be displayed in the GUI #
        self.currentSecondsLeft = -1
        self.currentMinutesLeft = -1
        self.currentHoursLeft = -1
        
    def _resetTimer(self):
        # Resetting timed variables #
        self.startTime = time.time()
        self.endTime = self.startTime + self.time
    
    # Calculates the amount of seconds left in timer #
    def _CurrentTimer_SecLeftCalc(self):
        self.currentSecondsLeft = temp = round(self.endTime - time.time(), 1)
        temp = str(temp)
        tempString = ""
        for digit in temp:
            if digit == ".":
                break
            tempString += digit
            
        self.currentSecondsLeft = int(tempString)
    
    # Calculates the amount of minutes left in timer #  
    def _CurrentTimer_MinLeftCalc(self):
        self.currentMinutesLeft = int(round((self.endTime - time.time()) / 60, 2))
    
    # Calculates the amount of hours left in timer #   
    def _CurrentTimer_HourLeftCalc(self):
        self.currentHoursLeft = int(round((self.endTime - time.time()) / 3600, 5))
        
    def _CurrentTimer_AllLeftCalc(self):
        # Updates seconds, minutes and hours left
        self._CurrentTimer_SecLeftCalc()
        self._CurrentTimer_MinLeftCalc()
        self._CurrentTimer_HourLeftCalc()