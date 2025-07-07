# modelo.py
import numpy as np
import pandas as pd


def preparar_datos(df, planta_id, umbral_similitud=0.1):
    """
    Filtra los datos para una planta específica, elimina valores de PHR consecutivos
    que varíen dentro de un umbral definido, y agrega una columna 'Tiempo' secuencial.
    También mantiene la posición original para rastrear el día real.
    """
    datos = df[df["Random"] == planta_id].copy().reset_index()
    datos.rename(columns={"index": "DiaReal"}, inplace=True)

    diferencia = datos["PHR"].diff().abs()
    diferencia.iloc[0] = np.inf
    mascara = diferencia > umbral_similitud
    datos_filtrados = datos[mascara].reset_index(drop=True)

    datos_filtrados["Tiempo"] = np.arange(len(datos_filtrados))
    return datos_filtrados


def calcular_derivada(datos):
    """
    Agrega columna 'Derivada' al DataFrame con np.gradient sobre 'PHR'.
    """
    datos = datos.copy()
    datos["Derivada"] = np.gradient(datos["PHR"], datos["Tiempo"])
    return datos


def generar_interpretacion(datos_filtrados, df_original=None):
    """
    Retorna el día real con mayor crecimiento y su etapa relativa.
    """
    if df_original is None:
        raise ValueError("Debes proporcionar el DataFrame original para comparar")

    df_original = df_original.copy()
    df_original["Derivada"] = np.gradient(df_original["PHR"].to_numpy())
    idx_max = df_original["Derivada"].idxmax()
    fila_max = df_original.loc[idx_max]

    dia_real = idx_max
    altura = fila_max["PHR"]
    valor_max = fila_max["Derivada"]

    # Buscar en qué etapa del gráfico suavizado (Tiempo) está este día
    if "DiaReal" in datos_filtrados.columns:
        coincidencias = datos_filtrados[datos_filtrados["DiaReal"] == dia_real]
        if not coincidencias.empty:
            etapa_relativa = coincidencias.iloc[0]["Tiempo"]
            etapa_inicio = int(etapa_relativa)
            etapa_fin = etapa_inicio + 1 if etapa_inicio + 1 < len(datos_filtrados) else etapa_inicio
        else:
            etapa_inicio = etapa_fin = etapa_relativa = np.nan
    else:
        etapa_inicio = etapa_fin = etapa_relativa = np.nan

    texto = (
        f"Mayor tasa de crecimiento registrada en el día real {dia_real} (altura: {altura:.2f}),\n"
        f"durante la etapa relativa entre {etapa_inicio} y {etapa_fin}, con un valor aproximado de {valor_max:.2f}."
    )

    coordenadas = (etapa_relativa, altura, valor_max)
    return texto, coordenadas
