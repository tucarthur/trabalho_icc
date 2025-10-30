import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

# Folder for output
RAW_DIR = Path("../data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# --- Sample data pools ---
establishments = [
    "Jaú Serve", "Savegnago", "Drogaria São Paulo", "Farmacia Droga Raia",
    "Uber", "99Pop", "Cinema Lumière", "Padaria Central",
    "Restaurante do Zé", "Posto Shell", "Onibus Urbano"
]

# Generate random dates (last 30 days)
def random_date():
    today = datetime.today()
    delta_days = random.randint(0, 120)
    return (today - timedelta(days=delta_days)).strftime("%Y-%m-%d")

# Generate random amounts
def random_amount():
    return round(random.uniform(5.0, 200.0), 2)

# Generate N fake expense entries
def generate_expenses(n=100):
    data = {
        "date": [random_date() for _ in range(n)],
        "establishment": [random.choice(establishments) for _ in range(n)],
        "amount": [random_amount() for _ in range(n)],
    }
    return pd.DataFrame(data)

def main():
    df = generate_expenses(100)
    output_path = RAW_DIR / "expenses.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} fake expense records at {output_path}")

if __name__ == "__main__":
    main()
