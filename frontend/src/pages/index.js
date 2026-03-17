import { useState } from 'react';

export default function DashboardScore() {
  const [idComercio, setIdComercio] = useState('');
  const [datosScore, setDatosScore] = useState(null);
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);

  const consultarScore = async (e) => {
    e.preventDefault();
    if (!idComercio) return;

    setCargando(true);
    setError('');
    setDatosScore(null);

    try {
      const respuesta = await fetch(`http://127.0.0.1:8000/api/v1/score/${idComercio}`);
      
      if (!respuesta.ok) {
        throw new Error('No se pudo encontrar el historial de este comercio.');
      }

      const datos = await respuesta.json();
      setDatosScore(datos);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-800">
      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8 border border-gray-100">
        <h1 className="text-3xl font-bold text-blue-900 mb-2">NeoScore AI</h1>
        <p className="text-gray-500 mb-6">Motor de Evaluación de Riesgo Conductual</p>

        {/* Formulario de búsqueda */}
        <form onSubmit={consultarScore} className="flex gap-4 mb-8">
          <input
            type="text"
            placeholder="Ej: COM-C5D4054C"
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={idComercio}
            onChange={(e) => setIdComercio(e.target.value)}
          />
          <button
            type="submit"
            disabled={cargando}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:bg-blue-300"
          >
            {cargando ? 'Evaluando...' : 'Evaluar Riesgo'}
          </button>
        </form>

        {/* Manejo de Errores */}
        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-6 border border-red-200">
            {error}
          </div>
        )}

        {/* Resultados del Score */}
        {datosScore && (
          <div className="animate-fade-in">
            <div className="bg-blue-50 rounded-xl p-6 mb-6 text-center border border-blue-100">
              <h2 className="text-sm font-semibold text-blue-800 uppercase tracking-wider mb-2">Score de Confianza</h2>
              <div className="text-6xl font-black text-blue-900 mb-2">
                {datosScore.neo_score} <span className="text-2xl text-blue-400">/ 1000</span>
              </div>
              <div className={`inline-block px-4 py-1 rounded-full text-sm font-bold ${
                datosScore.neo_score >= 750 ? 'bg-green-100 text-green-800' :
                datosScore.neo_score >= 400 ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {datosScore.clasificacion}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-100">
                <div className="text-sm text-gray-500 mb-1">Volumen Total Procesado</div>
                <div className="text-xl font-bold text-gray-800">
                  ${datosScore.desglose_metricas.volumen_total.toLocaleString()}
                </div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-100">
                <div className="text-sm text-gray-500 mb-1">Tasa de Contracargos</div>
                <div className="text-xl font-bold text-gray-800">
                  {datosScore.desglose_metricas.tasa_contracargos_pct}%
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}