import pandas as pd
import numpy as np


class InsightEngine:
    def __init__(self, df):
        self.df = df

    def correlation_insights(self, threshold=0.7):
        corr = self.df.corr(numeric_only=True)
        insights = []

        for col1 in corr.columns:
            for col2 in corr.columns:
                if col1 != col2:
                    value = corr.loc[col1, col2]

                    if abs(value) >= threshold:
                        relation = "positive" if value > 0 else "negative"

                        insights.append(
                            f"Strong {relation} correlation between {col1} and {col2} ({value:.2f})"
                        )

        return list(set(insights))

    def missing_insights(self):
        insights = []
        missing_percent = (self.df.isnull().sum() / len(self.df)) * 100

        for col, pct in missing_percent.items():
            if pct > 30:
                insights.append(f"{col} has high missing values ({pct:.2f}%)")
            elif pct > 0:
                insights.append(f"{col} has some missing values ({pct:.2f}%)")

        return insights

    def skewness_insights(self):
        insights = []
        numeric_cols = self.df.select_dtypes(include=np.number)

        skewness = numeric_cols.skew()

        for col, val in skewness.items():
            if val > 1:
                insights.append(f"{col} is highly positively skewed")
            elif val < -1:
                insights.append(f"{col} is highly negatively skewed")

        return insights

    def outlier_insights(self):
        insights = []
        numeric_cols = self.df.select_dtypes(include=np.number)

        for col in numeric_cols.columns:
            Q1 = numeric_cols[col].quantile(0.25)
            Q3 = numeric_cols[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers = numeric_cols[
                (numeric_cols[col] < lower) | (numeric_cols[col] > upper)
            ]

            if len(outliers) > 0:
                insights.append(f"{col} has {len(outliers)} potential outliers")

        return insights

    def cardinality_insights(self):
        insights = []

        for col in self.df.select_dtypes(exclude=np.number).columns:

            unique_pct = (
                self.df[col].nunique() /
                len(self.df)
            ) * 100

            if unique_pct > 80:
                insights.append(
                    f"{col} appears to be an identifier or high-cardinality column."
                )

        return insights

    def constant_column_insights(self):
        insights = []

        for col in self.df.columns:
            if self.df[col].nunique() == 1:
                insights.append(
                    f"{col} contains only one unique value."
                )

        return insights

    def duplicate_insights(self):

        duplicates = self.df.duplicated().sum()

        if duplicates > 0:
            return [
                f"Dataset contains {duplicates} duplicate rows."
            ]

        return []

    def datatype_insights(self):
        insights = []

        for col in self.df.columns:

            if self.df[col].dtype == "object":

                numeric_ratio = (
                    pd.to_numeric(
                        self.df[col],
                        errors="coerce"
                    )
                    .notna()
                    .mean()
                )

                if numeric_ratio > 0.8:
                    insights.append(
                        f"{col} may be stored as text instead of numeric."
                    )

        return insights

    def generate_all_insights(self):
        return {
            "correlation": self.correlation_insights(),
            "missing": self.missing_insights(),
            "skewness": self.skewness_insights(),
            "outliers": self.outlier_insights(),
            "cardinality": self.cardinality_insights(),
            "constant_columns": self.constant_column_insights(),
            "duplicates": self.duplicate_insights(),
            "datatypes": self.datatype_insights()
        }