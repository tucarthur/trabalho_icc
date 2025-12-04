import pandas as pd
from pathlib import Path
from utils import clean_data, create_category_mapping, aggregate_expenses
import os
import subprocess

RAW_PATH = Path("../data/raw/expenses.csv")
PROCESSED_PATH = Path("../data/processed/expenses_processed.csv")
ESTABLISHMENTS_PATH = Path("../data/establishments.csv")


###############################################################
#                    MENU DO TERMINAL                         #
###############################################################

DEFAULT_CSV = str(RAW_PATH)
CURRENT_CSV = DEFAULT_CSV


def escolher_csv():
    global CURRENT_CSV

    print("\nDigite o caminho COMPLETO do CSV que deseja usar:")
    caminho = input("> ")

    if not caminho.endswith(".csv"):
        print("\n❌ O arquivo precisa ser .csv.")
        return

    if not os.path.exists(caminho):
        print("\n❌ Caminho inválido.")
        return

    CURRENT_CSV = caminho
    print(f"\n✔ CSV atualizado para: {CURRENT_CSV}")


def rodar_etl():
    global CURRENT_CSV

    print("\n🔄 Iniciando processamento...")

    # Copia o CSV escolhido para o local padrão usado pelo ETL
    df_user = pd.read_csv(CURRENT_CSV)
    df_user.to_csv(RAW_PATH, index=False)

    # Agora roda o ETL NORMALMENTE (seu código original)
    main()

    print("\n✔ Processamento finalizado! Arquivo disponível em:")
    print(f"   → {PROCESSED_PATH}")


def abrir_graficos():
    print("\n📊 Abrindo gráficos no Streamlit...")
    subprocess.run(["streamlit", "run", "graficosnovo.py"])


def menu():
    global CURRENT_CSV

    while True:
        print("\n=================================")
        print("              MENU")
        print("=================================")
        print(f"CSV atual utilizado: {CURRENT_CSV}")
        print("\n1. Escolher outro CSV")
        print("2. Processar dados (ETL)")
        print("3. Visualizar métricas (gráficos)")
        print("4. Sair")

        opc = input("\nEscolha uma opção: ")

        if opc == "1":
            escolher_csv()
        elif opc == "2":
            rodar_etl()
        elif opc == "3":
            abrir_graficos()
        elif opc == "4":
            print("\nEncerrando...")
            break
        else:
            print("\n❌ Opção inválida.")


###############################################################
#                  CÓDIGO ORIGINAL DO ETL                     #
###############################################################

def main():
    # 1. Extract
    df = pd.read_csv(RAW_PATH)
    establishments_df = pd.read_csv(ESTABLISHMENTS_PATH)

    # 2. Transform
    df = create_category_mapping(df, establishments_df)
    df = clean_data(df)

    # 3. Load
    df.to_csv(PROCESSED_PATH, index=False)

    print("Data processed successfully!")


###############################################################
#                    EXECUÇÃO DO PROGRAMA                     #
###############################################################

if __name__ == "_main_":
    menu()
menu()