

from app.Services.documents.update_documents import UpdateDocuments
from app.Services.documents.seed_database import SeedDatabase

class ManageDocuments:


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
        # UpdateDocuments.update(ManageDocuments.storage_path)

        # Seed data base with updated documents
        SeedDatabase.seed(ManageDocuments.storage_path)