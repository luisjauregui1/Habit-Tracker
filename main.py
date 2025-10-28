# ============================================================
#  PROGRAMA: Registro de notas y hábitos diarios
#  AUTOR: Cyborg Demoníaco 
#  DESCRIPCIÓN:
#     Aplicación Tkinter que permite registrar texto diario,
#     marcar hábitos y guardar los datos automáticamente en JSON.
# ============================================================

# ---------------------------
# IMPORTACIONES
# ---------------------------
from datetime import datetime
import tkinter as tk
import calendar
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
X_INICIO = 560
Y_INICIO = 45
ESPACIO_X = 45   # Separación horizontal entre hábitos
ESPACIO_Y = 29   # Separación vertical entre filas (días)

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

def current_day():
    hoy = datetime.today()
    print("mes:",hoy.month)


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


def guardar_json_CB():
    """
    Guarda el estado booleano (True/False) de todos los checkbuttons en datos_cb.json.
    Se llama automáticamente cada vez que se hace clic en un checkbox.
    """
    global variables_cb
    fecha_mes_anio = get_month_name() # Obtiene 'Mes-Año' [6]
    datos_a_guardar = {}
    
    # 1. Cargar el JSON existente para evitar sobrescribir otros meses
    if os.path.exists(ARCHIVO_CB): # Verifica si el archivo existe [7]
        try:
            with open(ARCHIVO_CB, "r", encoding="utf-8") as f:
                datos_a_guardar = json.load(f)
        except json.JSONDecodeError:
            # Manejar archivo corrupto
            datos_a_guardar = {}
            
    # 2. Recolectar datos del mes actual
    datos_mes_actual = {}
    
    for nombre_habito, dias_vars in variables_cb.items(): 
        datos_mes_actual[nombre_habito] = {}
        
        for dia, var_cb in dias_vars.items():
            # **CLAVE: OBTENER EL VALOR USANDO .get()** [3]
            datos_mes_actual[nombre_habito][dia] = var_cb.get() 
            
    # 3. Actualizar y guardar en el archivo ARCHIVO_CB [4]
    datos_a_guardar[fecha_mes_anio] = datos_mes_actual
    
    with open(ARCHIVO_CB, "w", encoding="utf-8") as f:
        json.dump(datos_a_guardar, f, indent=4, ensure_ascii=False)

def cargar_json_CB():
    """
    Carga los estados booleanos guardados en datos_cb.json y los aplica 
    a las variables de los checkbuttons.
    """
    global variables_cb
    fecha_mes_anio = get_month_name() # [6]
    
    if not os.path.exists(ARCHIVO_CB): # [7]
        datos_iniciales = {}
        try:
            with open(ARCHIVO_CB, "w", encoding="utf-8") as f:
                json.dump(datos_iniciales, f, indent=4, ensure_ascii=False)
        except IOError:
            print(f"Error al intentar crear el archivo {ARCHIVO_CB}")
        return 
        
    else:
        # Lógica de carga para checkbuttons (donde antes estaba 'pass' [13])
        try:
            with open(ARCHIVO_CB, "r", encoding="utf-8") as file:
                datos = json.load(file)
                
            if fecha_mes_anio in datos:
                datos_mes_cb = datos[fecha_mes_anio]
                
                # Iterar sobre la estructura de variables creada en el Paso 4
                for nombre_habito, dias_vars in variables_cb.items():
                    if nombre_habito in datos_mes_cb:
                        datos_habito = datos_mes_cb[nombre_habito]
                        
                        for dia, var_cb in dias_vars.items():
                            if dia in datos_habito:
                                estado_guardado = datos_habito[dia]
                                # **CLAVE: RESTAURAR EL VALOR USANDO .set()** [3]
                                var_cb.set(estado_guardado) 

        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar o decodificar {ARCHIVO_CB}: {e}")

        
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
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master,
            text="",
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

# ---------------------------
# VARIABLES GLOBALES
# ---------------------------

# 1. Estructura para variables BooleanVar (Día x Hábito)
# Inicialización para mapear Hábito -> {Día: tk.BooleanVar}
variables_cb = {} 
# 2. Lista de objetos Dia (ya existente [4])
dias_mes = [] 
# ... (Resto de listas: checkBotton_lista, entradas)

# ============================================================
#                    INICIALIZACIÓN DE DATOS
# ============================================================
dias_mes = [Dia(i + 1) for i in range(get_days_of_month())]
# 1. Inicializar la estructura de variables_cb (Hábito -> {Día: BooleanVar})
variables_cb = {nombre: {} for nombre in NOMBRES_HABITOS}

entradas = []

# Crear lista de checkbuttons para todos los días y hábitos
total_checkbuttons = get_days_of_month() * MAX_HABITOS
checkBotton_lista = [ MinimalCheckbutton(window) for i in range(total_checkbuttons)]

# Cargar datos previos

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
    height=250,
    background=BACKGROUND_COLOR,
    highlightthickness=0
)
canvas_hola_mundo.place(x=X_POSICION_DERECHA, y=Y_POSICION_SUPERIOR)
dibujar_hola_mundo_vertical(canvas_hola_mundo)

# ============================================================
#                  GENERACIÓN DE INTERFAZ DINÁMICA
# ============================================================

current_day()

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
    dia_actual = str(dia_obj.numero) # Número del día

    # --- Generación de 6 hábitos por día ---
    for j in range(MAX_HABITOS):
        cb_index = start_index + j
        checkbox = checkBotton_lista[cb_index]
        
        # 1. Definir el nombre asociado (el hábito)
        nombre_habito = NOMBRES_HABITOS[j]
        
        # 2. Crear la variable booleana de Tkinter [3]
        var_cb = tk.BooleanVar(value=False) 
        
        # 3. Almacenar la variable en la estructura global (Hábito x Día)
        # Esto le da un "nombre asociado" (el hábito y el día) al valor
        variables_cb[nombre_habito][dia_actual] = var_cb 
        
        # 4. Configurar el Checkbutton con la variable y el comando de guardado
        checkbox.config(
            variable=var_cb, # Asociación de variables de widget [2]
            command=guardar_json_CB # Llama a la función de guardado cada vez que se presiona
        )
    
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
# CARGA FINAL DE DATOS Y BUCLE PRINCIPAL
# ============================================================

# Paso 1: Mover la llamada a cargar_json_CB() aquí.
cargar_json_CB() 


# ============================================================
#                      BUCLE PRINCIPAL
# ============================================================
window.mainloop()
