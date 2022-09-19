import pandas as pd
import urllib.request
import os

DATA_URL = "https://queimadas.dgi.inpe.br/home/downloadfile?path=%2Fapp%2Fapi%2Fdata%2Fdados_abertos%2Ffocos%2FMensal%2Ffocos_abertos_mensal_202208.csv"
DATA_FILE = 'data\ForestFires202208.csv'
urllib.request.urlretrieve(DATA_URL, DATA_FILE)

df = pd.read_csv('data\ForestFires202208.csv', encoding='utf-8', low_memory=False, date_parser=pd.to_datetime)
df = df[['lat', 'lon', 'data_hora_gmt', 'satelite','risco_fogo', 'pais']]

df.to_csv('data\ForestFires.csv', index=False)
os.remove('data\ForestFires202208.csv')

print(df.info())