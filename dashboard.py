import os
import glob
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="Trabajo Integrador de Estadística Descriptiva - UMG",
    page_icon="📊",
    layout="wide"
)

# Estilizado de componentes mediante CSS adaptativo
st.markdown("""
    <style>
    .main-title {
        color: #4A90E2;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* Formato adaptable para las tarjetas de métricas */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px;
        border-radius: 10px;
        border-left: 5px solid #1F4E79;
    }
    
/* Ajuste de tipografía para evitar puntos suspensivos en los valores */
    div[data-testid="stMetricLabel"] > div {
        color: #A0AAB5 !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #FFFFFF !important;
        font-size: 1.4rem !important; /* Tamaño reducido para visibilidad completa de unidades */
        font-weight: bold !important;
        white-space: nowrap !important;
    }
    
    /* Separador de la barra lateral */
    .sidebar-footer {
        font-size: 0.85rem;
        color: #B0B8C1;
        margin-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BARRA LATERAL (SIDEBAR INSTITUCIONAL)
# ==========================================
with st.sidebar:
    # Cargar el logo desde la carpeta local 'imagenes'
    ruta_imagenes = glob.glob("imagenes/*")
    if ruta_imagenes:
        st.image(ruta_imagenes[0], use_container_width=True)
    else:
        st.warning("⚠️ No se encontró la imagen en la carpeta 'imagenes'")
    
    st.markdown("### 🔍 Filtros de Visualización")
    
    # Cargar base de datos
    @st.cache_data
    def cargar_datos():
        try:
            return pd.read_csv("mediciones_limpias.csv")
        except FileNotFoundError:
            st.error("❌ No se encontró 'mediciones_limpias.csv'. Ejecutar primero 'python generar_excel.py'.")
            st.stop()

    df = cargar_datos()

    # Selector de Horario
    horarios_disponibles = ["Todos"] + list(df["Horario"].unique())
    horario_seleccionado = st.selectbox("Seleccionar Horario:", horarios_disponibles)

    # Bloque de información académica en el footer de la barra lateral
    st.markdown("""
        <div class="sidebar-footer">
            <strong>Trabajo Integrador de Estadística Descriptiva</strong><br><br>
            <strong>Universidad Mariano Gálvez</strong><br>
            <em>Estadística I</em><br><br>
            <strong>Creado por:</strong><br>
            • Holcen Ajín - 5190-25-24834<br>
            • Dario Rabe - 5190-25-23683
        </div>
    """, unsafe_allow_html=True)

# Filtrar DataFrame según el selector
if horario_seleccionado != "Todos":
    df_filtrado = df[df["Horario"] == horario_seleccionado]
else:
    df_filtrado = df.copy()

# ==========================================
# 3. ENCABEZADO Y TARJETAS DE MÉTRICAS (KPIs)
# ==========================================
st.markdown("<div class='main-title'>📊 Dashboard de Rendimiento de Internet - UMG</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Mediciones (n)", len(df_filtrado))
col2.metric("Descarga Promedio", f"{df_filtrado['Descarga'].mean():.2f} Mbps")
col3.metric("Subida Promedio", f"{df_filtrado['Subida'].mean():.2f} Mbps")
col4.metric("Ping Promedio", f"{df_filtrado['Ping'].mean():.0f} ms")

st.divider()

# ==========================================
# 4. PESTAÑAS DE ANÁLISIS VIRTUAL
# ==========================================
tab1, tab2, tab3 = st.tabs(["📈 Series Temporales", "📊 Distribución y Histogramas", "📋 Tabla de Datos"])

with tab1:
    st.subheader("Evolución del Rendimiento en el Tiempo")
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_filtrado.index + 1, 
        y=df_filtrado["Descarga"], 
        name="Descarga (Mbps)", 
        line=dict(color="#4A90E2", width=2)
    ))
    fig_line.add_trace(go.Scatter(
        x=df_filtrado.index + 1, 
        y=df_filtrado["Subida"], 
        name="Subida (Mbps)", 
        line=dict(color="#50E3C2", width=2)
    ))
    
    fig_line.update_layout(
        title="Velocidad de Descarga y Subida por Medición",
        xaxis_title="Número de Medición",
        yaxis_title="Velocidad (Mbps)",
        hovermode="x unified",
        template="plotly_dark"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("Distribución de Velocidad de Descarga")
        fig_hist = px.histogram(
            df_filtrado, 
            x="Descarga", 
            nbins=10, 
            color="Horario",
            title="Histograma de Descarga por Horario",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col_g2:
        st.subheader("Variabilidad de Latencia (Ping)")
        fig_box = px.box(
            df_filtrado, 
            x="Horario", 
            y="Ping", 
            color="Horario",
            title="Diagrama de Caja (Boxplot) para Latencia",
            points="all",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_box, use_container_width=True)

with tab3:
    st.subheader("Registro Depurado de Mediciones")
    st.dataframe(df_filtrado, use_container_width=True)