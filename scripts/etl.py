

import pandas as pd
from pathlib import Path
from utils import clean_data, create_category_mapping, aggregate_expenses

RAW_PATH = Path("../data/raw/expenses.csv")
PROCESSED_PATH = Path("../data/processed/cleaned_expenses.csv")


def main():
    # 1. Extract
    df = pd.read_csv(RAW_PATH)
    
    # 2. Transform
    df = create_category_mapping(df)
    df = clean_data(df)
    


    # 3. Aggregate
    category_summary, monthly_summary = aggregate_expenses(df) #ill figure what to do with these later

    # 4. Load
    df.to_csv(PROCESSED_PATH, index=False)
    

    print("Data processed successfully!")

if __name__ == "__main__":
    main()
