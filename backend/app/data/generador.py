import pandas as pd
import numpy as np
import uuid
import random
import os

from datetime import datetime, timedelta

def generar_datos_fintech(n_comercios = 50, dias_atras = 90):

    datos = []
    categorias = ['Minorista', 'Software', 'Gastronomia', 'Electronica', 'Servicios']

    print(f"--- Iniciando generación de datos para {n_comercios} comercios ---")

    for _ in range(n_comercios):
        id_comercio = f"COM-{str(uuid.uuid4())[:8].upper()}"
        categoria = random.choice(categorias)

        # Perfil del comercio (determina su riesgo futuro)
        perfil = random.choice(['estable', 'volatil', 'alto_riesgo'])

        # Definimos los parámetros según perfil.
        if perfil == 'estable':
            promedio_ventas_diarias = random.randint(10, 20)
            tasa_reembolso = 0.02
            tasa_contracargo = 0.005

        elif perfil == 'volatil':
            promedio_ventas_diarias = random.randint(5, 30)
            tasa_reembolso = 0.08
            tasa_contracargo = 0.02
        
        else: # alto_riesgo
            promedio_ventas_diarias = random.randint(2, 10)
            tasa_reembolso = 0.15
            tasa_contracargo = 0.05

        # Generamos transacciones para los últimos X días
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days = dias_atras)

        fecha_actual = fecha_inicio
        while fecha_actual <= fecha_fin:
            # Número de ventas hoy (con ruido estadístico)
            n_ventas = max(0, int(np.random.normal(promedio_ventas_diarias, promedio_ventas_diarias * 0.3)))

            for _ in range(n_ventas):
                monto = round(random.uniform(10.0, 500.0), 2)

                # Determinamos el estado de la transacción
                rand = random.random()
                if rand < tasa_contracargo:
                    estado = 'CONTRACARGO'
                
                elif rand < (tasa_contracargo + tasa_reembolso):
                    estado = 'REEMBOLSO'
                
                else:
                    estado = 'EXITO'

                datos.append({
                    'id_transaccion': str(uuid.uuid4()),
                    'id_comercio': id_comercio,
                    'categoria': categoria,
                    'monto': monto,
                    'fecha_hora': fecha_actual + timedelta(minutes = random.randint(0, 1440)),
                    'estado': estado,
                    'perfil_comercio_real': perfil # Solo para validar el modelo
                })

            fecha_actual += timedelta(days = 1)

    df = pd.DataFrame(datos)

    ruta_guardado = 'data/transacciones_crudas.csv'

    # Creamos un directorio si no existe (manejando rutas relativas)
    os.makedirs(os.path.dirname(ruta_guardado), exist_ok = True)

    df.to_csv(ruta_guardado, index = False)
    print(f"Dataset generado con {len(df)} transacciones.")
    return df

if __name__ == "__main__":
    generar_datos_fintech()