import os
import requests

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")


os.makedirs(RAW_DIR, exist_ok=True)


def download_file(year, quarter):
    filename = f"{quarter}{year}.zip"
    url = f"{BASE_URL}/{year}/{filename}"
    file_path = os.path.join(RAW_DIR, filename)

    print(f"Baixando: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        f.write(response.content)


def main():
    year = "2023"
    quarters = ["4T", "3T", "2T"]

    print("Ano selecionado:", year)
    print("Trimestres selecionados:", quarters)

    for quarter in quarters:
        download_file(year, quarter)


if __name__ == "__main__":
    main()
