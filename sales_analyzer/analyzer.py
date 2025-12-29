# analyzer.py - Sales Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class SalesAnalyzer:
    """Analyzes sales data and generates insights"""

    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Load sales data from CSV file"""
        try:
            self.df = pd.read_csv(self.data_path)

            if 'order_date' in self.df.columns:
                self.df['order_date'] = pd.to_datetime(self.df['order_date'])

            print("Data loaded successfully")
            print("Shape:", self.df.shape)

        except Exception as e:
            print("Error loading data:", e)

    def clean_data(self):
        """Clean the sales data"""
        if self.df is None:
            print("No data loaded")
            return

        # Remove duplicates
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        print("Duplicates removed:", before - after)

        # Handle missing values
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.df[col].fillna(self.df[col].median(), inplace=True)

        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            self.df[col].fillna(self.df[col].mode()[0], inplace=True)

    def calculate_basic_stats(self):
        """Calculate basic sales statistics"""
        if self.df is None:
            return {}

        stats = {
            "total_sales": self.df["total_amount"].sum(),
            "average_order_value": self.df["total_amount"].mean(),
            "total_orders": len(self.df),
            "unique_customers": self.df["customer_id"].nunique(),
            "unique_products": self.df["product_id"].nunique()
        }

        if 'order_date' in self.df.columns:
            stats["start_date"] = self.df["order_date"].min()
            stats["end_date"] = self.df["order_date"].max()

        return stats

    def analyze_sales_by_category(self):
        """Analyze sales by category"""
        if 'category' not in self.df.columns:
            return pd.DataFrame()

        category_sales = (
            self.df
            .groupby("category")
            .agg(
                total_sales=("total_amount", "sum"),
                total_quantity=("quantity", "sum"),
                order_count=("order_id", "count")
            )
            .sort_values("total_sales", ascending=False)
        )

        return category_sales

    def analyze_monthly_trends(self):
        """Analyze monthly sales trends"""
        if 'order_date' not in self.df.columns:
            return pd.DataFrame()

        self.df["month_year"] = self.df["order_date"].dt.to_period("M")

        monthly_sales = (
            self.df
            .groupby("month_year")
            .agg(
                total_sales=("total_amount", "sum"),
                total_quantity=("quantity", "sum"),
                unique_customers=("customer_id", "nunique"),
                order_count=("order_id", "count")
            )
        )

        monthly_sales["growth_rate"] = monthly_sales["total_sales"].pct_change() * 100

        return monthly_sales

    def create_visualizations(self, output_dir="data/reports"):
        """Create and save charts"""
        os.makedirs(output_dir, exist_ok=True)

        # Monthly sales trend
        monthly = self.analyze_monthly_trends()
        if not monthly.empty:
            plt.figure(figsize=(10, 5))
            monthly["total_sales"].plot(marker="o")
            plt.title("Monthly Sales Trend")
            plt.xlabel("Month")
            plt.ylabel("Total Sales")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/monthly_sales_trend.png")
            plt.close()

        # Category sales
        category = self.analyze_sales_by_category()
        if not category.empty:
            plt.figure(figsize=(10, 5))
            category["total_sales"].head(10).plot(kind="bar")
            plt.title("Top Categories by Sales")
            plt.xlabel("Category")
            plt.ylabel("Total Sales")
            plt.tight_layout()
            plt.savefig(f"{output_dir}/category_sales.png")
            plt.close()

        # Order value distribution
        plt.figure(figsize=(10, 5))
        plt.hist(self.df["total_amount"], bins=30)
        plt.title("Order Value Distribution")
        plt.xlabel("Order Value")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/order_value_distribution.png")
        plt.close()

    def generate_report(self, output_path="data/reports/sales_report.xlsx"):
        """Generate Excel report"""
        try:
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                pd.DataFrame([self.calculate_basic_stats()]).to_excel(
                    writer, sheet_name="Summary", index=False
                )

                monthly = self.analyze_monthly_trends()
                if not monthly.empty:
                    monthly.to_excel(writer, sheet_name="Monthly Trends")

                category = self.analyze_sales_by_category()
                if not category.empty:
                    category.to_excel(writer, sheet_name="Category Analysis")

                self.df.head(1000).to_excel(
                    writer, sheet_name="Sample Data", index=False
                )

            print("Report generated:", output_path)
            return True

        except Exception as e:
            print("Error generating report:", e)
            return False
