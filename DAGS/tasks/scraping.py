import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

from tasks.util.transformations import (
    extrair_polegadas,
    extrair_marca,
    extrair_painel,
    extrair_resolucao
)
from tasks.util.constants import LOCAL_OUTPUT_PATH

def scraping_kabum(**kwargs):
    headers = {"User-Agent": "Mozilla/5.0"}
    produtos = []
    data_extracao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for page in range(1, 50):
        url = f"https://www.kabum.com.br/tv/tv-4k?facet_filters=&sort=most_searched&page_size=20&page_number={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")
        if not script:
            break

        data = json.loads(script.string)
        inner = data["props"]["pageProps"]["data"]

        if isinstance(inner, str):
            inner = json.loads(inner)

        catalog = inner.get("catalogServer") or inner.get("catalogClient")
        if not catalog:
            break

        items = catalog.get("data", [])
        if not items:
            break

        for item in items:
            nome = item.get("name") or item.get("title")
            preco = item.get("priceMember") or item.get("price")
            link = "https://www.kabum.com.br" + item.get("link", "")
            imagem = item.get("image")

            produtos.append({
                "NOME": nome,
                "PRECO": preco,
                "LINK": link,
                "IMAGEM": imagem,
                "POLEGADAS": extrair_polegadas(nome),
                "MARCA": extrair_marca(nome),
                "PAINEL": extrair_painel(nome),
                "RESOLUCAO": extrair_resolucao(nome),
                "DATA_EXTRACAO": data_extracao
            })

    df = pd.DataFrame(produtos)
    df.to_csv(LOCAL_OUTPUT_PATH, index=False, encoding='utf-8-sig')

    kwargs['ti'].xcom_push(key='qtd_produtos', value=len(df))
