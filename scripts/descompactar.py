## Script para descompactar os arquivos em dados_compactados/, Passo 1 do desafio.

import zipfile
from pathlib import Path

# Encontra a raiz do projeto.
raiz_do_projeto = Path(__file__).parent.parent

# Caminhos das pastas.
pasta_origem = raiz_do_projeto / "dados_compactos"
pasta_destino = raiz_do_projeto / "dados_extraidos"

# Laço para encontrar os arquivos zip e extraí-los na devida pasta.
for zip_file in pasta_origem.rglob("*.zip"):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        pasta_final = pasta_destino / zip_file.parent.name
        zip_ref.extractall(pasta_final)
