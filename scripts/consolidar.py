# Passo 2 do desafio.
# Script para ler e consolidar os arquivos em dados_extraidos/ 

import pandas as pd
import numpy as np
from pathlib import Path

# Encontrando a raiz do projeto.
raiz_do_projeto = Path(__file__).parent.parent
pasta_extraidos = raiz_do_projeto / "dados_extraidos"

# Nova pasta para os dados tratados.
pasta_processados = raiz_do_projeto / "dados_processados"
pasta_processados.mkdir(parents=True, exist_ok=True) # Cria a pasta se não existir

# Lista para guardar os DataFrames.
lista_dfs = []

# Laço para encontrar os arquivos CSV e adicioná-los à lista.
for caminho_csv in pasta_extraidos.rglob("*.csv"):
    ano_dado = caminho_csv.parent.name # Nome da pasta como coluna "ano"
    print(f"Processando o ano {ano_dado}...")
    
    # Código retirado do README.
    df_ano = pd.read_csv(
        caminho_csv,
        sep=";",
        skiprows=3,
        encoding="latin-1",
        decimal=",",
        thousands="."
        )
    
    # Foram adicionados algumas sugestões do README, afim de melhorar as análises e organização do DataFrame.
    
    # Sugestão: Adição da coluna "ano" ao DataFrame.
    df_ano["Ano"] = ano_dado
    
    # Sugestão: Adição da coluna que diferencia "função" de "subfunção" do DataFrame.
    codigo_conta = df_ano["Conta"].str.split(" - ").str[0].str.strip()
    
    condicoes = [
        (codigo_conta.str.len() == 2),
        (codigo_conta.str.contains(".", regex=False) | codigo_conta.str.startswith("FU"))
    ]
    resultados = ["Função", "Subfunção"]

    df_ano["Função/Subfunção"] = np.select(condicoes, resultados, default="Total/Agregador")

    # Sugestão: Correção para o tipo de dado de Valor ser um dado numérico (float).
    df_ano["Valor"] = pd.to_numeric(df_ano["Valor"], errors="coerce")

    # Fim do laço, adicionando a lista de DataFrames.
    lista_dfs.append(df_ano)

# Concatenando todos os DataFrames em um único DataFrame.
df_consolidado = pd.concat(lista_dfs, ignore_index=True)

# Salvando o dataframe consolidado em um arquivo CSV.
caminho_saida = pasta_processados / "dados_consolidados.csv"
df_consolidado.to_csv(caminho_saida, 
                      index=False, 
                      sep=";", 
                      encoding="latin-1", 
                      decimal=",", 
                      float_format="%.2f")
