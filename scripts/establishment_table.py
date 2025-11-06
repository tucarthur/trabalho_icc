import pandas as pd
from pathlib import Path

def generate_establishments_csv(output_path: str = "../data/establishments.csv"):
    """
    Generate a CSV file with establishment names and their corresponding categories.
    This serves as a lookup table for category mapping.
    """
    
    # Define your reference data
    data = [
        # Supermarkets
        ("Savegnago", "Supermarket"),
        ("Jaú Serve", "Supermarket"),
        ("Pão de Açúcar", "Supermarket"),
        
        # Drugstores
        ("Drogaria São Paulo", "Drugstore"),
        ("Drogasil", "Drugstore"),
        ("Farmácia Popular", "Drugstore"),
        
        # Entertainment
        ("Cinemark", "Entertainment"),
        ("Cine Araújo", "Entertainment"),
        ("UCI", "Entertainment"),
        
        # Transportation
        ("Uber", "Transportation"),
        ("99Pop", "Transportation"),
        ("Táxi", "Transportation"),
        ("Ônibus Urbano", "Transportation"),
        
        # Restaurants
        ("McDonald's", "Restaurant"),
        ("Subway", "Restaurant"),
        ("Outback", "Restaurant"),
        
        # Default examples
        ("Padaria Central", "Others"),
        ("Posto Shell", "Others"),
    ]
    
    # Create DataFrame
    establishments_df = pd.DataFrame(data, columns=["establishment", "category"])
    
    # Ensure output folder exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save CSV
    establishments_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"✅ Establishments CSV saved to: {output_path}")

if __name__ == "__main__":
    generate_establishments_csv()

