import psutil
import time

class networkSpeed():
    def __init__(self):
        self._prevNetworkDownloads = 0
        self._loopedThroughNetworkFunctionOnce = False
        self.currentDownloadSpeed_MbPerSec = 0
    
    ######################
    ### GETTER METHODS ### 
    ######################
       
    def get_loopedThroughNetworkFunctionOnce(self):
        return self._loopedThroughNetworkFunctionOnce
    
    def get_currentDownloadSpeed_MbPerSec(self):
        return self.currentDownloadSpeed_MbPerSec
    
    def get_prevNetworkDownloads(self):
        return self._prevNetworkDownloads
    
    ######################
    ### SETTER METHODS ### 
    ######################
    
    def set_loopedThroughNetworkFunctionOnce(self, value):
        self._loopedThroughNetworkFunctionOnce = value
    
    def set_currentDownloadSpeed_MbPerSec(self, value):
        self.currentDownloadSpeed_MbPerSec = value
    
    def set_prevNetworkDownloads(self, value):
        self._prevNetworkDownloads = value
        
    ######################
    #### OTHER METHODS ###
    ######################
    
    def updateCurrentNetworkSpeed_MbPerSec(self):
        # Speed of Internet in Bytes --> Compared against speed 1 sec later
        speedCheck = psutil.net_io_counters().bytes_recv
        
        # To avoid a very high download number when at least one second hasn't passed.
        if self.get_loopedThroughNetworkFunctionOnce() is True:
            # net_io_counters() tells you data downloaded since system up --> This finds the download difference over a sec.
            newDownloadsSinceLastCheck = speedCheck - self.get_prevNetworkDownloads()
            
            if newDownloadsSinceLastCheck < 0.0001:
                newDownloadsSinceLastCheck = 0
            
            # Removing unnecessary download decimals.
            self.set_currentDownloadSpeed_MbPerSec(round((newDownloadsSinceLastCheck / 1048576), 4))
            
            # print(f"Download Speed (MB/s): {self.getcurrentDownloadSpeed_MbPerSec()}")
            
        else:
            self.set_loopedThroughNetworkFunctionOnce(True)
        
        # Setting comparison value for MB/s calc.
        self.set_prevNetworkDownloads(speedCheck)
        
        # Sleep for 1 sec to find MB/s --> This is now done in the GUI class
        # time.sleep(1)
        