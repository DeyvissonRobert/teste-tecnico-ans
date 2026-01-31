import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "despesas_consolidadas.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "analises"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Lendo dados consolidados...")

df = pd.read_csv(
    INPUT_FILE,
    sep=";",
    encoding="latin1",
    on_bad_lines="skip"
)

# Conversão dos valores monetários
for col in ["VL_SALDO_INICIAL", "VL_SALDO_FINAL"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

print("Total de registros:", len(df))

print("Agregando total por trimestre...")

por_trimestre = (
    df.groupby("trimestre", as_index=False)["VL_SALDO_FINAL"]
    .sum()
    .sort_values("VL_SALDO_FINAL", ascending=False)
)

output_trimestre = os.path.join(OUTPUT_DIR, "total_por_trimestre.csv")
por_trimestre.to_csv(output_trimestre, index=False, sep=";")

print("Arquivo gerado:", output_trimestre)

print("Agregando por conta contábil...")

por_conta = (
    df.groupby(["CD_CONTA_CONTABIL", "DESCRICAO"], as_index=False)["VL_SALDO_FINAL"]
    .sum()
    .sort_values("VL_SALDO_FINAL", ascending=False)
)

output_conta = os.path.join(OUTPUT_DIR, "total_por_conta_contabil.csv")
por_conta.to_csv(output_conta, index=False, sep=";")

print("Arquivo gerado:", output_conta)

print("Agregando por descrição...")

por_descricao = (
    df.groupby("DESCRICAO", as_index=False)["VL_SALDO_FINAL"]
    .sum()
    .sort_values("VL_SALDO_FINAL", ascending=False)
)

output_desc = os.path.join(OUTPUT_DIR, "total_por_descricao.csv")
por_descricao.to_csv(output_desc, index=False, sep=";")

print("Arquivo gerado:", output_desc)
