# main.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
from modelo import preparar_datos, calcular_derivada, generar_interpretacion

# === Cargar dataset ===
df = pd.read_csv("dataset.csv", sep=";")  # Cargar con separador correcto

# === Crear ventana principal ===
root = tk.Tk()
root.title("Análisis de Crecimiento de Plantas")
root.geometry("900x700")

# === Frame superior: selección ===
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Selecciona una planta:").pack(side=tk.LEFT, padx=5)

planta_var = tk.StringVar()
combobox_plantas = ttk.Combobox(frame_top, textvariable=planta_var, state="readonly")
combobox_plantas['values'] = df["Random"].unique().tolist()
combobox_plantas.current(0)
combobox_plantas.pack(side=tk.LEFT, padx=5)

def mostrar_grafico():
    planta = planta_var.get()
    datos = preparar_datos(df, planta)
    datos = calcular_derivada(datos)

    # Suavizado para gráfica (curvas suaves)
    x = datos["Tiempo"]
    y_phr = datos["PHR"]
    y_derivada = datos["Derivada"]

    if len(x) >= 4:  # solo si hay suficientes puntos
        x_smooth = np.linspace(x.min(), x.max(), 300)
        phr_spline = make_interp_spline(x, y_phr)(x_smooth)
        der_spline = make_interp_spline(x, y_derivada)(x_smooth)
    else:
        x_smooth = x
        phr_spline = y_phr
        der_spline = y_derivada

    # Limpiar gráfico anterior
    ax.clear()
    ax.plot(x_smooth, phr_spline, label="PHR (Altura)", linewidth=2)
    ax.plot(x_smooth, der_spline, label="Derivada", linestyle='--', linewidth=2)
    ax.set_title(f"Planta {planta}")
    ax.set_xlabel("Etapas de crecimiento (cambios significativos)")
    ax.set_ylabel("Valor")
    ax.legend()
    ax.grid(True)
    texto, coords = generar_interpretacion(datos, df[df["Random"] == planta])
    t, h, _ = coords
    ax.plot(t, h, "ro")
    ax.annotate("Máx crecimiento", xy=(t, h), xytext=(t + 0.3, h + 5),
                arrowprops=dict(arrowstyle="->", color="red"), color="red")
    
    canvas.draw()

    # Interpretación simple
    texto_interpretacion.delete("1.0", tk.END)
    texto_interpretacion.insert(tk.END, texto)

# Botón
boton_mostrar = tk.Button(frame_top, text="Mostrar gráfica", command=mostrar_grafico)
boton_mostrar.pack(side=tk.LEFT, padx=10)

# === Frame del gráfico ===
frame_grafico = tk.Frame(root)
frame_grafico.pack(pady=10, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# === Frame de interpretación ===
frame_texto = tk.Frame(root)
frame_texto.pack(pady=10, fill=tk.X)

tk.Label(frame_texto, text="Interpretación del crecimiento:", anchor="w").pack(fill=tk.X, padx=10)
texto_interpretacion = tk.Text(frame_texto, height=4)
texto_interpretacion.pack(fill=tk.X, padx=10)

def cerrar_app():
    plt.close('all')
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", cerrar_app)

root.mainloop()
