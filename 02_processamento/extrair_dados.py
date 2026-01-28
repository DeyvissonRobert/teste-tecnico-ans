import os
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)


def extract_zip_files():
    for file in os.listdir(RAW_DIR):
        if file.endswith(".zip"):
            zip_path = os.path.join(RAW_DIR, file)
            extract_path = os.path.join(PROCESSED_DIR, file.replace(".zip", ""))

            print(f"Extraindo {file}...")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)


def main():
    extract_zip_files()


if __name__ == "__main__":
    main()
