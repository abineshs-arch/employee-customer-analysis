import json
from pathlib import Path

import pandas as pd


class ReportGenerator:
    def __init__(self, df, cleaning_report, raw_rows,
                 chart_paths, benchmark=None, out_dir="outputs"):
        self._df = df
        self._cleaning = cleaning_report
        self._raw_rows = raw_rows
        self._charts = chart_paths
        self._benchmark = benchmark or {}
        self._out = Path(out_dir)
        (self._out / "reports").mkdir(parents=True, exist_ok=True)

    def compute_metrics(self):
        df = self._df
        yes = ["yes", "1", "true"]
        left = df["status"].astype(str).str.lower().isin(yes)
        over = df["OverTime"].astype(str).str.lower().isin(yes)
        dept = df.groupby("department")["salary"].mean()
        dept = dept.sort_values(ascending=False)
        attr = left.groupby(df["department"]).mean() * 100
        attr = attr.sort_values(ascending=False)
        role = df.groupby("designation")["salary"].mean()
        role = role.sort_values(ascending=False)
        return {
            "raw": int(self._raw_rows),
            "clean": int(len(df)),
            "dups": int(self._cleaning.get("duplicates_removed", 0)),
            "miss_b": int(self._cleaning.get("missing_before", 0)),
            "miss_a": int(self._cleaning.get("missing_after", 0)),
            "mean": float(df["salary"].mean()),
            "median": float(df["salary"].median()),
            "std": float(df["salary"].std()),
            "top_department": str(dept.index[0]),
            "top_avg": float(dept.iloc[0]),
            "low_department": str(dept.index[-1]),
            "low_avg": float(dept.iloc[-1]),
            "corr": float(df["experience"].corr(df["salary"])),
            "attrition": float(left.mean() * 100),
            "attr_department": str(attr.index[0]),
            "attr_department_pct": float(attr.iloc[0]),
            "ot": float(left[over].mean() * 100),
            "no_ot": float(left[~over].mean() * 100),
            "top_role": str(role.index[0]),
            "top_role_avg": float(role.iloc[0]),
            "api_benchmark": self._benchmark,
        }

    def build_findings(self, m):
        a = "Highest average monthly income: "
        b = a + m["top_department"] + " (" + str(round(m["top_avg"])) + ")."
        c = "Lowest average monthly income: "
        d = c + m["low_department"] + " (" + str(round(m["low_avg"])) + ")."
        e = "Experience vs income correlation r = " + str(round(m["corr"], 2)) + "."
        f = "Overall attrition is " + str(round(m["attrition"], 1)) + "%, "
        g = f + "highest in " + m["attr_department"]
        g = g + " (" + str(round(m["attr_department_pct"], 1)) + "%)."
        h = "Attrition with overtime: " + str(round(m["ot"], 1))
        h = h + "% vs " + str(round(m["no_ot"], 1)) + "% without."
        i = "Top paid role: " + m["top_role"]
        i = i + " (average " + str(round(m["top_role_avg"])) + ")."
        j = "Income mean " + str(round(m["mean"]))
        j = j + " vs median " + str(round(m["median"])) + "."
        return [b, d, e, g, h, i, j]

    def generate(self):
        m = self.compute_metrics()
        f = self.build_findings(m)
        out = self._out
        data = {"metrics": m, "findings": f}
        (out / "analysis_summary.json").write_text(
            json.dumps(data, indent=4), encoding="utf-8")
        txt = ["EXECUTIVE SUMMARY"] + ["- " + x for x in f]
        (out / "analysis_summary.txt").write_text(
            "\n".join(txt), encoding="utf-8")
        md = [
            "# Employee Data Analysis Report",
            "",
            "## Executive Summary",
            f[0] + " " + f[3],
            "",
            "## Dataset Overview",
            "- Records: " + str(m["raw"]) + " raw, "
            + str(m["clean"]) + " cleaned",
            "- Source: IBM Employee Dataset (Kaggle)",
            "",
            "## Data Quality Audit",
            "- Duplicates removed: " + str(m["dups"]),
            "- Missing values before / after: "
            + str(m["miss_b"]) + " / " + str(m["miss_a"]),
            "- Join-trend chart uses an approximate join year "
            "(2026 minus years at company).",
            "",
            "## Statistical Findings",
            "- Mean income: " + str(round(m["mean"])),
            "- Median income: " + str(round(m["median"])),
            "- Standard deviation: " + str(round(m["std"])),
            "",
            "## Embedded Visualizations",
        ]
        for p in self._charts:
            md.append("![" + Path(p).stem + "](../charts/" + Path(p).name + ")")
        md.append("")
        md.append("## Key Findings")
        for n, x in enumerate(f, 1):
            md.append(str(n) + ". " + x)
        md.append("")
        md.append("## Actionable Recommendations")
        md.append("- Review pay gaps between departments.")
        md.append("- Investigate the department with the highest attrition.")
        md.append("- Review overtime workload.")
        (out / "reports" / "analysis_report.md").write_text(
            "\n".join(md), encoding="utf-8")
        return m