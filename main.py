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
ARCHIVO_JSON = "datos_mes.json"  # archivo donde se guardan los valores de texto
ARCHIVO_JSON_CM = "datos_mes_cm.json"
MAX_HABITOS = 6

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def get_days_of_month():
    """
    ## Obtener días del mes actual

    Retorna el número total de días que tiene el **mes en curso** según la fecha actual.

    ### Returns
    - `int`: Cantidad de días del mes actual.

    ### Ejemplo
    ```python
    dias = get_days_of_month()
    print(dias)  # -> 30 o 31
    ```
    """
    now = datetime.now()
    return calendar.monthrange(now.year, now.month)[1]


def get_month_name():
    """
    ## Nombre del mes y año actual

    Devuelve el **nombre del mes** y el **año actual** en inglés,
    con el formato `Mes-Año`.

    ### Returns
    - `str`: Mes y año (ejemplo: `"September-2025"`).

    ### Ejemplo
    ```python
    mes = get_month_name()
    print(mes)  # -> "September-2025"
    ```
    """
    now = datetime.now()
    return now.strftime("%B-%Y")


def guardar_json_texto():
    """
    ## Guardar datos en JSON

    Guarda el texto escrito por el usuario en un archivo JSON,
    organizando la información por mes y día.

    ### Flujo
    1. Verifica si existe el archivo JSON.  
    2. Si no existe, crea uno nuevo.  
    3. Inserta o actualiza los valores del mes actual.  
    4. Sobrescribe el archivo con la información actualizada.

    ### Estructura del JSON
    ```json
    {
        "September-2025": {
            "1": "Texto del día 1",
            "2": "Texto del día 2"
        }
    }
    ```
    """
    fecha_mes_anio = get_month_name()  # mes-año actual
    # 1. Leer el JSON si existe, o iniciar vacío
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}
    # 2. Actualizar o crear el mes actual
    datos[fecha_mes_anio] = {}
    for dia in dias_mes:
        datos[fecha_mes_anio][str(dia.numero)] = dia.valor
    # 3. Guardar todo de nuevo
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def limitar_texto(var, dia_obj):
    """
    ## Limitar caracteres en entrada

    Restringe la cantidad de caracteres permitidos en el campo de texto
    y actualiza automáticamente el objeto asociado.  
    Además, guarda los cambios en el archivo JSON.

    ### Parámetros
    - `var (tk.StringVar)`: Variable de Tkinter que contiene el texto del día.  
    - `dia_obj (Dia)`: Objeto que representa el día y su valor.

    ### Notas
    - El límite está definido por `MAX_CHAR`.
    - Cada vez que el usuario escribe, se actualiza y guarda en JSON.
    """
    texto = var.get()
    if len(texto) > MAX_CHAR:
        var.set(texto[:MAX_CHAR])
    dia_obj.valor = var.get()
    guardar_json_texto()  # guardar automáticamente al escribir


def cargar_json():
    """
    ## Cargar datos desde JSON

    Lee los datos previamente guardados en el archivo JSON
    y los asigna a cada objeto `Dia` del mes actual.

    ### Flujo
    1. Verifica si el archivo existe.  
    2. Carga los datos si el mes actual está registrado.  
    3. Rellena los valores en cada objeto `Dia`.

    ### Ejemplo
    ```python
    cargar_json()
    print(dias_mes[0].valor)  # -> Texto guardado del día 1
    ```
    """
    fecha_mes_anio = get_month_name()
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as file:
            datos = json.load(file)

        if fecha_mes_anio in datos:
            print("sí está en el JSON")
            for dia in dias_mes:
                if str(dia.numero) in datos[fecha_mes_anio]:
                    dia.valor = datos[fecha_mes_anio][str(dia.numero)]

# ---------------------------
# CLASES
# ---------------------------
class Dia:
    """
    ## Clase Dia

    Representa un día del mes con un número y un valor de texto asociado.

    ### Atributos
    - `numero (int)`: Día del mes.  
    - `valor (str)`: Texto escrito por el usuario para ese día.
    """
    def __init__(self, numero):
        self.numero = numero
        self.valor = ""  # valor ingresado por el usuario


class Check_dia:
    """
    ## Clase Check_dia

    Representa un día con un valor booleano asociado (por ejemplo, un check de hábito).

    ### Atributos
    - `numero (int)`: Día del mes.  
    - `valor (bool | None)`: Valor booleano, inicialmente `None`.
    """
    def __init__(self, numero):
        self.numero = numero
        self.valor = None  # se tiene que almacenar en booleano

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
window.attributes("-zoomed", True)  # esto funciona en Linux, checar en Windows si funciona!
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# Título del mes
titulo_mes = tk.Label(
    window,
    text=f"Mes: {get_month_name()}",
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
    etiqueta = tk.Label(frame_dias, text=f"{dia_obj.numero}", width=8, bg=BACKGROUND_COLOR, fg="black")
    etiqueta.grid(row=i, column=0, padx=2, pady=2)

    dias_check_mark = tk.Label(frame_dias, text=f"{dia_obj.numero}", width=8, bg=BACKGROUND_COLOR, fg="black")
    dias_check_mark.grid(row=i, column=2, padx=50, pady=2)

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
        justify="left",
        highlightthickness=0,
    )
    entry.grid(row=i, column=1, padx=2, pady=2)

    # Guardamos la referencia
    entradas.append((dia_obj, entry))

window.mainloop()
