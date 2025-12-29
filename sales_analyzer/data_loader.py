import pandas as pd


class DataLoader:
    """Loads sales data from CSV file"""

    def __init__(self, file_path):
        self.file_path = file_path

    def load_csv(self):
        try:
            df = pd.read_csv(self.file_path)
            print("Data loaded successfully")
            return df
        except Exception as e:
            print("Error loading data:", e)
            return None
