import os
import zipfile
import pandas as pd
from pathlib import Path

from app.model import Companies

class CompanyService:


    # Folder where files will be stored
    storage_path = "storage/cvm/"


    # Busca arquivos FCA
    def get_company_data():

        print('  Buscando dados das empresas', flush=True)

        # Document folder in DFP storage
        folder_path = CompanyService.storage_path + "FCA"

        # Retrieve documents from DFP folder
        for filename in os.listdir(folder_path):

            file_path = folder_path + "/" + filename

            # Document year
            year = Path(file_path).stem

            # checking if it is a file
            if os.path.isfile(file_path):

                # Open document on Data Frame
                df1 = CompanyService.readZip(file_path, 'fca_cia_aberta_geral_' + year + '.csv')

                # Remove unused columns
                df1.drop('Data_Referencia', axis=1, inplace=True)
                df1.drop('Versao', axis=1, inplace=True)
                df1.drop('ID_Documento', axis=1, inplace=True)
                df1.drop('Data_Nome_Empresarial', axis=1, inplace=True)
                df1.drop('Nome_Empresarial_Anterior', axis=1, inplace=True)
                df1.drop('Data_Constituicao', axis=1, inplace=True)
                df1.drop('Data_Registro_CVM', axis=1, inplace=True)
                df1.drop('Categoria_Registro_CVM', axis=1, inplace=True)
                df1.drop('Data_Categoria_Registro_CVM', axis=1, inplace=True)
                df1.drop('Situacao_Registro_CVM', axis=1, inplace=True)
                df1.drop('Data_Situacao_Registro_CVM', axis=1, inplace=True)
                df1.drop('Pais_Origem', axis=1, inplace=True)
                df1.drop('Pais_Custodia_Valores_Mobiliarios', axis=1, inplace=True)
                df1.drop('Data_Situacao_Emissor', axis=1, inplace=True)
                df1.drop('Data_Especie_Controle_Acionario', axis=1, inplace=True)
                df1.drop('Dia_Encerramento_Exercicio_Social', axis=1, inplace=True)
                df1.drop('Mes_Encerramento_Exercicio_Social', axis=1, inplace=True)
                df1.drop('Data_Alteracao_Exercicio_Social', axis=1, inplace=True)

                # Convert columns to lowercase
                df1.columns= df1.columns.str.lower()

                # Rename columns
                df1.rename(columns={'codigo_cvm': 'cd_cvm', 'nome_empresarial': 'denom_cia'}, inplace=True)


                # Open document on Data Frame
                df2 = CompanyService.readZip(file_path, 'fca_cia_aberta_valor_mobiliario_' + year + '.csv')

                # Remove unused columns
                df2.drop('Data_Referencia', axis=1, inplace=True)
                df2.drop('Versao', axis=1, inplace=True)
                df2.drop('ID_Documento', axis=1, inplace=True)
                df2.drop('Sigla_Classe_Acao_Preferencial', axis=1, inplace=True)
                df2.drop('Classe_Acao_Preferencial', axis=1, inplace=True)
                df2.drop('Composicao_BDR_Unit', axis=1, inplace=True)
                df2.drop('Sigla_Entidade_Administradora', axis=1, inplace=True)
                df2.drop('Entidade_Administradora', axis=1, inplace=True)
                df2.drop('Data_Inicio_Negociacao', axis=1, inplace=True)
                df2.drop('Data_Fim_Negociacao', axis=1, inplace=True)
                df2.drop('Data_Inicio_Listagem', axis=1, inplace=True)
                df2.drop('Data_Fim_Listagem', axis=1, inplace=True)

                # Convert columns to lowercase
                df2.columns= df2.columns.str.lower()

                # Rename columns
                df2.rename(columns={'codigo_negociacao': 'ticker'}, inplace=True)

                df2 = df2[df2["mercado"].str.contains("Bolsa") == True]
                df2.drop('mercado', axis=1, inplace=True)

                result = pd.merge(df1, df2, on=['cnpj_companhia'])

                list_of_dicts = result.to_dict('records')
                Companies.insert_many(list_of_dicts).on_conflict(action='IGNORE').execute()


    """
    Open a zip file and read the given file

    """
    def readZip(path, filename):

        # Open Zip file
        zip = zipfile.ZipFile(path)

        # Convert document to DataFrame
        return pd.read_csv(zip.open(filename), encoding='latin1', sep=";", decimal=",", header=0)