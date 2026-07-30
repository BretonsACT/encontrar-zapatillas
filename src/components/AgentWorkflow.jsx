import React, { useState } from 'react';
import { CheckCircle2, RefreshCw, ChevronDown, ChevronUp, Cpu, ShoppingBag, Filter, ShieldCheck, Zap } from 'lucide-react';
import { RELIABLE_STORES } from '../data/asicsModels';

export default function AgentWorkflow({ isScanning, scanProgress, scanStoreLogs }) {
  const [isOpen, setIsOpen] = useState(true);

  const steps = [
    {
      number: 1,
      title: 'Perfilado del Corredor',
      status: 'completed',
      detail: 'Análisis de ritmo (5:15 min/km) y volumen (30 km/sem). Categoría ideal: Daily Trainer con amortiguación reactiva.',
      icon: Cpu
    },
    {
      number: 2,
      title: 'Criterio Estricto de Talla',
      status: 'completed',
      detail: 'Filtro fijado en 42.5 EU (Horma ASICS & Kiprun: 27.0 cm longitud de plantilla, apto para pies de 26.2-26.6 cm).',
      icon: Filter
    },
    {
      number: 3,
      title: 'Escaneo Decathlon + Multi-Tienda',
      status: isScanning ? 'in_progress' : 'completed',
      detail: `Verificación activa en Decathlon España y ${RELIABLE_STORES.length - 1} comercios verificados con garantía oficial.`,
      icon: ShoppingBag
    },
    {
      number: 4,
      title: 'Cruce de Chollos y Similares',
      status: isScanning ? 'in_progress' : 'completed',
      detail: 'Comparación automática de modelos ASICS con alternativas equivalentes Kiprun en Decathlon.',
      icon: ShieldCheck
    }
  ];

  return (
    <div className="glass-panel p-5 mb-8 border border-slate-800">
      <div 
        className="flex items-center justify-between cursor-pointer select-none"
        onClick={() => setIsOpen(!isOpen)}
        id="toggle-workflow-header"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              Flujo de Trabajo del Agente de Búsqueda
              <span className="text-xs bg-slate-800 text-slate-400 px-2.5 py-0.5 rounded-full border border-slate-700 font-mono">
                Pasos Ejecutados
              </span>
            </h3>
            <p className="text-xs text-slate-400">
              {isScanning ? 'Escaneando Decathlon y comercios en vivo...' : 'Búsqueda finalizada con 100% de coincidencia en talla 42.5 EU en Decathlon y tiendas'}
            </p>
          </div>
        </div>

        <button className="text-slate-400 hover:text-white transition-colors p-1">
          {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
      </div>

      {/* Expandable Workflow Content */}
      {isOpen && (
        <div className="mt-5 pt-5 border-t border-slate-800/80 fade-in">
          {/* Progress Bar when scanning */}
          {isScanning && (
            <div className="mb-6 bg-slate-900/90 p-4 rounded-xl border border-cyan-500/30">
              <div className="flex justify-between items-center text-xs mb-2">
                <span className="text-cyan-400 font-mono flex items-center gap-2">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  Escaneando comercios... ({scanProgress}%)
                </span>
                <span className="text-slate-400 font-mono">Decathlon & ASICS 42.5 Scanner</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-blue-500 via-cyan-500 to-emerald-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${scanProgress}%` }}
                ></div>
              </div>

              {/* Log ticker */}
              {scanStoreLogs.length > 0 && (
                <div className="mt-3 font-mono text-xs text-slate-400 bg-slate-950/80 p-2.5 rounded-lg border border-slate-800 max-h-24 overflow-y-auto">
                  {scanStoreLogs.map((log, index) => (
                    <div key={index} className="text-emerald-400 flex items-center gap-2">
                      <span className="text-slate-600">&gt;</span> {log}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Workflow Steps Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {steps.map((step) => {
              const IconComp = step.icon;
              return (
                <div 
                  key={step.number}
                  className="bg-slate-900/50 p-4 rounded-xl border border-slate-800/80 flex flex-col justify-between hover:border-slate-700 transition-all"
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 text-cyan-400 text-xs font-mono font-bold flex items-center justify-center">
                        0{step.number}
                      </span>
                      {step.status === 'completed' ? (
                        <span className="text-emerald-400 text-xs font-medium flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> OK
                        </span>
                      ) : (
                        <span className="text-amber-400 text-xs font-medium flex items-center gap-1 animate-pulse">
                          <RefreshCw className="w-3.5 h-3.5 animate-spin" /> Procesando...
                        </span>
                      )}
                    </div>
                    <h4 className="text-sm font-semibold text-slate-200 mb-1 flex items-center gap-2">
                      <IconComp className="w-4 h-4 text-cyan-400" />
                      {step.title}
                    </h4>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      {step.detail}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Stores scanned badge strip */}
          <div className="mt-4 pt-4 border-t border-slate-800/60 flex items-center justify-between flex-wrap gap-2 text-xs text-slate-400">
            <span>Tiendas monitoreadas por el Agente:</span>
            <div className="flex items-center gap-2 flex-wrap">
              {RELIABLE_STORES.map((s, i) => (
                <span 
                  key={i} 
                  className={`px-2.5 py-1 rounded-md text-[11px] border ${
                    s.isFeatured 
                      ? 'bg-blue-900/60 text-blue-200 border-blue-500/60 font-semibold' 
                      : 'bg-slate-800/90 text-slate-300 border-slate-700/60'
                  }`}
                >
                  {s.name} ({s.TrustScore})
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
