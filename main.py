import shutdownClass, GUIClass, networkSpeed
import datetime

def main():
    try:
        # Main GUI class
        app = GUIClass.GUI()
        # Runs GUI
        app.main()
    
    except Exception as eError:
        # Print Exception to Log file
        with open("log.txt", "a") as logfile:
            logfile.write(f"\n{datetime.datetime.now()}: {eError}")
            print("An Error Occurred")
        
# Runs Script #   
main()

# icon attribution: <a href="https://www.flaticon.com/free-icons/pillow" title="pillow icons">Pillow icons created by Freepik - Flaticon</a>