from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "consolidado_despesas_enriquecido.csv"


def carregar_dataframe():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, sep=";", encoding="latin1")

    # Garante que CNPJ seja string limpa
    df["CNPJ"] = (
        df["CNPJ"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )

    return df


def listar_operadoras(page: int = 1, limit: int = 10):
    df = carregar_dataframe()

    df = df.drop_duplicates(subset="CNPJ")

    total = len(df)
    start = (page - 1) * limit
    end = start + limit

    dados = df.iloc[start:end].fillna("").to_dict(orient="records")

    return {
        "data": dados,
        "page": page,
        "limit": limit,
        "total": total
    }


def buscar_operadora_por_cnpj(cnpj: str):
    df = carregar_dataframe()

    cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "")

    operadora = df[df["CNPJ"] == cnpj]

    if operadora.empty:
        return None

    return (
        operadora
        .drop_duplicates(subset="CNPJ")
        .iloc[0]
        .fillna("")
        .to_dict()
    )


def listar_despesas_por_cnpj(cnpj: str):
    df = carregar_dataframe()

    cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "")

    despesas = df[df["CNPJ"] == cnpj]

    if despesas.empty:
        return None

    despesas = despesas.sort_values(by=["Ano", "Trimestre"])

    return despesas[[
        "Ano",
        "Trimestre",
        "ValorDespesas"
    ]].fillna("").to_dict(orient="records")
