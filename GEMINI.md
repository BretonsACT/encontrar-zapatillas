# 👟 GEMINI.md - Configuración y Reglas del Agente Buscador de Zapatillas

Este archivo define el comportamiento, reglas de decisión, perfil de usuario y comercios monitoreados por el **Agente Buscador de Zapatillas (Decathlon & Multi-Tienda)**.
Puedes editar cualquier parámetro de este documento para modificar las prioridades y respuestas del agente en tiempo real.

---

## 👤 1. Perfil del Corredor (Parámetros Configurables)

| Parámetro | Valor Actual | Descripción / Efecto en las Recomendaciones |
| :--- | :--- | :--- |
| `genero` | **Hombre** | Selecciona hormas y modelos masculinos |
| `talla_eu` | **42.5 EU** | Longitud de plantilla **27.0 cm** (US 9 / UK 8). Filtro estricto de stock |
| `longitud_pie` | **26.2 cm - 26.6 cm** | Deja un margen térmico de 0.4cm - 0.8cm para tiradas largas |
| `distancia_tirada` | **10 km** | Tipo de zapatilla: *Daily Trainer* amortiguada y duradera |
| `frecuencia` | **3 salidas/semana** | Volumen semanal de ~30 km. Exige alta durabilidad de suela |
| `ritmo_habitual` | **5:15 min/km** | Ritmo ágil-medio. Favorece espumas reactivas (FF Blast+, Pebax®, VFOAM) |
| `tipo_pisada` | **Neutra / Supinadora ligera** | Evita postes rígidos de pronación severa salvo fatiga extrema |
| `terreno` | **Asfalto duro y paradas** | Prioriza amortiguación alta y compuesto antideslizante (AHAR / MFOAM) |
| `presupuesto_objetivo` | **< 100€ (Chollos preferentes)** | Da máxima prioridad a ofertas > 30% DTO |

---

## 🏪 2. Comercios Monitoreados y Reglas de Decisión

El agente analiza en tiempo real las mejores tiendas de zapatillas de España y Europa:

| Comercio | Prioridad Agente | Garantía y Devoluciones | Puntos Fuertes |
| :--- | :---: | :--- | :--- |
| **Decathlon España 💙** | 🥇 **Máxima** | 60 días prueba (Decathlon Club) + 3 años garantía | Chollos exclusividad ASICS, recogida 1h gratis en tienda y gama **Kiprun** |
| **ASICS Outlet Oficial 🏷️** | 🥇 **Máxima** | 30 días devolución gratis | Precios directos de fábrica en modelos de temporada anterior |
| **Zalando España 🛍️** | 🥈 **Alta** | 100 días devolución gratis | Gran volumen de stock talla 42.5 EU y envío muy rápido (24-48h) |
| **Runnerinn (Tradeinn) 📦** | 🥈 **Alta** | 30 días devolución | Catálogo de running más extenso de Europa y chollos frecuentes |
| **Deporvillage 🚴** | 🥈 **Alta** | 30 días devolución | Entrega rápida 24h y excelente atención |
| **Top4Running 🏃** | 🥉 **Media** | 30 días devolución | Tienda especializada en atletismo con ofertas exclusivas |
| **i-Run España 🏃** | 🥉 **Media** | 30 días devolución gratis | Gran catálogo especializado con ficha técnica detallada |
| **El Corte Inglés 🏬** | 🥉 **Media** | 60 días devolución | Garantía oficial y recogida gratuita en centros comerciales |
| **StreetProRunning 👟** | 🥉 **Media** | 30 días devolución | Chollos flash y promociones por cupones |
| **Alltricks España 🚴** | 🥈 **Alta** | 30 días devolución (60 días Club Alltricks) | Tienda líder running/ciclismo (Grupo Decathlon), gran stock y envío gratis >49€ |
---

## 🚀 3. Reglas de Comparación entre ASICS y Modelos Similares de Decathlon

El agente aplica la siguiente matriz de equivalencia técnica al analizar **Decathlon**:

```
 🏃 Modelo ASICS               💙 Equivalente / Oferta Decathlon           💡 Ventaja Decathlon
 ───────────────────────────── ───────────────────────────────────────── ────────────────────────────────
 ASICS Novablast 4 (90.00€)    ➜ Decathlon Kiprun KD900 Light (89.99€)   200g (23% más ligera) y Pebax®
 ASICS GEL-Cumulus 26 (160€)   ➜ ASICS Cumulus 26 Decathlon (94.99€)     💥 Ofertazo exclusivo -41% DTO
 ASICS GEL-Nimbus 26 (200€)    ➜ Decathlon Kiprun KS900 2 (79.99€)      Nube MFOAM por 60€ menos
 ASICS GT-2000 12 (160€)       ➜ ASICS GT-2000 12 Decathlon (114.99€)    Stock garantizado en tienda
```

---

## 🛠️ 4. Cómo Modificar el Comportamiento del Agente

Para cambiar las reglas del agente, edita este archivo `GEMINI.md` o modifica las variables en el código:

1. **Cambiar la Talla por Defecto**:
   Modifica `talla_eu` a tu talla deseada (ej: `43 EU`, `41.5 EU`) en `GEMINI.md` y en [`src/data/asicsModels.js`](file:///home/ACT/Downloads/Encontrar%20Zapatillas/src/data/asicsModels.js).

2. **Cambiar el Ritmo Objetivo**:
   - Para ritmos **< 4:30 min/km**: El agente promoverá zapatillas mixtas o de placa de carbono (Kiprun KD900X / ASICS Magic Speed).
   - Para ritmos **> 5:45 min/km**: El agente priorizará protección articular de máximo colchón (GEL-Nimbus 26 / Kiprun KS900 2).

3. **Añadir Nuevas Tiendas al Escáner**:
   Añade el nuevo comercio al array `RELIABLE_STORES` en [`src/data/asicsModels.js`](file:///home/ACT/Downloads/Encontrar%20Zapatillas/src/data/asicsModels.js) y al script [`agent_shoe_finder.py`](file:///home/ACT/Downloads/Encontrar%20Zapatillas/agent_shoe_finder.py).

4. **Ejecutar el Agente en Consola**:
   ```bash
   python3 agent_shoe_finder.py --decathlon --size 42.5 --distance 10k --pace "5:15"
   ```
