import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Data Analysis",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── IPL Color Theme ──────────────────────────────────────────────────────────
TEAM_COLORS = {
    "CSK":  "#F9CD1B",
    "MI":   "#004BA0",
    "RCB":  "#EC1C24",
    "KKR":  "#3A225D",
    "DC":   "#0078BC",
    "PBKS": "#ED1B24",
    "RR":   "#FF1744",
    "SRH":  "#FF6600",
    "GT":   "#1C1C6B",
    "LSG":  "#00B2A9",
}

IPL_COLORS = ["#F9CD1B", "#EC1C24", "#004BA0", "#FF6600",
              "#3A225D", "#00B2A9", "#1C1C6B", "#FF1744", "#0078BC", "#ED1B24"]

# ─── CSS Styling ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0d1a3a 100%);
    color: #ffffff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0a2e 0%, #0d1a3a 100%);
    border-right: 2px solid #F9CD1B;
}
[data-testid="stSidebar"] * { color: #ffffff !important; }

/* Title banner */
.ipl-title {
    background: linear-gradient(90deg, #F9CD1B, #FF6600, #EC1C24, #F9CD1B);
    background-size: 300% 300%;
    animation: gradientShift 3s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    letter-spacing: 3px;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, rgba(249,205,27,0.15), rgba(236,28,36,0.1));
    border: 1px solid rgba(249,205,27,0.4);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(249,205,27,0.3);
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #F9CD1B;
}
.metric-label {
    font-size: 0.85rem;
    color: #aaaacc;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Section headers */
.section-header {
    background: linear-gradient(90deg, #F9CD1B22, transparent);
    border-left: 4px solid #F9CD1B;
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    font-size: 1.3rem;
    font-weight: 700;
    color: #F9CD1B;
    margin: 20px 0 12px 0;
}

/* Streamlit widget labels */
label, .stSelectbox label, .stTextInput label {
    color: #F9CD1B !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #F9CD1B, #FF6600);
    color: #0a0a1a;
    font-weight: 800;
    border: none;
    border-radius: 25px;
    padding: 10px 30px;
    font-size: 1rem;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(249,205,27,0.5);
}

/* Divider */
hr { border-color: #F9CD1B44; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* Radio buttons */
.stRadio > div { gap: 8px; }

/* Footer */
.footer {
    margin-top: 60px;
    padding: 30px 20px;
    background: linear-gradient(135deg, rgba(249,205,27,0.08), rgba(236,28,36,0.08));
    border-top: 2px solid #F9CD1B44;
    border-radius: 16px;
    text-align: center;
}
.footer-name {
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #F9CD1B, #FF6600);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
}
.footer-title {
    color: #aaaacc;
    font-size: 0.85rem;
    margin-bottom: 18px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.footer-links {
    display: flex;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}
.footer-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    border-radius: 25px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    border: 1px solid;
}
.footer-link:hover { transform: translateY(-2px); }
.link-linkedin { background: rgba(10,102,194,0.2); border-color: #0A66C2; color: #0A66C2 !important; }
.link-github   { background: rgba(255,255,255,0.08); border-color: #ffffff88; color: #ffffff !important; }
.link-instagram{ background: rgba(225,48,108,0.2); border-color: #E1306C; color: #E1306C !important; }
.link-email    { background: rgba(249,205,27,0.15); border-color: #F9CD1B; color: #F9CD1B !important; }
.footer-copy {
    color: #555577;
    font-size: 0.78rem;
    margin-top: 12px;
}

/* Sidebar profile card */
.sidebar-profile {
    background: linear-gradient(135deg, rgba(249,205,27,0.1), rgba(236,28,36,0.08));
    border: 1px solid rgba(249,205,27,0.3);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    margin-top: 8px;
}
.sidebar-name {
    font-weight: 800;
    font-size: 1rem;
    color: #F9CD1B;
    margin-bottom: 10px;
}
.sidebar-icon-links {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}
.sidebar-icon-links a {
    font-size: 0.78rem;
    padding: 4px 10px;
    border-radius: 20px;
    text-decoration: none;
    font-weight: 600;
    border: 1px solid;
}
</style>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    m = pd.read_csv(os.path.join(base, "data", "matches.csv"))
    d = pd.read_csv(os.path.join(base, "data", "deliveries.csv"))
    m['Winning_team'] = m['Winning_team'].str.strip()
    m['Team1']        = m['Team1'].str.strip()
    m['Team2']        = m['Team2'].str.strip()
    d['total_runs']   = d['runs_of_bat'] + d['extras']
    return m, d

matches, deliveries = load_data()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏏 IPL ANALYSIS")
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Home",
        "🏆 Team Analysis",
        "🏏 Player Analysis",
        "🎳 Bowler Analysis",
        "🏟️ Venue Analysis",
        "📅 Season Analysis",
        "🎲 Toss Analysis",
        "💯 Highest Scores",
        "🤝 Top Partnerships",
    ])
    st.markdown("---")
    st.markdown(f"**📊 Dataset Info**")
    st.markdown(f"Matches: **{len(matches)}**")
    st.markdown(f"Deliveries: **{len(deliveries):,}**")
    st.markdown(f"Season: **{deliveries['season'].iloc[0]}**")
    st.markdown("---")
    st.markdown("""
    <div class="sidebar-profile">
        <div class="sidebar-name">👩‍💻 Charchika Roul</div>
        <div class="sidebar-icon-links">
            <a href="https://www.linkedin.com/in/charchika-roul-1b3674276" target="_blank"
               style="background:rgba(10,102,194,0.2);border-color:#0A66C2;color:#0A66C2;">
               💼 LinkedIn
            </a>
            <a href="https://github.com/CharchikaRoul" target="_blank"
               style="background:rgba(255,255,255,0.08);border-color:#fff8;color:#fff;">
               🐙 GitHub
            </a>
            <a href="https://www.instagram.com/arp1856?igsh=c256bnplNHo1MmV1" target="_blank"
               style="background:rgba(225,48,108,0.2);border-color:#E1306C;color:#E1306C;">
               📸 Instagram
            </a>
            <a href="mailto:charchikaroul7@gmail.com"
               style="background:rgba(249,205,27,0.15);border-color:#F9CD1B;color:#F9CD1B;">
               📧 Email
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
def show_footer():
    st.markdown("""
    <div class="footer">
        <div class="footer-name">Charchika Roul</div>
        <div class="footer-title">Data Analyst &nbsp;|&nbsp; Python Developer &nbsp;|&nbsp; IPL Enthusiast 🏏</div>
        <div class="footer-links">
            <a class="footer-link link-linkedin"
               href="https://www.linkedin.com/in/charchika-roul-1b3674276" target="_blank">
               💼 LinkedIn
            </a>
            <a class="footer-link link-github"
               href="https://github.com/CharchikaRoul" target="_blank">
               🐙 GitHub
            </a>
            <a class="footer-link link-instagram"
               href="https://www.instagram.com/arp1856?igsh=c256bnplNHo1MmV1" target="_blank">
               📸 Instagram
            </a>
            <a class="footer-link link-email"
               href="mailto:charchikaroul7@gmail.com">
               📧 charchikaroul7@gmail.com
            </a>
        </div>
        <div class="footer-copy">© 2024 Charchika Roul · Built with 🏏 Python & Streamlit · IPL Data Analysis System</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Helper ───────────────────────────────────────────────────────────────────
def metric_card(label, value):
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>"""

def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def ipl_bar(df, x, y, title, color=None):
    fig = px.bar(df, x=x, y=y, title=title,
                 color=color or y,
                 color_continuous_scale=["#EC1C24","#FF6600","#F9CD1B"],
                 template="plotly_dark")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(color="#F9CD1B", size=16),
        font_color="#ffffff",
        showlegend=False,
    )
    fig.update_traces(marker_line_width=0)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown('<div class="ipl-title">🏏 IPL DATA ANALYSIS SYSTEM 🏆</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aaa;font-size:1.1rem'>Powered by Python & Streamlit</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Top KPI cards
    total_runs   = int(deliveries['runs_of_bat'].sum())
    total_wkts   = deliveries['wicket_type'].notna().sum()
    top_scorer   = deliveries.groupby('striker')['runs_of_bat'].sum().idxmax()
    top_wkt      = deliveries[deliveries['wicket_type'].isin(['caught','bowled','lbw','stumped'])].groupby('bowler')['wicket_type'].count().idxmax()

    cols = st.columns(4)
    cards = [
        ("Total Matches", len(matches)),
        ("Total Runs", f"{total_runs:,}"),
        ("Total Wickets", f"{total_wkts:,}"),
        ("Top Scorer", top_scorer),
    ]
    for col, (label, val) in zip(cols, cards):
        col.markdown(metric_card(label, val), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section("🏆 Team Win Count")
        wins = matches['Winning_team'].value_counts().reset_index()
        wins.columns = ['Team', 'Wins']
        wins['Color'] = wins['Team'].map(TEAM_COLORS).fillna("#F9CD1B")
        fig = go.Figure(go.Bar(
            x=wins['Team'], y=wins['Wins'],
            marker_color=wins['Color'],
            text=wins['Wins'], textposition='outside',
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#fff", title_font_color="#F9CD1B", showlegend=False,
                          yaxis=dict(gridcolor="#333"), xaxis=dict(tickangle=-30))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("🏏 Top 8 Run Scorers")
        top8 = deliveries.groupby('striker')['runs_of_bat'].sum().sort_values(ascending=False).head(8).reset_index()
        top8.columns = ['Player', 'Runs']
        fig = ipl_bar(top8, 'Player', 'Runs', '')
        fig.update_layout(xaxis=dict(tickangle=-30))
        st.plotly_chart(fig, use_container_width=True)

    # Pie chart
    section("🥧 Win Share by Team")
    wins_pie = matches['Winning_team'].value_counts()
    fig = go.Figure(go.Pie(
        labels=wins_pie.index, values=wins_pie.values,
        marker_colors=[TEAM_COLORS.get(t, "#F9CD1B") for t in wins_pie.index],
        hole=0.45,
        textinfo='label+percent',
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#fff", showlegend=True,
                      legend=dict(font=dict(color="#fff")))
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TEAM ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Team Analysis":
    st.markdown('<div class="ipl-title">🏆 TEAM ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("---")

    wins  = matches['Winning_team'].value_counts()
    total = pd.concat([matches['Team1'], matches['Team2']]).value_counts()
    df = pd.DataFrame({'Matches': total, 'Wins': wins}).fillna(0)
    df['Losses']  = df['Matches'] - df['Wins']
    df['Win %']   = (df['Wins'] / df['Matches'] * 100).round(1)
    df = df.sort_values('Wins', ascending=False).astype({'Wins': int, 'Losses': int, 'Matches': int})
    df.index.name = 'Team'
    df = df.reset_index()

    col1, col2 = st.columns(2)
    with col1:
        section("📊 Wins vs Losses")
        fig = go.Figure()
        colors_list = [TEAM_COLORS.get(t, "#F9CD1B") for t in df['Team']]
        fig.add_trace(go.Bar(name='Wins',   x=df['Team'], y=df['Wins'],   marker_color=colors_list))
        fig.add_trace(go.Bar(name='Losses', x=df['Team'], y=df['Losses'], marker_color='#333355'))
        fig.update_layout(barmode='group', paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", font_color="#fff",
                          legend=dict(font=dict(color="#fff")),
                          xaxis=dict(tickangle=-30, gridcolor="#333"),
                          yaxis=dict(gridcolor="#333"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("🎯 Win Percentage")
        fig = px.bar(df.sort_values('Win %', ascending=True),
                     x='Win %', y='Team', orientation='h',
                     color='Win %', color_continuous_scale=["#EC1C24","#FF6600","#F9CD1B"],
                     template="plotly_dark", text='Win %')
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#fff", yaxis=dict(gridcolor="#333"), showlegend=False)
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    section("📋 Full Team Stats Table")
    df['Win %'] = df['Win %'].astype(str) + '%'
    st.dataframe(df, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PLAYER ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏏 Player Analysis":
    st.markdown('<div class="ipl-title">🏏 PLAYER ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("---")

    all_players = sorted(deliveries['striker'].unique())
    player = st.selectbox("🔍 Select or type a player name:", all_players)

    if player:
        bat = deliveries[deliveries['striker'] == player]
        innings_runs = bat.groupby(['match_id', 'innings'])['runs_of_bat'].sum()

        total_runs    = int(bat['runs_of_bat'].sum())
        total_balls   = int(bat['runs_of_bat'].count())
        matches_played= bat['match_id'].nunique()
        fours         = int((bat['runs_of_bat'] == 4).sum())
        sixes         = int((bat['runs_of_bat'] == 6).sum())
        hundreds      = int((innings_runs >= 100).sum())
        fifties       = int(((innings_runs >= 50) & (innings_runs < 100)).sum())
        highest       = int(innings_runs.max())
        dismissed     = deliveries[
            deliveries['player_dismissed'].str.lower() == player.lower()
        ]['match_id'].nunique()
        average     = round(total_runs / dismissed, 2) if dismissed > 0 else total_runs
        strike_rate = round((total_runs / total_balls) * 100, 2) if total_balls > 0 else 0

        st.markdown(f"### 🏏 Stats for **{player}**")

        # KPI Row 1
        cols = st.columns(4)
        for col, (lbl, val) in zip(cols, [
            ("Matches", matches_played), ("Runs", total_runs),
            ("Highest", highest),        ("Average", average)
        ]):
            col.markdown(metric_card(lbl, val), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # KPI Row 2
        cols2 = st.columns(4)
        for col, (lbl, val) in zip(cols2, [
            ("Strike Rate", strike_rate), ("100s", hundreds),
            ("50s", fifties),             ("4s / 6s", f"{fours} / {sixes}")
        ]):
            col.markdown(metric_card(lbl, val), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            section("📈 Innings-by-Innings Scores")
            inn_df = innings_runs.reset_index()
            inn_df.columns = ['match_id', 'innings', 'Runs']
            inn_df['Match #'] = range(1, len(inn_df) + 1)
            fig = px.bar(inn_df, x='Match #', y='Runs', color='Runs',
                         color_continuous_scale=["#333","#FF6600","#F9CD1B"],
                         template="plotly_dark")
            fig.add_hline(y=50, line_dash="dot", line_color="#F9CD1B", annotation_text="50")
            fig.add_hline(y=100, line_dash="dot", line_color="#EC1C24", annotation_text="100")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#fff", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            section("🥊 Boundary Breakdown")
            fig = go.Figure(go.Pie(
                labels=['Fours', 'Sixes', 'Other Runs'],
                values=[fours * 4, sixes * 6, total_runs - fours*4 - sixes*6],
                marker_colors=["#F9CD1B", "#EC1C24", "#004BA0"],
                hole=0.4, textinfo='label+percent'
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#fff")
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# BOWLER ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎳 Bowler Analysis":
    st.markdown('<div class="ipl-title">🎳 BOWLER ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("---")

    all_bowlers = sorted(deliveries['bowler'].unique())
    bowler = st.selectbox("🔍 Select a bowler:", all_bowlers)

    if bowler:
        bowl = deliveries[deliveries['bowler'] == bowler]
        legal = bowl[(bowl['wide'] == 0) & (bowl['noballs'] == 0)]
        overs = round(len(legal) / 6, 1)
        wicket_types = ['caught','bowled','lbw','stumped','caught and bowled','hit wicket']
        wickets    = int(bowl[bowl['wicket_type'].isin(wicket_types)].shape[0])
        runs_given = int(bowl['runs_of_bat'].sum() + bowl['wide'].sum() + bowl['noballs'].sum())
        economy    = round(runs_given / overs, 2) if overs > 0 else 0
        average    = round(runs_given / wickets, 2) if wickets > 0 else 0
        matches_b  = bowl['match_id'].nunique()

        per_match  = bowl[bowl['wicket_type'].isin(wicket_types)].groupby('match_id')['wicket_type'].count()
        best_wkts  = int(per_match.max()) if not per_match.empty else 0
        best_runs  = int(bowl[bowl['match_id'] == per_match.idxmax()]['runs_of_bat'].sum()) if not per_match.empty else 0

        st.markdown(f"### 🎳 Stats for **{bowler}**")

        cols = st.columns(4)
        for col, (lbl, val) in zip(cols, [
            ("Matches", matches_b), ("Overs", overs),
            ("Wickets", wickets),   ("Runs Given", runs_given)
        ]):
            col.markdown(metric_card(lbl, val), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        cols2 = st.columns(3)
        for col, (lbl, val) in zip(cols2, [
            ("Economy", economy), ("Average", average), ("Best", f"{best_wkts}/{best_runs}")
        ]):
            col.markdown(metric_card(lbl, val), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            section("📊 Wickets per Match")
            wpm = per_match.reset_index()
            wpm.columns = ['match_id', 'Wickets']
            wpm['Match #'] = range(1, len(wpm) + 1)
            fig = px.bar(wpm, x='Match #', y='Wickets', color='Wickets',
                         color_continuous_scale=["#004BA0","#FF6600","#EC1C24"],
                         template="plotly_dark")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#fff", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            section("🎯 Dismissal Types")
            dismissals = bowl[bowl['wicket_type'].isin(wicket_types)]['wicket_type'].value_counts()
            fig = go.Figure(go.Pie(
                labels=dismissals.index, values=dismissals.values,
                marker_colors=IPL_COLORS, hole=0.4, textinfo='label+percent'
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#fff")
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# VENUE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏟️ Venue Analysis":
    st.markdown('<div class="ipl-title">🏟️ VENUE ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("---")

    venue_matches = matches['Venue'].value_counts().reset_index()
    venue_matches.columns = ['Venue', 'Matches']
    venue_matches['Short'] = venue_matches['Venue'].str.split(',').str[0]

    col1, col2 = st.columns(2)
    with col1:
        section("🏟️ Matches per Venue")
        fig = px.bar(venue_matches, x='Matches', y='Short', orientation='h',
                     color='Matches', color_continuous_scale=["#EC1C24","#FF6600","#F9CD1B"],
                     template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#fff", showlegend=False,
                          yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("💥 Runs Scored at Each Venue")
        runs_venue = deliveries.groupby('venue')['runs_of_bat'].sum().sort_values(ascending=False).head(10).reset_index()
        runs_venue.columns = ['Venue', 'Runs']
        runs_venue['Short'] = runs_venue['Venue'].str.split(',').str[0]
        fig = ipl_bar(runs_venue, 'Short', 'Runs', '')
        fig.update_layout(xaxis=dict(tickangle=-30))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SEASON ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📅 Season Analysis":
    st.markdown('<div class="ipl-title">📅 SEASON ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("---")

    total_runs = int(deliveries['runs_of_bat'].sum())
    total_wkts = deliveries['wicket_type'].notna().sum()

    cols = st.columns(3)
    for col, (lbl, val) in zip(cols, [
        ("Total Matches", len(matches)),
        ("Total Runs", f"{total_runs:,}"),
        ("Total Wickets", f"{total_wkts:,}")
    ]):
        col.markdown(metric_card(lbl, val), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section("🏏 Top 10 Run Scorers")
        top10 = deliveries.groupby('striker')['runs_of_bat'].sum().sort_values(ascending=False).head(10).reset_index()
        top10.columns = ['Player', 'Runs']
        fig = ipl_bar(top10, 'Player', 'Runs', '')
        fig.update_layout(xaxis=dict(tickangle=-30))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("🎳 Top 10 Wicket Takers")
        wkt_types = ['caught','bowled','lbw','stumped','caught and bowled','hit wicket']
        top_bowlers = (deliveries[deliveries['wicket_type'].isin(wkt_types)]
                       .groupby('bowler')['wicket_type'].count()
                       .sort_values(ascending=False).head(10).reset_index())
        top_bowlers.columns = ['Bowler', 'Wickets']
        fig = px.bar(top_bowlers, x='Bowler', y='Wickets', color='Wickets',
                     color_continuous_scale=["#004BA0","#FF6600","#EC1C24"],
                     template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#fff", showlegend=False,
                          xaxis=dict(tickangle=-30))
        st.plotly_chart(fig, use_container_width=True)

    section("📋 Player of the Match Leaderboard")
    potm = matches['Player_of_match'].value_counts().head(10).reset_index()
    potm.columns = ['Player', 'Awards']
    st.dataframe(potm, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOSS ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎲 Toss Analysis":
    st.markdown('<div class="ipl-title">🎲 TOSS ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("---")

    wins_as_t1 = matches[matches['Winning_team'] == matches['Team1']].shape[0]
    wins_as_t2 = matches[matches['Winning_team'] == matches['Team2']].shape[0]
    total      = len(matches)

    cols = st.columns(3)
    for col, (lbl, val) in zip(cols, [
        ("Total Matches", total),
        ("Team1 Wins", f"{wins_as_t1} ({round(wins_as_t1/total*100,1)}%)"),
        ("Team2 Wins", f"{wins_as_t2} ({round(wins_as_t2/total*100,1)}%)")
    ]):
        col.markdown(metric_card(lbl, val), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section("🏆 Wins per Team")
        wins = matches['Winning_team'].value_counts().reset_index()
        wins.columns = ['Team', 'Wins']
        wins['Color'] = wins['Team'].map(TEAM_COLORS).fillna("#F9CD1B")
        fig = go.Figure(go.Bar(
            x=wins['Team'], y=wins['Wins'],
            marker_color=wins['Color'],
            text=wins['Wins'], textposition='outside'
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#fff", showlegend=False,
                          xaxis=dict(tickangle=-30), yaxis=dict(gridcolor="#333"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("🥧 Home vs Away Wins")
        fig = go.Figure(go.Pie(
            labels=['Team1 (Home) Wins', 'Team2 (Away) Wins'],
            values=[wins_as_t1, wins_as_t2],
            marker_colors=["#F9CD1B", "#EC1C24"],
            hole=0.45, textinfo='label+percent'
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#fff")
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# HIGHEST SCORES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💯 Highest Scores":
    st.markdown('<div class="ipl-title">💯 HIGHEST INDIVIDUAL SCORES</div>', unsafe_allow_html=True)
    st.markdown("---")

    scores = deliveries.groupby(['match_id', 'striker'])['runs_of_bat'].sum().reset_index()
    scores = scores.sort_values('runs_of_bat', ascending=False).head(20)
    scores.columns = ['Match ID', 'Player', 'Runs']
    scores = scores.reset_index(drop=True)
    scores.index += 1

    col1, col2 = st.columns(2)
    with col1:
        section("🏅 Top 15 Individual Innings")
        top15 = scores.head(15)
        fig = px.bar(top15, x='Player', y='Runs', color='Runs',
                     color_continuous_scale=["#004BA0","#FF6600","#F9CD1B"],
                     template="plotly_dark", text='Runs')
        fig.add_hline(y=100, line_dash="dash", line_color="#EC1C24", annotation_text="Century Line")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#fff", showlegend=False,
                          xaxis=dict(tickangle=-30))
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("📋 Top 20 Scores Table")
        st.dataframe(scores[['Player','Runs']].head(20), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOP PARTNERSHIPS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🤝 Top Partnerships":
    st.markdown('<div class="ipl-title">🤝 TOP PARTNERSHIPS</div>', unsafe_allow_html=True)
    st.markdown("---")

    team_innings = (deliveries.groupby(['match_id','innings','batting_team'])['runs_of_bat']
                    .sum().reset_index()
                    .sort_values('runs_of_bat', ascending=False).head(15))
    team_innings.columns = ['Match ID', 'Innings', 'Team', 'Runs']
    team_innings = team_innings.reset_index(drop=True)
    team_innings.index += 1

    col1, col2 = st.columns(2)
    with col1:
        section("💥 Highest Team Innings Totals")
        team_innings['Color'] = team_innings['Team'].map(TEAM_COLORS).fillna("#F9CD1B")
        fig = go.Figure(go.Bar(
            x=team_innings['Team'], y=team_innings['Runs'],
            marker_color=team_innings['Color'],
            text=team_innings['Runs'], textposition='outside'
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#fff", showlegend=False,
                          xaxis=dict(tickangle=-30), yaxis=dict(gridcolor="#333"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("📋 Top Innings Table")
        st.dataframe(team_innings[['Team','Innings','Runs']], use_container_width=True)

    section("📊 Average Runs by Team per Innings")
    avg_runs = (deliveries.groupby(['match_id','innings','batting_team'])['runs_of_bat']
                .sum().reset_index()
                .groupby('batting_team')['runs_of_bat'].mean()
                .sort_values(ascending=False).reset_index())
    avg_runs.columns = ['Team', 'Avg Runs']
    avg_runs['Color'] = avg_runs['Team'].map(TEAM_COLORS).fillna("#F9CD1B")
    fig = go.Figure(go.Bar(
        x=avg_runs['Team'], y=avg_runs['Avg Runs'].round(1),
        marker_color=avg_runs['Color'],
        text=avg_runs['Avg Runs'].round(1), textposition='outside'
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#fff", showlegend=False,
                      xaxis=dict(tickangle=-30), yaxis=dict(gridcolor="#333"))
    st.plotly_chart(fig, use_container_width=True)

# ─── Footer (shown on every page) ─────────────────────────────────────────────
show_footer()
