# ============================================================
#  PROGRAMA: Registro de notas y hábitos diarios
#  AUTOR: Usuario original
#  DESCRIPCIÓN:
#     Aplicación Tkinter que permite registrar texto diario,
#     marcar hábitos y guardar los datos automáticamente en JSON.
# ============================================================

# ---------------------------
# IMPORTACIONES
# ---------------------------
import tkinter as tk
import calendar
from datetime import datetime
import json
import os
import platform

# ============================================================
#                      CONFIGURACIÓN GENERAL
# ============================================================

# --- Colores y estilo ---
BACKGROUND_COLOR = "#D8BFA6"
ENTRY_BG_COLOR = "#6B6B6B"

# --- Parámetros visuales ---
ENTRY_WIDTH = 52
MAX_CHAR = 62

# --- Archivos de almacenamiento ---
ARCHIVO_JSON = "datos_mes.json"   # Guarda texto de cada día
ARCHIVO_CB = "datos_cb.json"      # Guarda valores booleanos de hábitos

# --- Parámetros lógicos ---
MAX_HABITOS = 6
NOMBRES_HABITOS = ["Hábito 1", "Hábito 2", "Hábito 3", "Hábito 4", "Hábito 5", "Hábito 6"]

# --- Posiciones iniciales para checkbuttons ---
X_INICIO = 580
Y_INICIO = 60
ESPACIO_X = 45   # Separación horizontal entre hábitos
ESPACIO_Y = 28   # Separación vertical entre filas (días)

# ============================================================
#                     FUNCIONES AUXILIARES
# ============================================================

def get_days_of_month():
    """
    Retorna el número total de días del mes actual.
    """
    now = datetime.now()
    return calendar.monthrange(now.year, now.month)[1]


def get_month_name():
    """
    Devuelve el nombre del mes y año actual en formato 'Mes-Año'.
    Ejemplo: 'October-2025'
    """
    now = datetime.now()
    return now.strftime("%B-%Y")


# ---------------------------
# FUNCIONES DE MANEJO DE DATOS
# ---------------------------

def guardar_json_texto():
    """
    Guarda los textos escritos por el usuario en un archivo JSON
    bajo la estructura:
    {
        "Mes-Año": {
            "1": "Texto del día 1",
            "2": "Texto del día 2"
        }
    }
    """
    fecha_mes_anio = get_month_name()

    # Leer JSON existente o crear uno nuevo
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}

    # Actualizar datos del mes actual
    datos[fecha_mes_anio] = {}
    for dia in dias_mes:
        datos[fecha_mes_anio][str(dia.numero)] = dia.valor

    # Guardar cambios
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def limitar_texto(var, dia_obj):
    """
    Limita la cantidad de caracteres permitidos en una entrada,
    convierte a minúsculas y actualiza automáticamente el JSON.
    """
    texto = var.get()
    texto_minus = texto.lower()

    # Convertir automáticamente a minúsculas
    if texto != texto_minus:
        var.set(texto_minus)
        texto = var.get()

    # Limitar longitud
    if len(texto) > MAX_CHAR:
        var.set(texto[:MAX_CHAR])

    # Guardar en memoria y JSON
    dia_obj.valor = var.get()
    guardar_json_texto()


def cargar_json():
    """
    Carga los datos guardados del archivo JSON para el mes actual.
    """
    fecha_mes_anio = get_month_name()
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as file:
            datos = json.load(file)
        if fecha_mes_anio in datos:
            for dia in dias_mes:
                if str(dia.numero) in datos[fecha_mes_anio]:
                    dia.valor = datos[fecha_mes_anio][str(dia.numero)]


def cargar_json_CB():
    """
    Crea o valida el archivo JSON de los checkbuttons.
    Si no existe, lo genera vacío.
    """
    if not os.path.exists(ARCHIVO_CB):
        datos_iniciales = {}
        try:
            with open(ARCHIVO_CB, "w", encoding="utf-8") as f:
                json.dump(datos_iniciales, f, indent=4, ensure_ascii=False)
        except IOError:
            print(f"Error al intentar crear el archivo {ARCHIVO_CB}")
    else:
        # Pendiente: lógica de carga para checkbuttons
        pass


# ============================================================
#                    FUNCIONES DE DIBUJO (CANVAS)
# ============================================================

def dibujar_hola_mundo_vertical(canvas):
    """
    Dibuja el texto "HOLA MUNDO" verticalmente de arriba hacia abajo
    en el canvas indicado.
    """
    palabra = "HOLA MUNDO"
    x_pos = 15
    start_y = 30
    line_height = 25

    for char in palabra:
        if char == ' ':
            start_y += line_height
            continue

        canvas.create_text(
            x_pos,
            start_y,
            text=char,
            font=("Arial", 14, "bold"),
            fill="#000000",
            anchor="center"
        )
        start_y += line_height


# ============================================================
#                         CLASES
# ============================================================

class Dia:
    """
    Representa un día del mes con número y texto asociado.
    """
    def __init__(self, numero):
        self.numero = numero
        self.valor = ""


class MinimalCheckbutton(tk.Checkbutton):
    """
    Checkbutton personalizado para representar los hábitos diarios.
    """
    def __init__(self, master=None, dia_numero=None, **kwargs):
        super().__init__(
            master,
            text=dia_numero,
            width=0,
            bg="#D8BFA6",
            selectcolor="#D8BFA6",
            highlightthickness=0,
            relief="flat",
            anchor="center",
            **kwargs,
        )


# ============================================================
#                     INTERFAZ GRÁFICA PRINCIPAL
# ============================================================

# --- Ventana principal ---
window = tk.Tk()
window.title("Notas por día")

# Maximizar ventana dependiendo del SO
if platform.system() == "Windows":
    window.state("zoomed")
else:
    window.attributes("-zoomed", True)

window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# --- Contenedor principal ---
frame_dias = tk.Frame(window, bg=BACKGROUND_COLOR)
frame_dias.grid(row=1, column=0)

# ============================================================
#                    INICIALIZACIÓN DE DATOS
# ============================================================

dias_mes = [Dia(i + 1) for i in range(get_days_of_month())]
entradas = []

# Crear lista de checkbuttons para todos los días y hábitos
total_checkbuttons = get_days_of_month() * MAX_HABITOS
checkBotton_lista = [
    MinimalCheckbutton(window, dia_numero=(i // MAX_HABITOS) + 1)
    for i in range(total_checkbuttons)
]

# Cargar datos previos
cargar_json_CB()
cargar_json()

# ============================================================
#                        ELEMENTOS DE INTERFAZ
# ============================================================

# --- Título del mes ---
titulo_mes = tk.Label(
    window,
    text=f"Mes: {get_month_name()}",
    font=("Arial", 18, "bold"),
    bg=BACKGROUND_COLOR,
    fg="black",
)
titulo_mes.grid(row=0, column=0, pady=(0, 10), sticky="w")

# --- Posiciones base ---
current_y = Y_INICIO

# --- Texto vertical "HOLA MUNDO" ---
X_POSICION_DERECHA = 1200
Y_POSICION_SUPERIOR = 10

canvas_hola_mundo = tk.Canvas(
    window,
    width=30,
    height=200,
    background=BACKGROUND_COLOR,
    highlightthickness=0
)
canvas_hola_mundo.place(x=X_POSICION_DERECHA, y=Y_POSICION_SUPERIOR)
dibujar_hola_mundo_vertical(canvas_hola_mundo)

# ============================================================
#                  GENERACIÓN DE INTERFAZ DINÁMICA
# ============================================================

for i, dia_obj in enumerate(dias_mes):
    # --- Etiqueta del día ---
    etiqueta = tk.Label(
        frame_dias,
        text=f"{dia_obj.numero}",
        width=4,
        bg=BACKGROUND_COLOR,
        fg="black",
        anchor="center",
        relief="groove",
    )
    etiqueta.grid(row=i, column=0, padx=2, pady=2)

    # --- Variable del Entry ---
    var = tk.StringVar(value=dia_obj.valor)
    var.trace_add("write", lambda *args, v=var, d=dia_obj: limitar_texto(v, d))

    # --- Posición inicial para los checkbuttons ---
    current_x = X_INICIO
    start_index = i * MAX_HABITOS

    # --- Generación de 6 hábitos por día ---
    for j in range(MAX_HABITOS):
        cb_index = start_index + j
        checkbox = checkBotton_lista[cb_index]
        checkbox.place(x=current_x, y=current_y)
        current_x += ESPACIO_X

    # --- Ajustar salto de línea entre días ---
    current_y += ESPACIO_Y

    # --- Campo de entrada (Entry) ---
    entry = tk.Entry(
        frame_dias,
        width=ENTRY_WIDTH,
        textvariable=var,
        bd=2,
        bg="#A37864",
        fg="#000000",
        font=("Arial", 12),
        justify="left",
        relief="flat",
        highlightthickness=0,
    )
    entry.grid(row=i, column=1, padx=2, pady=2)

    # Guardar referencia del entry y su día
    entradas.append((dia_obj, entry))

# ============================================================
#                      BUCLE PRINCIPAL
# ============================================================
window.mainloop()
