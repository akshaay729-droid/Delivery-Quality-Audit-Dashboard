import pandas as pd

def load_data():
    try:
        file_path = "data/delivery_data.xlsx"

        df = pd.read_excel(file_path)

        print("\n===== DELIVERY DATA LOADED =====\n")
        print(df)

        print(f"\nTotal Records Loaded: {len(df)}")

        return df

    except Exception as e:
        print(f"Error loading file: {e}")
        return None