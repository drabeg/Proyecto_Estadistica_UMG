# 📊 Análisis Estadístico de Calidad de Servicio (QoS) en Conexiones Residenciales

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.0%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

Proyecto académico desarrollado para el curso de **Estadística I** en la **Facultad de Ingeniería de la Universidad Mariano Gálvez de Guatemala (UMG)**.

Este proyecto evalúa el desempeño, variabilidad y estabilidad de una red de internet residencial mediante la recolección de métricas de **Calidad de Servicio (QoS)**, integrando un análisis cuantitativo riguroso con un *dashboard* interactivo desplegado en la web.

---

## 📌 Tabla de Contenidos
1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Metodología Estadística](#-metodología-estadística)
3. [Características del Dashboard Interactivo](#-características-del-dashboard-interactivo)
4. [Estructura del Repositorio](#-estructura-del-repositorio)
5. [Instalación y Ejecución Local](#-instalación-y-ejecución-local)
6. [Resultados Principales](#-resultados-principales)
7. [Creado por](#-creado-por)

---

## 📸 Descripción del Proyecto

El objetivo central es demostrar empíricamente el impacto del tráfico en horas pico sobre el rendimiento del ancho de banda residencial. Se evaluó una muestra de **30 mediciones** de velocidad de descarga divididas en tres franjas horarias (Mañana, Tarde y Noche), acompañadas de métricas de velocidad de subida y latencia (*Ping*).

---

## 📐 Metodología Estadística

El desarrollo analítico se fundamenta en los siguientes conceptos de estadística descriptiva:

* **Regla de Sturges:** Determinación del número de clases ($k = 6$) y amplitud del intervalo ($c = 12.50\text{ Mbps}$) para la agrupación de frecuencias continuas.
* **Medidas de Tendencia Central:** Media Aritmética ($\bar{x}$) y Mediana ($Me$) para la evaluación de sesgos en la distribución.
* **Medidas de Dispersión:** Desviación Estándar Muestral ($s$) y Coeficiente de Variación ($CV\%$) para cuantificar la estabilidad de la red.
* **Análisis Cuartílico e IQR:** Cálculo del Rango Intercuartílico ($IQR = Q_3 - Q_1$) y detección de valores atípicos (*outliers*) mediante diagramas de caja.

---

## 🚀 Características del Dashboard Interactivo

La plataforma web desarrollada con **Streamlit** y **Plotly** ofrece:
* 📊 **Tarjetas de Métricas:** Resumen dinámico de promedios para descarga, subida y latencia.
* 📈 **Histograma Ajustado:** Distribución de frecuencias agrupadas con fronteras de clase basadas en Sturges.
* 📦 **Diagrama de Caja (Boxplot):** Identificación gráfica de caídas severas de red y rango intercuartílico.
* 📉 **Comparativa Multi-serie:** Visualización temporal interdiaria (Mañana vs. Tarde vs. Noche).
* 📑 **Visualizador de Datos:** Tablas procesadas y descriptivas integradas.

---

## 📁 Estructura del Repositorio

├── .streamlit/
│   └── config.toml          # Configuración visual de la app
├── data/
│   └── mediciones_qos.csv   # Dataset muestral
├── app.py                   # Script principal de Streamlit
├── requirements.txt         # Dependencias del entorno de Python
└── README.md                # Documentación del proyecto

---

## 🛠️ Instalación y Ejecución Local

1. **Clonar este repositorio:**
    git clone https://github.com/TU_USUARIO/NOMBRE_DE_TU_REPOSITORIO.git
    cd NOMBRE_DE_TU_REPOSITORIO

2. **Crear y activar un entorno virtual:**
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate

3. **Instalar dependencias:**
    pip install -r requirements.txt

4. **Ejecutar la aplicación:**
    streamlit run app.py

---

## 📊 Resultados Principales

* **Comportamiento Matutino:** Alta estabilidad con un coeficiente de variación mínimo ($CV = 2.68\%$) y media cercana a $80\text{ Mbps}$.
* **Degradación Nocturna:** Saturación crítica del canal residencial reflejada en una dispersión alta ($CV = 34.34\%$) y un punto atípico de $11.15\text{ Mbps}$.
* **Simetría de Subida y Latencia:** La velocidad de subida se mantuvo constante ($\bar{x} = 9.87\text{ Mbps}$, $CV = 4.56\%$) con una latencia promedio de $14.20\text{ ms}$.

---

## 👨‍💻 Creado por:

* **Dario Rabe** - 5190-25-23683
* **Holcen Ajín** - 5190-25-24834

*Estadística I*  
**Universidad Mariano Gálvez**