def detect_column_types(df):
    numeric = df.select_dtypes(include=['number']).columns.tolist()
    categorical = df.select_dtypes(exclude=['number']).columns.tolist()

    return numeric, categorical

def get_best_hue(df, categorical_cols):
    for col in categorical_cols:
        if 2 <= df[col].nunique() <= 5:
            return col
    return None