

import pandas as pd
from pathlib import Path
from utils import clean_data, create_category_mapping, aggregate_expenses

RAW_PATH = Path("../data/raw/expenses.csv")
PROCESSED_PATH = Path("../data/processed/expenses_processed.csv")
ESTABLISHMENTS_PATH = Path("../data/establishments.csv")


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

if __name__ == "__main__":
    main()
