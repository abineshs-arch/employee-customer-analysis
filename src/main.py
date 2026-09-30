import pandas as pd

from src.analysis.analyzer import DataAnalyzer
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


if __name__ == "__main__":
    main()