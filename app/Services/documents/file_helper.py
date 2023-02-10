import os
import os.path, time
import zipfile
import pandas as pd

from os.path import exists
from datetime import datetime

class FileHelper:


    """
    Check if folder exists

    Check if a given directory exists in storage
    and, if it doesn't, create the folder
    
    """   
    def folder_exists(folder_path):
  
        # checking if the directory exist or not.
        if not os.path.isdir(folder_path):
            
            # if the directory is not present then create it.
            os.makedirs(folder_path)


    """
    Check if file is updated

    Check if last modification on file
    has been performed today, this is to
    avoid download same file more then once

    """
    def file_is_updated(file_path):

        if (exists(file_path) == False):
            return False

        last_update = datetime.strptime(time.ctime(os.path.getmtime(file_path)), '%a %b %d %H:%M:%S %Y')
        return last_update.date() >= datetime.today().date()
    

    """
    Open a zip file and read the given file

    """
    def readZip(path, filename):

        # Open Zip file
        zip = zipfile.ZipFile(path)

        # Convert document to DataFrame
        return pd.read_csv(zip.open(filename), encoding='latin1', sep=";", decimal=",", header=0)