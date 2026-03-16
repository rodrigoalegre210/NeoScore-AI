import pandas as pd
import os

def calcular_metricas_comercio():
    ruta_entrada = 'data/transacciones_crudas.csv'
    ruta_salida = 'data/caracteristicas_comercios.csv'
    
    print("--- Iniciando cálculo de métricas (Ingeniería de Características) ---")
    
    # Verificación de seguridad
    if not os.path.exists(ruta_entrada):
        print(f"Error: No se encontró el archivo en {ruta_entrada}. Asegúrate de ejecutar desde la raíz del proyecto.")
        return
        
    # Cargamos los datos
    df = pd.read_csv(ruta_entrada)
    
    # 1. Separamos las transacciones exitosas para las métricas financieras
    df_exitoso = df[df['estado'] == 'EXITO']
    
    # Calculamos Ticket Promedio, Varianza (Desviación Estándar) y Volumen Total
    metricas_ingresos = df_exitoso.groupby('id_comercio').agg(
        ticket_promedio=('monto', 'mean'),
        varianza_ingresos=('monto', 'std'), # Mide la estabilidad de las ventas
        volumen_total=('monto', 'sum')
    ).fillna(0) # Si solo hay 1 transacción, 'std' devuelve NaN. Lo rellenamos con 0.
    
    # 2. Calculamos Tasas de Riesgo sobre el total de transacciones (incluyendo fallidas)
    total_tx = df.groupby('id_comercio').size()
    tx_contracargo = df[df['estado'] == 'CONTRACARGO'].groupby('id_comercio').size()
    tx_reembolso = df[df['estado'] == 'REEMBOLSO'].groupby('id_comercio').size()
    
    # Creamos un DataFrame temporal para el riesgo
    riesgo = pd.DataFrame({
        'total_tx': total_tx,
        'contracargos': tx_contracargo,
        'reembolsos': tx_reembolso
    }).fillna(0) # Llenamos con 0 si un comercio no tiene contracargos/reembolsos
    
    # Calculamos los porcentajes reales
    riesgo['tasa_contracargos'] = riesgo['contracargos'] / riesgo['total_tx']
    riesgo['tasa_reembolsos'] = riesgo['reembolsos'] / riesgo['total_tx']
    
    # 3. Unimos las métricas financieras con métricas de riesgo
    metricas_finales = metricas_ingresos.join(riesgo[['tasa_contracargos', 'tasa_reembolsos']])
    
    # Recuperamos el perfil real (estable, volatil, alto_riesgo) para usarlo al entrenar la IA
    perfiles = df[['id_comercio', 'perfil_comercio_real']].drop_duplicates().set_index('id_comercio')
    metricas_finales = metricas_finales.join(perfiles)
    
    # Limpiamos y preparamos para exportar
    metricas_finales = metricas_finales.round(4).reset_index()
    
    # Guardamos el nuevo dataset
    metricas_finales.to_csv(ruta_salida, index=False)
    print(f"Características calculadas exitosamente para {len(metricas_finales)} comercios.")
    print(f"Archivo consolidado guardado en: {ruta_salida}")
    
    return metricas_finales

if __name__ == "__main__":
    calcular_metricas_comercio()