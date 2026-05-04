import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

@st.cache_data
def load_data(file):
    loader = DataLoader(file)
    df = loader.load_data()          # read ONCE
    info = loader.basic_info(df)     # reuse df
    return df, info

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="AutoEDA AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS injection ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── CSS Variables ── */
:root {
  --bg:        #08090d;
  --bg-panel:  #0f1117;
  --bg-card:   #141720;
  --bg-card2:  #1a1e2e;
  --border:    #1e2235;
  --border-glow: #2a3050;
  --accent:    #4fd9c4;
  --accent2:   #7b6ff0;
  --accent3:   #f06090;
  --text:      #e8eaf0;
  --text-muted:#7a8099;
  --text-dim:  #3e4460;
  --success:   #3dd68c;
  --warning:   #f5a623;
  --danger:    #f06060;
  --radius:    12px;
  --radius-sm: 8px;
}

/* ── Base Reset ── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  font-family: 'DM Sans', sans-serif;
  color: var(--text);
}

[data-testid="stSidebar"] {
  background: var(--bg-panel) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Hide default streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* KEEP header visible so sidebar toggle works */
header { visibility: visible;
            opacity: 0.3;}

/* Hide only toolbar content, not container */
[data-testid="stToolbar"] {
  opacity: 1;
}
.block-container { padding: 0 2rem 4rem !important; max-width: 1400px !important; }

/* ── Top hero bar ── */
.hero-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 0 24px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 32px;
  margin-top: 32px;

}
.hero-logo {
  width: 46px; height: 46px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; font-weight: 800;
  color: var(--bg);
  font-family: 'Syne', sans-serif;
  flex-shrink: 0;
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.65rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: linear-gradient(90deg, var(--text) 60%, var(--accent));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}
.hero-sub {
  font-size: 0.78rem;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.04em;
  margin: 2px 0 0;
}
.hero-badge {
  margin-left: auto;
  background: rgba(79,217,196,0.1);
  border: 1px solid rgba(79,217,196,0.3);
  color: var(--accent);
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.72rem;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.05em;
}

/* ── Section headers ── */
.section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 6px;
}
.section-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 20px;
  letter-spacing: -0.02em;
}
.section-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 36px 0;
}

/* ── Cards ── */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 22px;
  margin-bottom: 16px;
  transition: border-color 0.2s;
}
.card:hover { border-color: var(--border-glow); }

.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  text-align: center;
}
.metric-value {
  font-family: 'Syne', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  color: var(--accent);
  letter-spacing: -0.03em;
  line-height: 1;
}
.metric-label {
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 6px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.metric-sub {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 4px;
}

/* ── Insight pills ── */
.insight-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 14px;
  background: var(--bg-card2);
  border-left: 3px solid var(--accent);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  margin-bottom: 8px;
  font-size: 0.85rem;
  color: var(--text);
  line-height: 1.5;
}
.insight-item.warn  { border-left-color: var(--warning); }
.insight-item.error { border-left-color: var(--danger); }
.insight-item.ok    { border-left-color: var(--success); }
.insight-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); margin-top: 7px; flex-shrink: 0; }
.insight-dot.warn  { background: var(--warning); }
.insight-dot.error { background: var(--danger); }
.insight-dot.ok    { background: var(--success); }

/* ── Category chip ── */
.chip {
  display: inline-block;
  background: rgba(79,217,196,0.12);
  border: 1px solid rgba(79,217,196,0.25);
  color: var(--accent);
  border-radius: 20px;
  padding: 3px 12px;
  font-size: 0.7rem;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.06em;
  margin-right: 6px;
}
.chip.purple { background: rgba(123,111,240,0.12); border-color: rgba(123,111,240,0.25); color: var(--accent2); }
.chip.pink   { background: rgba(240,96,144,0.12); border-color: rgba(240,96,144,0.25); color: var(--accent3); }

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
  background: var(--bg-card) !important;
  border: 2px dashed var(--border-glow) !important;
  border-radius: var(--radius) !important;
  padding: 20px !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent) !important; }
[data-testid="stFileUploader"] label { color: var(--text-muted) !important; }

/* ── Streamlit widgets ── */
[data-testid="stSelectbox"] > div,
/* Target actual input only */
input[type="password"], input[type="text"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 8px !important;
  padding: 8px !important;
}

/* Focus state */
input[type="password"]:focus, input[type="text"]:focus {
  border-color: var(--accent) !important;
  outline: none !important;
}
[data-testid="stSelectbox"] > div:focus-within,
[data-testid="stTextInput"] > div > div:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(79,217,196,0.12) !important;
}

/* ── Button ── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent), #38c4b0) !important;
  color: var(--bg) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.02em !important;
  padding: 10px 24px !important;
  transition: opacity 0.15s, transform 0.1s !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Tabs ── */
[data-testid="stTabs"] > div:first-child {
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
button[data-baseweb="tab"] {
  font-family: 'Syne', sans-serif !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  color: var(--text-muted) !important;
  padding: 10px 20px !important;
  border-radius: 0 !important;
  letter-spacing: 0.02em !important;
  border-bottom: 2px solid transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom-color: var(--accent) !important;
  background: transparent !important;
}
[data-testid="stTabsContent"] { padding-top: 24px !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: var(--radius) !important; overflow: hidden !important; }
iframe[title="st_aggrid"] { border: none !important; }

/* ── Sidebar internals ── */
.sidebar-logo {
  display: flex; align-items: center; gap: 12px;
  padding: 8px 0 24px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}
.sidebar-logo-icon {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 800;
  color: var(--bg);
  font-family: 'Syne', sans-serif;
}
.sidebar-section {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin: 20px 0 8px;
}
.sidebar-stat {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 12px;
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  margin-bottom: 6px;
  font-size: 0.8rem;
}
.sidebar-stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--accent);
  font-weight: 500;
}

/* ── Result block ── */
.result-block {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  margin-top: 16px;
}
.result-score {
  font-family: 'Syne', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  color: var(--accent);
  letter-spacing: -0.05em;
  line-height: 1;
}
.result-score-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-top: 4px;
}

/* ── AI output ── */
.ai-output {
  background: linear-gradient(135deg, rgba(79,217,196,0.05), rgba(123,111,240,0.05));
  border: 1px solid rgba(79,217,196,0.2);
  border-radius: var(--radius);
  padding: 24px;
  font-size: 0.9rem;
  line-height: 1.75;
  color: var(--text);
}

/* ── Misc ── */
.stAlert { border-radius: var(--radius-sm) !important; }
.stMarkdown p { color: var(--text); }
.stJson { background: var(--bg-card) !important; border-radius: var(--radius) !important; }
[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Imports (after CSS) ────────────────────────────────────────────────────────
from core.data_loader import DataLoader
from core.profiler import DataProfiler
from core.visualizer import DataVisualizer
from core.insights import InsightEngine
from core.ml_engine import MLEngine
from core.ai_assistant import AIAssistant

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">⬡</div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1rem;letter-spacing:-0.02em;">AutoEDA</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:var(--text-muted);letter-spacing:0.05em;">v2.0 · PRODUCTION</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Upload Dataset</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        st.markdown('<div class="sidebar-section">Dataset Info</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">AI Provider</div>', unsafe_allow_html=True)
    provider = st.selectbox("", ["OpenAI", "Gemini"], label_visibility="collapsed")
    api_key = st.text_input("API Key", type="password", placeholder="sk-••••••••••••••••••••")

    st.markdown("""
    <div style="
        margin-top:40px;
        font-size:0.7rem;
        color:var(--text-dim);
        font-family:'JetBrains Mono',monospace;
        border-top:1px solid var(--border);
        padding-top:12px;
        text-align:center;
    ">
        Built for production · MIT License
    </div>
    """, unsafe_allow_html=True)


# ── Hero bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-bar">
    <div class="hero-logo">⬡</div>
    <div>
        <div class="hero-title">AutoEDA</div>
        <div class="hero-sub">Automated Exploratory Data Analysis · Machine Learning · AI Insights</div>
    </div>
    <div class="hero-badge">● LIVE</div>
</div>
""", unsafe_allow_html=True)

# ── No file state ──────────────────────────────────────────────────────────────
if not uploaded_file:
    st.markdown("""
    <div style="text-align:center;padding:80px 0 60px;">
        <div style="font-size:3.5rem;margin-bottom:20px;">⬡</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                    letter-spacing:-0.03em;margin-bottom:12px;color:var(--text);">
            Drop your dataset. Get instant intelligence.
        </div>
        <div style="color:var(--text-muted);font-size:0.95rem;max-width:480px;margin:0 auto 32px;line-height:1.7;">
            Upload any CSV file to unlock automated profiling, visualizations, rule-based insights,
            ML model training, and AI-powered explanations — all in one pipeline.
        </div>
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
            <span class="chip">📊 Auto Profiling</span>
            <span class="chip purple">🔍 Smart Insights</span>
            <span class="chip pink">🤖 ML Training</span>
            <span class="chip">✨ AI Explanations</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load data ──────────────────────────────────────────────────────────────────
with st.spinner("Loading dataset…"):
    with st.spinner("Loading dataset…"):
        df, info = load_data(uploaded_file)

    profiler = DataProfiler(df)
    column_types = profiler.column_classification()


# ── KPI row ────────────────────────────────────────────────────────────────────
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

# ── Main tabs ──────────────────────────────────────────────────────────────────
tab_data, tab_profile, tab_viz, tab_insights, tab_ml, tab_ai = st.tabs([
    "📋  Data Preview",
    "🔬  Profile",
    "📈  Visualize",
    "💡  Insights",
    "🤖  ML Model",
    "✨  AI Assistant",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Data Preview
# ══════════════════════════════════════════════════════════════════════════════
with tab_data:
    st.markdown('<div class="section-label">Raw Dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Data Preview</div>', unsafe_allow_html=True)

    n_preview = st.select_slider(
        "Rows to preview", options=[5, 10, 25, 50, 100], value=10,
        label_visibility="visible"
    )
    st.dataframe(df.head(n_preview), use_container_width=True, height=380)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-label">Loader Info</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Basic Info</div>', unsafe_allow_html=True)
        st.json(info)
    with c2:
        st.markdown('<div class="section-label">Column Map</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Classification</div>', unsafe_allow_html=True)
        st.json(column_types)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Profiler
# ══════════════════════════════════════════════════════════════════════════════
with tab_profile:
    st.markdown('<div class="section-label">Automated Profiling</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Data Health Report</div>', unsafe_allow_html=True)

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
            <div class="metric-sub">{'⚠️ Consider deduplication' if dup_count > 0 else '✅ Dataset is clean'}</div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("##### Missing Values")
        mv_df = profiler.missing_values()
        st.dataframe(mv_df, use_container_width=True)


        #--------------data quality score-------------    
        missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        duplicate_pct = (profiler.duplicate_rows() / df.shape[0]) * 100

        score = max(0, 100 - int(0.7 * missing_pct + 0.3 * duplicate_pct))

        st.markdown(f"""
        <div class="metric-card"">
            <div class="metric-value">{score}</div>
            <div class="metric-label">Data Quality Score</div>
        </div>
        """, unsafe_allow_html=True)
        

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("##### Summary Statistics")
    st.dataframe(profiler.summary_stats(), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Visualizations
# ══════════════════════════════════════════════════════════════════════════════
with tab_viz:
    if df is None or df.empty:
        st.error("Invalid or empty dataset.")
        st.stop()

    if df.shape[1] == 0:
        st.error("No columns found in dataset.")
        st.stop()
    st.markdown('<div class="section-label">Charts & Graphs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Visual Exploration</div>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

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
                chart_type = st.radio("Chart", ["Histogram", "Violin", "Boxplot"], key="num_chart_type")
            
            with v2:
                if chart_type == "Histogram":
                    fig = visualizer.histogram(selected_num_col)
                    st.markdown(f"##### Histogram — `{selected_num_col}`")
                    st.plotly_chart(fig,use_container_width=True)
                    # st.pyplot(visualizer.histogram(selected_num_col))
                elif chart_type == "Violin":
                    st.markdown("#### Violin Plot")
                    st.plotly_chart(visualizer.violin_plot(selected_num_col))
                elif chart_type == "Boxplot":
                    fig = visualizer.boxplot(selected_num_col)
                    st.markdown(f"##### Boxplot — `{selected_num_col}`")
                    # st.pyplot(visualizer.boxplot(selected_num_col))
                    st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("No numeric columns available for distribution charts.")


        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        if categorical_cols:
            v1, v2 = st.columns([1, 3])
            with v1:
                st.markdown("##### Categorical Distributions \n --- \n")
                selected_cat_col = st.selectbox("Column", categorical_cols, key="cat_col")
                chart_type = st.radio("Chart", ["Bar","pie/donut"],key="cat_chart_type")
            with v2:
                if chart_type == "Bar":
                    st.markdown(f"##### Bar Chart — `{selected_cat_col}`")
                    st.plotly_chart(visualizer.categorical_bar(selected_cat_col), use_container_width=True)
                elif chart_type == "pie/donut":
                    p1 , p2 = st.columns(2)
                    with p1:
                        st.markdown(f"##### Pie Chart — `{selected_cat_col}`")
                        st.plotly_chart(visualizer.pie_chart(selected_cat_col), use_container_width=True)
                    with p2:
                        st.markdown(f"##### Donut Chart — `{selected_cat_col}`")
                        st.plotly_chart(visualizer.donut_chart(selected_cat_col), use_container_width=True)
        else:
            st.info("No categorical columns available for distribution charts.")
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        if categorical_cols and numeric_cols:
            v1, v2 = st.columns([1,3])
            # st.write("Note: For combined categorical-numeric charts, select one column of each type. The visualizer will automatically suggest the best chart based on the data distribution and cardinality.")
            with v1:
                st.markdown("##### Categorical vs Numeical\n --- \n")
                selected_cat_col = st.selectbox("Select Categorical column", categorical_cols)
                selected_num_col = st.selectbox("Select Numeric column", numeric_cols)
                chart_type = st.radio("Chart",['Boxplot','violin','Average Bar'])
            with v2:
                if chart_type == "Boxplot":
                    st.markdown(f"##### Boxplot — `{selected_cat_col}` vs `{selected_num_col}`")
                    st.plotly_chart(visualizer.categorical_vs_numeric_box(selected_cat_col, selected_num_col))
                elif chart_type == "violin":
                    st.markdown(f"##### Violin Plot — `{selected_cat_col}` vs `{selected_num_col}`")
                    st.plotly_chart(visualizer.categorical_vs_numeric_violin(selected_cat_col, selected_num_col))
                elif chart_type == "Average Bar":
                    st.markdown(f"##### Average Bar Chart — `{selected_cat_col}` vs `{selected_num_col}`")
                    st.plotly_chart(visualizer.categorical_mean(selected_cat_col, selected_num_col))
        else:
            st.info("Need at least one numeric and one categorical column for combined charts.")
            

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        if len(numeric_cols) >= 2:
            st.markdown("##### Scatter Plot")
            sc1, sc2= st.columns([1, 3])
            with sc1:
                x_col = st.selectbox("X Axis", numeric_cols, key="x_col")
                y_col = st.selectbox("Y Axis", numeric_cols,
                                     index=min(1, len(numeric_cols)-1), key="y_col")
            
                from utils import helpers  

                auto_hue = helpers.get_best_hue(df,categorical_cols)
                hue_col = st.selectbox(
                    "Color by (optional)",
                    [None] + categorical_cols,
                    index=(categorical_cols.index(auto_hue) + 1) if auto_hue else 0
                )

            with sc2:
                if x_col != y_col:
                    st.markdown(f"`{x_col}` vs `{y_col}`")
                    st.plotly_chart(visualizer.scatter_with_trend(x_col, y_col, hue_col))
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
                    st.plotly_chart(heatmap_fig,use_container_width=True)
                else:
                    st.info("Need at least 2 numeric columns for a correlation heatmap.")


            with h2:
                st.markdown("#### Pair Plot")
                st.pyplot(visualizer.pair_plot())
        else:
            st.info("Not enough numeric columns for correlation analysis.")

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        if len(categorical_cols) >= 2:
            st.markdown("##### Categorical vs Categorical")
            cat1, cat2 = st.columns([1,3])
            with cat1:
                cat_col1 = st.selectbox("X axis", categorical_cols, key="cat_col1")
                cat_col2 = st.selectbox("Y axis", categorical_cols,
                                        index=min(1, len(categorical_cols)-1), key="cat_col2")
                
                chart_type = st.radio("Chart", ["Grouped Bar", "Stacked Bar", "Heatmap"])
            
            with cat2:
                if cat_col1 != cat_col2:
                    if chart_type == "Grouped Bar":
                        st.markdown(f"##### Grouped Bar Chart — `{cat_col1}` vs `{cat_col2}`")
                        st.plotly_chart(visualizer.categorical_vs_categorical_bar(cat_col1,cat_col2))
                    elif chart_type == "Stacked Bar":
                        st.markdown(f"##### Stacked Bar Chart — `{cat_col1}` vs `{cat_col2}`")
                        st.plotly_chart(visualizer.categorical_vs_categorical_stacked(cat_col1,cat_col2))
                    elif chart_type == "Heatmap":
                        st.markdown(f"##### Heatmap - `{cat_col1}` vs `{cat_col2}`")
                        st.plotly_chart(visualizer.categorical_heatmap(cat_col1, cat_col2))
                else:
                    st.info("Please select different Columns for X and Y axis.")
        else:
            st.info("Need at least 2 categorical columns for categorical vs categorical charts.")
# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Insights
# ══════════════════════════════════════════════════════════════════════════════
with tab_insights:
    st.markdown('<div class="section-label">Rule-Based Engine</div>', unsafe_allow_html=True)
    
    with st.spinner("Generating insights…"):
        if "insights" not in st.session_state:
            with st.spinner("Generating insights…"):
                engine = InsightEngine(df)
                st.session_state["insights"] = engine.generate_all_insights()

        insights = st.session_state["insights"]

    # Color map for insight categories
    category_colors = {
        "missing":    ("warn",  "⚠️"),
        "outlier":    ("error", "🔴"),
        "skewness":   ("warn",  "📐"),
        "correlation":("ok",    "🔗"),
        "cardinality":("warn",  "🎯"),
        "duplicate":  ("error", "🔁"),
    }

    total_insights = sum(len(v) for v in insights.values())
    st.markdown(f"""
    <div style="display:flex;gap:12px;align-items:center;margin-bottom:20px;">
        <span style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--accent);">
            {total_insights}
        </span>
        <span style="color:var(--text-muted);font-size:0.9rem;">insights discovered across {len(insights)} categories</span>
    </div>
    """, unsafe_allow_html=True)

    for category, items in insights.items():
        dot_class, emoji = category_colors.get(category, ("ok", "📌"))
        with st.expander(f"{emoji}  {category.replace('_',' ').title()}  ({len(items)} findings)", expanded=True):
            if items:
                for item in items:
                    st.markdown(f"""
                    <div class="insight-item {dot_class}">
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

    report = f"""
    AutoEDA Report

    Rows: {df.shape[0]}
    Columns: {df.shape[1]}

    Insights:
    {insights}
    """

    st.download_button(
        "Download Report",
        report,
        file_name="eda_report.txt"
)
        
# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — ML Model
# ══════════════════════════════════════════════════════════════════════════════
with tab_ml:
    st.markdown('<div class="section-label">AutoML Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Train a Model</div>', unsafe_allow_html=True)

    ml1, ml2 = st.columns([1, 2])
    with ml1:
        st.markdown("**Select target column**")
        target_column = st.selectbox("Target", df.columns, label_visibility="collapsed")
        train_btn = st.button("🚀  Train Model", use_container_width=True)

    with ml2:
        st.markdown("""
        <div class="card" style="color:var(--text-muted);font-size:0.85rem;line-height:1.7;">
            AutoEDA will automatically detect whether to run a
            <strong style="color:var(--accent)">Regression</strong> or
            <strong style="color:var(--accent2)">Classification</strong> pipeline
            based on your target column, then train, evaluate, and report results instantly.
        </div>
        """, unsafe_allow_html=True)

    if train_btn:
        if df[target_column].nunique() < 2:
            st.warning("Target column must have at least 2 unique values")
        else:
            with st.spinner("Training model — this may take a moment…"):
                ml_engine = MLEngine(df, target_column)
                results = ml_engine.train()

            model_type = results.get("type", "unknown")
            badge_color = "var(--accent)" if model_type == "regression" else "var(--accent2)"

            st.markdown(f"""
            <div class="result-block">
                <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;">
                    <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;">Model trained</span>
                    <span class="chip {'purple' if model_type != 'regression' else ''}">
                        {model_type.upper()}
                    </span>
                </div>
            """, unsafe_allow_html=True)

            if model_type == "regression":
                ra, rb = st.columns(2)
                ra.markdown(f"""
                <div class="metric-card">
                    <div class="result-score" style="color:var(--accent);">{results['r2']:.4f}</div>
                    <div class="result-score-label">R² Score</div>
                </div>
                """, unsafe_allow_html=True)
                rb.markdown(f"""
                <div class="metric-card">
                    <div class="result-score" style="color:var(--accent3);">{results['mse']:.4f}</div>
                    <div class="result-score-label">Mean Squared Error</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card" style="text-align:left;margin-bottom:16px;">
                    <div class="result-score" style="color:var(--accent2);">{results['accuracy']:.4f}</div>
                    <div class="result-score-label">Accuracy Score</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("**Classification Report**")
                st.code(results["report"], language="text")

            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — AI Assistant
# ══════════════════════════════════════════════════════════════════════════════
with tab_ai:
    st.markdown('<div class="section-label">Powered by LLMs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Insight Assistant</div>', unsafe_allow_html=True)

    ai1, ai2 = st.columns([1, 2])

    with ai1:
        st.markdown("""
        <div class="card" style="font-size:0.85rem;line-height:1.7;color:var(--text-muted);">
            The AI assistant reads all rule-based insights discovered in your dataset and generates
            a natural-language explanation, actionable recommendations, and data quality score.
        </div>
        """, unsafe_allow_html=True)

        current_provider = st.session_state.get("ai_provider_label", provider)
        st.markdown(f"""
        <div class="sidebar-stat" style="margin-top:8px;">
            <span>Provider</span>
            <span class="sidebar-stat-val">{provider}</span>
        </div>
        <div class="sidebar-stat">
            <span>API Key</span>
            <span class="sidebar-stat-val">{'✅ Set' if api_key else '❌ Missing'}</span>
        </div>
        """, unsafe_allow_html=True)

        gen_btn = st.button("✨  Generate AI Insights", use_container_width=True)

    with ai2:
        if gen_btn:
            if not api_key or api_key.strip() == "":
                st.warning("⚠️  Please enter a valid API key in the sidebar.")
            else:
                with st.spinner(f"Consulting {provider}…"):
                    # Re-generate insights if not already done
                    all_insights = st.session_state.get("insights")

                    if not all_insights:
                        engine = InsightEngine(df)
                        all_insights = engine.generate_all_insights()

                    assistant = AIAssistant(provider, api_key.strip())
                    ai_output = assistant.generate_summary(all_insights)

                st.markdown(f"""
                <div class="ai-output">
                    {ai_output.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:40px 0;color:var(--text-dim);">
                <div style="font-size:2.5rem;margin-bottom:12px;">✨</div>
                <div style="font-size:0.9rem;">Click "Generate AI Insights" to get an LLM-powered<br>
                analysis of your dataset's characteristics.</div>
            </div>
            """, unsafe_allow_html=True)