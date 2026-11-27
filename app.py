import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y PALETA DE COLORES
# ==============================================================================
st.set_page_config(
    page_title="Dashboard Matrículas - Univ. Colegio Mayor de Cundinamarca",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta de colores corporativa
COLOR_BG_MAIN = "#0B132B"  # Azul medianoche profundo (Fondo principal)
COLOR_BG_SIDEBAR = "#1C2541"  # Azul marino oscuro (Barra lateral y tarjetas)
COLOR_ACCENT_DARK = "#3A506B"  # Azul pizarra (Bordes, botones, barras secundarias)
COLOR_ACCENT_LIGHT = "#5BC0BE"  # Turquesa brillante (Destacados, gráficos principales)
COLOR_TEXT = "#FFFFFF"

PALETA_GRAFICOS = ["#5BC0BE", "#3A506B", "#1C2541", "#88D4D2", "#4E6E91", "#2A3B5C"]

# ==============================================================================
# 2. ESTILOS CSS PERSONALIZADOS
# ==============================================================================
st.markdown(
    f"""
    <style>
        /* Fondo principal de la aplicación */
        .stApp {{
            background-color: {COLOR_BG_MAIN};
            color: {COLOR_TEXT};
        }}
        
        /* Barra lateral (Panel izquierdo) */
        [data-testid="stSidebar"] {{
            background-color: {COLOR_BG_SIDEBAR};
            border-right: 1px solid {COLOR_ACCENT_DARK};
        }}
        [data-testid="stSidebar"] * {{
            color: {COLOR_TEXT} !important;
        }}
        
        /* Títulos y encabezados */
        h1, h2, h3, h4 {{
            color: {COLOR_ACCENT_LIGHT} !important;
            font-weight: 700;
        }}
        
        /* Contenedores de reseñas debajo de gráficos */
        .resena-box {{
            background-color: {COLOR_BG_SIDEBAR};
            border-left: 5px solid {COLOR_ACCENT_LIGHT};
            border-top: 1px solid {COLOR_ACCENT_DARK};
            border-right: 1px solid {COLOR_ACCENT_DARK};
            border-bottom: 1px solid {COLOR_ACCENT_DARK};
            padding: 16px 20px;
            border-radius: 8px;
            margin-top: 15px;
            color: {COLOR_TEXT};
            font-size: 15px;
            line-height: 1.5;
        }}
        .resena-titulo {{
            color: {COLOR_ACCENT_LIGHT};
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 6px;
        }}

        /* Estilo de las Pestañas (Tabs) */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: {COLOR_BG_SIDEBAR};
            padding: 8px;
            border-radius: 10px;
            border: 1px solid {COLOR_ACCENT_DARK};
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            color: {COLOR_TEXT};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLOR_ACCENT_LIGHT} !important;
            color: {COLOR_BG_MAIN} !important;
        }}

        /* Botones */
        .stButton > button {{
            background-color: {COLOR_ACCENT_DARK};
            color: {COLOR_TEXT};
            border: 1px solid {COLOR_ACCENT_LIGHT};
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            background-color: {COLOR_ACCENT_LIGHT};
            color: {COLOR_BG_MAIN};
        }}

        /* Métricas KPI */
        [data-testid="stMetric"] {{
            background-color: {COLOR_BG_SIDEBAR};
            border: 1px solid {COLOR_ACCENT_DARK};
            padding: 12px 16px;
            border-radius: 8px;
        }}
        [data-testid="stMetricLabel"] {{
            color: #B0C4DE !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {COLOR_ACCENT_LIGHT} !important;
        }}
    </style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# 3. CARGA Y LIMPIEZA DE DATOS
# ==============================================================================
@st.cache_data
def cargar_datos():
    ruta = os.path.join(
        "database",
        "Valor_de_Matricula_-_Programas_Universidad_Colegio_Mayor_de_Cundinamarca_20261126.csv",
    )
    # Detección automática de separador (coma o punto y coma)
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="latin-1")

    # Limpiar espacios en blanco en nombres de columnas
    df.columns = df.columns.str.strip()

    # Asegurar que las 5 columnas existan y limpiar sus valores de texto
    cols_objetivo = [
        "PROGRAMA",
        "NIVEL DE INGRESOS",
        "NIVEL DE INGRESO MAXIMO",
        "VALOR DE MATRICULA",
        "Valor en SMLMV",
    ]
    for col in cols_objetivo:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Crear columnas numéricas auxiliares para cálculos y ordenamiento en gráficos
    def limpiar_numero(serie):
        return pd.to_numeric(
            serie.astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip(),
            errors="coerce",
        )

    df["_num_matricula"] = limpiar_numero(df["VALOR DE MATRICULA"])
    df["_num_smlmv"] = pd.to_numeric(
        df["Valor en SMLMV"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.strip(),
        errors="coerce",
    )
    return df


try:
    df_raw = cargar_datos()
except FileNotFoundError:
    st.error(
        "❌ No se encontró el archivo en la ruta: `database\\Valor_de_Matricula_-_Programas_Universidad_Colegio_Mayor_de_Cundinamarca_20261126.csv`"
    )
    st.stop()

# ==============================================================================
# 4. PANEL IZQUIERDO: FILTROS ENCADENADOS (EN CASCADA)
# ==============================================================================
st.sidebar.markdown("## 🔍 Filtros Encadenados")
st.sidebar.caption(
    "Seleccione en orden descendente. Cada filtro actualiza dinámicamente las opciones disponibles de los siguientes niveles."
)

# Función para reiniciar filtros
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

if st.sidebar.button("🔄 Limpiar todos los filtros", use_container_width=True):
    st.session_state.reset_counter += 1
    st.rerun()

rc = st.session_state.reset_counter

# --- NIVEL 1: PROGRAMA ---
df_step1 = df_raw.copy()
opciones_1 = ["Todos"] + sorted(df_step1["PROGRAMA"].dropna().unique().tolist())
sel_programa = st.sidebar.selectbox("1. PROGRAMA", opciones_1, key=f"f1_{rc}")
if sel_programa != "Todos":
    df_step1 = df_step1[df_step1["PROGRAMA"] == sel_programa]

# --- NIVEL 2: NIVEL DE INGRESOS ---
df_step2 = df_step1.copy()
opciones_2 = ["Todos"] + sorted(
    df_step2["NIVEL DE INGRESOS"].dropna().unique().tolist()
)
sel_nivel_ing = st.sidebar.selectbox(
    "2. NIVEL DE INGRESOS", opciones_2, key=f"f2_{rc}"
)
if sel_nivel_ing != "Todos":
    df_step2 = df_step2[df_step2["NIVEL DE INGRESOS"] == sel_nivel_ing]

# --- NIVEL 3: NIVEL DE INGRESO MAXIMO ---
df_step3 = df_step2.copy()
opciones_3 = ["Todos"] + sorted(
    df_step3["NIVEL DE INGRESO MAXIMO"].dropna().unique().tolist()
)
sel_nivel_max = st.sidebar.selectbox(
    "3. NIVEL DE INGRESO MAXIMO", opciones_3, key=f"f3_{rc}"
)
if sel_nivel_max != "Todos":
    df_step3 = df_step3[df_step3["NIVEL DE INGRESO MAXIMO"] == sel_nivel_max]

# --- NIVEL 4: VALOR DE MATRICULA ---
df_step4 = df_step3.copy()
opciones_4 = ["Todos"] + sorted(
    df_step4["VALOR DE MATRICULA"].dropna().unique().tolist(),
    key=lambda x: (
        float("".join(filter(str.isdigit, x)))
        if any(c.isdigit() for c in x)
        else 0
    ),
)
sel_matricula = st.sidebar.selectbox(
    "4. VALOR DE MATRICULA", opciones_4, key=f"f4_{rc}"
)
if sel_matricula != "Todos":
    df_step4 = df_step4[df_step4["VALOR DE MATRICULA"] == sel_matricula]

# --- NIVEL 5: Valor en SMLMV ---
df_filtrado = df_step4.copy()
opciones_5 = ["Todos"] + sorted(
    df_filtrado["Valor en SMLMV"].dropna().unique().tolist()
)
sel_smlmv = st.sidebar.selectbox("5. Valor en SMLMV", opciones_5, key=f"f5_{rc}")
if sel_smlmv != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Valor en SMLMV"] == sel_smlmv]

st.sidebar.markdown("---")
st.sidebar.info(
    f"📊 **Registros activos:** {len(df_filtrado)} de {len(df_raw)}"
)

# ==============================================================================
# 5. ENCABEZADO PRINCIPAL Y MÉTRICAS RESUMEN
# ==============================================================================
st.title("🎓 Análisis de Valores de Matrícula")
st.markdown(
    "Universidad Colegio Mayor de Cundinamarca — Visualización Interactiva por Categorías"
)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Programas Filtrados", df_filtrado["PROGRAMA"].nunique())
with col_m2:
    st.metric("Niveles de Ingreso", df_filtrado["NIVEL DE INGRESOS"].nunique())
with col_m3:
    prom_mat = df_filtrado["_num_matricula"].mean()
    st.metric(
        "Matrícula Promedio",
        f"${prom_mat:,.0f}" if pd.notna(prom_mat) else "N/A",
    )
with col_m4:
    prom_smlmv = df_filtrado["_num_smlmv"].mean()
    st.metric(
        "Promedio SMLMV",
        f"{prom_smlmv:.2f} SMLMV" if pd.notna(prom_smlmv) else "N/A",
    )

st.markdown("---")


# Función auxiliar para aplicar diseño uniforme a gráficos Plotly
def estilizar_figura(fig, titulo):
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=18, color=COLOR_ACCENT_LIGHT)),
        paper_bgcolor=COLOR_BG_SIDEBAR,
        plot_bgcolor=COLOR_BG_MAIN,
        font=dict(color=COLOR_TEXT, size=12),
        xaxis=dict(gridcolor=COLOR_ACCENT_DARK, zerolinecolor=COLOR_ACCENT_DARK),
        yaxis=dict(gridcolor=COLOR_ACCENT_DARK, zerolinecolor=COLOR_ACCENT_DARK),
        margin=dict(l=30, r=30, t=55, b=30),
        legend=dict(
            bgcolor=COLOR_BG_SIDEBAR, bordercolor=COLOR_ACCENT_DARK, borderwidth=1
        ),
    )
    return fig


# ==============================================================================
# 6. PESTAÑAS POR CATEGORÍA CON GRÁFICOS Y RESEÑAS
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📚 PROGRAMA",
    "💰 NIVEL DE INGRESOS",
    "📈 NIVEL DE INGRESO MAXIMO",
    "💵 VALOR DE MATRICULA",
    "⚖️ Valor en SMLMV",
])

# --- PESTAÑA 1: PROGRAMA

import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y PALETA DE COLORES
# ==============================================================================
st.set_page_config(
    page_title="Dashboard Matrículas - Univ. Colegio Mayor de Cundinamarca",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta de colores solicitada
COLOR_BG_MAIN = "#0B132B"
COLOR_BG_SIDEBAR = "#1C2541"
COLOR_ACCENT_DARK = "#3A506B"
COLOR_ACCENT_LIGHT = "#5BC0BE"
COLOR_TEXT = "#FFFFFF"

PALETA_GRAFICOS = ["#5BC0BE", "#3A506B", "#1C2541", "#88D4D2", "#4E6E91", "#2A3B5C"]

# ==============================================================================
# 2. ESTILOS CSS PERSONALIZADOS
# ==============================================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {COLOR_BG_MAIN};
            color: {COLOR_TEXT};
        }}
        [data-testid="stSidebar"] {{
            background-color: {COLOR_BG_SIDEBAR};
            border-right: 1px solid {COLOR_ACCENT_DARK};
        }}
        [data-testid="stSidebar"] * {{
            color: {COLOR_TEXT} !important;
        }}
        h1, h2, h3, h4 {{
            color: {COLOR_ACCENT_LIGHT} !important;
            font-weight: 700;
        }}
        .resena-box {{
            background-color: {COLOR_BG_SIDEBAR};
            border-left: 5px solid {COLOR_ACCENT_LIGHT};
            border-top: 1px solid {COLOR_ACCENT_DARK};
            border-right: 1px solid {COLOR_ACCENT_DARK};
            border-bottom: 1px solid {COLOR_ACCENT_DARK};
            padding: 16px 20px;
            border-radius: 8px;
            margin-top: 15px;
            color: {COLOR_TEXT};
            font-size: 15px;
            line-height: 1.5;
        }}
        .resena-titulo {{
            color: {COLOR_ACCENT_LIGHT};
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 6px;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: {COLOR_BG_SIDEBAR};
            padding: 8px;
            border-radius: 10px;
            border: 1px solid {COLOR_ACCENT_DARK};
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            color: {COLOR_TEXT};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLOR_ACCENT_LIGHT} !important;
            color: {COLOR_BG_MAIN} !important;
        }}
        .stButton > button {{
            background-color: {COLOR_ACCENT_DARK};
            color: {COLOR_TEXT};
            border: 1px solid {COLOR_ACCENT_LIGHT};
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            background-color: {COLOR_ACCENT_LIGHT};
            color: {COLOR_BG_MAIN};
        }}
        [data-testid="stMetric"] {{
            background-color: {COLOR_BG_SIDEBAR};
            border: 1px solid {COLOR_ACCENT_DARK};
            padding: 12px 16px;
            border-radius: 8px;
        }}
        [data-testid="stMetricLabel"] {{
            color: #B0C4DE !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {COLOR_ACCENT_LIGHT} !important;
        }}
    </style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# 3. CARGA Y LIMPIEZA DE DATOS
# ==============================================================================
@st.cache_data
def cargar_datos():
    ruta = os.path.join(
        "database",
        "Valor_de_Matricula_-_Programas_Universidad_Colegio_Mayor_de_Cundinamarca_20261126.csv",
    )
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="latin-1")

    df.columns = df.columns.str.strip()

    cols_objetivo = [
        "PROGRAMA",
        "NIVEL DE INGRESOS",
        "NIVEL DE INGRESO MAXIMO",
        "VALOR DE MATRICULA",
        "Valor en SMLMV",
    ]
    for col in cols_objetivo:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    def limpiar_numero(serie):
        return pd.to_numeric(
            serie.astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip(),
            errors="coerce",
        )

    df["_num_matricula"] = limpiar_numero(df["VALOR DE MATRICULA"])
    df["_num_smlmv"] = pd.to_numeric(
        df["Valor en SMLMV"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.strip(),
        errors="coerce",
    )
    return df


try:
    df_raw = cargar_datos()
except FileNotFoundError:
    st.error(
        "❌ No se encontró el archivo en la ruta: `database\\Valor_de_Matricula_-_Programas_Universidad_Colegio_Mayor_de_Cundinamarca_20261126.csv`"
    )
    st.stop()

# ==============================================================================
# 4. PANEL IZQUIERDO: FILTROS ENCADENADOS
# ==============================================================================
st.sidebar.markdown("## 🔍 Filtros Encadenados")
st.sidebar.caption(
    "Cada selección filtra automáticamente las opciones disponibles en los niveles siguientes."
)

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

if st.sidebar.button("🔄 Limpiar todos los filtros", use_container_width=True):
    st.session_state.reset_counter += 1
    st.rerun()

rc = st.session_state.reset_counter

# 1. PROGRAMA
df_step1 = df_raw.copy()
opciones_1 = ["Todos"] + sorted(df_step1["PROGRAMA"].dropna().unique().tolist())
sel_programa = st.sidebar.selectbox("1. PROGRAMA", opciones_1, key=f"f1_{rc}")
if sel_programa != "Todos":
    df_step1 = df_step1[df_step1["PROGRAMA"] == sel_programa]

# 2. NIVEL DE INGRESOS
df_step2 = df_step1.copy()
opciones_2 = ["Todos"] + sorted(
    df_step2["NIVEL DE INGRESOS"].dropna().unique().tolist()
)
sel_nivel_ing = st.sidebar.selectbox(
    "2. NIVEL DE INGRESOS", opciones_2, key=f"f2_{rc}"
)
if sel_nivel_ing != "Todos":
    df_step2 = df_step2[df_step2["NIVEL DE INGRESOS"] == sel_nivel_ing]

# 3. NIVEL DE INGRESO MAXIMO
df_step3 = df_step2.copy()
opciones_3 = ["Todos"] + sorted(
    df_step3["NIVEL DE INGRESO MAXIMO"].dropna().unique().tolist()
)
sel_nivel_max = st.sidebar.selectbox(
    "3. NIVEL DE INGRESO MAXIMO", opciones_3, key=f"f3_{rc}"
)
if sel_nivel_max != "Todos":
    df_step3 = df_step3[df_step3["NIVEL DE INGRESO MAXIMO"] == sel_nivel_max]

# 4. VALOR DE MATRICULA
df_step4 = df_step3.copy()
opciones_4 = ["Todos"] + sorted(
    df_step4["VALOR DE MATRICULA"].dropna().unique().tolist(),
    key=lambda x: (
        float("".join(filter(str.isdigit, x)))
        if any(c.isdigit() for c in x)
        else 0
    ),
)
sel_matricula = st.sidebar.selectbox(
    "4. VALOR DE MATRICULA", opciones_4, key=f"f4_{rc}"
)
if sel_matricula != "Todos":
    df_step4 = df_step4[df_step4["VALOR DE MATRICULA"] == sel_matricula]

# 5. Valor en SMLMV
df_filtrado = df_step4.copy()
opciones_5 = ["Todos"] + sorted(
    df_filtrado["Valor en SMLMV"].dropna().unique().tolist()
)
sel_
