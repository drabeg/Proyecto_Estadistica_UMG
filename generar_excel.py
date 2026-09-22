import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ==========================================
# 1. CONEXIÓN DIRECTA A GOOGLE DRIVE
# ==========================================
# ID del archivo extraído directamente de la URL de Google Sheets
SPREADSHEET_ID = "1xiU1x2_IV6K-nS0afhPV0zals3_Dh_Ba1xhIF-gztFM"

# Construir la URL de exportación en formato CSV desde Google Drive
url_drive = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid=0"

try:
    # Leer mediciones en tiempo real directamente desde la nube
    df = pd.read_csv(url_drive)
    print("✅ Conexión con Google Drive establecida correctamente.")
except Exception as e:
    print("❌ Error al conectar con Google Drive. Verificar que el acceso general esté como 'Cualquier persona con el enlace'.")
    print(f"Detalle técnico: {e}")
    exit()

# ==========================================
# 2. PROCESAMIENTO Y LIMPIEZA DE DATOS (ETL)
# ==========================================
# Eliminar espacios innecesarios en los encabezados de las columnas
df.columns = df.columns.str.strip()

# Mapear las columnas para estandarizarlas independientemente del formato original
col_map = {}
for col in df.columns:
    c_lower = col.lower()
    if 'descarga' in c_lower: col_map[col] = 'Descarga'
    elif 'subida' in c_lower: col_map[col] = 'Subida'
    elif 'ping' in c_lower: col_map[col] = 'Ping'
    elif 'horario' in c_lower: col_map[col] = 'Horario'
    elif 'fecha' in c_lower: col_map[col] = 'Fecha'
    elif 'hora' in c_lower: col_map[col] = 'Hora'
    elif 'no' in c_lower: col_map[col] = 'No'

df = df.rename(columns=col_map)

# Crear función para limpiar y convertir valores a numéricos (float)
def normalizar_float(val):
    if pd.isna(val) or str(val).strip() == "":
        return None
    val_str = str(val).replace(",", ".").replace(":", ".")
    return float(val_str)

# Aplicar la limpieza numérica a las variables clave
df["Descarga"] = df["Descarga"].apply(normalizar_float)
df["Subida"] = df["Subida"].apply(normalizar_float)
df["Ping"] = df["Ping"].apply(normalizar_float)

# Imputar datos faltantes de las noches mediante la mediana correspondiente al horario
df["Descarga"] = df.groupby("Horario")["Descarga"].transform(lambda x: x.fillna(round(x.median(), 2)))
df["Subida"] = df.groupby("Horario")["Subida"].transform(lambda x: x.fillna(round(x.median(), 2)))
df["Ping"] = df.groupby("Horario")["Ping"].transform(lambda x: x.fillna(round(x.median(), 0)))

# Garantizar la presencia de la columna correlativa para preservar el orden
if "No" not in df.columns or df["No"].isnull().any():
    df["No"] = range(1, len(df) + 1)

# Guardar el archivo CSV depurado para consumo del Dashboard en Streamlit
df.to_csv("mediciones_limpias.csv", index=False)

# ==========================================
# 3. GENERACIÓN DEL EXCEL CON FÓRMULAS NATIVAS
# ==========================================
# Crear el libro y la hoja de trabajo en openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Mediciones y Estadística"

# Definir la paleta de colores y estilos corporativos
font_title = Font(name="Calibri", size=14, bold=True, color="1F4E79")
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
fill_header = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
border_thin = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9")
)

# Colocar el título principal del informe
ws["A1"] = "ANÁLISIS ESTADÍSTICO DE RENDIMIENTO DE INTERNET - UMG"
ws["A1"].font = font_title

# Formatear y escribir la cabecera de la tabla principal de datos
headers = ["No.", "Fecha", "Hora", "Horario", "Descarga (Mbps)", "Subida (Mbps)", "Ping (ms)"]
for col_idx, h in enumerate(headers, 1):
    cell = ws.cell(row=3, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")

# Escribir las mediciones procesadas en las celdas correspondientes
for row_idx, row_data in df.iterrows():
    r = row_idx + 4
    ws.cell(row=r, column=1, value=row_data["No"]).alignment = Alignment(horizontal="center")
    ws.cell(row=r, column=2, value=str(row_data["Fecha"])).alignment = Alignment(horizontal="center")
    ws.cell(row=r, column=3, value=str(row_data["Hora"])).alignment = Alignment(horizontal="center")
    ws.cell(row=r, column=4, value=str(row_data["Horario"])).alignment = Alignment(horizontal="center")
    
    c_d = ws.cell(row=r, column=5, value=row_data["Descarga"])
    c_d.number_format = "0.00"
    
    c_s = ws.cell(row=r, column=6, value=row_data["Subida"])
    c_s.number_format = "0.00"
    
    c_p = ws.cell(row=r, column=7, value=row_data["Ping"])
    c_p.number_format = "0"

    for col in range(1, 8):
        ws.cell(row=r, column=col).border = border_thin

# Configurar la tabla de medidas estadísticas mediante fórmulas nativas en español
ws["I3"] = "Medida Estadística"
ws["J3"] = "Fórmula / Valor"
ws["I3"].font = font_header; ws["I3"].fill = fill_header
ws["J3"].font = font_header; ws["J3"].fill = fill_header

formulas = [
    ("Cantidad de datos (n)", "=CONTAR(E4:E33)"),
    ("Media (Mbps)", "=PROMEDIO(E4:E33)"),
    ("Mediana (Mbps)", "=MEDIANA(E4:E33)"),
    ("Moda (Mbps)", "=MODA.UNO(E4:E33)"),
    ("Valor Mínimo (Mbps)", "=MIN(E4:E33)"),
    ("Valor Máximo (Mbps)", "=MAX(E4:E33)"),
    ("Rango (Mbps)", "=J9-J8"),
    ("Varianza Muestral", "=VAR.S(E4:E33)"),
    ("Desviación Estándar (Mbps)", "=DESVEST.M(E4:E33)"),
    ("Coeficiente de Variación (%)", "=(J12/J5)*100"),
    ("Cuartil 1 (Q1 - Mbps)", "=CUARTIL.INC(E4:E33; 1)"),
    ("Cuartil 2 (Q2 - Mbps)", "=CUARTIL.INC(E4:E33; 2)"),
    ("Cuartil 3 (Q3 - Mbps)", "=CUARTIL.INC(E4:E33; 3)"),
    ("Rango Intercuartílico (IQR)", "=J16-J14")
]

# Insertar las fórmulas y aplicar formato numérico específico según corresponda
for idx, (lbl, fml) in enumerate(formulas, 4):
    ws.cell(row=idx, column=9, value=lbl).border = border_thin
    c = ws.cell(row=idx, column=10, value=fml)
    c.border = border_thin
    if "%" in lbl: c.number_format = "0.00\"%\""
    elif "Cantidad" in lbl: c.number_format = "0"
    else: c.number_format = "0.00"

# Autoajustar los anchos de columnas para garantizar la legibilidad
for col in ws.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

# Guardar el libro de trabajo resultante
wb.save("Proyecto_Estadistica_UMG.xlsx")
print("✅ ¡Sincronización completada! Se generó el archivo 'Proyecto_Estadistica_UMG.xlsx' de forma exitosa.")