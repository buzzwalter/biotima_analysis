import datetime
import pandas as pd
import numpy as np

class DataLoader:
    '''
    Class for handling loading of data.  Opens the possibility for many file types to be used seamlessly throughout the analysis
    '''
    def __init__(self,file_path):
        '''
        constructor for DataLoader class
        
        parameters:
            - file_path string associated with data location.

        no return
        '''
        self.file_path = file_path
    
    @staticmethod
    def load_data(self):
        """
        Loads data from a specified file path. 

        no parameters
         
        returns: 
            - data frame of the associated voltage versus time data.
        """
        try:
            df = pd.read_csv(self.file_path,delimiter=',',names=['time','volts'])
        except Exception as e:
            log_message(str(e))
            print(f"Error: {str(e)}")
        return df

class DataSaver:
    """
    class for handling saving with overloaded method.  Opens the possibility of saving to many file types seamlessly throughout the analysis.
    """
    def __init__(self,file_path=None):
        '''
        constructor for DataSaver class

        parameters:
            - file_path string associated with save location.  Takes None as default to allow for timestamped default path

        no return
        '''
        
        if file_path==None:
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M-%S")
            file_path = "./results/{timestamps}analysis.txt"

        self.file_path = file_path
    
    @staticmethod
    def save_data(self,data):
        """
        path specific save_data method

        parameters:
            - data numpy array of values

        no return
        """
        np.savetxt(self.file_path,data)
        pass

def log_message(message):
    """
    Logs a message with a timestamp to a specified log file.

    parameters:
        - message string

    no return
    """
    # Define the log file location
    log_file = "./log/analysis.log"
    
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the log message
    log_entry = f"[{timestamp}] {message}\n"
    
    # write the log message to the file
    with open(log_file, "w") as file:
        file.write(log_entry)