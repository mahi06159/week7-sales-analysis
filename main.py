from sales_analyzer.analyzer import SalesAnalyzer

DATA_PATH = "data/raw/sales_data.csv"
REPORT_PATH = "data/reports/sales_report.xlsx"

def main():
    analyzer = SalesAnalyzer(DATA_PATH)

    analyzer.clean_data()

    stats = analyzer.calculate_basic_stats()
    print("Basic Statistics:", stats)

    analyzer.create_visualizations()
    analyzer.generate_report(REPORT_PATH)


if __name__ == "__main__":
    main()
