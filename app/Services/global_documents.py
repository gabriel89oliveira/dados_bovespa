import datetime
import sys
import os
import os.path, time
import zipfile
import pandas as pd
from os.path import exists
from urllib import request
from datetime import datetime
from pathlib import Path

import http.client as http
http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'

from app.model import IncomeStatements

class GlobalDocuments:


    # Folder where files will be stored
    storage_path = "storage/cvm/"


    """
    Update

    Update documents on storage folder and
    then seed the data base

    """
    def update():

        # Update documents on storage folder
        # GlobalDocuments.update_documents()

        # Seed data base with updated documents
        GlobalDocuments.seed_database()
        

    """
    Update all documents from CVM in storage folder

    Download DRE, ITR and FCA documents from CVM portal.
    These documents have information compiled for all 
    companies grouped by year.

    Source: http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/...

    """
    def update_documents():

        # Document list
        documents = ['FCA', 'DRE', 'ITR']

        for document in documents:

            # Check if folder for document exists
            GlobalDocuments.folder_exists(GlobalDocuments.storage_path + "/" + document)

            # Retrieve documents since 2010
            for year in list(range(2010, datetime.now().year + 1)):
                
                # Path for document in storage
                file_path = GlobalDocuments.storage_path + "/" + document + "/" + str(year) + ".zip"

                # Get document if it doesn't exist
                if(exists(file_path) == False):
                    GlobalDocuments.download(document, year)
                    continue

                # Force update document since last year
                if(year >= datetime.now().year - 1):

                    # Check if document is out of date
                    if (GlobalDocuments.file_is_updated(file_path) == False):
                        GlobalDocuments.download(document, year)
    
 
    """
    Download document from origin

    Download file from CVM portal and store it
    in storage folder
    
    """ 
    def download(document, year):

        # Get origin path based on document type
        origin = GlobalDocuments.getOriginPath(document, year)

        # Define where file will be stored
        destiny = GlobalDocuments.storage_path + "/" + document + "/" + str(year) + ".zip"

        if(origin != False):
            print('  |- Fazendo download: ' + document + ' | ' + str(year), flush=True, file=sys.stdout)
            request.urlretrieve(origin, destiny)


    """
    Get original path to data

    Concatenate the url for document source
    at CVM portal based on document type and
    period of release.
    
    """
    def getOriginPath(document, year):

        if(document == 'DFP' and year >= 2010):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_" + str(year) + ".zip"

        if(document == 'ITR' and year >= 2011):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/ITR_CIA_ABERTA_" + str(year) + ".zip"

        if(document == 'FCA' and year >= 2018):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FCA/DADOS/fca_cia_aberta_" + str(year) + ".zip"

        return False


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
    Seed database

    Seed database with values from
    documents in storage folder

    """
    def seed_database():

        GlobalDocuments.get_income_statement()


    """
    Get Income Statement

    Get data for Income Statement that is
    stored in DFP and ITR documents

    """
    def get_income_statement():

        print('  Rodando Seed para DFP', flush=True)

        # Document folder in DFP storage
        folder_path = GlobalDocuments.storage_path + "DFP"

        # Retrieve documents from DFP folder
        for filename in os.listdir(folder_path):
            
            # Seed data in data base
            GlobalDocuments.seed_income_statement(folder_path + "/" + filename, 'dfp')


        print('  Rodando Seed para ITR', flush=True)

        # Document folder in ITR storage
        folder_path = GlobalDocuments.storage_path + "ITR"

        # Retrieve documents from DFP folder
        for filename in os.listdir(folder_path):
            
            # Seed data in data base
            GlobalDocuments.seed_income_statement(folder_path + "/" + filename, 'itr')


    """
    Seed Income Statement

    Seed data in data base restored 
    from DFP and ITR documents

    """
    def seed_income_statement(file_path, document):

        # Document year
        year = Path(file_path).stem
        
        # checking if it is a file
        if os.path.isfile(file_path):

            # Open document on Data Frame
            df = GlobalDocuments.readZip(file_path, document + '_cia_aberta_DRE_con_' + year + '.csv')

            # Remove unused rows
            df = df[df["ORDEM_EXERC"].str.contains("PENÚLTIMO") == False]

            # Remove unused columns
            df = df.drop('VERSAO', axis=1)
            df = df.drop('GRUPO_DFP', axis=1)
            df = df.drop('ORDEM_EXERC', axis=1)

            # Convert columns to lowercase
            df.columns= df.columns.str.lower()

            print('  |- Fazendo seed: ' + str(year), flush=True)

            # Seed in chunks
            while (len(df.index) > 0):

                chunk_df = df.head(2000)
                list_of_dicts = chunk_df.to_dict('records')
                IncomeStatements.insert_many(list_of_dicts).on_conflict(action='IGNORE').execute()
                df = df.iloc[2000:]

    
    """
    Open a zip file and read the given file

    """
    def readZip(path, filename):

        # Open Zip file
        zip = zipfile.ZipFile(path)

        # Convert document to DataFrame
        return pd.read_csv(zip.open(filename), encoding='latin1', sep=";", decimal=",", header=0)
    
