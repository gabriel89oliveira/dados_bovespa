import datetime
import sys
import os
import os.path, time
from os.path import exists
from urllib import request
from datetime import datetime

import http.client as http
http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'


class GlobalDocuments:

    storage_path = "storage/cvm/"

    """
    Update all documents from CVM

    """
    def update():

        # Document list
        documents = ['FCA', 'DRE', 'ITR']

        for document in documents:

            # Check if folder exists
            GlobalDocuments.folder_exists(GlobalDocuments.storage_path + "/" + document)

            for year in list(range(2010, datetime.now().year + 1)):
                
                # Get all documents if no exists
                file_path = GlobalDocuments.storage_path + "/" + document + "/" + str(year) + ".zip"
                if(exists(file_path) == False):
                    GlobalDocuments.download(document, year)
                    continue

                # Force update document since last year
                if(year >= datetime.now().year - 1):

                    # Check if document is out of date
                    document_path = GlobalDocuments.storage_path + "/" + document + "/" + str(year) + ".zip"
                    if (GlobalDocuments.file_is_updated(document_path) == False):
                        GlobalDocuments.download(document, year)

    
 
    """
    Download document from origin
    
    """ 
    def download(document, year):

        origin = GlobalDocuments.getOriginPath(document, year)
        destiny = GlobalDocuments.storage_path + "/" + document + "/" + str(year) + ".zip"

        if(origin != False):
            print('  |- Fazendo download: ' + document + ' | ' + str(year), flush=True, file=sys.stdout)
            request.urlretrieve(origin, destiny)


    """
    Get original path to data
    
    """
    def getOriginPath(document, year):

        if(document == 'DFP'):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_" + str(year) + ".zip"

        if(document == 'ITR' and year > 2010):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/ITR_CIA_ABERTA_" + str(year) + ".zip"

        if(document == 'FCA' and year > 2017):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FCA/DADOS/fca_cia_aberta_" + str(year) + ".zip"

        return False


    """
    Check if a given directory exists in storage
    If not, create it
    
    """   
    def folder_exists(folder_path):
  
        # checking if the directory exist or not.
        if not os.path.isdir(folder_path):
            
            # if the directory is not present then create it.
            os.makedirs(folder_path)


    """
    Check if file is from today

    """
    def file_is_updated(file_path):

        if (exists(file_path) == False):
            return False

        # time.ctime(os.path.getmtime(file_path))
        last_update = datetime.strptime(time.ctime(os.path.getmtime(file_path)), '%a %b %d %H:%M:%S %Y')
        return last_update.date() >= datetime.today().date()