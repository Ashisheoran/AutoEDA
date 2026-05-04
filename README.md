# 🚀 AutoEDA with AI Insight Assistant

AutoEDA is an intelligent exploratory data analysis (EDA) system that automates data profiling, visualization, insight generation, and optional machine learning — all through an interactive Streamlit dashboard.

---

## 📌 Overview

This project simplifies the data analysis workflow by allowing users to upload a dataset (CSV) and instantly receive:

* Data profiling
* Visualizations
* Smart insights
* AI-generated explanations
* Optional ML model training

---

## ✨ Features

### 📊 Automated Data Profiling

* Dataset overview (rows, columns, types)
* Missing value analysis
* Duplicate detection
* Data quality score

### 📈 Visualizations

* **Numeric:** Histogram, Boxplot, Violin Plot
* **Categorical:** Bar Chart, Pie/Donut Chart
* **Relationships:**

  * Scatter Plot (with trendline)
  * Correlation Heatmap
  * Pair Plot
* **Advanced Analysis:**

  * Categorical vs Numeric
  * Categorical vs Categorical

### 🧠 Smart Insights Engine

* Detects:

  * Missing values
  * Outliers
  * Skewness
  * Correlations
* Prioritizes insights based on severity

### 🤖 AI Insight Assistant

* Converts technical insights into natural language
* Supports:

  * OpenAI API
  * Google Gemini API
* Generates:

  * Observations
  * Issues
  * Recommendations

### ⚙️ Machine Learning (Optional)

* Basic model training
* Feature-target selection
* Performance metrics

---

## 🏗️ Project Structure

```
AutoEDA/
│
├── app/
│   ├── main.py          # Streamlit UI
│   └── components/
│
├── core/
│   ├── data_loader.py
│   ├── profiler.py
│   ├── visualizer.py
│   ├── insights.py
│   ├── ai_assistant.py
│   └── ml_engine.py
│
├── utils/
│   └── helpers.py
│
├── data/
├── models/
├── notebooks/
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/autoeda-pro.git
cd autoeda-pro

python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app/main.py
```

Then open:

```
http://localhost:8501
```

---

## 🔑 API Configuration (Optional)

### OpenAI

```bash
set OPENAI_API_KEY=your_api_key   # Windows
export OPENAI_API_KEY=your_api_key  # Mac/Linux
```

### Google Gemini

```bash
set GOOGLE_API_KEY=your_api_key
```

You can also enter API keys directly in the Streamlit sidebar.

---

## 📊 Example Use Cases

* Quick EDA for CSV datasets
* Data quality analysis
* Feature exploration before ML
* Academic projects
* Business data insights

---

## 🧠 Tech Stack

* Python
* Pandas, NumPy
* Plotly, Seaborn, Matplotlib
* Scikit-learn
* Streamlit
* OpenAI / Gemini APIs

---

## 🚀 Future Enhancements

* Auto feature engineering
* Model recommendation system
* PDF report export
* Cloud deployment (Streamlit Cloud / AWS)

---

## 👨‍💻 Author

**Ashish**
---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
