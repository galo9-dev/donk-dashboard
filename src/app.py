import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="donk Dashboard",
    page_icon="🎯",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/donk_stats.csv", skiprows=2)
    df.columns = ["Resultado", "Evento", "Equipo", "Mapas", "KPR_DPR", "plus_minus", "Rating"]
    
    # Separar KPR y DPR
    df[["KPR", "DPR"]] = df["KPR_DPR"].str.split(" - ", expand=True).astype(float)
    df = df.drop(columns=["KPR_DPR"])
    
    # Limpiar Rating (sacar asteriscos)
    df["Rating"] = df["Rating"].astype(str).str.replace("*", "", regex=False).astype(float)
    
    # Limpiar Mapas
    df["Mapas"] = pd.to_numeric(df["Mapas"], errors="coerce")
    
    # Columna era
    df["Era"] = df["Equipo"].apply(lambda x: "Spirit" if x == "Spirit" else "Spirit Academy / Otro")
    
    # Columna torneo ganado
    df["Ganado"] = df["Resultado"].str.strip() == "1st"
    
    return df

df = cargar_datos()

# Header
st.title("🎯 donk — El Mejor Jugador del Mundo")
st.markdown("Análisis completo de Danil 'donk' Kryshkovets en el circuito profesional de CS2")
st.divider()

# Filtrar solo Spirit (era pro)
df_spirit = df[df["Equipo"] == "Spirit"].copy()

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Rating Promedio", f"{df_spirit['Rating'].mean():.2f}")
col2.metric("Torneos Jugados", len(df_spirit))
col3.metric("Torneos Ganados", df_spirit["Ganado"].sum())
col4.metric("Mapas Jugados", int(df_spirit["Mapas"].sum()))
col5.metric("KPR Promedio", f"{df_spirit['KPR'].mean():.2f}")

st.divider()

# Gráfico Rating a lo largo del tiempo
st.subheader("📈 Rating 2.0 por Torneo")

df_plot = df_spirit.iloc[::-1].reset_index(drop=True)
df_plot["#"] = range(1, len(df_plot) + 1)

fig_rating = px.line(
    df_plot,
    x="#",
    y="Rating",
    hover_name="Evento",
    markers=True,
    color_discrete_sequence=["#FF4B4B"]
)
fig_rating.add_hline(y=1.0, line_dash="dash", line_color="gray", annotation_text="Rating 1.0 (promedio)")
fig_rating.update_layout(
    xaxis_title="Torneo (cronológico)",
    yaxis_title="Rating 2.0",
    height=400
)
st.plotly_chart(fig_rating, use_container_width=True)

st.divider()

# Gráfico Plus/Minus
st.subheader("⚔️ Diferencia de Kills por Torneo")
fig_pm = px.bar(
    df_plot,
    x="#",
    y="plus_minus",
    hover_name="Evento",
    color="plus_minus",
    color_continuous_scale=["#FF4B4B", "#00CC44"],
    color_continuous_midpoint=0
)
fig_pm.update_layout(
    xaxis_title="Torneo (cronológico)",
    yaxis_title="+/-",
    height=350,
    showlegend=False
)
st.plotly_chart(fig_pm, use_container_width=True)

st.divider()

# Torneos ganados
st.subheader("🏆 Torneos Ganados con Spirit")
ganados = df_spirit[df_spirit["Ganado"]][["Evento", "Mapas", "Rating", "plus_minus"]].reset_index(drop=True)
ganados.index += 1
st.dataframe(ganados, use_container_width=True)

st.divider()

# KPR vs DPR
st.subheader("🎯 KPR vs DPR por Torneo")
fig_kd = go.Figure()
fig_kd.add_trace(go.Scatter(x=df_plot["#"], y=df_plot["KPR"], name="KPR", line=dict(color="#FF4B4B"), mode="lines+markers"))
fig_kd.add_trace(go.Scatter(x=df_plot["#"], y=df_plot["DPR"], name="DPR", line=dict(color="#4B9EFF"), mode="lines+markers"))
fig_kd.update_layout(
    xaxis_title="Torneo (cronológico)",
    yaxis_title="Ratio por Ronda",
    height=350
)
st.plotly_chart(fig_kd, use_container_width=True)



st.divider()

# Rating promedio por año
st.subheader("📅 Evolución del Rating Promedio por Año")

# Extraer año del evento usando el índice cronológico
df_spirit_copy = df_spirit.copy()
df_spirit_copy["Año"] = df_spirit_copy["Evento"].str.extract(r"(\d{4})")
rating_por_año = df_spirit_copy.groupby("Año")["Rating"].mean().reset_index()
rating_por_año["Rating"] = rating_por_año["Rating"].round(2)

fig_año = px.bar(
    rating_por_año,
    x="Año",
    y="Rating",
    text="Rating",
    color="Rating",
    color_continuous_scale=["#FF4B4B", "#FFD700"],
)
fig_año.add_hline(y=1.0, line_dash="dash", line_color="gray")
fig_año.update_traces(textposition="outside")
fig_año.update_layout(height=350, showlegend=False)
st.plotly_chart(fig_año, use_container_width=True)