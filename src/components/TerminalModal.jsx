import React, { useState } from 'react';
import { X, Terminal, Copy, Check } from 'lucide-react';

export default function TerminalModal({ isOpen, onClose }) {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const commandText = `python3 agent_shoe_finder.py --decathlon --size 42.5 --distance 10k --pace "5:15"`;

  const copyCommand = () => {
    navigator.clipboard.writeText(commandText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md fade-in">
      <div className="glass-panel w-full max-w-2xl bg-slate-950 border border-slate-700/80 p-6 rounded-2xl shadow-2xl relative font-mono">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <Terminal className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100 font-sans">
                Ejecutar Agente CLI en Terminal Python
              </h2>
              <p className="text-xs text-slate-400 font-sans">
                Script de consola con soporte para Decathlon, ASICS y modelos Kiprun
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

        {/* Code Console */}
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 text-xs text-emerald-400 relative">
          <button 
            onClick={copyCommand}
            className="absolute top-3 right-3 bg-slate-800 hover:bg-slate-700 text-slate-300 p-1.5 rounded text-[11px] flex items-center gap-1 border border-slate-700"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? 'Copiado' : 'Copiar'}
          </button>
          
          <p className="text-slate-500 mb-2"># Comando CLI del Agente para escanear Decathlon y comparar marcas:</p>
          <div className="text-slate-200 select-all font-mono py-1 pr-16">
            $ {commandText}
          </div>
        </div>

        {/* Output Preview */}
        <div className="mt-4 bg-slate-950 p-4 rounded-xl border border-slate-800 text-[11px] text-slate-300 space-y-1 max-h-48 overflow-y-auto font-mono">
          <div className="text-cyan-400">[AGENTE DECATHLON & ASICS] Escaneando Hombre | Talla: 42.5 EU | 10km @ 5:15 pace...</div>
          <div className="text-blue-400">[DECATHLON] Consultando Decathlon España (Stock 42.5 EU: OK)...</div>
          <div className="text-slate-400">[TIENDAS] Consultando ASICS Outlet, Zalando, Tradeinn, Deporvillage...</div>
          <div className="text-emerald-400">[DECATHLON CHOLLO] ASICS GEL-Cumulus 26 -&gt; 94.99€ en Decathlon (-41%)</div>
          <div className="text-emerald-400">[DECATHLON SIMILAR] Kiprun KD900 Light -&gt; 89.99€ en Decathlon (200g, Pebax foam)</div>
          <div className="text-orange-400">[CHOLLO OUTLET] ASICS Novablast 4 -&gt; 90.00€ en ASICS Outlet (-40%)</div>
        </div>

        {/* Footer */}
        <div className="mt-5 pt-4 border-t border-slate-800 flex items-center justify-between text-xs font-sans">
          <span className="text-slate-400">Archivo: <code className="text-emerald-400">agent_shoe_finder.py</code></span>
          <button onClick={onClose} className="btn-secondary text-xs">
            Cerrar
          </button>
        </div>

      </div>
    </div>
  );
}
