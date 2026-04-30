import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="donk Dashboard",
    page_icon="🎯",
    layout="wide"
)
st.markdown("""
<style>
.stApp {
    background-image: url("https://www.hltv.org/img/static/team/logo/7020");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.85);
    z-index: 0;
}

.main > div {
    position: relative;
    z-index: 1;
}
section[data-testid="stSidebar"] {
    background-color: #111111;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/donk_stats.csv", skiprows=2)
    df.columns = ["Result", "Event", "Team", "Maps", "KPR_DPR", "plus_minus", "Rating"]
    df[["KPR", "DPR"]] = df["KPR_DPR"].str.split(" - ", expand=True).astype(float)
    df = df.drop(columns=["KPR_DPR"])
    df["Rating"] = df["Rating"].astype(str).str.replace("*", "", regex=False).astype(float)
    df["Maps"] = pd.to_numeric(df["Maps"], errors="coerce")
    df["Era"] = df["Team"].apply(lambda x: "Spirit" if x == "Spirit" else "Spirit Academy / Other")
    df["Won"] = df["Result"].str.strip() == "1st"
    return df

df = cargar_datos()

st.title("🎯 donk — The Best Player in the World")
st.markdown("Complete analysis of Danil 'donk' Kryshkovets in the CS2 professional circuit")
st.divider()

col_foto, col_bio = st.columns([1, 3])

with col_foto:
    st.image("assets/donk.png", width=350)

with col_bio:
    st.markdown("### Danil 'donk' Kryshkovets")
    st.markdown("""
    🇷🇺 **Born:** July 10, 2006 — Novosibirsk, Russia  
    🏅 **Team:** Team Spirit  
    🎮 **Role:** Rifler / Entry  
    ⭐ **Peak Ranking:** #1 in the world (2024)  
    
    donk burst onto the professional CS2 scene in late 2023 and quickly established himself 
    as the most dominant player in the world. Known for his exceptional aim, consistency, 
    and clutch performances, he became the face of Team Spirit's era of dominance.
    """)

st.divider()

df_spirit = df[df["Team"] == "Spirit"].copy()

col1, col2, col3, col4, col5 = st.columns(5)
...

df_filtrado = df[df["Team"] == "Spirit"].copy()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Avg Rating", f"{df_filtrado['Rating'].mean():.2f}")
col2.metric("Tournaments Played", len(df_filtrado))
col3.metric("Tournaments Won", df_filtrado["Won"].sum())
col4.metric("Maps Played", int(df_filtrado["Maps"].sum()))
col5.metric("Avg KPR", f"{df_filtrado['KPR'].mean():.2f}")



st.divider()

st.sidebar.title("🔍 Filters")
tournament_type = st.sidebar.selectbox(
    "Tournament Type",
    ["All Tournaments", "Majors Only", "IEM Only", "BLAST Only"]
)
years = ["All Years"] + sorted(df_spirit["Event"].str.extract(r"(\d{4})")[0].dropna().unique().tolist(), reverse=True)
selected_year = st.sidebar.selectbox("Year", years)

def filtrar_torneos(df, tipo):
    if tipo == "Majors Only":
        return df[df["Event"].str.contains("Major", case=False)]
    elif tipo == "IEM Only":
        return df[df["Event"].str.contains("IEM", case=False)]
    elif tipo == "BLAST Only":
        return df[df["Event"].str.contains("BLAST", case=False)]
    return df

df_filtrado = filtrar_torneos(df_spirit, tournament_type)
if selected_year != "All Years":
    df_filtrado = df_filtrado[df_filtrado["Event"].str.contains(selected_year)]
df_plot = df_filtrado.iloc[::-1].reset_index(drop=True)
df_plot["#"] = range(1, len(df_plot) + 1)



df_plot = df_filtrado.iloc[::-1].reset_index(drop=True)
df_plot["#"] = range(1, len(df_plot) + 1)

st.subheader("📈 Rating 2.0 per Tournament")
fig_rating = px.line(
    df_plot,
    x="#",
    y="Rating",
    hover_name="Event",
    markers=True,
    color_discrete_sequence=["#FF4B4B"]
)
fig_rating.add_hline(y=1.0, line_dash="dash", line_color="gray", annotation_text="Rating 1.0 (average)")
fig_rating.update_layout(
    xaxis_title="Tournament (chronological)",
    yaxis_title="Rating 2.0",
    height=400
)
st.plotly_chart(fig_rating, use_container_width=True)

st.divider()

st.subheader("⚔️ Kill Difference per Tournament")
fig_pm = px.bar(
    df_plot,
    x="#",
    y="plus_minus",
    hover_name="Event",
    color="plus_minus",
    color_continuous_scale=["#FF4B4B", "#00CC44"],
    color_continuous_midpoint=0
)
fig_pm.update_layout(
    xaxis_title="Tournament (chronological)",
    yaxis_title="+/-",
    height=350,
    showlegend=False
)
st.plotly_chart(fig_pm, use_container_width=True)

st.divider()

st.subheader("🏆 Tournaments Won with Spirit")
won = df_filtrado[df_filtrado["Won"]][["Event", "Maps", "Rating", "plus_minus"]].reset_index(drop=True)
won.index += 1
st.dataframe(won, use_container_width=True)

st.divider()

st.subheader("🎯 KPR vs DPR per Tournament")
fig_kd = go.Figure()
fig_kd.add_trace(go.Scatter(x=df_plot["#"], y=df_plot["KPR"], name="KPR", line=dict(color="#FF4B4B"), mode="lines+markers"))
fig_kd.add_trace(go.Scatter(x=df_plot["#"], y=df_plot["DPR"], name="DPR", line=dict(color="#4B9EFF"), mode="lines+markers"))
fig_kd.update_layout(
    xaxis_title="Tournament (chronological)",
    yaxis_title="Ratio per Round",
    height=350
)
st.plotly_chart(fig_kd, use_container_width=True)

st.divider()

st.subheader("📅 Average Rating per Year")
df_filtrado_copy = df_filtrado.copy()
df_filtrado_copy["Year"] = df_filtrado_copy["Event"].str.extract(r"(\d{4})")
rating_per_year = df_filtrado_copy.groupby("Year")["Rating"].mean().reset_index()
rating_per_year["Rating"] = rating_per_year["Rating"].round(2)

fig_year = px.bar(
    rating_per_year,
    x="Year",
    y="Rating",
    text="Rating",
    color="Rating",
    color_continuous_scale=["#FF4B4B", "#FFD700"],
)
fig_year.add_hline(y=1.0, line_dash="dash", line_color="gray")
fig_year.update_traces(textposition="outside")
fig_year.update_layout(height=350, showlegend=False)
st.plotly_chart(fig_year, use_container_width=True)

st.divider()

# =============================================
# GOAT COMPARISON SECTION
# =============================================

st.header("🐐 The GOAT Debate — donk vs s1mple vs ZywOo")
st.markdown("""
Comparing donk's career stats against the two most debated GOATs in CS history — 
**s1mple** and **ZywOo** — with one key difference: donk achieved this in just **2 years**.
""")

@st.cache_data
def cargar_comparativa():
    def procesar(path, nombre):
        df = pd.read_csv(path, skiprows=2)
        df.columns = ["Result", "Event", "Team", "Maps", "KPR_DPR", "plus_minus", "Rating"]
        df["Rating"] = df["Rating"].astype(str).str.replace("*", "", regex=False)
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
        df["Maps"] = pd.to_numeric(df["Maps"], errors="coerce")
        df[["KPR", "DPR"]] = df["KPR_DPR"].str.split(" - ", expand=True).astype(float)
        df["Player"] = nombre
        df["Won"] = df["Result"].str.strip() == "1st"
        return df.dropna(subset=["Rating"])
    
    donk = procesar("data/donk_stats.csv", "donk")
    s1mple = procesar("data/s1mple_stats.csv", "s1mple")
    zywoo = procesar("data/zywOo_stats.csv", "ZywOo")
    
    return pd.concat([donk, s1mple, zywoo], ignore_index=True)

df_goat = cargar_comparativa()

# Stats de resumen por jugador
summary = df_goat.groupby("Player").agg(
    Tournaments=("Event", "count"),
    Maps=("Maps", "sum"),
    Avg_Rating=("Rating", "mean"),
    Avg_KPR=("KPR", "mean"),
    Avg_DPR=("DPR", "mean"),
    Wins=("Won", "sum")
).reset_index()
summary["Avg_Rating"] = summary["Avg_Rating"].round(2)
summary["Avg_KPR"] = summary["Avg_KPR"].round(2)
summary["Avg_DPR"] = summary["Avg_DPR"].round(2)
summary["Win Rate"] = (summary["Wins"] / summary["Tournaments"] * 100).round(1)

# KPIs por jugador
col1, col2, col3 = st.columns(3)

photos = {
    "donk": "assets/donk_player.png",
    "s1mple": "assets/s1mple_player.png",
    "ZywOo": "assets/zywoo_player.png"
}

for col, player in zip([col1, col2, col3], ["donk", "s1mple", "ZywOo"]):
    row = summary[summary["Player"] == player].iloc[0]
    with col:
        st.image(photos[player], width=200)
        st.markdown(f"### {'🥇' if player == 'donk' else '🏅'} {player}")
        st.metric("Avg Rating", row["Avg_Rating"])
        st.metric("Tournaments", int(row["Tournaments"]))
        st.metric("Maps Played", int(row["Maps"]))
        st.metric("Tournament Win Rate", f"{row['Win Rate']}%")

st.divider()

# Comparativa de Rating promedio
st.subheader("📊 Average Rating Comparison")
colors = {"donk": "#FF4B4B", "s1mple": "#4B9EFF", "ZywOo": "#00CC44"}
fig_comp = px.bar(
    summary,
    x="Player",
    y="Avg_Rating",
    color="Player",
    text="Avg_Rating",
    color_discrete_map=colors
)
fig_comp.add_hline(y=1.0, line_dash="dash", line_color="gray")
fig_comp.update_traces(textposition="outside")
fig_comp.update_layout(height=400, showlegend=False, yaxis_range=[0.9, 1.5])
st.plotly_chart(fig_comp, use_container_width=True)

st.divider()

# Distribucion de ratings
st.subheader("📈 Rating Distribution — Who Peaks Higher?")
fig_box = px.box(
    df_goat,
    x="Player",
    y="Rating",
    color="Player",
    color_discrete_map=colors
)
fig_box.update_layout(height=400, showlegend=False)
st.plotly_chart(fig_box, use_container_width=True)

st.divider()
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 12px;'>
    Data sourced from <a href='https://www.hltv.org' target='_blank' style='color: #FF4B4B;'>HLTV.org</a> 
    · Built with Python & Streamlit · 2026
</div>
""", unsafe_allow_html=True)