import pandas as pd
import os

INPUT_FILE = "data/processed/despesas_consolidadas.csv"
OUTPUT_FILE = "data/processed/consolidado_despesas.csv"

print("Iniciando consolidação - etapa 1.3")

df = pd.read_csv(INPUT_FILE, sep=";", encoding="latin1")

df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
df["Ano"] = df["DATA"].dt.year

df["ValorDespesas"] = pd.to_numeric(
    df["VL_SALDO_FINAL"].astype(str).str.replace(",", "."),
    errors="coerce"
)

df = df[df["ValorDespesas"] > 0]


# Usando REG_ANS como identificador temporário, pois ainda não tenho CNPJ e RazaoSocial reais
df_final = pd.DataFrame({
    "CNPJ": df["REG_ANS"],
    "RazaoSocial": df["DESCRICAO"],
    "Trimestre": df["trimestre"],
    "Ano": df["Ano"],
    "ValorDespesas": df["ValorDespesas"]
})

df_final.to_csv(
    "data/processed/consolidado_despesas.csv",
    sep=";",
    index=False,
    encoding="latin1"
)


print(f"Arquivo gerado com sucesso: {OUTPUT_FILE}")
print(f"Total de registros: {len(df_final)}")
