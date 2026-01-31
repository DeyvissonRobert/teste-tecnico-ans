import requests
import os

URL = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "operadoras_ativas.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Baixando cadastro de operadoras ativas...")

response = requests.get(URL)
response.raise_for_status()

with open(OUTPUT_FILE, "wb") as f:
    f.write(response.content)

print(f"Arquivo salvo em: {OUTPUT_FILE}")
