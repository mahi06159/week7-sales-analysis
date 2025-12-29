import matplotlib.pyplot as plt
import os


class Visualizer:
    """Creates visual charts"""

    def __init__(self, dataframe):
        self.df = dataframe

    def monthly_sales_trend(self, monthly_data, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        plt.figure(figsize=(10, 5))
        monthly_data["total_sales"].plot(marker="o")
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/monthly_trend.png")
        plt.close()

    def category_sales(self, category_data, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        plt.figure(figsize=(10, 5))
        category_data["total_sales"].head(10).plot(kind="bar")
        plt.title("Top Categories by Sales")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/category_sales.png")
        plt.close()
