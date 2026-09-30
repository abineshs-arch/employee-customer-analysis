import numpy as np
import pandas as pd


class DataAnalyzer:
    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    def numpy_operations(self) -> dict:
        salaries = self._df["salary"].to_numpy(dtype=float)
        column = salaries.reshape(-1, 1)
        factors = np.array([[1.00, 1.05, 1.10]])
        scenarios = column * factors  # broadcasting: (n,1) * (1,3) -> (n,3)

        matrix = self._df[["performance_score", "experience", "JobSatisfaction"]].to_numpy(dtype=float)
        weights = np.array([0.5, 0.3, 0.2])
        composite = np.dot(matrix, weights)

        return {
            "first_10_salaries": salaries[:10].tolist(),
            "salary_mean": float(np.mean(salaries)),
            "salary_sum": float(np.sum(salaries)),
            "salary_std": float(np.std(salaries)),
            "scenario_means": scenarios.mean(axis=0).tolist(),
            "composite_score_mean": float(composite.mean()),
        }

    def department_summary(self) -> pd.DataFrame:
        return self._df.groupby("department").agg(
            employee_count=("employee_id", "count"),
            avg_salary=("salary", "mean"),
            max_salary=("salary", "max"),
        )

    def merge_departments(self, dept_df: pd.DataFrame) -> pd.DataFrame:
        # Left join keeps every employee even if a department is missing from the budget file.
        merged = pd.merge(self._df, dept_df, on="department", how="left")
        payroll = merged.groupby("department")["salary"].sum() * 12
        budgets = dept_df.set_index("department")["budget"]
        utilization = (payroll / budgets * 100).round(1).rename("budget_utilization_pct")
        print(utilization)
        return merged