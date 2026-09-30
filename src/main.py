from src.data.cleaner import DataCleaner
from src.data.loader import DataLoader


def main() -> None:
    loader = DataLoader("data/raw/employees.csv")
    raw_df = loader.load()

    cleaner = DataCleaner(raw_df)
    (
        cleaner.remove_duplicates()
        .strip_text()
        .fix_numeric_types(["MonthlyIncome", "Age"])
        .handle_missing()
        .rename_columns()
    )
    cleaner.save("data/processed/cleaned_employees.csv")
    print("Cleaning report:", cleaner.report)
    print("Cleaned shape:", cleaner.df.shape)


if __name__ == "__main__":
    main()