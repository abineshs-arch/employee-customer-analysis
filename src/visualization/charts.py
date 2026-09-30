from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


class VisualizationManager:
    def __init__(self, df: pd.DataFrame, out_dir: str = "outputs/charts") -> None:
        self._df = df
        self._out = Path(out_dir)
        self._out.mkdir(parents=True, exist_ok=True)

    def _save(self, name: str) -> str:
        path = self._out / name
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()
        return str(path)

    def bar_avg_salary(self) -> str:
        avg = self._df.groupby("department")["salary"].mean().sort_values()
        plt.figure(figsize=(8, 5))
        plt.bar(avg.index, avg.values, color="steelblue", label="Average monthly income")
        plt.title("Average Monthly Income by Department")
        plt.xlabel("Department")
        plt.ylabel("Average monthly income")
        plt.grid(axis="y", alpha=0.3)
        plt.legend()
        return self._save("1_bar_avg_salary.png")

    def line_join_trend(self) -> str:
        # The dataset has no joining date, so we approximate the join year as 2026 - years at company.
        join_year = 2026 - self._df["experience"]
        counts = join_year.value_counts().sort_index().cumsum()
        plt.figure(figsize=(8, 5))
        plt.plot(counts.index, counts.values, marker="o", label="Cumulative joins")
        plt.title("Cumulative Employee Joins (approximate join year)")
        plt.xlabel("Approximate join year")
        plt.ylabel("Cumulative employees")
        plt.grid(alpha=0.3)
        plt.legend()
        return self._save("2_line_join_trend.png")

    def hist_salary(self) -> str:
        plt.figure(figsize=(8, 5))
        plt.hist(self._df["salary"], bins=25, color="seagreen", edgecolor="white", label="Employees")
        plt.title("Monthly Income Distribution")
        plt.xlabel("Monthly income")
        plt.ylabel("Frequency")
        plt.grid(axis="y", alpha=0.3)
        plt.legend()
        return self._save("3_hist_salary.png")

    def scatter_exp_salary(self) -> str:
        plt.figure(figsize=(8, 5))
        plt.scatter(self._df["experience"], self._df["salary"], alpha=0.5, label="Employees")
        plt.title("Years at Company vs Monthly Income")
        plt.xlabel("Years at company")
        plt.ylabel("Monthly income")
        plt.grid(alpha=0.3)
        plt.legend()
        return self._save("4_scatter_exp_salary.png")

    def donut_headcount(self) -> str:
        counts = self._df["department"].value_counts()
        plt.figure(figsize=(7, 7))
        plt.pie(
            counts.values,
            labels=counts.index,
            autopct="%1.1f%%",
            wedgeprops={"width": 0.4},
        )
        plt.title("Department Headcount Share")
        return self._save("5_donut_headcount.png")

    def render_all(self) -> list[str]:
        return [
            self.bar_avg_salary(),
            self.line_join_trend(),
            self.hist_salary(),
            self.scatter_exp_salary(),
            self.donut_headcount(),
        ]