import pandas as pd

class DataProfiler:
    def __init__(self,df: pd.DataFrame):
        self.df = df
    
    def get_dtypes(self):
        return self.df.dtypes.astype(str).to_dict()
    
    def missing_values(self):
        missing = self.df.isnull().sum()
        percent = round((missing / len(self.df)) * 100,2)

        return pd.DataFrame({
            "missing_count": missing,
            "missing_percent": percent
        }).sort_values(by="missing_percent",ascending=False)
    
    def duplicate_rows(self):
        return self.df.duplicated().sum()
    
    def summary_stats(self):
        return self.df.describe(include='all').transpose()
    
    def column_classification(self):
        numeric = self.df.select_dtypes(include=['number']).columns.tolist()
        categorical = self.df.select_dtypes(include='object').columns.tolist()

        return {
            "numeric": numeric,
            "categorical": categorical
        }