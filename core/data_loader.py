import pandas as pd

class DataLoader:
    def __init__(self, file):
        self.file = file
        self.file_name = self.file.name.lower()
    def load_data(self):
        try:
            if self.file_name.endswith('.csv'):
                df = pd.read_csv(self.file, on_bad_lines='skip')
            elif self.file_name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(self.file, sheet_name="E Comm")
            elif self.file_name.endswith('.json'):
                df = pd.read_json(self.file)
            else:
                raise ValueError("Unsupported file format. Please provide a CSV, Excel, or JSON file.")
            return df
        except Exception as e:
            raise ValueError(f"Error Loading file: {e}")
        
    def basic_info(self,df):
        info = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list(df.columns)
        }
        return info