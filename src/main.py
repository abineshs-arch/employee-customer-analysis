import pandas as pd

from src.analysis.analyzer import DataAnalyzer
from src.api.client import APIClient
from src.data.cleaner import DataCleaner
from src.data.loader import DataLoader


def main() -> None:
    raw_df = DataLoader("data/raw/employees.csv").load()
    cleaner = DataCleaner(raw_df)
    (
        cleaner.remove_duplicates()
        .strip_text()
        .fix_numeric_types(["MonthlyIncome", "Age"])
        .handle_missing()
        .rename_columns()
    )
    cleaner.save("data/processed/cleaned_employees.csv")

    analyzer = DataAnalyzer(cleaner.df)
    print(analyzer.numpy_operations())
    print(analyzer.department_summary())
    merged = analyzer.merge_departments(pd.read_csv("data/raw/departments.csv"))
    print(merged[["employee_id", "department", "salary", "budget"]].head())

    client = APIClient()
    payload = client.fetch_rates()
    if payload:
        benchmark = client.parse_benchmark(payload)
        client.save_cache(benchmark, "data/processed/api_cache.json")
        print("Benchmark rates:", benchmark)


if __name__ == "__main__":
    main()