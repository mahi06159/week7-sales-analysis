import numpy as np


class DataCleaner:
    """Cleans sales data"""

    def __init__(self, dataframe):
        self.df = dataframe

    def clean(self):
        if self.df is None:
            return None

        # Remove duplicates
        self.df.drop_duplicates(inplace=True)

        # Handle missing numerical values
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.df[col].fillna(self.df[col].median(), inplace=True)

        # Handle missing categorical values
        categorical_cols = self.df.select_dtypes(include=["object"]).columns
        for col in categorical_cols:
            self.df[col].fillna(self.df[col].mode()[0], inplace=True)

        return self.df
import numpy as np


class DataCleaner:
    """Cleans sales data"""

    def __init__(self, dataframe):
        self.df = dataframe

    def clean(self):
        if self.df is None:
            return None

        # Remove duplicates
        self.df.drop_duplicates(inplace=True)

        # Handle missing numerical values
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.df[col].fillna(self.df[col].median(), inplace=True)

        # Handle missing categorical values
        categorical_cols = self.df.select_dtypes(include=["object"]).columns
        for col in categorical_cols:
            self.df[col].fillna(self.df[col].mode()[0], inplace=True)

        return self.df
