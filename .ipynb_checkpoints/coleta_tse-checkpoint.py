#coleta automatizada com Python

import requests
import pandas as pd
from io import BytesIO
from zipfile import ZipFile

url = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_MT.zip"
response = requests.get(url)

with ZipFile(BytesIO(response.content)) as z:
    for file_name in z.namelist():
        if file_name.endswith('.csv'):
            df = pd.read_csv(z.open(file_name), sep=';', encoding='latin1')
            print(df.head())