import pandas as pd
import urllib.request
import os
import numpy as np

# DATA_URL = "https://queimadas.dgi.inpe.br/home/downloadfile?path=%2Fapp%2Fapi%2Fdata%2Fdados_abertos%2Ffocos%2FMensal%2Ffocos_abertos_mensal_202208.csv"
# DATA_FILE = 'data\ForestFires202208.csv'
# urllib.request.urlretrieve(DATA_URL, DATA_FILE)

df = pd.read_csv('data\ForestFires.csv', encoding='utf-8', low_memory=False, date_parser=pd.to_datetime)
print(df.info())

df = df[['lat', 'lon', 'data_hora_gmt', 'satelite', 'pais']]

df_split = np.array_split(df, 3)

df_split[0].to_csv('data\ForestFires0.csv', index=False)
df_split[1].to_csv('data\ForestFires1.csv', index=False)
df_split[2].to_csv('data\ForestFires2.csv', index=False)

# df.to_csv('data\ForestFires.csv', index=False)
# os.remove('data\ForestFires202208.csv')

# print(df.info())