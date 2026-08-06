# Arquivo utilizado para executar os scripts da pasta scripts/, preparando o banco de dados.

import subprocess
import sys
import time
from pathlib import Path

# Esta função executa os arquivos na pasta scripts/ na ordem correta.
def executar_script (arquivo_script: Path):
    caminho_str = str(arquivo_script)
    print(f"Executando script {caminho_str}...")
    tempo_inicial = time.time()

    resultado = subprocess.run([sys.executable, caminho_str])

    # Tratamento de erros, se o algum script falhar.
    if resultado.returncode == 0:
        tempo_final = time.time()
        duracao = tempo_final - tempo_inicial
        print(f"[SUCESSO] {arquivo_script.name} concluido! (Tempo: {duracao:.2f}s)\n")
    else:
        print(f"[ERRO] Erro no script {arquivo_script.name}. Processo interrompido automaticamente.")
        sys.exit(1)
    
if __name__ == "__main__":
    print("Iniciada a preparacao de dados.")
    print("=" * 50 + "\n")

    pasta_scripts = Path("scripts")
    # Ordem dos scripts
    executar_script(pasta_scripts / "descompactar.py")
    executar_script(pasta_scripts / "consolidar.py")
    executar_script(pasta_scripts / "otimizar_formato.py")

    print("Sucesso! Os scripts foram executados e a base de dados esta pronta para ser utilizada.")