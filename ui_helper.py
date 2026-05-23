import streamlit as st

def load_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

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

.wordmark {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.3rem;
    font-weight: 600;
    color: #f8fafc;
    letter-spacing: -0.02em;
}

.wordmark span { color: #00f5ff; }

.version-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #334155;
    letter-spacing: 0.12em;
}

.section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 6px;
}
.section-title {
  font-family: IBM Plex Mono;
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
  font-family: 'IBM Plex Mono', monospace;
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

            
.chip-card {
    background: #111318;
    border: 1px solid #1e2330;
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
            
.chip {
  display: inline-block;
  background: rgba(79,217,196,0.12);
  border: 1px solid rgba(79,217,196,0.25);
  color: var(--accent);
  border-radius: 10px;
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
  margin: 6px 0 12px;
  font-size: 0.8rem;
}
.sidebar-stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--accent);
  font-weight: 500;
}

.result-block {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  margin-top: 16px;
}
.result-score {
  font-family: IBM Plex Mono;
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

