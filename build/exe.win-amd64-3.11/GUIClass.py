import tkinter as tk
import pyautogui
import time
import threading
import timerClass
import shutdownClass
import datetime
from networkSpeed import networkSpeed

class GUI():
    def __init__(self):
        # Setting thread to None --> This is to be checked to ensure only one external thread is running
        self.countdownThread = None
        
        # Tkinter window --> Used for any GUI
        self.window = tk.Tk()
        
        # Creating an object to judge speed of current download in MB/s --> Network
        self.networkSpeed = networkSpeed()
        
        # Creating a class variable for the timer
        self.timer = None  
        # Creating a class variable to hold whether start button has been clicked or not
        self.startButtonClicked = False
        
        # Ratio == 215/126 #
        # Calculating the PCs currently resolution.
        self.screenWidth = self.window.winfo_screenwidth()
        self.screenHeight = self.window.winfo_screenheight()

        # Calculating the size of the window.
        self.windowWidth = int(self.screenWidth*0.3)
        self.windowHeight = int(self.screenHeight*0.3)

        # Calculating the position of screen where the window is to be placed.
        self.screenPositionX = int(self.screenWidth*0.35)
        self.screenPositionY = int(self.screenPositionX*0.3)
        
        # Setting Window Title
        self.window.title("Download Sleeper")
        # Changing window background colour
        self.window.configure(bg="gray25")
        
        # Window Size based on resolution of PC --> Second part justifies where in screen pop up should show #
        self.window.geometry(f"{self.windowWidth}x{self.windowHeight}+{self.screenPositionX}+{self.screenPositionY}")
        # Make the window non-resizable
        self.window.resizable(False, False)
        
        # Create an event flag to communicate between threads
        self.stopCountdownEvent = threading.Event()
        
    def main(self):
        # Create the top label
        self.title_Label = tk.Label(self.window, text="Download Sleeper", fg="lightgreen", bg="gray25")
        # Configure the font size --> Size configured from screen resolution #
        self.title_Label.configure(font=("Arial", 50, "bold"))
        self.title_Label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Create the time_Spinbox --> Stores Number of Secs/Mins/Hours
        self.time_SpinboxInputValue = tk.StringVar()
        self.time_SpinboxInputValue.set(0)
        self.time_Spinbox = tk.ttk.Spinbox(self.window, textvariable=self.time_SpinboxInputValue, from_=0, to=1000)
        self.time_Spinbox.place(relx=0.45, rely=0.4, anchor=tk.CENTER)
        
        # Create the time_Spinbox label --> Simple Text infront of spinbox
        self.Spinbox_Label = tk.Label(self.window, text="Time Value:", fg="lightgreen", bg="gray25")
        self.Spinbox_Label.configure(font=("Helvetica", 18, "bold"))
        self.Spinbox_Label.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
        
        # Create the dropdown menu --> Time Type
        self.time_selectedDropdownOption = tk.StringVar()
        self.time_Dropdown = tk.ttk.Combobox(self.window, textvariable=self.time_selectedDropdownOption, state="readonly")
        self.time_Dropdown['values'] = ('Seconds', 'Minutes', 'Hours')
        self.time_Dropdown['width'] = 20
        self.time_Dropdown.place(relx=0.45, rely=0.5, anchor=tk.CENTER)
        # Set a default option for the dropdown menu
        self.time_Dropdown.current(0) 
        
        # Create the dropdown label --> Simple text infront of dropdown
        self.Dropdown_Label = tk.Label(self.window, text="Time Type:", fg="lightgreen", bg="gray25")
        self.Dropdown_Label.configure(font=("Helvetica", 18, "bold"))
        self.Dropdown_Label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        
        # Create the "Play" button
        self.button_Play = tk.Button(self.window, text="Play", command=self._pressStartButton)
        self.button_Play.configure(font=("Helvetica", 20, "bold"), bg="gray")
        self.button_Play.place(relx=0.6, rely=0.37, anchor=tk.CENTER)
        
        # Create the "Stop" button
        self.button_Stop = tk.Button(self.window, text="Stop", command=self._pressStopButton)
        self.button_Stop.configure(font=("Helvetica", 20, "bold"), bg="darkred")
        self.button_Stop.place(relx=0.6, rely=0.53, anchor=tk.CENTER)
        
        # Create a label that displays the remaining time      
        self.timeLeft_Label = tk.Label(self.window, text="", fg="lightblue", bg="gray25")
        # Configure the font size --> Size configured from screen resolution #
        self.timeLeft_Label.configure(font=("Arial", 14))
        self.timeLeft_Label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        
        # Create a label that displays the current time
        self.Clock_Label = tk.Label(self.window, fg="yellow", bg="black")
        # Configure the font size --> Size configured from screen resolution #
        self.Clock_Label.configure(font=("Arial", 14, "bold"))
        self.Clock_Label.place(relx=0.9, rely=0.02, anchor=tk.NW)
        # Function that updates the clock every second
        self._currentTimeUpdate()
        
        # Check download speed every second --> This must be called every 1000ms (Defined in the function itself)
        self._constantDownloadChecker()
        
        # Create a label that displays current download speed
        self.Download_Label = tk.Label(self.window, text="", fg="#FF6633", bg="grey25")
        # Configure the font size --> Size configured from screen resolution #
        self.Download_Label.configure(font=("Arial", 14, "bold"))
        self.Download_Label.place(relx=0.8, rely=0.9, anchor=tk.SW)
        self._currentDownloadPlotter()
        
        # If close button (x) is pressed --> Close all external threads too (prevents the program throwing exceptions)
        self.window.protocol("WM_DELETE_WINDOW", self._closingWindow)
        
        # self.countdownTimerStandby()
        self._checkForTimerStart()
            
        self.window.mainloop()
    
    def _constantDownloadChecker(self):
        # Check download speed every second --> Update this speed
        self.networkSpeed.updateCurrentNetworkSpeed_MbPerSec()
        
        self._checkForTimerStart()
        
        self.window.after(1000, self._constantDownloadChecker)
    
    def _checkForTimerStart(self):
        # Checking if download speed is less than 500kB/s
        if self.networkSpeed.get_currentDownloadSpeed_MbPerSec() < 0.5:
            self._startCountdownTimer()
        else:
            self._stopCountdownTimer()
    
    def _countdownTimer(self):
        try:
            # Reset the end and start times of the timer --> Also marks the timer as in use #
            self.timer._resetTimer()
            
            print(f"Timer Type: {self.timer.timerType}\n")
            
            # Running timer whilst timer hasn't been cancelled and countdown hasn't reached 0
            while not self.stopCountdownEvent.is_set() and time.time() < self.timer.endTime:
                
                # Function that updates the timeLeft_label every second that a timer exists
                self._currentTimeLeftUpdate()
                        
                ### Printing Remaining Time ###
                self.timer._CurrentTimer_AllLeftCalc()
                
                # Acts as a time.sleep(1) --> Exits immediately if stopped, doesnt have to finish the time.sleep() interval
                if self.stopCountdownEvent.wait(timeout=1):
                    break
        
            # Setting variables to tell that timer has stopped #
            self.countdownThread = None
            
            if time.time() >= self.timer.endTime:
                print("--------------------------------------------------------")
                print("\nTimer Finished\n")
                
                # Method to Shutdown PC --> Waits 2 seconds then shuts down
                shutdownClass.shutdownPC()
                
                # Setting Class Variables to avoid repeat timers after timer has finished
                self.startButtonClicked = False
                
            else:
                print("Timer Stopped")
            
            if self.timer is not None:
                self.timer = None
        
        except Exception as eError:
            with open("log.txt", "a") as logfile:
                logfile.write(f"\n{datetime.datetime.now()}: {eError}")
                print(f"An Error Occurred: {eError}")
        
    def _pressStartButton(self):
        self.startButtonClicked = True
        self.button_Play.config(font=("Helvetica", 20, "bold"), bg="green")
        self.button_Stop.config(font=("Helvetica", 20, "bold"), bg="gray")
        self._startCountdownTimer()
    
    def _pressStopButton(self):
        self.startButtonClicked = False
        self.button_Stop.config(font=("Helvetica", 20, "bold"), bg="darkred")
        self.button_Play.config(font=("Helvetica", 20, "bold"), bg="gray")
        self._stopCountdownTimer()
    
    # Function tied to "Start" button --> starts timer
    def _startCountdownTimer(self):
        if self.startButtonClicked:
            if self.countdownThread is None:
                # Getting Values for size of timer
                currentDropdownValue = self.time_selectedDropdownOption.get()
                currentSpinboxValue = self.time_SpinboxInputValue.get()
                
                # Only start timer if its greater than 1 second
                if float(currentSpinboxValue) > 0:
                    print("--------------------------------------------------------")
                    # Creating a timer from spinbox and dropdown values
                    self.timer = timerClass.timer(currentSpinboxValue, currentDropdownValue)
                    
                    # Reset the stop event flag
                    self.stopCountdownEvent.clear()
                    
                    # Running countdown timer in its own thread so that the rest of the window can still be accessed.
                    self.countdownThread = threading.Thread(target=self._countdownTimer)
                    self.countdownThread.start()
        
    # Private function to stop the timer (used via a button)
    def _stopCountdownTimer(self):
        self.stopCountdownEvent.set()
        
    def _currentTimeLeftUpdate(self):
        if self.timer is not None:
            self.timer._CurrentTimer_AllLeftCalc()
            
            # Current time left (seconds)
            _currentTimeLeft = self.timer.currentSecondsLeft

            _countdown_HoursLeft = _currentTimeLeft // 3600
            _countdown_MinutesLeft = (_currentTimeLeft % 3600) // 60
            _countdown_SecondsLeft = _currentTimeLeft % 60
            
            timeLeftText = "Time Remaining:\n{:02d}:{:02d}:{:02d}".format(_countdown_HoursLeft, _countdown_MinutesLeft, _countdown_SecondsLeft)

            self.timeLeft_Label.config(text=f"{timeLeftText}", fg="lightblue", bg="black")
            
            self.window.after(1000, self._currentTimeLeftUpdate)
        else:
            self.timeLeft_Label.config(text="", bg="gray25")
    
    # Updates GUI clock
    def _currentTimeUpdate(self):
        currentTime = time.strftime("%H:%M:%S")  # Get the current time
        self.Clock_Label.config(text=f"Clock\n{currentTime}")  # Update the label text
        self.window.after(1000, self._currentTimeUpdate)
        
    def _currentDownloadPlotter(self):
        self.Download_Label.config(text=f"Download (MB/s):\n{self.networkSpeed.get_currentDownloadSpeed_MbPerSec()}")
        self.window.after(1000, self._currentDownloadPlotter)
    
    # Private function that is called when the window is closed  
    def _closingWindow(self):
        # Stops countdown timer
        self._stopCountdownTimer()
        
        # Join external thread back onto main thread (if it exists)
        if self.countdownThread is not None:
            self.countdownThread.join()
        
        # Closes window
        self.window.destroy()
        