import React from 'react';
import { X, Check, Sparkles } from 'lucide-react';

export default function QuestionnaireModal({ 
  isOpen, 
  onClose, 
  userAnswers, 
  setUserAnswers, 
  onApply 
}) {
  if (!isOpen) return null;

  const handleSelect = (key, value) => {
    setUserAnswers(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md fade-in">
      <div className="glass-panel w-full max-w-2xl bg-slate-900/95 border border-slate-700/80 p-6 rounded-2xl shadow-2xl relative max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-100">
                Preguntas de Personalización del Agente
              </h2>
              <p className="text-xs text-slate-400">
                El agente usará tus respuestas para ordenar los modelos ASICS y Decathlon con mayor precisión
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            id="close-questions-modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Questions Body */}
        <div className="space-y-6">

          {/* Question 1: Pronation / Footstrike */}
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2 flex items-center justify-between">
              <span>1. ¿Cómo es tu tipo de pisada?</span>
              <span className="text-xs text-cyan-400 font-normal">Relevante para estabilidad</span>
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {[
                { id: 'neutra', label: 'Pisada Neutra', desc: 'Desgaste uniforme de suela. Ideal para Novablast, Nimbus, Cumulus y KD900.' },
                { id: 'pronadora', label: 'Leve Pronadora', desc: 'El pie apoya hacia dentro al fatigarte en 10k. Ideal para GT-2000 12.' },
                { id: 'supinadora', label: 'Supinadora / Apoyo exterior', desc: 'Apoyo en el canto exterior. Priorizar amortiguación sin postes (KS900).' },
                { id: 'nose', label: 'No lo sé con certeza', desc: 'El agente priorizará modelos neutros de alta tolerancia.' }
              ].map(opt => (
                <div 
                  key={opt.id}
                  onClick={() => handleSelect('pronation', opt.id)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                    userAnswers.pronation === opt.id
                      ? 'bg-cyan-950/40 border-cyan-400 text-cyan-200 shadow-md shadow-cyan-950/50'
                      : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-sm">{opt.label}</span>
                    {userAnswers.pronation === opt.id && <Check className="w-4 h-4 text-cyan-400" />}
                  </div>
                  <p className="text-xs text-slate-400">{opt.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Question 2: Surface */}
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2 flex items-center justify-between">
              <span>2. ¿Por qué terreno corres tus 10 km habitualmente?</span>
              <span className="text-xs text-orange-400 font-normal">Para tipo de suela</span>
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { id: 'asfalto', label: 'Asfalto y Aceras', desc: 'Máxima absorción de impacto duro' },
                { id: 'mixto', label: 'Mixto (Asfalto + Parque)', desc: 'Tierra compacta y aceras' },
                { id: 'pista', label: 'Cinta / Pista', desc: 'Mayor reactividad y ligereza' }
              ].map(opt => (
                <div 
                  key={opt.id}
                  onClick={() => handleSelect('surface', opt.id)}
                  className={`p-3 rounded-xl border cursor-pointer transition-all ${
                    userAnswers.surface === opt.id
                      ? 'bg-orange-950/40 border-orange-400 text-orange-200'
                      : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-xs">{opt.label}</span>
                    {userAnswers.surface === opt.id && <Check className="w-3.5 h-3.5 text-orange-400" />}
                  </div>
                  <p className="text-[11px] text-slate-400">{opt.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Question 3: Cushion Feel */}
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2 flex items-center justify-between">
              <span>3. ¿Qué sensación de rodaje prefieres a 5:15 min/km?</span>
              <span className="text-xs text-emerald-400 font-normal">Tacto de mediasuela</span>
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { id: 'reactiva', label: 'Reactiva y Rebotona', desc: 'Sensación ágil y rápida (Novablast / Kiprun KD900)' },
                { id: 'maxima', label: 'Máxima Nube / Colchón', desc: 'Protección total (Nimbus / Kiprun KS900)' },
                { id: 'equilibrada', label: 'Equilibrada Diaria', desc: 'Tacto natural y ligero (Cumulus 26)' }
              ].map(opt => (
                <div 
                  key={opt.id}
                  onClick={() => handleSelect('cushion', opt.id)}
                  className={`p-3 rounded-xl border cursor-pointer transition-all ${
                    userAnswers.cushion === opt.id
                      ? 'bg-emerald-950/40 border-emerald-400 text-emerald-200'
                      : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-xs">{opt.label}</span>
                    {userAnswers.cushion === opt.id && <Check className="w-3.5 h-3.5 text-emerald-400" />}
                  </div>
                  <p className="text-[11px] text-slate-400">{opt.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Question 4: Budget */}
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">
              4. Presupuesto Máximo de Compra
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {[
                { id: 'sub100', label: 'Hasta 95€' },
                { id: '100-130', label: '95€ - 130€' },
                { id: '130-160', label: '130€ - 160€' },
                { id: 'sin_limite', label: 'Sin límite' }
              ].map(opt => (
                <button
                  key={opt.id}
                  onClick={() => handleSelect('budget', opt.id)}
                  className={`py-2 px-3 rounded-lg border text-xs font-semibold transition-all ${
                    userAnswers.budget === opt.id
                      ? 'bg-purple-900/50 border-purple-400 text-purple-200'
                      : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="mt-8 pt-4 border-t border-slate-800 flex items-center justify-end gap-3">
          <button
            onClick={onClose}
            className="btn-secondary text-xs"
          >
            Cancelar
          </button>
          <button
            onClick={() => {
              onApply();
              onClose();
            }}
            className="btn-primary text-xs"
            id="apply-questions-btn"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Aplicar Afinación al Agente
          </button>
        </div>

      </div>
    </div>
  );
}
