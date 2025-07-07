# 🌱 Análisis de Crecimiento de Plantas

Este proyecto permite visualizar el crecimiento de plantas a través de una interfaz gráfica interactiva creada en `Tkinter`. El gráfico muestra la altura (`PHR`) de la planta a lo largo del tiempo, suaviza las curvas con interpolación cúbica (`scipy`), calcula derivadas para identificar momentos de mayor crecimiento, y destaca visualmente la etapa de cambio más significativa.

---

## 📋 Características principales

- Interfaz gráfica intuitiva con `Tkinter`
- Carga dinámica de datos desde archivo `.csv`
- Suavizado de curvas con `make_interp_spline` (`scipy`)
- Cálculo de derivadas numéricas para detección de máximos de crecimiento
- Identificación del día real de mayor tasa de crecimiento
- Agrupación de etapas similares para reducir ruido visual
- Gráfico interactivo embebido en la GUI

---

## 📁 Estructura del proyecto

├── main.py # Lógica de la interfaz gráfica
├── modelo.py # Procesamiento de datos, derivadas y análisis
├── dataset.csv # Archivo con los datos de las plantas (entrada)
├── README.md # Este documento
└── requirements.txt # Archivo con dependencias (opcional)


---

## ⚙️ Requisitos

- Python 3.10 o superior
- pip (administrador de paquetes)
- Sistema operativo Windows / Linux / macOS

---

## 🧪 Instalación

### 1. Clonar o descargar este repositorio

```bash
git clone https://github.com/tunombre/crecimiento-plantas.git
cd crecimiento-plantas
```
### 2. Crear entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
```
### 3. Activar entorno virtual
- En Windows:
```bash
venv\Scripts\activate
```
- En Linux / macOS:
```bash
source venv/bin/activate
```
### 4. Activar entorno virtual
```bash
pip install -r requirements.txt
```
## 🚀 Ejecución de la aplicación

Asegúrate de tener dataset.csv en la misma carpeta que main.py. Luego:
```bash
python main.py
```
## 🧠 Descripción técnica del funcionamiento

Carga de datos desde dataset.csv, que debe tener al menos dos columnas:

- Random: identificador de la planta
- PHR: altura registrada (Promedio de la altura relativa)

Se filtran las alturas consecutivas que cambian poco, usando un umbral de similitud (umbral_similitud).

Se genera una nueva columna Tiempo que representa etapas significativas de cambio.

Se calcula la derivada de PHR con numpy.gradient.

Se identifica el punto de mayor crecimiento, en base al valor máximo de la derivada en el dataset original (sin filtrar).

Se grafica:
- Altura original suavizada (PHR)
- Derivada de crecimiento
- Punto de máximo crecimiento resaltado en rojo

Se entrega una interpretación textual automática indicando:
- Día real donde ocurrió el máximo crecimiento
- Altura en ese momento
- Intervalo relativo de etapas gráficas donde ocurrió el cambio
