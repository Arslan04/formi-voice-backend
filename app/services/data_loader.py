import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

class DataLoader:
    def __init__(self):
        self.rooms = None
        self.rules = None
        self.staff_queries = None
        self.pricing = None
        self.discounts = None

    def load_all(self):
        self.rooms = pd.read_csv(DATA_DIR / "room_info.csv")
        self.rules = pd.read_csv(DATA_DIR / "hotel_rules.csv")
        self.staff_queries = pd.read_csv(DATA_DIR / "staff_queries.csv")
        self.pricing = pd.read_csv(DATA_DIR / "room_pricing.csv")
        self.discounts = pd.read_csv(DATA_DIR / "discounts.csv")

        # Preprocessing / Cleaning (optional, e.g. date parsing)
        self.pricing['Date'] = pd.to_datetime(self.pricing['Date'], errors='coerce')
        
        # Fill missing values with placeholders
        self.rooms.fillna("NA", inplace=True)
        self.rules.fillna("NA", inplace=True)
        self.staff_queries.fillna("NA", inplace=True)
        self.discounts.fillna("NA", inplace=True)
print("DATA_DIR resolved to:", DATA_DIR)
print("CSV files found:", list(DATA_DIR.glob("*.csv")))
