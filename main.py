import tkinter as tk
import calendar
from datetime import datetime
import json
import os

# ---------------------------
# CONSTANTES
# ---------------------------
BACKGROUND_COLOR = "#B5EDF5"
ENTRY_BG_COLOR = "#6B6B6B"
ENTRY_WIDTH = 50
MAX_CHAR = 55
ARCHIVO_JSON = "datos_mes.json"  # archivo donde se guardan los valores


# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def get_days_of_month():
    now = datetime.now()
    return calendar.monthrange(now.year, now.month)[1]


def get_month_name():
    now = datetime.now()
    return now.strftime("%B-%Y")

def checar_existencia_mes(validar):

    fecha_mes_anio = validar
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}
    
    if fecha_mes_anio not in datos:
        print("se agrego el mes y año")
        datos[fecha_mes_anio] = {}
    
    


def guardar_json_texto():
    """Guarda todos los valores actuales en el JSON"""
    fecha_mes_anio = get_month_name() # solo obtienes la fecha en mes-año
    checar_existencia_mes(fecha_mes_anio)
    datos = {fecha_mes_anio: {} }
    for dia in dias_mes:
        datos[fecha_mes_anio][str(dia.numero)] = dia.valor

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def limitar_texto(var, dia_obj):
    """Limita los caracteres y actualiza el objeto automáticamente"""
    texto = var.get()
    if len(texto) > MAX_CHAR:
        var.set(texto[:MAX_CHAR])
    dia_obj.valor = var.get()
    guardar_json_texto()  # guardar automáticamente al escribir


def cargar_json():
    """Carga los valores guardados en los objetos Dia"""
    fecha_mes_anio = get_month_name()
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)

        if fecha_mes_anio in datos:
            print("si esta en el json")
            for dia in dias_mes:
                if str(dia.numero) in datos[fecha_mes_anio]:
                    dia.valor = datos[fecha_mes_anio][str(dia.numero)]


# ---------------------------
# CLASES
# ---------------------------
class Dia:
    def __init__(self, numero):
        self.numero = numero
        self.valor = ""  # valor ingresado por el usuario


# ---------------------------
# INICIALIZACIÓN DE DATOS
# ---------------------------
dias_mes = [Dia(i + 1) for i in range(get_days_of_month())]
entradas = []  # lista de tuplas (Dia, Entry)
cargar_json()  # cargar valores existentes

# ---------------------------
# INTERFAZ GRÁFICA
# ---------------------------
window = tk.Tk()
window.title("Notas por día")
window.state("zoomed")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# Título del mes
titulo_mes = tk.Label(
    window,
    text=get_month_name(),
    font=("Arial", 18, "bold"),
    bg=BACKGROUND_COLOR,
    fg="black",
)
titulo_mes.grid(row=0, column=0, pady=(0, 10), sticky="w")

# Contenedor para los días
frame_dias = tk.Frame(window, bg=BACKGROUND_COLOR)
frame_dias.grid(row=1, column=0)

# Generar campos dinámicamente por día
for i, dia_obj in enumerate(dias_mes):
    # Etiqueta del día
    etiqueta = tk.Label(
        frame_dias, text=f"{dia_obj.numero}", width=8, bg=BACKGROUND_COLOR, fg="black"
    )
    etiqueta.grid(row=i, column=0, padx=2, pady=2)

    # Variable para el Entry
    var = tk.StringVar(value=dia_obj.valor)  # cargamos el valor existente
    var.trace_add("write", lambda *args, v=var, d=dia_obj: limitar_texto(v, d))

    # Entry del día
    entry = tk.Entry(
        frame_dias,
        width=ENTRY_WIDTH,
        textvariable=var,
        bg="#FFE5B4",
        fg="#5C4033",
        font=("Arial", 12),
        justify="center",
        highlightthickness=0,
    )
    entry.grid(row=i, column=1, padx=2, pady=2)

    # Guardamos la referencia
    entradas.append((dia_obj, entry))


window.mainloop()
