import pandas as pd 

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report
)

class MLEngine:
    def __init__(self,df: pd.DataFrame, target_column: str):
        self.df = df.copy()
        self.target_column = target_column

    #-----------helpler--------------
    def _detect_problem_type(self):
        if self.df[self.target_column].dtype == "object":
            return "classification"
        elif self.df[self.target_column].nunique() <= 10:
            return "classification"
        else:
            return "regression"
        
    def _preprocess(self):
        df = self.df.copy()

        #drop rows where target is missing
        df = df.dropna(subset=[self.target_column])

        #saparate feature and target
        X = df.drop(columns = self.target_column)
        y = df[self.target_column]

        #encode categorical features
        X = pd.get_dummies(X, drop_first=True)

        # Encode target  if classification
        if y.dtype == "object":
            le = LabelEncoder()
            y = le.fit_transform(y)

        #fill remaining missing values
        X = X.fillna(X.mean(numeric_only=True))

        return X,y
    
    #----------Training-----------
    def train(self):
        problem_type = self._detect_problem_type()
        X,y = self._preprocess()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if problem_type == "regression":
            model = LinearRegression()
            model.fit(X_train, y_train)

            preds = model.predict(X_test)

            return {
                "type": "regression",
                "mse": mean_squared_error(y_test, preds),
                "r2": r2_score(y_test, preds),
            }
        
        else:
            model = LogisticRegression()
            model.fit(X_train, y_train)

            preds = model.predict(X_test)

            return {
                "type": "classification",
                "accuracy": accuracy_score(y_test, preds),
                "report": classification_report(y_test, preds),
            }