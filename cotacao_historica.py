import pandas as pd

# Ler arquivo da Bovespa
data = pd.read_csv('storage\COTAHIST_A2018.txt')
data.columns = ['data']
data.drop(data.tail(1).index,inplace=True)

# Inicia DataFrame
df = pd.DataFrame()

# Tipo de registro
df['TIPO DE REGISTRO'] = data['data'].str[:2]

# Data do pregão
df['DATA DO PREGÃO'] = data['data'].str[2:10]
df['DATA DO PREGÃO'] = pd.to_datetime(df["DATA DO PREGÃO"], format='%Y%m%d')

# Código BDI
df['CÓDIGO BDI'] = data['data'].str[10:12]

# Código de negociação do papel
df['CÓDIGO DE NEGOCIAÇÃO DO PAPEL'] = data['data'].str[12:24]
df['CÓDIGO DE NEGOCIAÇÃO DO PAPEL'] = df['CÓDIGO DE NEGOCIAÇÃO DO PAPEL'].str.replace(" ", "")

# Tipo de mercado
df['TIPO DE MERCADO'] = data['data'].str[24:27]

# Nome resumido da empresa
df['NOME DA EMPRESA'] = data['data'].str[27:39]
df['NOME DA EMPRESA'] = df['NOME DA EMPRESA'].str.replace(" ", "")

# Especificaçao do papel
df['ESPECIFICAÇÃO DO PAPEL'] = data['data'].str[39:49]

# Prazo em dias do mercado a termo
df['PRAZO EM DIAS DO MERCADO A TERMO'] = data['data'].str[49:52]

# Moeda de referencia
df['MOEDA'] = data['data'].str[52:56]

# Preço de abertura
df['ABERTURA'] = data['data'].str[56:69]
df['ABERTURA'] = df['ABERTURA'].str.replace(" ", "")
df['ABERTURA'] = pd.to_numeric(df['ABERTURA'])
df['ABERTURA'] = df['ABERTURA'] / 100

# Preço máximo
df['MÁXIMO'] = data['data'].str[69:82]
df['MÁXIMO'] = df['MÁXIMO'].str.replace(" ", "")
df['MÁXIMO'] = pd.to_numeric(df['MÁXIMO'])
df['MÁXIMO'] = df['MÁXIMO'] / 100

# Preço mínimo
df['MÍNIMO'] = data['data'].str[82:95]
df['MÍNIMO'] = df['MÍNIMO'].str.replace(" ", "")
df['MÍNIMO'] = pd.to_numeric(df['MÍNIMO'])
df['MÍNIMO'] = df['MÍNIMO'] / 100

# Preço médio
df['PREÇO MÉDIO'] = data['data'].str[95:108]
df['PREÇO MÉDIO'] = df['PREÇO MÉDIO'].str.replace(" ", "")
df['PREÇO MÉDIO'] = pd.to_numeric(df['PREÇO MÉDIO'])
df['PREÇO MÉDIO'] = df['PREÇO MÉDIO'] / 100

# Último preço
df['ÚLTIMO'] = data['data'].str[108:121]
df['ÚLTIMO'] = df['ÚLTIMO'].str.replace(" ", "")
df['ÚLTIMO'] = pd.to_numeric(df['ÚLTIMO'])
df['ÚLTIMO'] = df['ÚLTIMO'] / 100

# Volume total de titulos negociados
df['VOLUME'] = data['data'].str[170:188]
df['VOLUME'] = pd.to_numeric(df['VOLUME'])

# Fator de cotação do papel
df['FATCOT'] = data['data'].str[210:217]
df['FATCOT'] = pd.to_numeric(df['FATCOT'])

# Código ISIN
df['CODISIN'] = data['data'].str[230:242]

# Código do emissor
df['COD EMISSOR'] = df['CODISIN'].str[2:6]

# Tipo de ativo
df['TIPO DE ATIVO'] = df['CODISIN'].str[6:9]

# Espécie de ativo
df['ESPÉCIE DE ATIVO'] = df['CODISIN'].str[9:11]

print(df)