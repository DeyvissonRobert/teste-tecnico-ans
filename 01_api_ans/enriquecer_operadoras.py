import pandas as pd

print("Iniciando etapa 2.2 - Enriquecimento de dados")

DESPESAS_FILE = "data/processed/consolidado_despesas.csv"
OPERADORAS_FILE = "data/raw/operadoras_ativas.csv"

OUTPUT_FILE = "data/processed/consolidado_despesas_enriquecido.csv"

df_despesas = pd.read_csv(DESPESAS_FILE, sep=";", encoding="latin1")
df_operadoras = pd.read_csv(OPERADORAS_FILE, sep=";", encoding="latin1")

# Padronizar CNPJ (remover caracteres não numéricos)
df_despesas["CNPJ"] = df_despesas["CNPJ"].astype(str).str.replace(r"\D", "", regex=True)
df_operadoras["CNPJ"] = df_operadoras["CNPJ"].astype(str).str.replace(r"\D", "", regex=True)

# Remover duplicidades no cadastro de operadoras
df_operadoras = df_operadoras.drop_duplicates(subset="CNPJ")

# Selecionar apenas colunas relevantes do cadastro
df_operadoras = df_operadoras[
    ["CNPJ", "REGISTRO_OPERADORA", "Modalidade", "UF"]
]

# Join dos dados
df_final = df_despesas.merge(
    df_operadoras,
    on="CNPJ",
    how="left"
)

# Renomear coluna para padronização
df_final = df_final.rename(columns={
    "REGISTRO_OPERADORA": "RegistroANS"
})

# Salvar resultado
df_final.to_csv(
    OUTPUT_FILE,
    sep=";",
    index=False,
    encoding="latin1"
)

print("Etapa 2.2 concluída com sucesso")
print(f"Arquivo gerado: {OUTPUT_FILE}")
print(f"Total de registros: {len(df_final)}")
