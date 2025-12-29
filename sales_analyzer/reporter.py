import pandas as pd


class Reporter:
    """Exports reports to Excel"""

    def __init__(self, dataframe):
        self.df = dataframe

    def export_excel(self, summary, monthly, category, output_path):
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            pd.DataFrame([summary]).to_excel(
                writer, sheet_name="Summary", index=False
            )

            if not monthly.empty:
                monthly.to_excel(writer, sheet_name="Monthly Trends")

            if not category.empty:
                category.to_excel(writer, sheet_name="Category Analysis")

            self.df.head(1000).to_excel(
                writer, sheet_name="Sample Data", index=False
            )
