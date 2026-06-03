"""
NutriSim — Sistema de recomendación de sustituciones nutricionales
Trabajo Final de Máster · Bioinformática y Bioestadística · UOC 2026
Aracelli Salinas Venegas

Uso:
    streamlit run nutrisim_app.py

Archivos necesarios en la misma carpeta:
    - cereales_final.csv
    - scaler.pkl
    - knn_normalizado.pkl
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import os

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="NutriSim · Similitud Nutricional",
    page_icon="🥣",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# CONSTANTES
# ──────────────────────────────────────────────
COLS_NUTRI = [
    "Energy",
    "Protein",
    "Carbohydrate, by difference",
    "Total lipid (fat)",
    "Fatty acids, total saturated",
    "Fiber, total dietary",
    "Total Sugars",
    "Sodium, Na",
]

COLS_ES = [
    "Energía (kcal)",
    "Proteína (g)",
    "Carbohidratos (g)",
    "Grasa total (g)",
    "Grasa saturada (g)",
    "Fibra (g)",
    "Azúcares (g)",
    "Sodio (mg)",
]

NS_COLOR = {
    "A": "#27ae60",
    "B": "#82c91e",
    "C": "#f5a623",
    "D": "#e67e22",
    "E": "#c0392b",
}

NS_BG = {
    "A": "#d4edda",
    "B": "#e8f5e9",
    "C": "#fff8e1",
    "D": "#fdebd0",
    "E": "#fde8e8",
}

NS_TEXT = {
    "A": "#155724",
    "B": "#2e7d32",
    "C": "#7c5e00",
    "D": "#7c3c0b",
    "E": "#721c24",
}

GRADES_ORDER = ["A", "B", "C", "D", "E"]

# ──────────────────────────────────────────────
# CARGA DE DATOS Y MODELOS (cacheados)
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_data(show_spinner="Cargando catálogo de cereales…")
def load_data():
    path = os.path.join(BASE_DIR, "cereales_final.csv")
    df = pd.read_csv(path)
    # Etiqueta de búsqueda limpia
    df["_label"] = (
        df["description"].str.strip()
        + "  —  "
        + df["brand_owner"].str.strip()
        + "  ["
        + df["nutriscore_grade"]
        + "]"
    )
    return df


@st.cache_resource(show_spinner="Cargando modelos…")
def load_models():
    scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
    knn = joblib.load(os.path.join(BASE_DIR, "knn_normalizado.pkl"))
    return scaler, knn


# ──────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ──────────────────────────────────────────────
def nutriscore_badge(grade: str) -> str:
    color = NS_COLOR.get(grade, "#888")
    return (
        f'<span style="background:{color};color:white;padding:3px 14px;'
        f'border-radius:5px;font-weight:bold;font-size:1.05rem;">{grade}</span>'
    )


def recommend(df, scaler, knn, row_idx: int, n: int = 10):
    X = df[COLS_NUTRI].values
    X_norm = scaler.transform(X)
    query = X_norm[[row_idx]]
    dists, idxs = knn.kneighbors(query, n_neighbors=n + 1)
    neighbors = [
        (int(idxs[0][i]), float(dists[0][i]))
        for i in range(len(idxs[0]))
        if idxs[0][i] != row_idx
    ][:n]
    return neighbors


def build_rec_table(df, neighbors):
    rows = []
    for rank, (idx, dist) in enumerate(neighbors, 1):
        r = df.iloc[idx]
        rows.append(
            {
                "#": rank,
                "Producto": r["description"],
                "Marca": r["brand_owner"],
                "Nutri-Score": r["nutriscore_grade"],
                "Distancia": round(dist, 3),
                "Energía": round(r["Energy"], 0),
                "Proteína": round(r["Protein"], 1),
                "Carbohidratos": round(r["Carbohydrate, by difference"], 1),
                "Grasa total": round(r["Total lipid (fat)"], 1),
                "Grasa saturada": round(r["Fatty acids, total saturated"], 1),
                "Fibra": round(r["Fiber, total dietary"], 1),
                "Azúcares": round(r["Total Sugars"], 1),
                "Sodio": round(r["Sodium, Na"], 0),
            }
        )
    return pd.DataFrame(rows)


def style_table(df_table):
    def color_ns(val):
        bg = NS_BG.get(val, "white")
        fg = NS_TEXT.get(val, "black")
        return f"background-color:{bg};color:{fg};font-weight:bold;text-align:center;"

    def dist_bar(val):
        pct = min(val / 2.0, 1.0) * 100  # distancia máxima esperada ~2
        return f"background: linear-gradient(90deg, #bde0fe {pct:.0f}%, white {pct:.0f}%);"

    return (
        df_table.style.applymap(color_ns, subset=["Nutri-Score"])
        .applymap(dist_bar, subset=["Distancia"])
        .format({"Distancia": "{:.3f}", "Energía": "{:.0f}", "Sodio": "{:.0f}"})
        .set_properties(**{"text-align": "left"})
    )


def comparison_chart(product, neighbors, df):
    VARS = [
        "Energy",
        "Protein",
        "Carbohydrate, by difference",
        "Total lipid (fat)",
        "Fiber, total dietary",
        "Total Sugars",
        "Sodium, Na",
    ]
    LABELS = [
        "Energía<br>(kcal)",
        "Proteína<br>(g)",
        "Carbohidratos<br>(g)",
        "Grasa<br>(g)",
        "Fibra<br>(g)",
        "Azúcares<br>(g)",
        "Sodio<br>(mg)",
    ]

    fig = go.Figure()

    # Producto original
    fig.add_trace(
        go.Bar(
            name=f"📌 {product['description'][:35]} [{product['nutriscore_grade']}]",
            x=LABELS,
            y=[product[v] for v in VARS],
            marker_color=NS_COLOR.get(product["nutriscore_grade"], "#888"),
            marker_line_width=0,
            opacity=0.95,
        )
    )

    # Top 3 recomendaciones
    palette = ["#3498db", "#9b59b6", "#16a085"]
    for i, (idx_r, dist) in enumerate(neighbors[:3]):
        rec = df.iloc[idx_r]
        fig.add_trace(
            go.Bar(
                name=f"#{i+1} {rec['description'][:28]} [{rec['nutriscore_grade']}] (d={dist:.2f})",
                x=LABELS,
                y=[rec[v] for v in VARS],
                marker_color=palette[i],
                marker_line_width=0,
                opacity=0.75,
            )
        )

    fig.update_layout(
        barmode="group",
        title="Perfil nutricional: producto original vs. top 3 recomendaciones (por 100 g)",
        yaxis_title="Cantidad",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=430,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13),
        margin=dict(t=80, b=40),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#eee")

    return fig


# ──────────────────────────────────────────────
# CABECERA
# ──────────────────────────────────────────────
st.markdown(
    """
    <h1 style='margin-bottom:0'>🥣 NutriSim</h1>
    <p style='color:gray;font-size:1.05rem;margin-top:4px'>
    Sistema de recomendación de sustituciones nutricionales · Cereales de desayuno · USDA FoodData Central
    </p>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

st.info(
    "**ℹ️ Aviso:** Este sistema proporciona información comparativa objetiva basada en 8 variables "
    "nutricionales. No considera condiciones individuales (alergias, enfermedades, requerimientos "
    "clínicos) y **no reemplaza la consulta con un profesional de la salud o nutricionista.**"
)

# ──────────────────────────────────────────────
# CARGA
# ──────────────────────────────────────────────
try:
    df = load_data()
    scaler, knn = load_models()
except FileNotFoundError as e:
    st.error(
        f"❌ Archivo no encontrado: {e}\n\n"
        "Asegúrate de que `cereales_final.csv`, `scaler.pkl` y `knn_normalizado.pkl` "
        "estén en la misma carpeta que este script."
    )
    st.stop()

# ──────────────────────────────────────────────
# BÚSQUEDA
# ──────────────────────────────────────────────
st.markdown("### 🔍 Buscar producto")

col_search, col_info = st.columns([3, 1])
with col_search:
    query_text = st.text_input(
        "Nombre del cereal:",
        placeholder="Ej: Cheerios, Granola, Corn Flakes, Bran Flakes…",
        label_visibility="collapsed",
    )
with col_info:
    st.markdown(
        f"<small>Catálogo: <b>{len(df):,}</b> productos</small>",
        unsafe_allow_html=True,
    )

if not query_text:
    st.markdown("👆 Escribe el nombre de un cereal para comenzar.")
    with st.expander("Ver ejemplos de productos disponibles"):
        sample = (
            df.sample(12)[
                ["description", "brand_owner", "nutriscore_grade", "Energy",
                 "Fiber, total dietary", "Total Sugars"]
            ]
            .rename(
                columns={
                    "description": "Producto",
                    "brand_owner": "Marca",
                    "nutriscore_grade": "Nutri-Score",
                    "Energy": "Energía (kcal)",
                    "Fiber, total dietary": "Fibra (g)",
                    "Total Sugars": "Azúcares (g)",
                }
            )
        )
        st.dataframe(sample, use_container_width=True, hide_index=True)
    st.stop()

# Filtrar resultados
mask = df["description"].str.contains(query_text, case=False, na=False)
matches = df[mask]

if matches.empty:
    st.warning(
        f"No se encontraron productos con '{query_text}'. "
        "Prueba con un término más general (ej: 'granola', 'oat', 'corn')."
    )
    st.stop()

options = matches["_label"].tolist()
selected_label = st.selectbox(
    f"Se encontraron **{len(matches)}** productos. Selecciona uno:",
    options,
)
selected_pos = options.index(selected_label)
selected_row_idx = matches.index[selected_pos]
product = df.loc[selected_row_idx]

# ──────────────────────────────────────────────
# PRODUCTO SELECCIONADO
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📋 Producto seleccionado")

c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    st.markdown(f"**{product['description']}**")
    st.markdown(f"🏷️ {product['brand_owner']}  ·  📦 {product['food_category']}")
with c2:
    grade = product["nutriscore_grade"]
    st.markdown(f"**Nutri-Score**", unsafe_allow_html=True)
    st.markdown(nutriscore_badge(grade), unsafe_allow_html=True)
with c3:
    st.metric("Puntuación neta", f"{int(product['nutriscore_points'])} pts")

with st.expander("📊 Ver perfil nutricional completo (por 100 g)"):
    nutri_profile = pd.DataFrame(
        {
            "Nutriente": COLS_ES,
            "Valor": [round(product[c], 2) for c in COLS_NUTRI],
        }
    )
    st.dataframe(nutri_profile, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
# RECOMENDACIONES
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🔄 Top 10 sustitutos más similares nutricionalmente")

with st.spinner("Buscando vecinos más cercanos…"):
    neighbors = recommend(df, scaler, knn, selected_row_idx, n=10)

rec_df = build_rec_table(df, neighbors)
st.dataframe(style_table(rec_df), use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
# GRÁFICO COMPARATIVO
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Comparación visual (producto original vs. top 3)")

fig = comparison_chart(product, neighbors, df)
st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# RESUMEN NUTRI-SCORE
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💡 Resumen")

orig_rank = GRADES_ORDER.index(grade)
improved = sum(
    1
    for _, (idx_r, _) in enumerate(neighbors)
    if GRADES_ORDER.index(df.iloc[idx_r]["nutriscore_grade"]) < orig_rank
)
equal_ns = sum(
    1
    for _, (idx_r, _) in enumerate(neighbors)
    if df.iloc[idx_r]["nutriscore_grade"] == grade
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Nutri-Score original", grade)
m2.metric("Con Nutri-Score mejor", improved, delta=f"+{improved}" if improved > 0 else None)
m3.metric("Con mismo Nutri-Score", equal_ns)
m4.metric("Distancia al más cercano", f"{neighbors[0][1]:.3f}")

if improved > 0:
    st.success(
        f"✅ {improved} de las 10 recomendaciones tienen un **Nutri-Score superior** al producto original ({grade}). "
        f"Considera revisar las primeras opciones de la tabla."
    )
elif grade == "A":
    st.success("🏆 El producto seleccionado ya tiene la **mejor calificación Nutri-Score (A)**.")
else:
    st.info(
        "ℹ️ Los productos recomendados tienen un Nutri-Score similar al original. "
        "Las diferencias nutricionales son graduales en esta zona del catálogo."
    )

# ──────────────────────────────────────────────
# PIE DE PÁGINA
# ──────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Datos: USDA FoodData Central — Branded Foods (11.608 productos) · "
    "Modelo: k-NN (k=10, distancia euclidiana, espacio normalizado z-score) · "
    "Nutri-Score: Hercberg et al., Int J Vitam Nutr Res 2022 · "
    "TFM Bioinformática y Bioestadística, UOC 2026"
)
