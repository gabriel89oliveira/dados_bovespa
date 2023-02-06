import pandas as pd

from app.model import HistoricPrices


# Ler arquivo da Bovespa
data = pd.read_csv('storage\COTAHIST_A2022.txt')
data.columns = ['data']
data.drop(data.tail(1).index,inplace=True)


# Inicia DataFrame
df = pd.DataFrame()


# Data do pregão
df['date'] = data['data'].str[2:10]
df['date'] = pd.to_datetime(df["date"], format='%Y%m%d')

# Código de negociação do papel
df['ticker'] = data['data'].str[12:24]
df['ticker'] = df['ticker'].str.replace(" ", "")

# Tipo de mercado - A vista, fracionado, leilão
df['market'] = data['data'].str[24:27]

# Nome resumido da empresa
df['company_name'] = data['data'].str[27:39]
df['company_name'] = df['company_name'].str.replace(" ", "")

# Especificaçao do papel - BDR, LFT, ON
df['specification'] = data['data'].str[39:49]

# Preço de abertura
df['open_price'] = data['data'].str[56:69]
df['open_price'] = df['open_price'].str.replace(" ", "")
df['open_price'] = pd.to_numeric(df['open_price'])
df['open_price'] = df['open_price'] / 100

# Preço máximo
df['maximum_price'] = data['data'].str[69:82]
df['maximum_price'] = df['maximum_price'].str.replace(" ", "")
df['maximum_price'] = pd.to_numeric(df['maximum_price'])
df['maximum_price'] = df['maximum_price'] / 100

# Preço mínimo
df['minimum_price'] = data['data'].str[82:95]
df['minimum_price'] = df['minimum_price'].str.replace(" ", "")
df['minimum_price'] = pd.to_numeric(df['minimum_price'])
df['minimum_price'] = df['minimum_price'] / 100

# Preço médio
df['average_price'] = data['data'].str[95:108]
df['average_price'] = df['average_price'].str.replace(" ", "")
df['average_price'] = pd.to_numeric(df['average_price'])
df['average_price'] = df['average_price'] / 100

# Último preço
df['close_price'] = data['data'].str[108:121]
df['close_price'] = df['close_price'].str.replace(" ", "")
df['close_price'] = pd.to_numeric(df['close_price'])
df['close_price'] = df['close_price'] / 100

# Volume total de titulos negociados
df['volume'] = data['data'].str[170:188]
df['volume'] = pd.to_numeric(df['volume'])

# Fator de cotação do papel
df['factor'] = data['data'].str[210:217]
df['factor'] = pd.to_numeric(df['factor'])

# Código ISIN
df['isin'] = data['data'].str[230:242]

# # Tipo de registro
# df['TIPO DE REGISTRO'] = data['data'].str[:2]

# # Código BDI
# df['CÓDIGO BDI'] = data['data'].str[10:12]

# # Prazo em dias do mercado a termo
# df['PRAZO EM DIAS DO MERCADO A TERMO'] = data['data'].str[49:52]

# # Moeda de referencia
# df['MOEDA'] = data['data'].str[52:56]

# # Código do emissor
# df['COD EMISSOR'] = df['CODISIN'].str[2:6]

# # Tipo de ativo
# df['TIPO DE ATIVO'] = df['CODISIN'].str[6:9]

# # Espécie de ativo
# df['ESPÉCIE DE ATIVO'] = df['CODISIN'].str[9:11]


# list_of_dicts = df.to_dict('records')
# # HistoricPrices.insert_many(list_of_dicts).execute()

# n_items = list(islice(list_of_dicts.items(), 10))


df = df[df["market"].str.contains("010|020") == True]

while (len(df.index) > 0):

    chunk_df = df.head(1000)
    list_of_dicts = chunk_df.to_dict('records')
    HistoricPrices.insert_many(list_of_dicts).execute()

    df = df.iloc[1000:]