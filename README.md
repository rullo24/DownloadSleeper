### Description ###
- Author: Hyper2406
- Date: 21-06-2023
- Version: 1.0

This program has been designed to shutdown the PC of the client after a download has finished. 
To ensure a shutdown is not triggered by a false alarm, a timer has also been implemented. 
This timer starts when the PC's network speed drops below 500kB/s. After the timer has completed, the PC is shutdown.
If the PC has a 'hiccup' in its download time where the network speed drops below 500kB/s, the timer will stop (and turn off) if the PC again starts downloading.

### How it Works ###
1. Open sleeper.exe.
2. Set your timer variables.
    - This tells the computer how much time should be allowed from the moment the network speed drops until shutdown (a larger value indicates a larger room for 'hiccups').
3. Press the "Start" button. 
4. From here, the script will perform the rest of the 'behind-the-scenes' steps.