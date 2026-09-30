from pathlib import Path

import pandas as pd

from src.utils.exceptions import InvalidDatasetError

REQUIRED_COLUMNS = ["EmployeeNumber", "Department", "MonthlyIncome", "Age"]


class DataLoader:
    def __init__(self, file_path: str, required_columns: list[str] | None = None) -> None:
        self._file_path = Path(file_path)
        self._required_columns = required_columns or REQUIRED_COLUMNS
        self.df: pd.DataFrame | None = None

    def load(self) -> pd.DataFrame:
        if not self._file_path.exists():
            raise InvalidDatasetError(f"File not found: {self._file_path}")
        self.df = pd.read_csv(self._file_path)
        self._validate()
        return self.df

    def _validate(self) -> None:
        missing = [c for c in self._required_columns if c not in self.df.columns]
        if missing:
            raise InvalidDatasetError(f"Missing columns: {missing}")
        if len(self.df) < 100:
            raise InvalidDatasetError("Dataset needs at least 100 records")

    def inspect(self) -> None:
        print("Shape:", self.df.shape)
        print(self.df.head())
        print(self.df.tail())
        self.df.info()
        print(self.df.describe())
        print(self.df.isna().sum())