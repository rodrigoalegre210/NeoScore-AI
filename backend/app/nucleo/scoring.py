import pandas as pd
import math
import os

def calcular_score_comercio(id_comercio: str) -> dict:
    """
    Calcula el NeoScore basado en volumen, estabilidad y riesgo.
    Retorna un diccionario con el score final y el nivel de riesgo.
    """
    # 1. Obtenemos la ruta donde está guardado este archivo (scoring.py)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Subimos 3 niveles: nucleo -> app -> backend -> (llegamos a la raíz NeoScore)
    directorio_raiz = os.path.abspath(os.path.join(directorio_actual, "../../.."))
    
    # 3. Construimos la ruta exacta hacia el CSV
    ruta_datos = os.path.join(directorio_raiz, 'data', 'caracteristicas_comercios.csv')
    
    try:
        df = pd.read_csv(ruta_datos)
    except FileNotFoundError:
        return {"error": f"Base de datos no encontrada en: {ruta_datos}"} # Agregamos la ruta al error para debuggear si falla

    # Buscar el comercio específico
    comercio = df[df['id_comercio'] == id_comercio]
    
    if comercio.empty:
        return {"error": f"Comercio {id_comercio} no encontrado en el historial."}

    # ... (EL RESTO DEL CÓDIGO SE MANTIENE EXACTAMENTE IGUAL) ...

    # Extraer las métricas
    datos = comercio.iloc[0]
    volumen = datos['volumen_total']
    varianza = datos['varianza_ingresos']
    tasa_contracargos = datos['tasa_contracargos']
    tasa_reembolsos = datos['tasa_reembolsos']

    # --- FÓRMULA DEL NEOSCORE ---
    # Partimos de un score base de 500 (sobre 1000)
    score_base = 500
    
    # 1. Bono por volumen de ventas (Máximo 300 puntos)
    bono_volumen = min((volumen / 5000) * 100, 300)
    
    # 2. Penalización por inestabilidad (Varianza alta = ingresos impredecibles)
    penalizacion_inestabilidad = min((varianza / 100) * 10, 150)
    
    # 3. Penalización severa por riesgo (Contracargos y reembolsos matan el score)
    penalizacion_riesgo = (tasa_contracargos * 8000) + (tasa_reembolsos * 3000)

    # Cálculo final
    score_final = score_base + bono_volumen - penalizacion_inestabilidad - penalizacion_riesgo
    
    # Acotar el resultado entre 0 y 1000
    score_final = max(0, min(1000, int(score_final)))

    # Determinar el nivel de riesgo para la Fintech
    if score_final >= 750:
        nivel_riesgo = "Riesgo Bajo (Aprobación Automática)"
    elif score_final >= 400:
        nivel_riesgo = "Riesgo Moderado (Revisión Manual)"
    else:
        nivel_riesgo = "Riesgo Alto (Rechazo)"

    return {
        "id_comercio": id_comercio,
        "neo_score": score_final,
        "clasificacion": nivel_riesgo,
        "desglose_metricas": {
            "volumen_total": float(volumen),
            "tasa_contracargos_pct": round(float(tasa_contracargos) * 100, 2)
        }
    }