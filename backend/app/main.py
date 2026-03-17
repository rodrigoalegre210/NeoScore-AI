from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.nucleo.scoring import calcular_score_comercio

import os
import pandas as pd

# Inicializar la aplicación
app = FastAPI(
    title="NeoScore AI API",
    description="Motor de Credit Scoring Conductual para Fintechs",
    version="1.0.0"
)

# Configurar CORS (Vital para conectar con el Frontend en Next.js más adelante)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, aquí iría el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def estado_servidor():
    return {"estado": "en_linea", "mensaje": "NeoScore AI operando correctamente"}

@app.get("/api/v1/score/{id_comercio}")
def obtener_score(id_comercio: str):
    """
    Recibe un ID de comercio y retorna su evaluación de riesgo crediticio.
    """
    resultado = calcular_score_comercio(id_comercio)
    
    if "error" in resultado:
        # Si hay error, devolvemos un código HTTP 404 (No encontrado)
        raise HTTPException(status_code=404, detail=resultado["error"])
        
    return resultado

@app.get("/api/v1/comercios/aleatorio")
def obtener_comercio_aleatorio():
    """
    Endpoint de utilidad para probar el frontend sin tener que buscar IDs manualmente.
    """
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # main.py está en app/. Subimos 2 niveles: app -> backend -> (raíz NeoScore)
    directorio_raiz = os.path.abspath(os.path.join(directorio_actual, "../.."))
    ruta_datos = os.path.join(directorio_raiz, 'data', 'caracteristicas_comercios.csv')
    
    try:
        df = pd.read_csv(ruta_datos)
        id_aleatorio = df['id_comercio'].sample(1).values[0]
        return {"id_comercio": id_aleatorio}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leyendo la base de datos en: {ruta_datos}")