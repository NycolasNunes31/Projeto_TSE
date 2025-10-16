from fastapi import FastAPI
import pandas as pd
import sqlite3
import requests
from io import BytesIO
from zipfile import ZipFile

app = FastAPI()


def atualizar_dados_tse():
    url = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_MT.zip"
    response = requests.get(url)
    with ZipFile(BytesIO(response.content)) as z:
        for file_name in z.namelist():
            if file_name.endswith('.csv'):
                df = pd.read_csv(z.open(file_name), sep=';', encoding='latin1')
                conn = sqlite3.connect('tse_mt.db')
                df.to_sql('resultados', conn, if_exists='replace', index=False)
                conn.close()
                print("✅ Banco atualizado com sucesso!")


atualizar_dados_tse()

@app.get("/")
def home():
    return {"mensagem": "API do TSE - Eleições 2022 MT funcionando 🚀"}

@app.get("/dados_mt")
def get_dados():
    conn = sqlite3.connect('tse_mt.db')
    df = pd.read_sql_query("SELECT * FROM resultados LIMIT 100", conn)
    conn.close()
    return df.to_dict(orient='records')
