import pandas as pd
import numpy as np


class InsightEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    # 1. Correlation Insights
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

        return list(set(insights))  # remove duplicates

    # 2. Missing Value Insights
    def missing_insights(self):
        insights = []
        missing_percent = (self.df.isnull().sum() / len(self.df)) * 100

        for col, pct in missing_percent.items():
            if pct > 30:
                insights.append(f"{col} has high missing values ({pct:.2f}%)")
            elif pct > 0:
                insights.append(f"{col} has some missing values ({pct:.2f}%)")

        return insights

    # 3. Skewness Insights
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

    # 4. Outlier Detection (IQR)
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

    # Combine all insights
    def generate_all_insights(self):
        return {
            "correlation": self.correlation_insights(),
            "missing": self.missing_insights(),
            "skewness": self.skewness_insights(),
            "outliers": self.outlier_insights(),
        }