import os
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

from app.Services.documents.file_helper import FileHelper

from app.model import IncomeStatements

class SeedDatabase:


    def seed(storage_path):
        SeedDatabase.get_documents(storage_path)


    """
    Get Income Statement

    Get data for Income Statement that is
    stored in DFP and ITR documents

    """
    def get_documents(storage_path):


        print('  Rodando Seed para DFP', flush=True)

        statements = pd.DataFrame()
        assets = pd.DataFrame()

        # Document folder in DFP storage
        folder_path = storage_path + "DFP"

        # Retrieve documents from DFP folder
        for filename in os.listdir(folder_path):
            
            # Concat values from DRE
            item = SeedDatabase.retrieve_data(folder_path + "/" + filename, 'dfp', 'DRE')
            statements = pd.concat([statements, item])

            # Concat values from DFC MD
            item = SeedDatabase.retrieve_data(folder_path + "/" + filename, 'dfp', 'DFC_MI')
            statements = pd.concat([statements, item])

            # Concat values from Assets
            item = SeedDatabase.retrieve_data(folder_path + "/" + filename, 'dfp', 'BPA')
            assets = pd.concat([assets, item])

            # Concat values from Liabilities
            item = SeedDatabase.retrieve_data(folder_path + "/" + filename, 'dfp', 'BPP')
            assets = pd.concat([assets, item])


        print('  Rodando Seed para ITR', flush=True)

        # Document folder in ITR storage
        folder_path = storage_path + "ITR"

        # Retrieve documents from DFP folder
        for filename in os.listdir(folder_path):
            
            # Seed data in data base
            item = SeedDatabase.retrieve_data(folder_path + "/" + filename, 'itr', 'DRE')
            statements = pd.concat([statements, item])

            # Concat values from DFC MD
            item = SeedDatabase.retrieve_data(folder_path + "/" + filename, 'itr', 'DFC_MI')
            statements = pd.concat([statements, item])

            # Concat values from Assets
            item = SeedDatabase.retrieve_data(folder_path + "/" + filename, 'itr', 'BPA')
            assets = pd.concat([assets, item])

            # Concat values from Liabilities
            item = SeedDatabase.retrieve_data(folder_path + "/" + filename, 'itr', 'BPP')
            assets = pd.concat([assets, item])

        # Make adjustments to statements
        statements = SeedDatabase.adjust_statements(statements)

        # Make adjustments to assets
        assets = SeedDatabase.adjust_assets(assets)
        
        # Seed quarter values
        print('  Semeando valores de demonstrativo', flush=True)
        SeedDatabase.seed_db(statements)

        print('  Semeando valores de balanço', flush=True)
        SeedDatabase.seed_db(assets)
    

    """
    Adjust Statements

    Make adjustments to statements to filter
    unecessary data, an calculate quarter values

    """
    def adjust_statements(statements):

        # Convert values to datetime
        statements['dt_ini_exerc'] = pd.to_datetime(statements['dt_ini_exerc'])
        statements['dt_fim_exerc'] = pd.to_datetime(statements['dt_fim_exerc'])

        # Convert values to float
        statements['vl_conta'] = statements['vl_conta'].astype(float)
        
        # Convert numbers of vl_conta to same scale
        statements['vl_conta'] = np.where(statements['escala_moeda'] == 'MIL', statements['vl_conta'] * 1000, statements['vl_conta'])

        # Get period time in months
        statements['trimestre'] = round((statements.dt_fim_exerc - statements.dt_ini_exerc)/np.timedelta64(1, 'M') / 3, 0)

        # Set unique index
        statements['id'] = statements['cd_cvm'].astype(str) + '_' + statements['cd_conta'] + '_' + statements['dt_ini_exerc'].astype(str) + '_' + statements['trimestre'].astype(str)

        # Calculate quarter values
        print('  Calculando valores trimestrais', flush=True)
        statements = SeedDatabase.quarter_values(statements)

        return statements
    

    """
    Adjust Assets

    Make adjustments to assets to filter unecessary
    data, an calculate quarter values

    """
    def adjust_assets(assets):

        # Convert values to datetime
        assets['dt_fim_exerc'] = pd.to_datetime(assets['dt_fim_exerc'])

        # Convert values to float
        assets['vl_conta'] = assets['vl_conta'].astype(float)
        
        # Convert numbers of vl_conta to same scale
        assets['vl_conta'] = np.where(assets['escala_moeda'] == 'MIL', assets['vl_conta'] * 1000, assets['vl_conta'])

        return assets

        
    """
    Seed Income Statement

    Seed data in data base restored 
    from DFP and ITR documents

    """
    def retrieve_data(file_path, document, file):

        # Document year
        year = Path(file_path).stem
        
        # checking if it is a file
        if os.path.isfile(file_path):

            # Open document on Data Frame
            df = FileHelper.readZip(file_path, document + '_cia_aberta_' + file + '_con_' + year + '.csv')

            # Remove unused rows
            df = df[df["ORDEM_EXERC"].str.contains("PENÚLTIMO") == False]

            # Remove unused columns
            df = df.drop('VERSAO', axis=1)
            df = df.drop('GRUPO_DFP', axis=1)
            df = df.drop('ORDEM_EXERC', axis=1)

            # Convert columns to lowercase
            df.columns = df.columns.str.lower()

            return df


    # """
    # Convert column values to
    # specific types as needed

    # """
    # def convert_columns(statements):

    #     # Convert values to datetime
    #     statements['dt_ini_exerc'] = pd.to_datetime(statements['dt_ini_exerc'])
    #     statements['dt_fim_exerc'] = pd.to_datetime(statements['dt_fim_exerc'])

    #     # Convert values to float
    #     statements['vl_conta'] = statements['vl_conta'].astype(float)

    #     return statements


    """
    Calculate Quarter Values for
    column vl_conta

    """
    def quarter_values(statements):

        # Create a copy of statements
        last_statements = statements[['cd_cvm', 'cd_conta', 'dt_ini_exerc', 'trimestre', 'vl_conta']].copy()

        # Increment one to each quarter 
        last_statements.loc[:, 'trimestre'] += 1

        # Create an id similar to statements, but with new quarter value
        last_statements['id'] = last_statements['cd_cvm'].astype(str) + '_' + last_statements['cd_conta'] + '_' + last_statements['dt_ini_exerc'].astype(str) + '_' + last_statements['trimestre'].astype(str)

        # Pick necessary columns
        last_statements = last_statements[['id', 'vl_conta']]

        # Rename column of values
        last_statements.rename(columns={'vl_conta': 'vl_conta_ultimo'}, inplace=True)

        # Merge statements by id
        result = pd.merge(statements, last_statements, on="id", how="left")

        # Create an adjust column to filter error values
        result['ajuste'] = result['vl_conta_ultimo'].fillna(0) / result['vl_conta_ultimo'].fillna(0)
        result['ajuste'] = result['ajuste'].fillna(0)
        result['vl_conta_ultimo'] = result['vl_conta_ultimo'].fillna(0)

        # Calculate quarter value
        result['vl_trimestre'] = (result['vl_conta'] - result['vl_conta_ultimo']) * result['ajuste']
        result.loc[result['trimestre'] == 1, 'vl_trimestre'] = result.loc[result['trimestre'] == 1, 'vl_conta']

        # Remove unused columns
        result.drop('id', axis=1, inplace=True)
        result.drop('vl_conta_ultimo', axis=1, inplace=True)
        result.drop('ajuste', axis=1, inplace=True)

        return result


    def seed_db(statements):
            
        # print('  |- Fazendo seed: ' + str(year), flush=True)

        # Seed in chunks
        while (len(statements.index) > 0):
            
            print('   Itens restantes: ' + str(len(statements.index)), flush=True)
            chunk_df = statements.head(10000)
            list_of_dicts = chunk_df.to_dict('records')
            IncomeStatements.insert_many(list_of_dicts).on_conflict(action='IGNORE').execute()
            statements = statements.iloc[10000:]
