from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "consolidado_despesas_enriquecido.csv"


def obter_estatisticas():
    df = pd.read_csv(DATA_PATH, sep=";", encoding="latin1")

    df["ValorDespesas"] = pd.to_numeric(df["ValorDespesas"], errors="coerce")
    df = df.dropna(subset=["ValorDespesas"])

    total_despesas = df["ValorDespesas"].sum()
    media_despesas = df["ValorDespesas"].mean()

    top_5_operadoras = (
        df.groupby("RazaoSocial")["ValorDespesas"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
        .rename(columns={"ValorDespesas": "TotalDespesas"})
        .to_dict(orient="records")
    )

    return {
        "total_despesas": round(total_despesas, 2),
        "media_despesas": round(media_despesas, 2),
        "top_5_operadoras": top_5_operadoras
    }
