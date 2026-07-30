import React from 'react';
import { Zap, SlidersHorizontal, Terminal, Ruler } from 'lucide-react';

export default function Header({ 
  activeFilter, 
  setActiveFilter, 
  onOpenQuestions, 
  onOpenSizeGuide, 
  onOpenTerminal,
  onRunScan,
  isScanning,
  totalModelsCount
}) {
  return (
    <header className="fade-in mb-8">
      {/* Top Banner */}
      <div className="glass-panel p-6 mb-6 relative overflow-hidden">
        <div className="absolute -right-16 -top-16 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute right-32 -bottom-20 w-64 h-64 bg-orange-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 relative z-10">
          <div>
            <div className="flex items-center gap-3 mb-2 flex-wrap">
              <span className="badge-glow flex items-center gap-1.5">
                <span className="live-indicator"></span> Agente Inteligente Activo
              </span>
              <span className="bg-blue-900/60 text-blue-300 text-xs px-3 py-1 rounded-full border border-blue-600/50 font-semibold flex items-center gap-1">
                💙 Integración Decathlon España
              </span>
              <span className="bg-slate-800 text-slate-300 text-xs px-3 py-1 rounded-full border border-slate-700 font-mono">
                Talla 42.5 EU / US 9
              </span>
            </div>
            
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-2">
              Buscador de Zapatillas <span className="text-gradient">Agente Decathlon & ASICS</span>
            </h1>
            <p className="text-slate-400 text-sm sm:text-base max-w-2xl">
              Agente autónomo de escaneo multi-tienda configurado para tu perfil: 
              <strong className="text-slate-200"> 10 km por sesión</strong>, ritmo de 
              <strong className="text-slate-200"> 5:15 min/km</strong> y 
              <strong className="text-slate-200"> 3 salidas/semana</strong> en talla <strong className="text-cyan-400">42.5 EU</strong>.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 w-full lg:w-auto">
            <button 
              onClick={onRunScan}
              disabled={isScanning}
              className="btn-primary flex-1 sm:flex-none justify-center"
              id="btn-scan-stores"
            >
              <Zap className={`w-4 h-4 ${isScanning ? 'animate-spin' : ''}`} />
              {isScanning ? 'Escaneando Tiendas...' : 'Re-Escanear Decathlon & Tiendas'}
            </button>

            <button 
              onClick={onOpenQuestions}
              className="btn-secondary flex-1 sm:flex-none justify-center"
              id="btn-open-questions"
            >
              <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
              Afinar Preguntas
            </button>

            <button 
              onClick={onOpenSizeGuide}
              className="btn-secondary px-3"
              title="Guía de Talla 42.5 EU"
              id="btn-size-guide"
            >
              <Ruler className="w-4 h-4 text-amber-400" />
            </button>

            <button 
              onClick={onOpenTerminal}
              className="btn-secondary px-3"
              title="Ver Script de Agente en Python CLI"
              id="btn-python-cli"
            >
              <Terminal className="w-4 h-4 text-emerald-400" />
            </button>
          </div>
        </div>

        {/* Profile Stats Bar */}
        <div className="mt-6 pt-5 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs sm:text-sm">
          <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
            <span className="text-slate-500 block text-xs">Distancia Habitual</span>
            <span className="font-semibold text-slate-200 flex items-center gap-1 mt-0.5">
              🏃 10 km por sesión
            </span>
          </div>
          <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
            <span className="text-slate-500 block text-xs">Ritmo Objetivo</span>
            <span className="font-semibold text-cyan-400 flex items-center gap-1 mt-0.5 font-mono">
              ⚡ 5:15 min/km (Medio-Ágil)
            </span>
          </div>
          <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
            <span className="text-slate-500 block text-xs">Motor de Búsqueda</span>
            <span className="font-semibold text-blue-400 flex items-center gap-1 mt-0.5">
              💙 Decathlon + ASICS Outlet
            </span>
          </div>
          <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
            <span className="text-slate-500 block text-xs">Talla Filtro Estricto</span>
            <span className="font-semibold text-orange-400 flex items-center gap-1 mt-0.5 font-mono">
              👟 42.5 EU (27.0 cm / US 9)
            </span>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        <button
          onClick={() => setActiveFilter('all')}
          className={`px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
            activeFilter === 'all'
              ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-slate-700/60'
          }`}
          id="filter-all"
        >
          Todas las Opciones ({totalModelsCount})
        </button>
        <button
          onClick={() => setActiveFilter('decathlon')}
          className={`px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-1.5 ${
            activeFilter === 'decathlon'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30 ring-2 ring-blue-400'
              : 'bg-blue-950/40 text-blue-300 hover:bg-blue-900/60 border border-blue-700/60'
          }`}
          id="filter-decathlon"
        >
          💙 Ofertas Decathlon & Similares
        </button>
        <button
          onClick={() => setActiveFilter('chollos')}
          className={`px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
            activeFilter === 'chollos'
              ? 'bg-orange-500 text-slate-950 shadow-lg shadow-orange-500/20'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-slate-700/60'
          }`}
          id="filter-chollos"
        >
          🔥 Chollos (&gt;30% DTO)
        </button>
        <button
          onClick={() => setActiveFilter('reactivas')}
          className={`px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
            activeFilter === 'reactivas'
              ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/20'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-slate-700/60'
          }`}
          id="filter-reactivas"
        >
          🚀 Recom. 5:15 pace (Novablast / KD900)
        </button>
        <button
          onClick={() => setActiveFilter('maxima')}
          className={`px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
            activeFilter === 'maxima'
              ? 'bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/20'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-slate-700/60'
          }`}
          id="filter-maxima"
        >
          ☁️ Máxima Protección (Nimbus / KS900)
        </button>
        <button
          onClick={() => setActiveFilter('económitas')}
          className={`px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
            activeFilter === 'económitas'
              ? 'bg-purple-500 text-white shadow-lg shadow-purple-500/20'
              : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-slate-700/60'
          }`}
          id="filter-economicas"
        >
          💰 Menos de 95€
        </button>
      </div>
    </header>
  );
}
