# 🚀 NeoScore AI: Motor de Credit Scoring Conductual

NeoScore AI es un sistema de evaluación de riesgo crediticio diseñado para el ecosistema Fintech. A diferencia de los burós de crédito tradicionales, NeoScore analiza el **comportamiento transaccional real** de un comercio (volumen de ventas, estabilidad de ingresos, tasas de contracargos y reembolsos) para generar un score de confianza dinámico.

## 🎯 El Problema que Resuelve
Muchas pasarelas de pago y empresas de préstamos descartan comercios rentables porque no tienen un historial crediticio bancario formal. NeoScore transforma la data cruda de transacciones en un indicador de riesgo procesable, permitiendo aprobaciones de crédito más justas y seguras basadas en el flujo de caja real.

## 🏗️ Arquitectura del Proyecto

El proyecto está dividido en un motor analítico (Backend) y un panel de visualización (Frontend):

* **Motor de Datos (Python/Pandas):** Generación de datos sintéticos y pipeline de *Feature Engineering* para calcular métricas clave (Varianza de ingresos, tasas de fraude).
* **Core API (FastAPI):** Microservicio ultrarrápido que procesa las métricas a través de un algoritmo de ponderación y devuelve un Score de 0 a 1000.
* **Dashboard (Next.js + Tailwind CSS):** Interfaz de usuario minimalista para que los analistas de riesgo consulten el estado de un comercio en tiempo real.

## ⚙️ Cómo ejecutarlo localmente

### 1. Backend (FastAPI)
\`\`\`bash
# Instalar dependencias
pip install fastapi "uvicorn[standard]" pandas numpy

# Generar datos y características
python backend/aplicacion/datos/generador.py
python backend/aplicacion/datos/caracteristicas.py

# Levantar el servidor
uvicorn backend.aplicacion.principal:app --reload
\`\`\`

### 2. Frontend (Next.js)
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`
El dashboard estará disponible en `http://localhost:3000`.

## 📈 Escalabilidad Futura
* Integración de modelos de Machine Learning (Random Forest) para predecir la probabilidad de *default*.
* Conexión con Webhooks para automatizar la retención o liberación de fondos.