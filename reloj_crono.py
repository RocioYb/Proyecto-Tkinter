import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import pytz
# -------------------------------------
# Ventana principal
# -------------------------------------
ventana = tk.Tk()
ventana.title("Reloj Mundial / Cronometro")
ventana.geometry("700x600")
ventana.config(bg="#1a1a1a")

# Variables globales
modo = "reloj"
corriendo = False
inicio_tiempo = 0
tiempo_transcurrido = 0

# -------------------------------------
# Función para limpiar todo lo que haya en la ventana
# -------------------------------------
def limpiar():
    for widget in ventana.winfo_children():
        widget.destroy()

# -------------------------------------
# Quitar atajos anteriores
# -------------------------------------
def limpiar_atajos():
    for tecla in ["<space>", "p", "r", "<Return>", "m"]:
        ventana.unbind(tecla)

# -------------------------------------
# Vista del reloj mundial
# -------------------------------------
def vista_reloj():
    limpiar()
    limpiar_atajos()
    global modo
    modo = "reloj"

    tk.Label(ventana, text="Reloj Mundial", font=("Arial", 20, "bold"), bg="#1a1a1a", fg="white").pack(pady=10)

    # Zonas horarias
    zonas = {
        "Buenos Aires": "America/Argentina/Buenos_Aires",
        "Nueva York": "America/New_York",
        "Londres": "Europe/London",
        "Tokio": "Asia/Tokyo",
        "Sidney": "Australia/Sydney"
    }

    seleccion = tk.StringVar(value="Buenos Aires")
    menu = ttk.Combobox(ventana, values=list(zonas.keys()), textvariable=seleccion, font=("Arial", 12))
    menu.pack(pady=10)

    reloj = tk.Label(ventana, font=("Arial", 60, "bold"), bg="#1a1a1a", fg="white")
    fecha = tk.Label(ventana, font=("Arial", 16), bg="#1a1a1a", fg="white")
    reloj.pack(pady=10)
    fecha.pack()
   
    # Actualiza la hora cada segundo
    def actualizar_hora():
        if modo != "reloj":
            return
        ciudad = seleccion.get()
        zona = pytz.timezone(zonas[ciudad])
        ahora = datetime.now(zona)
        reloj.config(text=ahora.strftime("%H:%M:%S"))
        fecha.config(text=ahora.strftime("%A, %d %B %Y"))
        ventana.after(1000, actualizar_hora)

    actualizar_hora()

    # Botón para ir al cronometro
    tk.Button(
        ventana,
        text=" Ir al Cronómetro (Tecla M)",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="black",
        command=vista_cronometro
    ).pack(pady=20)

    # Atajo con la tecla M
    ventana.bind("m", lambda e: vista_cronometro())

# -------------------------------------
# Vista del cronómetro con vueltas
# -------------------------------------
def vista_cronometro():
    limpiar()
    limpiar_atajos()
    global modo, corriendo, inicio_tiempo, tiempo_transcurrido
    modo = "cronometro"

    tk.Label(ventana, text=" Cronómetro", font=("Arial", 20, "bold"), bg="#1a1a1a", fg="white").pack(pady=10)

    # Etiqueta que muestra el tiempo
    reloj = tk.Label(ventana, text="00:00:00.000", font=("Arial", 50, "bold"), bg="#1a1a1a", fg="white")
    reloj.pack(pady=20)

    # Frame y lista para vueltas
    frame_vueltas = tk.Frame(ventana, bg="#1a1a1a")
    frame_vueltas.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame_vueltas)
    scrollbar.pack(side="right", fill="y")

    lista_vueltas = tk.Listbox(
        frame_vueltas,
        yscrollcommand=scrollbar.set,
        font=("Arial", 12),
        fg="black",
        height=10
    )
    lista_vueltas.pack(fill="both", expand=True)
    scrollbar.config(command=lista_vueltas.yview)

    # Funciones internas del cronometro
    def actualizar():
        if corriendo and modo == "cronometro":
            tiempo = time.time() - inicio_tiempo + tiempo_transcurrido
            horas = int(tiempo // 3600)
            minutos = int((tiempo % 3600) // 60)
            segundos = int(tiempo % 60)
            milesimas = int((tiempo - int(tiempo)) * 1000)
            reloj.config(text=f"{horas:02d}:{minutos:02d}:{segundos:02d}.{milesimas:03d}")
            ventana.after(10, actualizar)

    def iniciar(event=None):
        global corriendo, inicio_tiempo
        if not corriendo:
            corriendo = True
            inicio_tiempo = time.time()
            actualizar()

    def parar(event=None):
        global corriendo, tiempo_transcurrido
        if corriendo:
            corriendo = False
            tiempo_transcurrido += time.time() - inicio_tiempo

    def reiniciar(event=None):
        global corriendo, inicio_tiempo, tiempo_transcurrido
        corriendo = False
        inicio_tiempo = 0
        tiempo_transcurrido = 0
        reloj.config(text="00:00:00.000")
        lista_vueltas.delete(0, tk.END)

    def parcial(event=None):
        tiempo_actual = reloj.cget("text")
        lista_vueltas.insert(tk.END, f"Vuelta {lista_vueltas.size() + 1}: {tiempo_actual}")

    # Botones
    frame_botones = tk.Frame(ventana, bg="#1a1a1a")
    frame_botones.pack(pady=10)

    # Instrucciones de atajos de teclado
    instrucciones = tk.Label(
        ventana, 
        text="Atajos: Iniciar (**Espacio**) | Parar (**P**) | Reiniciar (**R**) | Tiempo Parcial (**Enter**) | volver (**M**)", 
        font=("Arial", 10, "bold"), 
        bg="#1a1a1a", 
        fg="#00aaff"
    )
    instrucciones.pack(pady=5)

    tk.Button(frame_botones, text=" Iniciar", width=10, command=iniciar, bg="black", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
    tk.Button(frame_botones, text="Parar", width=10, command=parar, bg="black", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)
    tk.Button(frame_botones, text="Reiniciar ", width=10, command=reiniciar, bg="black", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10)
    tk.Button(frame_botones, text="Parcial", width=10, command=parcial, bg="black", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=10)

    # Botón para volver al reloj
    tk.Button(
        ventana,
        text="Volver al Reloj Mundial",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="black",
        command=vista_reloj
    ).pack(pady=20)

    # Atajos de teclado
    ventana.bind("<space>", iniciar)
    ventana.bind("p", parar)
    ventana.bind("r", reiniciar)
    ventana.bind("<Return>", parcial)
    ventana.bind("m", lambda e: vista_reloj())

# -------------------------------------
# Arranca en modo reloj
# -------------------------------------
vista_reloj()
ventana.mainloop()