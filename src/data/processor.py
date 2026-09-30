from abc import ABC, abstractmethod

import pandas as pd


class BaseDataProcessor(ABC):
    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    @abstractmethod
    def process(self) -> pd.DataFrame:
        """Each child class must write its own process()."""


class EmployeeDataProcessor(BaseDataProcessor):
    def __init__(self, df: pd.DataFrame, min_salary: int = 0) -> None:
        super().__init__(df)
        self._min_salary = min_salary

    def process(self) -> pd.DataFrame:
        return self._df[self._df["salary"] >= self._min_salary]