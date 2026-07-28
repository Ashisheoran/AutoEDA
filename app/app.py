import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

@st.cache_data
def load_data(file):
    loader = DataLoader(file)
    df = loader.load_data()         
    info = loader.basic_info(df)     
    return df, info

st.set_page_config(
    page_title="AutoEDA",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)


from core.data_loader import DataLoader
from core.profiler import DataProfiler
from core.visualizer import DataVisualizer
from core.insights import InsightEngine
from core.ml_engine import MLEngine
from core.ai_assistant import AIAssistant
from core.report_generator import ReportGenerator
from ui_helper import load_css

load_css()

with st.sidebar:

    st.markdown('<div class="sidebar-section">Upload Dataset</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv","xlsx","xls","json"], label_visibility="collapsed")

    if uploaded_file:
        st.markdown('<div class="sidebar-section">Dataset Info</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">AI Provider</div>', unsafe_allow_html=True)
    provider = st.selectbox("", ["OpenAI", "Gemini"], label_visibility="collapsed")
    api_key = st.text_input("API Key", type="password", placeholder="enter api key")



if uploaded_file:
    st.markdown("""
    <div class="hero-bar">
        <div>
            <div class="wordmark">
                Auto<span class="wordmark-highlight">EDA</span>
            </div>
        </div>

    """, unsafe_allow_html=True)


if not uploaded_file:
    st.markdown("""
    <div style="text-align:center;padding:200px 0 30px;">
        <div class="wordmark" style="font-size:4rem;">
            Auto<span class="wordmark-highlight">EDA</span>
        </div>
        <div style="color:var(--text-muted);font-size:1.2rem;max-width:600px;margin:0 auto 32px;line-height:1.7;color:#c6fdff;opacity:0.6;">
            Upload a CSV dataset to generate data profile reports, visualizations, statistical insights, and ML analysis in single dashboard.</div>
        <div style="display:flex;gap:12px;justify-content:center; color:#e8ffed">
            <span class="chip-card"> Auto Profiling</span>
            <span class="chip-card"> Smart Insights</span>
            <span class="chip-card"> ML Training</span>
            <span class="chip-card"> AI Explanations</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


with st.spinner("Loading dataset…"):
    with st.spinner("Loading dataset…"):
        df, info = load_data(uploaded_file)

    profiler = DataProfiler(df)
    column_types = profiler.column_classification()



st.markdown('<div class="section-label">Dataset Overview</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, value, label, color="var(--accent)"):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{color};">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

n_rows = info.get("rows", len(df))
n_cols = info.get("columns", len(df.columns))
n_num  = len(df.select_dtypes(include="number").columns)
n_cat  = len(df.select_dtypes(exclude="number").columns)
missing_pct = round(df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100, 1)

kpi(k1, f"{n_rows:,}", "Total Rows")
kpi(k2, n_cols, "Columns")
kpi(k3, n_num, "Numeric", "var(--accent2)")
kpi(k4, n_cat, "Categorical", "var(--accent3)")
kpi(k5, f"{missing_pct}%", "Missing Data",
    "var(--warning)" if missing_pct > 5 else "var(--success)")

st.markdown("<div style='margin-bottom:28px;'></div>", unsafe_allow_html=True)


data_tab, prolile_tab, viz_tab, insights_tab, clean_tab, ml_tab, ai_tab, report_tab= st.tabs([
    "Data Preview",
    "Profile",
    "Visualize",
    "Insights",
    "Data Cleaning",
    "ML Model",
    "AI Assistant",
    "Report Download",
])

# TAB 1 — Data Preview

with data_tab:
    st.markdown('<div class="section-title">Data Preview</div>', unsafe_allow_html=True)

    n_preview = st.select_slider(
        "Rows to preview", options=[5, 10, 50, 75, 100], value=10,
        label_visibility="visible"
    )
    st.dataframe(df.head(n_preview), height=380)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Basic Info</div>', unsafe_allow_html=True)
        st.json(info)
    with c2:
        st.markdown('<div class="section-title">Classification</div>', unsafe_allow_html=True)
        st.json(column_types)

# TAB 2 — Profiler

with prolile_tab:

    p1, p2 = st.columns([1, 2])

    with p1:
        st.markdown("##### Data Types")
        st.json(profiler.get_dtypes())

        st.markdown("##### Duplicate Rows")
        dup_count = profiler.duplicate_rows()
        dup_color = "var(--danger)" if dup_count > 0 else "var(--success)"
        st.markdown(f"""
        <div class="metric-card" style="text-align:left;margin-top:8px;">
            <div class="metric-value" style="color:{dup_color};">{dup_count}</div>
            <div class="metric-label">Duplicate rows detected</div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("##### Missing Values")
        mv_df = profiler.missing_values()
        st.dataframe(mv_df)


        missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        duplicate_pct = (profiler.duplicate_rows() / df.shape[0]) * 100
        

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("##### Statistical Summary")
    st.dataframe(profiler.summary_stats())

# TAB 3 — Visualizations

with viz_tab:
    if df is None or df.empty:
        st.error("Invalid or empty dataset.")
        st.stop()

    if df.shape[1] == 0:
        st.error("No columns found in dataset.")
        st.stop()

    visualizer = DataVisualizer(df)
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    if not numeric_cols and not categorical_cols:
        st.error("No valid columns found for visualization.")
        st.stop()
    else:
        if numeric_cols:
            v1, v2 = st.columns([1, 3])
            with v1:
                st.markdown("##### Numeric Distributions\n --- \n")
                selected_num_col = st.selectbox("Column", numeric_cols, key="viz_col")
                chart_type = st.radio("Chart", ["Histogram","violin", "Boxplot", "KDE"], key="num_chart_type")
            
            with v2:
                if chart_type == "Histogram":
                    fig = visualizer.histogram(selected_num_col)
                    st.markdown(f"##### Histogram — `{selected_num_col}`")
                    st.plotly_chart(fig)
                    # st.pyplot(visualizer.histogram(selected_num_col))

                elif chart_type == "Boxplot":
                    fig = visualizer.boxplot(selected_num_col)
                    st.markdown(f"##### Boxplot — `{selected_num_col}`")
                    # st.pyplot(visualizer.boxplot(selected_num_col))
                    st.plotly_chart(fig)
                
                elif chart_type == "violin":
                    fig = visualizer.violin_plot(selected_num_col)
                    st.markdown(f"##### Violin Plot — `{selected_num_col}`")
                    st.plotly_chart(fig)

                elif chart_type == "KDE":
                    st.plotly_chart(
                        visualizer.kde_plot(selected_num_col),
                        use_container_width=True
                    )

        else:
            st.info("No numeric columns available for distribution charts.")


        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        if categorical_cols:
            v1, v2 = st.columns([1, 3])
            with v1:
                st.markdown("##### Categorical Distributions \n --- \n")
                selected_cat_col = st.selectbox("Column", categorical_cols, key="cat_col")
                chart_type = st.radio("Chart", ["Count Plot","pie/donut", "Bar"],key="cat_chart_type")
            with v2:
                if chart_type == "Bar":
                    st.markdown(f"##### Bar Chart — `{selected_cat_col}`")
                    st.plotly_chart(visualizer.categorical_bar(selected_cat_col))
                elif chart_type == "Count Plot":
                    st.plotly_chart(visualizer.count_plot(selected_cat_col))
                elif chart_type == "pie/donut":
                    p1 , p2 = st.columns(2)
                    with p1:
                        st.markdown(f"##### Pie Chart — `{selected_cat_col}`")
                        st.plotly_chart(visualizer.pie_chart(selected_cat_col))
                    with p2:
                        st.markdown(f"##### Donut Chart — `{selected_cat_col}`")
                        st.plotly_chart(visualizer.donut_chart(selected_cat_col))
        else:
            st.info("No categorical columns available for distribution charts.")
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        if categorical_cols and numeric_cols:
            v1, v2 = st.columns([1,3])
            with v1:
                st.markdown("##### Categorical vs Numeical\n --- \n")
                
                selected_cat_col = st.selectbox("Select Categorical column", categorical_cols)
                selected_num_col = st.selectbox("Select Numeric column", numeric_cols)
                chart_type = st.radio("Chart",['Boxplot','Average Bar', 'Violin'], key="cat_num_chart_type")
            with v2:
                if chart_type == "Boxplot":
                    fig = visualizer.categorical_vs_numeric_box(selected_cat_col, selected_num_col)
                    if fig:
                        st.markdown(f"##### Boxplot — `{selected_cat_col}` vs `{selected_num_col}`")
                        st.plotly_chart(fig)
                    else:
                        st.info("Too many unique categories for visualization.")
                elif chart_type == "Average Bar":
                    st.markdown(f"##### Average Bar Chart — `{selected_cat_col}` vs `{selected_num_col}`")
                    st.plotly_chart(visualizer.categorical_mean(selected_cat_col, selected_num_col))
                elif chart_type == "Violin":
                    fig = visualizer.categorical_vs_numeric_violin(selected_cat_col, selected_num_col)
                    if fig:
                        st.markdown(f"##### Violin Plot — `{selected_cat_col}` vs `{selected_num_col}`")
                        st.plotly_chart(fig)
                    else:
                        st.info("Too many unique categories for visualization.")
        else:
            st.info("Need at least one numeric and one categorical column for combined charts.")
            
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        if len(categorical_cols) >= 2:
            cat1, cat2 = st.columns([1,3])
            with cat1:
                st.markdown("##### Categorical vs Categorical \n --- \n")
                cat_col1 = st.selectbox("X axis", categorical_cols, key="cat_col1")
                cat_col2 = st.selectbox("Y axis", categorical_cols,
                                        index=min(1, len(categorical_cols)-1), key="cat_col2")
                
                chart_type = st.radio("Chart", ["Grouped Bar", "stacked Bar", "Heatmap"])
            
            with cat2:
                if cat_col1 != cat_col2:
                    if chart_type == "Grouped Bar":
                        st.markdown(f"##### Grouped Bar Chart — `{cat_col1}` vs `{cat_col2}`")
                        st.plotly_chart(visualizer.categorical_vs_categorical_bar(cat_col1,cat_col2))

                    elif chart_type == "stacked Bar":
                        st.markdown(f"##### Stacked Bar Chart — `{cat_col1}` vs `{cat_col2}`")
                        st.plotly_chart(visualizer.categorical_vs_categorical_stacked(cat_col1, cat_col2))

                    elif chart_type == "Heatmap":
                        st.markdown(f"##### Heatmap - `{cat_col1}` vs `{cat_col2}`")
                        st.plotly_chart(visualizer.categorical_heatmap(cat_col1, cat_col2))
                else:
                    st.info("Please select different Columns for X and Y axis.")
        else:
            st.info("Need at least 2 categorical columns for categorical vs categorical charts.")
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        if len(numeric_cols) >= 2:
            sc1, sc2= st.columns([1, 3])
            with sc1:
                st.markdown("##### Numerical vs Numerical \n --- \n")
                x_col = st.selectbox("X Axis", numeric_cols, key="x_col")
                y_col = st.selectbox("Y Axis", numeric_cols,
                                     index=min(1, len(numeric_cols)-1), key="y_col")
            
                def get_best_hue(df, categorical_cols):
                    for col in categorical_cols:
                        if 2 <= df[col].nunique() <= 5:
                            return col
                    return None
                
                auto_hue = get_best_hue(df,categorical_cols)
                hue_col = st.selectbox(
                    "Color by (optional)",
                    [None] + categorical_cols,
                    index=(categorical_cols.index(auto_hue) + 1) if auto_hue else 0
                )
                
                chart_type = st.radio("Charts", ["Scatter", "Line"])

            with sc2:
                if x_col != y_col:
                    st.markdown(f"`{x_col}` vs `{y_col}`")
                    if chart_type == "Scatter":
                        st.plotly_chart(visualizer.scatter_with_trend(x_col, y_col, hue_col))
                    elif chart_type == "Line":
                        st.plotly_chart(visualizer.line_chart(x_col, y_col))
                else:
                    st.info("Please select different columns for X and Y axes.")

                
        
        else:
            st.info("Need at least 2 numeric columns for scatter plot.")

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        if len(numeric_cols) >= 2:
            h1,h2 = st.columns([1,1])
            with h1:
                st.markdown("##### Correlation Heatmap")
                @st.cache_data
                def get_heatmap(df):
                    return DataVisualizer(df).correlation_heatmap()

                heatmap_fig = get_heatmap(df)
                if heatmap_fig:
                    st.plotly_chart(heatmap_fig)
                else:
                    st.info("Need at least 2 numeric columns for a correlation heatmap.")


            with h2:
                st.markdown("#### Pair Plot")
                st.pyplot(visualizer.pair_plot())
        else:
            st.info("Not enough numeric columns for correlation analysis.")

# TAB 4 — Insights

with insights_tab:
    
    with st.spinner("Generating insights…"):
        if "insights" not in st.session_state:
            with st.spinner("Generating insights…"):
                engine = InsightEngine(df)
                st.session_state["insights"] = engine.generate_all_insights()

        insights = st.session_state["insights"]

    category_colors = {
        "missing":    ("warn"),
        "outlier":    ("error"),
        "skewness":   ("warn"),
        "correlation":("ok"),
        "cardinality":("warn"),
        "duplicate":  ("error"),
        "datatypes":  ("warn")
    }

    total_insights = sum(len(v) for v in insights.values())
    st.markdown(f"""
    <div style="display:flex; gap:12px; align-items:center; margin-bottom:20px;">
        <span style="font-family:'IBM Plex Mono',sans-serif;font-size:2rem;font-weight:800;color:var(--accent);">
            {total_insights}
        </span>
        <span style="color:var(--text-muted);font-size:0.9rem;">insights discovered in {len(insights)} categories</span>
    </div>
    """, unsafe_allow_html=True)

    for category, items in insights.items():
        dot_class = category_colors.get(category, ("ok"))
        c1,c2 = st.columns([2,1])

        with c1:
            with st.expander(f"{category.replace('_',' ').title()}  ({len(items)} findings)", expanded=True):
                if items:
                    for item in items:
                        st.markdown(f"""
                        <div class="insight-item {dot_class}"">
                            <div class="insight-dot {dot_class}"></div>
                            <span>{item}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="insight-item ok">
                        <div class="insight-dot ok"></div>
                        <span>No significant issues detected in this category.</span>
                    </div>
                    """, unsafe_allow_html=True)
    

# TAB 5 — Data Cleaning
with clean_tab:
    if "cleaned_df" not in st.session_state:
        st.session_state["cleaned_df"] = df.copy()

    cleaned_df = st.session_state["cleaned_df"]

    c1, c2 = st.columns([7, 1])
    with c1:
        if st.button("⟳ Refresh"):
            pass
    with c2: 
        csv = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button("Export Cleaned Data", data=csv, file_name="cleaned_data.csv", mime="text/csv")

    dc1, dc2 = st.columns(2)

    with dc1:
        st.subheader("Missing Values")
        missing_cols = [col for col in cleaned_df.columns if cleaned_df[col].isnull().sum() > 0]
        if missing_cols:
            column = st.selectbox("Select column to clean", missing_cols, key="clean_col")
            
            method = st.selectbox("Imputation method", ["Mean", "Median", "Mode"], key="impute_method")
            if st.button("Fill Missing Values"):
                if column not in cleaned_df.columns:
                    st.error("Selected column not found in dataset.")
                elif cleaned_df[column].isnull().sum() == 0:
                    st.info("No missing values in selected column.")
                else:
                    if method == "Mean":
                        imputed_value = cleaned_df[column].mean()
                    elif method == "Median":
                        imputed_value = cleaned_df[column].median()
                    elif method == "Mode":
                        imputed_value = cleaned_df[column].mode()[0]

                    cleaned_df[column] = cleaned_df[column].fillna(imputed_value)
                    st.success(f"Missing values in `{column}` imputed with {method.lower()} value: {imputed_value:.2f}")
                st.session_state["cleaned_df"] = cleaned_df
        else:
            st.info("No columns with missing values.")
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        st.subheader("Duplicate Rows")
        duplicates = cleaned_df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)

        if duplicates > 0:
            if st.button("Remove Duplicates"):
                cleaned_df = cleaned_df.drop_duplicates()
                st.success(f"Removed {duplicates} duplicate rows.")
                st.session_state["cleaned_df"] = cleaned_df
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        st.subheader("Constant Columns")
        constant_cols = [col for col in cleaned_df.columns if cleaned_df[col].nunique(dropna=False) <= 1]
        if constant_cols:
            st.write("Columns with constant values:")
            for col in constant_cols:
                st.code(col)
            if st.button("Remove Constant Columns"):
                cleaned_df = cleaned_df.drop(columns=constant_cols)
                st.success(f"Removed {len(constant_cols)} constant columns.")
                st.session_state["cleaned_df"] = cleaned_df

        else:
            st.info("No columns with constant values.")


    with dc2:    
        st.subheader("Drop Columns")
        drop_cols = st.multiselect("Columns to Drop", cleaned_df.columns, key="drop_cols")
        if st.button("Drop Selected Columns"):
            if drop_cols:
                cleaned_df = cleaned_df.drop(columns=drop_cols)
                new_duplicates = cleaned_df.duplicated().sum()

                st.success(f"{len(drop_cols)} Columns Dropped: {', '.join(drop_cols)}")
                
                if new_duplicates > 0:
                    st.warning(
                        f"⚠️ {new_duplicates} duplicate rows detected after dropping columns. "
                        "This can occur when a unique identifier column (e.g., CustomerID) is removed."
                    )
                st.session_state["cleaned_df"] = cleaned_df
            else:
                st.info("No columns selected for dropping.")


        cleaned_df = st.session_state.get("cleaned_df", df)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        st.subheader("Rename Column")
        old_col = st.selectbox("Select column to rename", cleaned_df.columns, key="rename_col")
        new_col = st.text_input("New Name", key="new_col").strip()
    
        if st.button("Rename Column"):
            if old_col and new_col:
                cleaned_df = cleaned_df.rename(columns={old_col: new_col})
                st.success(f"Column `{old_col}` renamed to `{new_col}`.")
                st.session_state["cleaned_df"] = cleaned_df
            else:
                st.warning("Please enter both old and new column names.")





# TAB 6 — ML Model

with ml_tab:
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        st.info("ML training requires at least one numeric column.")
        
    else:
        st.markdown('<div class="section-label">Train a Model</div>', unsafe_allow_html=True)


        st.markdown("**Select target column**")
        target_column = st.selectbox("Target", df.columns, label_visibility="collapsed")
        train_btn = st.button("Train Model")

        if train_btn:
            if df[target_column].nunique() < 2:
                st.warning("Target column must have at least 2 unique values")
            else:
                with st.spinner("Training model....."):
                    ml_engine = MLEngine(df, target_column)
                    results = ml_engine.train()
                    st.session_state["ml_results"] = results
                    
                model_type = results.get("type", "unknown")
                best_result = results["best_result"]
                best_model = results["best_model"]


                t1, t2 = st.columns([1, 3])
                t1.markdown(f"""
                    <div style="margin:30px 0">
                        <span class="chip {'purple' if model_type != 'regression' else ''}"> {model_type.upper()}</span>
                        <span>Model trained</span>
                    </div>
                """, unsafe_allow_html=True)

                t2.success(
                    f"Best Model: {results['best_model']} "
                    f"({results['best_score']})"
                )


                if results["type"] == "regression":

                    c1, c2 = st.columns(2)

                    c1.metric("R² Score", best_result["R2 Score"])
                    c2.metric("MSE", f"{best_result['MSE']:,.2f}")

                else:
                    ca, cb = st.columns([2,3])
                    ca.metric("Accuracy", best_result["Accuracy"])

                    cb.markdown("### Classification Report")
                    cb.code(best_result["Report"])

                st.markdown("#### Model Comparison")
                results_df = pd.DataFrame(results["results"])
                results_df = results_df.drop(columns=["Report", "Feature Importance"], errors="ignore")
                st.dataframe(results_df)

                importance_df = best_result.get("Feature Importance")
                if importance_df is not None and not importance_df.empty:
                    st.markdown("#### Top Features")
                    
                    f1, f2 = st.columns([1, 2])
                    f1.dataframe(importance_df)
                    f2.bar_chart(importance_df.set_index("Feature"))




# TAB 7 — AI Assistant

with ai_tab:

    ai1, ai2 = st.columns([2, 3])

    with ai1:
        selected_prompt = st.selectbox(
            "Select a question to ask about your dataset:",
            [
                "Provide an executive summary of the dataset.",
                "Provide business insights and trends from the dataset",
                "What are the most important insights from the dataset?",
                "Are there any issues with data quality?",
                "Is this dataset ready for machine learning?",
                "What preprocessing steps would you recommend?",
                "Can you summarize the ML model results?"
            ],
            key="preset_prompts"
        )
        st.markdown("---")

        user_prompt = st.text_area(
            "Ask a Question about your dataset or model:",
            placeholder="Example: Is this dataset ready for machine learning?"
        )

        custom_btn = st.button("Generate Response")

    with ai2:
        if custom_btn:
            if user_prompt.strip():
                selected_prompt = user_prompt



            if selected_prompt:

                if not api_key or api_key.strip() == "":
                    st.warning(
                        "Please enter a valid API key in the sidebar."
                    )

                else:

                    with st.spinner("Analyzing dataset..."):

                        all_insights = st.session_state.get("insights")

                        if not all_insights:
                            engine = InsightEngine(df)
                            all_insights = engine.generate_all_insights()

                        assistant = AIAssistant(
                            provider,
                            api_key.strip()
                        )
                        dataset_info = {
                        "Rows": len(df),
                        "Columns": len(df.columns),
                        "Missing Values": int(df.isnull().sum().sum()),
                        "Duplicate Rows": int(df.duplicated().sum())
                        }

                        ai_output = assistant.generate_summary(
                            insights=all_insights,
                            dataset_info=dataset_info,
                            ml_results=st.session_state.get("ml_results"),
                            custom_prompt=selected_prompt
                        )

                        st.session_state["ai_summary"] = ai_output

                    st.markdown(ai_output)

    
# TAB 8 — report download

    with report_tab:
        st.markdown("This feature is coming soon...........")
        # report_charts = []

        # visualizer = DataVisualizer(df)

        # numeric_cols = df.select_dtypes(
        #     include="number"
        # ).columns.tolist()

        # categorical_cols = df.select_dtypes(
        #     exclude="number"
        # ).columns.tolist()


        # # Distribution Chart
        # if numeric_cols:
        #     report_charts.append(
        #         visualizer.histogram(
        #             numeric_cols[0]
        #         )
        #     )


        # # Scatter + Correlation
        # if len(numeric_cols) >= 2:

        #     report_charts.append(
        #         visualizer.scatter_with_trend(
        #             numeric_cols[0],
        #             numeric_cols[1]
        #         )
        #     )

        #     heatmap = visualizer.correlation_heatmap()

        #     if heatmap:
        #         report_charts.append(heatmap)


        # # Main Categorical Distribution
        # if categorical_cols:

        #     report_charts.append(
        #         visualizer.categorical_bar(
        #             categorical_cols[0]
        #         )
        #     )


        # # Categorical vs Numeric
        # if categorical_cols and numeric_cols:

        #     report_charts.append(
        #         visualizer.categorical_vs_numeric_box(
        #             categorical_cols[0],
        #             numeric_cols[0]
        #         )
        #     )
        # ml_results = None
        # if "ml_results" in st.session_state:
        #     ml_results = st.session_state["ml_results"]
        
        # ai_summary = None
        # if "ai_summary" in st.session_state:
        #     ai_summary = st.session_state["ai_summary"]

        # report_generator = ReportGenerator(
        #     df=df,
        #     insights=insights,
        #     charts=report_charts,
        #     ml_results=ml_results,
        #     ai_summary=ai_summary
        # )

        # report_html = report_generator.generate_html_report()

        # st.download_button(
        #     label="📄 Download HTML Report",
        #     data=report_html,
        #     file_name="autoeda_report.html",
        #     mime="text/html"
        # )

