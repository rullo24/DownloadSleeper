from cx_Freeze import setup, Executable
import sys

# Specify the main script
mainScript = 'main.py'

# Determine the base parameter based on the platform
if sys.platform == 'win32' or sys.platform == 'darwin':
    base = 'Win32GUI'
else:
    base = None

# Create an instance of the Executable class
executable = Executable(script=mainScript, base=base, icon="sleeping.ico")

# icon attribution: <a href="https://www.flaticon.com/free-icons/pillow" title="pillow icons">Pillow icons created by Freepik - Flaticon</a>

# Set additional options for the setup
options = {
    'build_exe': {
        'includes': ['datetime', 'time', 'os', 'tkinter', 'threading', 'pyautogui', 'psutil'],  # Include additional modules
        'include_files': ['networkSpeed.py', 'shutdownClass.py', 'timerClass.py', 'GUIClass.py']
    }
}

# Call the setup function
setup(
    name='Download_Sleeper',
    version='1.0',
    description='Shutdowns PC upon download completion',
    executables=[executable],
    options=options,
)
