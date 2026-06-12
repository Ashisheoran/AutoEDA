import pandas as pd 

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report
)

class MLEngine:
    
    def __init__(self,df, target_column):
        self.df = df.copy()
        self.target_column = target_column


    def _problem_type_detect(self):
        if self.df[self.target_column].dtype == "object":
            return "classification"
        elif self.df[self.target_column].nunique() <= 10:
            return "classification"
        else:
            return "regression"
    
    def _get_model(self, problem_type):

        if problem_type == "regression":
            return {
                "Linear Regression": LinearRegression(),
                "Random Forest": RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
            }

        else:
            return {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Random Forest": RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1),
                "Decision Tree": DecisionTreeClassifier(random_state=42),
            }
        
    def _preprocess(self):
        df = self.df.copy()

        df = df.dropna(subset=[self.target_column])

        X = df.drop(columns = self.target_column)
        y = df[self.target_column]

        X = pd.get_dummies(X, drop_first=True)

        if y.dtype == "object":
            le = LabelEncoder()
            y = le.fit_transform(y)

        X = X.fillna(X.mean(numeric_only=True))

        return X,y
    

    def train(self):
        problem_type = self._problem_type_detect()
        X,y = self._preprocess()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        models = self._get_model(problem_type)

        results = []

        best_model = None
        best_score = -9999
        best_result = None

        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            feature_importance = None

            if hasattr(model, "feature_importances_"):
                feature_importance = pd.DataFrame({
                    "Feature": X.columns,
                    "Importance": model.feature_importances_
                }).sort_values(
                    "Importance",
                    ascending=False
                ).head(10)

            if problem_type == "regression":

                r2 = r2_score(y_test, preds)
                mse = mean_squared_error(y_test, preds)
                model_result = {
                    "Model": name,
                    "R2 Score": round(r2, 4),
                    "MSE": round(mse, 4),
                    "Feature Importance": feature_importance
                }

                score = r2

            else:
                accuracy = accuracy_score(y_test, preds)
                report_dict = classification_report(y_test, preds, output_dict=True)
                report_text = classification_report(y_test, preds)

                model_result = {
                    "Model": name,
                    "Accuracy": round(accuracy, 4),
                    "Precision": round(report_dict["weighted avg"]["precision"], 4),
                    "Recall": round(report_dict["weighted avg"]["recall"], 4),
                    "F1 Score": round(report_dict["weighted avg"]["f1-score"], 4),
                    "Report": report_text,  # text version
                    "Feature Importance": feature_importance
                }

                score = accuracy

            results.append(model_result)

            if score > best_score:
                best_score = score
                best_model = name
                best_result = model_result

            if hasattr(model, "feature_importances_"):
                importance = pd.DataFrame({
                    "Feature": X.columns,
                    "Importance": model.feature_importances_
                }).sort_values(
                    "Importance",
                    ascending=False
                ).head(10)

        return {
            "type": problem_type,
            "results": results,
            "best_model": best_model,
            "best_result": best_result,
            "best_score": round(best_score, 4)
        }