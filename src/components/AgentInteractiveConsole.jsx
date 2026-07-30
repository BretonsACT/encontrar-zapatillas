import React, { useState, useRef, useEffect } from 'react';
import { Bot, Send, Sparkles, RefreshCw, ChevronRight } from 'lucide-react';

export default function AgentInteractiveConsole({ onSelectFilter }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'agent',
      text: '¡Hola! Soy tu **Agente Buscador de Zapatillas**. He escaneado **Decathlon España**, ASICS Outlet, Zalando y 6 tiendas más para tu talla **42.5 EU** (10 km a 5:15 min/km).\n\n¿En qué te puedo ayudar? Puedes pedirme las mejores zapatillas, ofertas en Decathlon o comparativas con modelos similares.',
      timestamp: 'Ahora',
      suggestions: [
        '🏆 ¿Cuáles son las mejores zapatillas?',
        '💙 Ver chollos en Decathlon España',
        '🚀 Comparar Novablast 4 vs Kiprun KD900',
        '💰 Zapatillas < 95€ con stock 42.5 EU'
      ]
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isThinking]);

  const handleSend = (queryText) => {
    const q = (queryText || inputQuery).trim();
    if (!q) return;

    // Add user message
    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: q,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    if (!queryText) setInputQuery('');
    setIsThinking(true);

    // Simulate Agent execution and decision
    setTimeout(() => {
      let replyText = '';
      let actionFilter = 'all';
      let suggestions = [];

      const lowerQ = q.toLowerCase();

      if (lowerQ.includes('mejor') || lowerQ.includes('best') || lowerQ.includes('top') || lowerQ.includes('recomiend')) {
        actionFilter = 'all';
        replyText = `🏆 **Veredicto Automático del Agente - Mejores Zapatillas (Talla 42.5 EU / 10km @ 5:15):**\n\n1. 🥇 **ASICS Novablast 4 (90,00€ en ASICS Outlet / 109,99€ en Decathlon)**: 98% Afinidad. Geometría en trampolín ideal para mover las piernas a 5:15 min/km.\n2. 💥 **ASICS GEL-Cumulus 26 (94,99€ en Decathlon España)**: 95% Afinidad. Ofertazo imbatible (-41% DTO) con la máxima versatilidad y PureGEL.\n3. ⚡ **Decathlon Kiprun KD900 Light (89,99€ en Decathlon)**: 96% Afinidad. Solo 200g y espuma Pebax® VFOAM. La alternativa ultraligera a Novablast.\n4. ☁️ **Decathlon Kiprun KS900 2 (79,99€ en Decathlon Club)**: 93% Afinidad. Nube de confort MFOAM por 60€ menos que Nimbus.\n\nHe actualizado la lista para mostrarte todas las opciones ordenadas por compatibilidad real.`;
        suggestions = ['💙 Ver solo ofertas Decathlon', '🚀 Novablast vs KD900', '💰 Ver opciones < 95€'];
      } else if (lowerQ.includes('decathlon') || lowerQ.includes('kiprun')) {
        actionFilter = 'decathlon';
        replyText = `🔍 **Análisis del Agente en Decathlon España:**\n\nhe localizado **4 ofertas destacadas** para tu perfil (10 km a 5:15 min/km en 42.5 EU):\n\n1. **ASICS GEL-Cumulus 26** por **94,99€** (Chollo exclusivo Decathlon con 41% DTO).\n2. **Decathlon Kiprun KD900 Light** por **89,99€** (Mediasuela Pebax®, solo 200g, la alternativa directa a Novablast 4).\n3. **Decathlon Kiprun KS900 2** por **79,99€** (Nube MFOAM con garantía de 60 días de prueba Decathlon Club).\n4. **ASICS Novablast 4** por **109,99€** (Stock disponible en tienda con recogida gratis en 1 hora).\n\nHe filtrado la vista para mostrarte los modelos con oferta en Decathlon.`;
        suggestions = ['🚀 Novablast vs KD900', 'Ver todas las opciones'];
      } else if (lowerQ.includes('novablast') || lowerQ.includes('kd900') || lowerQ.includes('comparar')) {
        actionFilter = 'reactivas';
        replyText = `⚡ **Comparativa Agente: ASICS Novablast 4 vs Kiprun KD900 Light:**\n\n• **ASICS Novablast 4 (90,00€ en Outlet / 109,99€ en Decathlon)**: 260g, drop 8mm, tecnología FF Blast+ ECO. Geometría trampolín súper ágil.\n• **Decathlon Kiprun KD900 Light (89,99€ en Decathlon)**: 200g (23% más ligera), drop 6mm, espuma de Pebax®. Respuesta inmediata para 5:15 pace.\n\n👉 **Veredicto:** Si priorizas ligereza extrema y mejor relación calidad/precio en Decathlon, la **KD900 Light** gana por peso; si prefieres la horma tradicional ASICS, la **Novablast 4** es imbatible.`;
        suggestions = ['💙 Ver ofertas Decathlon', '💰 Ver opciones < 95€'];
      } else if (lowerQ.includes('95') || lowerQ.includes('barata') || lowerQ.includes('presupuesto') || lowerQ.includes('chollo')) {
        actionFilter = 'económitas';
        replyText = `💰 **Agente de Chollos (Talla 42.5 EU < 100€):**\n\n• **ASICS Novablast 4**: **90,00€** en ASICS Outlet.\n• **ASICS GEL-Cumulus 26**: **94,99€** en Decathlon España.\n• **Kiprun KS900 2**: **79,99€** en Decathlon Club.\n• **Kiprun KD900 Light**: **89,99€** en Decathlon.\n\nHe activado el filtro de precios económicos en la aplicación.`;
        suggestions = ['💙 Ver solo Decathlon', '☁️ Ver máxima amortiguación'];
      } else if (lowerQ.includes('nube') || lowerQ.includes('rodilla') || lowerQ.includes('amortigua') || lowerQ.includes('nimbus')) {
        actionFilter = 'maxima';
        replyText = `☁️ **Recomendación para Máxima Protección Articular:**\n\n1. **ASICS GEL-Nimbus 26** (139,95€ en Zalando / 149,99€ en Decathlon): Referencia absoluta con tecnología PureGEL.\n2. **Decathlon Kiprun KS900 2** (79,99€ en Decathlon Club): MFOAM ultra mullido por 60€ menos. Excelente opción para rodajes diarios sin fatiga.`;
        suggestions = ['💙 Ver en Decathlon', '⚡ Comparar con Novablast 4'];
      } else {
        replyText = `🤖 **Agente Procesado:** He revisado tu consulta "${q}". He actualizado el catálogo de zapatillas para tu perfil de **10 km a 5:15 min/km** en talla **42.5 EU**. Puedes ver las mejores ofertas en Decathlon y tiendas verificadas justo debajo.`;
        suggestions = ['🏆 ¿Cuáles son las mejores?', '💙 Ver ofertas Decathlon', '🔥 Chollos >30% DTO'];
      }

      onSelectFilter(actionFilter);

      const agentReply = {
        id: Date.now() + 1,
        sender: 'agent',
        text: replyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        suggestions
      };

      setMessages(prev => [...prev, agentReply]);
      setIsThinking(false);
    }, 450);
  };

  return (
    <div className="glass-panel p-5 mb-8 border border-cyan-500/30 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none"></div>

      {/* Console Header */}
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-slate-950 shadow-md shadow-cyan-500/20">
            <Bot className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <h3 className="text-base font-extrabold text-slate-100 flex items-center gap-2">
              Agente Virtual Buscador & Comparador Decathlon
              <span className="badge-glow text-[10px] py-0.5 px-2">IA Activa</span>
            </h3>
            <p className="text-xs text-slate-400">
              Escribe o selecciona una consulta para comunicarte directamente con el agente
            </p>
          </div>
        </div>

        <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400 font-mono">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Modelo Decathlon + ASICS Scanner</span>
        </div>
      </div>

      {/* Messages Stream Area */}
      <div className="bg-slate-950/80 rounded-xl p-4 border border-slate-800/90 max-h-72 overflow-y-auto space-y-4 text-xs sm:text-sm">
        {messages.map(msg => (
          <div key={msg.id} className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
            <div className="flex items-center gap-1.5 mb-1 text-[11px] text-slate-500">
              <span>{msg.sender === 'user' ? 'Tú' : 'Agente Antigravity AI'}</span>
              <span>•</span>
              <span>{msg.timestamp}</span>
            </div>

            <div className={`p-3.5 rounded-2xl max-w-2xl leading-relaxed ${
              msg.sender === 'user'
                ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-br-none shadow-md'
                : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none'
            }`}>
              <div className="whitespace-pre-line">
                {msg.text.split('**').map((part, idx) => 
                  idx % 2 === 1 ? <strong key={idx} className="text-cyan-300 font-semibold">{part}</strong> : part
                )}
              </div>

              {/* Suggestions buttons inside agent message */}
              {msg.suggestions && msg.suggestions.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-800/80 flex flex-wrap gap-1.5">
                  {msg.suggestions.map((sug, i) => (
                    <button
                      key={i}
                      onClick={() => handleSend(sug)}
                      className="bg-slate-800 hover:bg-cyan-950 hover:border-cyan-500/50 text-cyan-300 text-xs px-2.5 py-1 rounded-lg border border-slate-700 transition-all flex items-center gap-1"
                    >
                      <span>{sug}</span>
                      <ChevronRight className="w-3 h-3 text-cyan-400" />
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {isThinking && (
          <div className="flex items-center gap-2 text-xs text-cyan-400 font-mono py-2">
            <RefreshCw className="w-3.5 h-3.5 animate-spin" />
            <span>El Agente está consultando ofertas en Decathlon España y ASICS Outlet...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input prompt area */}
      <form 
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="mt-3 flex items-center gap-2"
      >
        <div className="relative flex-1">
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder="Ej: ¿Cuáles son las mejores zapatillas? o busca ofertas en Decathlon..."
            className="w-full bg-slate-900 border border-slate-700/80 rounded-xl py-2.5 px-4 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition-colors"
          />
          <Sparkles className="w-4 h-4 text-cyan-400 absolute right-3 top-3 pointer-events-none opacity-60" />
        </div>

        <button
          type="submit"
          disabled={!inputQuery.trim() || isThinking}
          className="btn-primary text-xs py-2.5 px-4 whitespace-nowrap disabled:opacity-50"
        >
          <span>Preguntar</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}
