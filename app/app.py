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
    page_title="AutoEDA AI",
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
from app.ui_helper import load_css

load_css()

with st.sidebar:

    st.markdown('<div class="sidebar-section">Upload Dataset</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

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


data_tab, prolile_tab, viz_tab, insights_tab, ml_tab, ai_tab, report_tab, cleaning_tab = st.tabs([
    "Data Preview",
    "Profile",
    "Visualize",
    "Insights",
    "ML Model",
    "AI Assistant",
    "Report Download",
    "Data Cleaning"
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
                    st.markdown(f"##### Boxplot — `{selected_cat_col}` vs `{selected_num_col}`")
                    st.plotly_chart(visualizer.categorical_vs_numeric_box(selected_cat_col, selected_num_col))

                elif chart_type == "Average Bar":
                    st.markdown(f"##### Average Bar Chart — `{selected_cat_col}` vs `{selected_num_col}`")
                    st.plotly_chart(visualizer.categorical_mean(selected_cat_col, selected_num_col))
                elif chart_type == "Violin":
                    st.markdown(f"##### Violin Plot — `{selected_cat_col}` vs `{selected_num_col}`")
                    st.plotly_chart(visualizer.categorical_vs_numeric_violin(selected_cat_col, selected_num_col))
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
                st.markdown("""
                <div class="insight-item ok">
                    <div class="insight-dot ok"></div>
                    <span>No significant issues detected in this category.</span>
                </div>
                """, unsafe_allow_html=True)
    


# TAB 5 — ML Model

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
                badge_color = "var(--accent)" if model_type == "regression" else "var(--accent2)"

                st.markdown(f"""
                    <div style="margin:30px 0">
                        <span class="chip {'purple' if model_type != 'regression' else ''}"> {model_type.upper()}</span>
                        <span>Model trained</span>
                    </div>
                """, unsafe_allow_html=True)
                    

                best_result = results["best_result"]

                if results["type"] == "regression":

                    c1, c2 = st.columns(2)

                    c1.metric("R² Score", best_result["r2"])
                    c2.metric("MSE", best_result["mse"])

                else:
                    ca, cb = st.columns([2,3])
                    ca.metric("Accuracy", best_result["Accuracy"])

                    cb.markdown("### Classification Report")

                    cb.code(best_result["Report"])

                st.markdown("#### Model Comparison")

                results_df = pd.DataFrame(results["results"])

                st.dataframe(results_df)

                st.success(
                    f"Best Model: {results['best_model']} "
                    f"({results['best_score']})"
                )


# TAB 6 — AI Assistant

with ai_tab:
    ai1, ai2 = st.columns([1, 2])

    with ai1:
 
        current_provider = st.session_state.get("ai_provider_label", provider)
        st.markdown(f"""
        <div class="sidebar-stat" style="margin-top:8px;">
            <span>Provider</span>
            <span class="sidebar-stat-val">{provider}</span>
        </div>
        <div class="sidebar-stat">
            <span>API Key</span>
            <span class="sidebar-stat-val">{'Set' if api_key else 'Missing'}</span>
        </div>
        """, unsafe_allow_html=True)

        gen_btn = st.button("Generate AI Insights")

    with ai2:
        if gen_btn:
            if not api_key or api_key.strip() == "":
                st.warning("Please enter a valid API key in the sidebar.")
            else:
                with st.spinner(f"Thinking..."):

                    all_insights = st.session_state.get("insights")

                    if not all_insights:
                        engine = InsightEngine(df)
                        all_insights = engine.generate_all_insights()

                    assistant = AIAssistant(provider, api_key.strip())
                    ai_output = assistant.generate_summary(all_insights)
                    st.session_state["ai_summary"] = ai_output

                st.markdown(f"""
                <div class="ai-output">
                    {ai_output.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
    

    with report_tab:
        report_charts = []
        visualizer = DataVisualizer(df)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
            
        if numeric_cols:
            report_charts.append(visualizer.histogram(numeric_cols[0]))
            report_charts.append(visualizer.boxplot(numeric_cols[0]))
            report_charts.append(visualizer.violin_plot(numeric_cols[0]))


        if len(numeric_cols) >= 2:
            heatmap = visualizer.correlation_heatmap()
            report_charts.append(visualizer.scatter_with_trend(numeric_cols[0], numeric_cols[1]))

            if heatmap:
                report_charts.append(heatmap)

        if categorical_cols:
            report_charts.append(visualizer.categorical_bar(categorical_cols[0]))
            report_charts.append(visualizer.pie_chart(categorical_cols[0]))
            report_charts.append(visualizer.donut_chart(categorical_cols[0]))

        if categorical_cols and numeric_cols:
            report_charts.append(visualizer.categorical_vs_numeric_box(categorical_cols[0], numeric_cols[0]))
            report_charts.append(visualizer.categorical_mean(categorical_cols[0], numeric_cols[0]))
            report_charts.append(visualizer.categorical_vs_numeric_violin(categorical_cols[0], numeric_cols[0]))

        if len(categorical_cols) >= 2:
            report_charts.append(visualizer.categorical_vs_categorical_bar(categorical_cols[0], categorical_cols[1]))
            report_charts.append(visualizer.categorical_vs_categorical_stacked(categorical_cols[0], categorical_cols[1]))
            report_charts.append(visualizer.categorical_heatmap(categorical_cols[0], categorical_cols[1]))
        
        ml_results = None
        if "ml_results" in st.session_state:
            ml_results = st.session_state["ml_results"]
        
        ai_summary = None
        if "ai_summary" in st.session_state:
            ai_summary = st.session_state["ai_summary"]

        report_generator = ReportGenerator(
            df=df,
            insights=insights,
            charts=report_charts,
            ml_results=ml_results,
            ai_summary=ai_summary
        )

        report_html = report_generator.generate_html_report()

        st.download_button(
            label="📄 Download HTML Report",
            data=report_html,
            file_name="autoeda_report.html",
            mime="text/html"
        )


with cleaning_tab:
    st.info("Data cleaning features coming soon!")