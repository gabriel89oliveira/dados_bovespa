from os.path import exists
from datetime import datetime

from app.Services.documents.file_helper import FileHelper
from app.Services.documents.download_document import DownloadDocument

class UpdateDocuments:


    """
    Update all documents from CVM in storage folder

    Download DRE, ITR and FCA documents from CVM portal.
    These documents have information compiled for all 
    companies grouped by year.

    Source: http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/...

    """
    def update(storage_path):

        # Document list
        documents = ['FCA', 'DRE', 'ITR']

        for document in documents:

            # Check if folder for document exists
            FileHelper.folder_exists(storage_path + "/" + document)

            # Retrieve documents since 2010
            for year in list(range(2010, datetime.now().year + 1)):
                
                # Path for document in storage
                file_path = storage_path + "/" + document + "/" + str(year) + ".zip"

                # Get document if it doesn't exist
                if(exists(file_path) == False):
                    DownloadDocument.download(storage_path, document, year)
                    continue

                # Force update document since last year
                if(year >= datetime.now().year - 1):

                    # Check if document is out of date
                    if (FileHelper.file_is_updated(file_path) == False):
                        DownloadDocument.download(storage_path, document, year)