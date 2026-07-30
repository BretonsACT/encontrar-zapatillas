import React from 'react';
import { X, Ruler, CheckCircle2, AlertCircle } from 'lucide-react';

export default function SizeGuideModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md fade-in">
      <div className="glass-panel w-full max-w-lg bg-slate-900/95 border border-slate-700/80 p-6 rounded-2xl shadow-2xl relative">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <Ruler className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-100">
                Guía de Talla ASICS & Decathlon: 42.5 EU
              </h2>
              <p className="text-xs text-slate-400">
                Especificaciones exactas de medida y horma para running
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="space-y-4 text-xs sm:text-sm">
          
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 block text-[10px]">Talla Europa</span>
              <span className="font-bold text-cyan-400 text-base font-mono">42.5 EU</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 block text-[10px]">Talla USA</span>
              <span className="font-bold text-slate-200 text-base font-mono">9.0 US</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 block text-[10px]">Talla UK</span>
              <span className="font-bold text-slate-200 text-base font-mono">8.0 UK</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 block text-[10px]">Longitud Plantilla</span>
              <span className="font-bold text-orange-400 text-base font-mono">27.0 cm</span>
            </div>
          </div>

          {/* Advice Box */}
          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-2">
            <h4 className="font-semibold text-slate-200 flex items-center gap-1.5 text-xs text-amber-400">
              <AlertCircle className="w-4 h-4" /> Recomendaciones para Correr 10 km:
            </h4>
            <ul className="space-y-1.5 text-xs text-slate-300">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 mt-0.5" />
                <span>
                  <strong>Margen Térmico de Impacto:</strong> Al correr 10 km a 5:15 min/km, el pie se dilata entre 0.4cm y 0.7cm. La plantilla de 27.0 cm de la talla 42.5 EU es perfecta si tu pie desnudo mide entre <strong>26.2 cm y 26.6 cm</strong>.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 mt-0.5" />
                <span>
                  <strong>Horma ASICS & Kiprun Decathlon:</strong> Los modelos Novablast 4, Cumulus 26 y Kiprun KD900 tallan 100% exactos (True to Size). No es necesario pedir media talla más.
                </span>
              </li>
            </ul>
          </div>

        </div>

        {/* Footer */}
        <div className="mt-6 pt-4 border-t border-slate-800 text-right">
          <button onClick={onClose} className="btn-primary text-xs">
            Entendido
          </button>
        </div>

      </div>
    </div>
  );
}
