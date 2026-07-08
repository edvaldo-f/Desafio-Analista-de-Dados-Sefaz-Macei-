# Passo 3 do desafio
# Script para otimizar o formato do arquivo consolidado dos dados

import pandas as pd
from pathlib import Path

"""
==========================================================
Para essa otimização, será usado a conversão para o formato Parquet.
Justificativas no README.    
==========================================================
"""

# Encontrando a raiz do projeto.
raiz_do_projeto = Path(__file__).parent.parent
# Caminho do arquivo consolidado.
caminho_arquivo_consolidado = raiz_do_projeto / "dados_processados" / "dados_consolidados.csv"

print(f"Lendo o arquivo consolidado em {caminho_arquivo_consolidado}...")
# Caminho do arquivo otimizado.
pasta_otimizados = raiz_do_projeto / "dados_otimizados"
pasta_otimizados.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir

# Lendo e convertendo o arquivo consolidado para o formato Parquet.
df_consolidado = pd.read_csv(
    caminho_arquivo_consolidado, 
    sep=";", 
    encoding="latin-1", 
    decimal=",")

caminho_parquet = pasta_otimizados / "dados_otimizados.parquet"
df_consolidado.to_parquet(caminho_parquet, index=False)

