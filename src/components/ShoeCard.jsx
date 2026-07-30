import React, { useState } from 'react';
import { ExternalLink, CheckCircle2, ShieldCheck, Flame, Zap, ChevronDown, ChevronUp, Tag, Truck, Award } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function ShoeCard({ shoe, isTopPick }) {
  const [showAllStores, setShowAllStores] = useState(false);

  const handleBuyClick = () => {
    confetti({
      particleCount: 45,
      spread: 70,
      origin: { y: 0.8 }
    });
  };

  const displayedStores = showAllStores ? shoe.stores : shoe.stores.slice(0, 3);

  return (
    <div className={`glass-card p-6 relative overflow-hidden flex flex-col justify-between transition-all ${
      isTopPick 
        ? 'border-2 border-cyan-500/80 shadow-2xl shadow-cyan-500/15' 
        : shoe.isDecathlonSpecial
        ? 'border border-blue-500/60 bg-blue-950/20'
        : ''
    }`}>
      {/* Top Banner Tag */}
      {isTopPick && (
        <div className="absolute top-0 right-0 bg-gradient-to-l from-cyan-500 to-blue-600 text-slate-950 text-[11px] font-extrabold uppercase px-4 py-1 rounded-bl-xl shadow-md flex items-center gap-1 z-20">
          <Zap className="w-3.5 h-3.5 fill-slate-950" /> #1 Elección Agente para 10k @ 5:15
        </div>
      )}

      {!isTopPick && shoe.isDecathlonSpecial && (
        <div className="absolute top-0 right-0 bg-gradient-to-l from-blue-600 to-indigo-600 text-white text-[11px] font-extrabold uppercase px-4 py-1 rounded-bl-xl shadow-md flex items-center gap-1 z-20">
          <Award className="w-3.5 h-3.5" /> 💙 Destacado Decathlon España
        </div>
      )}

      <div>
        {/* Header section with category and affinity score */}
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2 mb-0.5">
              <span className="text-xs font-bold text-cyan-400 tracking-wide uppercase">
                {shoe.category}
              </span>
              {shoe.brand && (
                <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700 font-mono">
                  {shoe.brand}
                </span>
              )}
            </div>

            <h2 className="text-2xl font-black text-slate-100 mt-0.5 flex items-center gap-2">
              {shoe.name}
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              {shoe.subtitle}
            </p>
          </div>

          <div className="text-right flex-shrink-0">
            <div className="inline-flex flex-col items-end">
              <span className="text-xs text-slate-400">Afín a tu perfil</span>
              <span className="text-2xl font-black text-emerald-400 font-mono flex items-center gap-1">
                {shoe.affinityScore}% <span className="text-xs font-normal text-emerald-500">compat.</span>
              </span>
            </div>
          </div>
        </div>

        {/* Shoe Image and Quick Specs Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 my-4">
          
          {/* Image Column */}
          <div className="md:col-span-5 relative group overflow-hidden rounded-xl bg-slate-950/70 border border-slate-800 flex items-center justify-center p-3">
            <img 
              src={shoe.image} 
              alt={shoe.name} 
              className="w-full h-48 object-contain transition-transform duration-500 group-hover:scale-105"
            />
            {shoe.discountPercent > 0 && (
              <span className="absolute bottom-3 left-3 bg-orange-500 text-slate-950 font-black text-xs px-2.5 py-1 rounded-md shadow-md flex items-center gap-1">
                <Flame className="w-3.5 h-3.5 fill-slate-950" /> -{shoe.discountPercent}% DTO
              </span>
            )}
            <span className="absolute bottom-3 right-3 bg-slate-900/90 text-slate-300 text-[11px] font-mono px-2 py-0.5 rounded border border-slate-700">
              Talla 42.5 EU OK
            </span>
          </div>

          {/* Details & Specs Column */}
          <div className="md:col-span-7 flex flex-col justify-between">
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed mb-3">
              {shoe.summary}
            </p>

            {/* Spec Pills */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4 text-xs">
              <div className="bg-slate-900/80 p-2 rounded-lg border border-slate-800">
                <span className="text-slate-500 block text-[10px]">Drop</span>
                <span className="font-semibold text-slate-200">{shoe.drop}</span>
              </div>
              <div className="bg-slate-900/80 p-2 rounded-lg border border-slate-800">
                <span className="text-slate-500 block text-[10px]">Peso H42.5</span>
                <span className="font-semibold text-slate-200">{shoe.weight}</span>
              </div>
              <div className="bg-slate-900/80 p-2 rounded-lg border border-slate-800">
                <span className="text-slate-500 block text-[10px]">Tecnología Espuma</span>
                <span className="font-semibold text-cyan-400 truncate block">{shoe.foam}</span>
              </div>
              <div className="bg-slate-900/80 p-2 rounded-lg border border-slate-800">
                <span className="text-slate-500 block text-[10px]">Tipo Pisada</span>
                <span className="font-semibold text-slate-200 truncate block">{shoe.footstrike}</span>
              </div>
            </div>

            {/* Personalized Why Ideal Points */}
            <div className="bg-slate-900/40 p-3 rounded-xl border border-slate-800/80">
              <span className="text-[11px] font-semibold text-cyan-400 uppercase tracking-wider block mb-1.5 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" /> ¿Por qué encaja con tus 10km a 5:15 min/km?
              </span>
              <ul className="space-y-1 text-xs text-slate-300">
                {shoe.whyIdeal.map((point, idx) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <span className="text-cyan-500 font-bold">•</span>
                    <span>{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Price & Stores Comparison Section */}
        <div className="mt-6 pt-5 border-t border-slate-800">
          <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
            <h4 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <Tag className="w-4 h-4 text-orange-400" />
              Comparador de Precios (Talla 42.5 EU en Decathlon y Tiendas Verificadas)
            </h4>
            <div className="text-xs text-slate-400">
              Mejor precio actual: <strong className="text-emerald-400 text-base font-mono">{shoe.bestPrice.toFixed(2)}€</strong>
              <span className="line-through text-slate-500 ml-1.5">{shoe.basePrice.toFixed(2)}€</span>
            </div>
          </div>

          {/* Stores List */}
          <div className="space-y-2">
            {displayedStores.map((store, idx) => {
              const isDecathlonStore = store.name.toLowerCase().includes('decathlon');

              return (
                <div 
                  key={idx}
                  className={`p-3 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-3 transition-all ${
                    isDecathlonStore 
                      ? 'bg-blue-950/40 border-blue-600/50 hover:border-blue-400 shadow-md shadow-blue-950/30'
                      : 'bg-slate-900/70 border-slate-800/90 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xl">{store.logo}</span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-xs text-slate-200">{store.name}</span>
                        {isDecathlonStore && (
                          <span className="text-[10px] bg-blue-600 text-white font-bold px-2 py-0.5 rounded shadow-sm">
                            💙 Opción Decathlon
                          </span>
                        )}
                        <span className="text-[10px] bg-slate-800 text-emerald-400 px-2 py-0.5 rounded border border-slate-700 flex items-center gap-1">
                          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /> {store.verifiedReliability}
                        </span>
                      </div>
                      <div className="flex items-center gap-3 text-[11px] text-slate-400 mt-0.5">
                        <span className="text-orange-400 font-medium">Talla: {store.sizeAvailable}</span>
                        <span className="flex items-center gap-1"><Truck className="w-3 h-3" /> {store.shipping}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between sm:justify-end gap-4 border-t sm:border-t-0 pt-2 sm:pt-0 border-slate-800">
                    <div className="text-left sm:text-right">
                      <span className="text-base font-extrabold text-slate-100 font-mono block">
                        {store.price.toFixed(2)}€
                      </span>
                      {store.originalPrice > store.price && (
                        <span className="text-[10px] text-slate-500 line-through">
                          {store.originalPrice.toFixed(2)}€
                        </span>
                      )}
                    </div>

                    <a 
                      href={store.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      onClick={handleBuyClick}
                      className={`btn-primary text-xs py-1.5 px-3 whitespace-nowrap ${
                        isDecathlonStore ? 'bg-gradient-to-r from-blue-600 to-cyan-600' : ''
                      }`}
                    >
                      <span>Ver Oferta</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Show more stores toggle if applicable */}
          {shoe.stores.length > 3 && (
            <button
              onClick={() => setShowAllStores(!showAllStores)}
              className="mt-3 text-xs text-cyan-400 hover:text-cyan-300 font-medium flex items-center justify-center gap-1 w-full py-1.5 rounded bg-slate-900/40 border border-slate-800"
            >
              {showAllStores ? (
                <>Ver menos tiendas <ChevronUp className="w-3.5 h-3.5" /></>
              ) : (
                <>Ver {shoe.stores.length - 3} tienda(s) adicional(es) <ChevronDown className="w-3.5 h-3.5" /></>
              )}
            </button>
          )}

        </div>
      </div>
    </div>
  );
}
