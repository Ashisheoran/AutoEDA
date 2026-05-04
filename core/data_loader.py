import pandas as pd

class DataLoader:
    def __init__(self, file):
        self.file = file

    def load_data(self):
        """ Load CSV File into pandas DataFrame"""
        try:
            df = pd.read_csv(self.file, on_bad_lines='skip')
            return df
        except Exception as e:
            raise ValueError(f"Error Loading file: {e}")
        
    def basic_info(self,df):
        """Return basic dataset info"""
        info = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list[df.columns]
        }
        return info







"""
Why This Design (Pay attention):-
Encapsulated inside a class → future extensibility (Excel, DB, APIs)
No UI logic → reusable
Explicit error handling → avoids silent failures
"""