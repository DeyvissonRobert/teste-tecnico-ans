import pandas as pd

print("Iniciando etapa 2.3 - Agregação de despesas")

INPUT_FILE = "data/processed/consolidado_despesas_enriquecido.csv"
OUTPUT_FILE = "data/processed/despesas_agregadas.csv"

df = pd.read_csv(INPUT_FILE, sep=";", encoding="latin1")

# Garantir valores numéricos
df["ValorDespesas"] = pd.to_numeric(df["ValorDespesas"], errors="coerce")

# Remover valores inválidos
df = df[df["ValorDespesas"] > 0]

# Tratar UF ausente
df["UF"] = df["UF"].fillna("NA")

# Agregação
df_agregado = (
    df.groupby(["RazaoSocial", "UF"])
      .agg(
          TotalDespesas=("ValorDespesas", "sum"),
          MediaDespesas=("ValorDespesas", "mean"),
          DesvioPadrao=("ValorDespesas", "std")
      )
      .reset_index()
)

# Ordenar do maior para o menor
df_agregado = df_agregado.sort_values("TotalDespesas", ascending=False)

df_agregado.to_csv(
    OUTPUT_FILE,
    sep=";",
    index=False,
    encoding="latin1"
)

print("Etapa 2.3 concluída com sucesso")
print(f"Arquivo gerado: {OUTPUT_FILE}")
print(f"Total de registros agregados: {len(df_agregado)}")
