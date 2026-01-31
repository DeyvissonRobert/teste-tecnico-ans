import pandas as pd
from pathlib import Path
import zipfile

BASE_DIR = Path("data/processed")
OUTPUT_DIR = BASE_DIR
ANALISES_DIR = BASE_DIR / "analises"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ANALISES_DIR.mkdir(parents=True, exist_ok=True)

arquivos = list(BASE_DIR.glob("*/*.csv"))

dfs = []

print("Iniciando consolidação dos dados...")

for arquivo in arquivos:
    print(f"Lendo arquivo: {arquivo}")

    # Extrair trimestre e ano do nome da pasta (ex: 2T2023)
    pasta = arquivo.parent.name
    trimestre = pasta[:2]
    ano = pasta[2:]

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin1",
        low_memory=False
    )

    colunas_esperadas = {
        "CNPJ": "CNPJ",
        "RazaoSocial": "RazaoSocial",
        "VL_SALDO_FINAL": "ValorDespesas"
    }

    df = df.rename(columns=colunas_esperadas)

    df = df[list(colunas_esperadas.values())]

    df["Trimestre"] = trimestre
    df["Ano"] = ano

    dfs.append(df)

consolidado = pd.concat(dfs, ignore_index=True)

print(f"Total de registros antes do tratamento: {len(consolidado)}")

consolidado["ValorDespesas"] = (
    consolidado["ValorDespesas"]
    .astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)

consolidado["ValorDespesas"] = pd.to_numeric(
    consolidado["ValorDespesas"],
    errors="coerce"
)

# Remover valores zerados ou negativos
consolidado = consolidado[consolidado["ValorDespesas"] > 0]

# Tratar CNPJ duplicado com Razão Social diferente
duplicados = (
    consolidado.groupby("CNPJ")["RazaoSocial"]
    .nunique()
    .reset_index()
)

cnpjs_conflitantes = duplicados[duplicados["RazaoSocial"] > 1]["CNPJ"]

if not cnpjs_conflitantes.empty:
    print(f"CNPJs com múltiplas razões sociais: {len(cnpjs_conflitantes)}")

    consolidado = (
        consolidado.sort_values("RazaoSocial")
        .drop_duplicates(subset=["CNPJ", "Trimestre", "Ano", "ValorDespesas"])
    )

print(f"Total de registros após tratamento: {len(consolidado)}")

# Salvar CSV final
csv_final = OUTPUT_DIR / "despesas_consolidadas.csv"
consolidado.to_csv(csv_final, index=False, sep=";", encoding="utf-8")

# Compactar em ZIP
zip_path = OUTPUT_DIR / "consolidado_despesas.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_final, arcname="despesas_consolidadas.csv")

print("Arquivo consolidado e compactado com sucesso!")
