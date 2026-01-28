import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "despesas_consolidadas.csv")


def read_and_concatenate_csvs():
    dataframes = []

    for folder in os.listdir(DATA_DIR):
        folder_path = os.path.join(DATA_DIR, folder)

        if not os.path.isdir(folder_path):
            continue

        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                file_path = os.path.join(folder_path, file)

                print(f"Lendo arquivo: {file_path}")
                df = pd.read_csv(file_path, sep=";", encoding="latin1")

                df["trimestre"] = folder
                dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)


def main():
    df_final = read_and_concatenate_csvs()

    print("Total de registros:", len(df_final))

    df_final.to_csv(OUTPUT_FILE, index=False, sep=";")
    print(f"Arquivo consolidado salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
