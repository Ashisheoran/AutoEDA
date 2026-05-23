import pandas as pd

class DataLoader:
    def __init__(self, file):
        self.file = file

    def load_data(self):
        try:
            df = pd.read_csv(self.file, on_bad_lines='skip')
            return df
        except Exception as e:
            raise ValueError(f"Error Loading file: {e}")
        
    def basic_info(self,df):
        info = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list[df.columns]
        }
        return info