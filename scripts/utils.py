# scripts/utils.py
import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows with missing values
    df = df.dropna(subset=["amount", "category"])
    # Ensure amount is numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    # Normalize category capitalization
    df["category"] = df["category"].str.strip().str.title()
    # Ensure date column is datetimelike if present
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def create_category_mapping(df: pd.DataFrame) -> pd.DataFrame:
    """Assign a category based on establishment name keywords."""
    def map_category(name: str) -> str:
        name = str(name).lower()
        
        # Supermarkets
        if "jaú" in name or "savegnago" in name:
            return "Supermarket"
        
        # Drugstores
        if "drogaria" in name or "farmacia" in name:
            return "Drugstore"
        
        # Entertainment
        if "cinema" in name:
            return "Entertainment"
        
        # Transportation
        if any(x in name for x in ["uber", "99pop", "taxi", "bus", "ônibus"]):
            return "Transportation"
        
        # Default
        return "Others"

    # Apply mapping
    df["category"] = df["establishment"].apply(map_category)
    return df

def aggregate_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total spending by category and optionally by month."""
    # Sum of all amounts by category
    category_summary = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values(by="amount", ascending=False)
    )

    # If the dataset has dates, add a monthly summary too
    monthly_summary = None
    if "date" in df.columns:
        # make a safe copy and ensure datetime dtype
        tmp = df.copy()
        tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
        tmp = tmp.dropna(subset=["date"])
        if not tmp.empty:
            monthly_summary = (
                tmp.groupby(tmp["date"].dt.to_period("M"))["amount"]
                .sum()
                .reset_index()
            )
            monthly_summary["date"] = monthly_summary["date"].astype(str)
    
    return category_summary, monthly_summary