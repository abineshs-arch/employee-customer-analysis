from pathlib import Path

import pandas as pd

RENAME_MAP = {
    "EmployeeNumber": "employee_id",
    "Age": "age",
    "Gender": "gender",
    "Department": "department",
    "JobRole": "designation",
    "MonthlyIncome": "salary",
    "YearsAtCompany": "experience",
    "PerformanceRating": "performance_score",
    "Attrition": "status",
}


class DataCleaner:
    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df.copy()
        self.report: dict[str, int] = {}

    def remove_duplicates(self) -> "DataCleaner":
        before = len(self._df)
        self._df = self._df.drop_duplicates()
        self.report["duplicates_removed"] = before - len(self._df)
        return self

    def strip_text(self) -> "DataCleaner":
        for col in self._df.select_dtypes(exclude="number").columns:
            self._df[col] = self._df[col].str.strip()
        return self

    def fix_numeric_types(self, columns: list[str]) -> "DataCleaner":
        for col in columns:
            self._df[col] = pd.to_numeric(self._df[col], errors="coerce")
        return self

    def handle_missing(self) -> "DataCleaner":
        self.report["missing_before"] = int(self._df.isna().sum().sum())
        num_cols = self._df.select_dtypes(include="number").columns
        self._df[num_cols] = self._df[num_cols].fillna(self._df[num_cols].median())
        for col in self._df.select_dtypes(exclude="number").columns:
            if self._df[col].isna().any():
                self._df[col] = self._df[col].fillna(self._df[col].mode()[0])
        self.report["missing_after"] = int(self._df.isna().sum().sum())
        return self

    def rename_columns(self) -> "DataCleaner":
        self._df = self._df.rename(columns=RENAME_MAP)
        return self

    def save(self, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._df.to_csv(path, index=False)

    @property
    def df(self) -> pd.DataFrame:
        return self._df