# Arquivo utilizado para executar os scripts da pasta scripts/, preparando o banco de dados.

import subprocess
import sys
import time

# Esta função executa os arquivos na pasta scripts/ na ordem correta.
def executar_script (arquivo_script):
    print(f"Executando script {arquivo_script}...")
    tempo_inicial = time.time()

    resultado = subprocess.run([sys.executable, arquivo_script])

    # Tratamento de erros, se o algum script falhar.
    if resultado.returncode == 0:
        tempo_final = time.time()
        duracao = tempo_final - tempo_inicial
        print(f"✅ {arquivo_script} concluído! (Tempo: {duracao:.2f}s)\n")
    else:
        print(f"❌ Erro no script {arquivo_script}. Processo interrompido automaticamente.")
        sys.exit(1)
    
if __name__ == "__main__":
    print("🚀 Iniciada a preparação de dados.")
    print("=" * 50 + "\n")

    # Ordem dos scripts
    executar_script("scripts\descompactar.py")
    executar_script("scripts\consolidar.py")
    executar_script("scripts\otimizar_formato.py")

    print("🎉 Sucesso! Os scripts foram executados e a base de dados está pronta para ser utilizada.")