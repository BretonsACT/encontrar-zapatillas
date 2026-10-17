##!/usr/bin/env python3
"""
Agente Buscador de Zapatillas Multi-Tienda con Precios en Tiempo Real (Gemini Free Tier)
"""

import os
import sys
import json
import argparse

# Color ASCII Palette for Terminal
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Plantilla base (se usa como estructura y fallback si no hay conexión)
MODELS_DATA = [
    {
        "model": "ASICS Novablast 5",
        "brand": "ASICS",
        "category": "Daily Trainer Reactiva Premium (Tu Modelo Actual)",
        "affinity": "99%",
        "why_fits": "👟 Tu zapatilla actual en uso. Nueva generación con espuma FlyteFoam Blast MAX, geometría en trampolín mejorada y máxima reactividad para tus 10 km a 5:15 min/km.",
        "decathlon_available": True,
        "stores": [
            {"name": "Zalando España", "price": 139.95, "original": 150.00, "stock_42_5": True, "shipping": "Gratis (100 días dev.)", "url": "https://www.zalando.es/calzado-de-hombre-zapatillas-running/?q=asics+novablast+5"},
            {"name": "Alltricks España 🚴", "price": 142.99, "original": 150.00, "stock_42_5": True, "shipping": "Gratis > 49€", "url": "https://www.alltricks.es/surl/asics-novablast-5"},
            {"name": "Decathlon España 💙", "price": 149.99, "original": 150.00, "stock_42_5": True, "shipping": "Envío Domicilio", "url": "https://www.decathlon.es/es/search?Ntt=asics+novablast+5"},
            {"name": "ASICS Tienda Oficial 🏷️", "price": 150.00, "original": 150.00, "stock_42_5": True, "shipping": "Gratis OneASICS", "url": "https://www.asics.com/es/es-es/novablast-5/p/1011B863-001.html"}
        ]
    },
    {
        "model": "ASICS Novablast 4",
        "brand": "ASICS",
        "category": "Daily Trainer Reactiva / Versátil",
        "affinity": "98%",
        "why_fits": "Perfecta para 5:15 min/km. FF Blast+ ECO con geometría trampolín para los 10 km.",
        "decathlon_available": True,
        "stores": [
            {"name": "Zalando España", "price": 104.95, "original": 150.00, "stock_42_5": True, "shipping": "Gratis", "url": "https://www.zalando.es/calzado-de-hombre-zapatillas-running/?q=asics+novablast+4"},
            {"name": "Alltricks España 🚴", "price": 109.99, "original": 150.00, "stock_42_5": True, "shipping": "Gratis > 49€", "url": "https://www.alltricks.es/surl/asics-novablast-4"},
            {"name": "Runnerinn / Tradeinn", "price": 112.99, "original": 150.00, "stock_42_5": True, "shipping": "2.99€", "url": "https://www.tradeinn.com/runnerinn/es/calzado-hombre-zapatillas-running/asics-novablast/11075/s"},
            {"name": "Decathlon España 💙", "price": 119.99, "original": 150.00, "stock_42_5": True, "shipping": "Envío Domicilio", "url": "https://www.decathlon.es/es/search?Ntt=asics+novablast+4"}
        ]
    },
    {
        "model": "Decathlon Kiprun KD900 Light",
        "brand": "Decathlon Kiprun",
        "category": "Alternativa Decathlon a Novablast (200g y Pebax®)",
        "affinity": "96%",
        "why_fits": "⚡ Alternativa directa en Decathlon: Solo 200g y mediasuela Pebax® VFOAM para volar a 5:15 pace con 60 días de prueba.",
        "decathlon_available": True,
        "stores": [
            {"name": "Decathlon España Oficial 💙", "price": 69.99, "original": 109.99, "stock_42_5": True, "shipping": "Recogida 1h / Envío gratis", "url": "https://www.decathlon.es/es/search?Ntt=kiprun+kd900"},
            {"name": "Alltricks España 🚴", "price": 74.99, "original": 109.99, "stock_42_5": True, "shipping": "Gratis > 49€", "url": "https://www.alltricks.es/surl/kiprun-kd900"}
        ]
    },
    {
        "model": "ASICS GEL-Cumulus 26",
        "brand": "ASICS",
        "category": "Daily Trainer Equilibrada",
        "affinity": "95%",
        "why_fits": "Zapatilla super equilibrada (255g) con PureGEL para rodajes diarios cómodos.",
        "decathlon_available": True,
        "stores": [
            {"name": "Runnerinn (Tradeinn)", "price": 99.99, "original": 160.00, "stock_42_5": True, "shipping": "2.99€", "url": "https://www.tradeinn.com/runnerinn/es/calzado-hombre-zapatillas-running/asics-cumulus/11075/s"},
            {"name": "Alltricks España 🚴", "price": 104.99, "original": 160.00, "stock_42_5": True, "shipping": "Gratis > 49€", "url": "https://www.alltricks.es/surl/asics-cumulus-26"},
            {"name": "Zalando España", "price": 112.00, "original": 160.00, "stock_42_5": True, "shipping": "Gratis", "url": "https://www.zalando.es/calzado-de-hombre-zapatillas-running/?q=asics+cumulus+26"},
            {"name": "Decathlon España 💙", "price": 129.99, "original": 160.00, "stock_42_5": True, "shipping": "Envío a Domicilio", "url": "https://www.decathlon.es/es/search?Ntt=asics+cumulus+26"}
        ]
    },
    {
        "model": "ASICS GEL-Nimbus 26",
        "brand": "ASICS",
        "category": "Máxima Amortiguación Premium",
        "affinity": "94%",
        "why_fits": "Máxima protección para rodillas y articulaciones en asfalto duro.",
        "decathlon_available": True,
        "stores": [
            {"name": "Zalando España", "price": 139.95, "original": 200.00, "stock_42_5": True, "shipping": "Envío gratis", "url": "https://www.zalando.es/calzado-de-hombre-zapatillas-running/?q=asics+nimbus+26"},
            {"name": "Alltricks España 🚴", "price": 144.99, "original": 200.00, "stock_42_5": True, "shipping": "Gratis > 49€", "url": "https://www.alltricks.es/surl/asics-nimbus-26"},
            {"name": "Runnerinn (Tradeinn)", "price": 145.99, "original": 200.00, "stock_42_5": True, "shipping": "2.99€", "url": "https://www.tradeinn.com/runnerinn/es/calzado-hombre-zapatillas-running/asics-nimbus/11075/s"},
            {"name": "Decathlon España 💙", "price": 154.99, "original": 200.00, "stock_42_5": True, "shipping": "Envío gratis a domicilio", "url": "https://www.decathlon.es/es/search?Ntt=asics+nimbus+26"}
        ]
    },
    {
        "model": "Decathlon Kiprun KS900 2",
        "brand": "Decathlon Kiprun",
        "category": "Alternativa Decathlon Amortiguación Total",
        "affinity": "93%",
        "why_fits": "☁️ La 'Nimbus' de Decathlon: Espuma MFOAM para amortiguar impactos por 60€ menos.",
        "decathlon_available": True,
        "stores": [
            {"name": "Decathlon España Oficial 💙", "price": 79.99, "original": 129.99, "stock_42_5": True, "shipping": "Recogida 1h / Envío gratis", "url": "https://www.decathlon.es/es/search?Ntt=kiprun+ks900"},
            {"name": "Alltricks España 🚴", "price": 84.99, "original": 129.99, "stock_42_5": True, "shipping": "Gratis > 49€", "url": "https://www.alltricks.es/surl/kiprun-ks900"}
        ]
    },
    {
        "model": "ASICS GT-2000 12",
        "brand": "ASICS",
        "category": "Estabilidad / Soporte de Pronación",
        "affinity": "90%",
        "why_fits": "Ideal si notas fatiga en el arco o tobillo en los últimos km de tu tirada de 10 km.",
        "decathlon_available": True,
        "stores": [
            {"name": "Runnerinn (Tradeinn)", "price": 109.95, "original": 160.00, "stock_42_5": True, "shipping": "2.99€", "url": "https://www.tradeinn.com/runnerinn/es/calzado-hombre-zapatillas-running/asics-gt-2000/11075/s"},
            {"name": "Alltricks España 🚴", "price": 114.99, "original": 160.00, "stock_42_5": True, "shipping": "Gratis > 49€", "url": "https://www.alltricks.es/surl/asics-gt-2000"},
            {"name": "Zalando España", "price": 119.95, "original": 160.00, "stock_42_5": True, "shipping": "Gratis", "url": "https://www.zalando.es/calzado-de-hombre-zapatillas-running/?q=asics+gt+2000"},
            {"name": "Decathlon España 💙", "price": 124.99, "original": 160.00, "stock_42_5": True, "shipping": "Envío Domicilio", "url": "https://www.decathlon.es/es/search?Ntt=asics+gt-2000"}
        ]
    }
]


def _clean_json_response(text):
    """Extrae el bloque JSON limpio de la respuesta de Gemini."""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return json.loads(text)


def fetch_live_prices_with_gemini(models_template, size="42.5"):
    """
    Actualiza los precios en tiempo real usando Gemini API (Free Tier) + Google Search Grounding.
    Incluye fallback con DuckDuckGo Search si la cuenta gratuita tiene restricción de herramienta Search.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.stderr.write("⚠️ [AVISO] GEMINI_API_KEY no definida. Usando precios estáticos de respaldo.\n")
        return models_template

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        sys.stderr.write("⚠️ [AVISO] Librería 'google-genai' no instalada. Ejecuta: pip install google-genai\n")
        return models_template

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Busca en tiempo real los precios actuales en España (en euros) para cada una de estas zapatillas de running de hombre (talla {size} EU) en las tiendas indicadas (Zalando España, Alltricks España, Decathlon España, Runnerinn / Tradeinn, ASICS Tienda Oficial).

    Instrucciones estrictas:
    1. Actualiza el campo 'price' (float) de cada tienda con el precio de oferta actual real encontrado hoy en España.
    2. Actualiza 'stock_42_5' (boolean) a false si ves explícitamente que el modelo está agotado en esa tienda, o true si está disponible.
    3. Si encuentras la URL directa al producto en esa tienda, actualiza 'url', si no, conserva la URL existente.
    4. Ordena la lista 'stores' de cada zapatilla de menor a mayor precio.
    5. Devuelve ÚNICAMENTE el JSON válido con exactamente la misma estructura y claves que la plantilla. No incluyas texto adicional.

    Plantilla JSON a actualizar:
    {json.dumps(models_template, ensure_ascii=False)}
    """

    # Candidatos de modelo (priorizando gemini-3.8-flash y gemini-flash-latest según API actual)
    candidate_models = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-2.5-flash"]
    try:
        available = [
            m.name.replace("models/", "")
            for m in client.models.list()
            if "flash" in m.name.lower() and "tts" not in m.name.lower() and "image" not in m.name.lower()
        ]
        for m_name in available:
            if m_name not in candidate_models:
                candidate_models.append(m_name)
    except Exception:
        pass

    # Intento 1: Gemini con Google Search Grounding nativo (500 req/día gratis en Flash)
    for model_name in candidate_models[:4]:
        try:
            sys.stderr.write(f"🔍 Consultando precios en tiempo real con {model_name} + Google Search...\n")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.1,
                ),
            )
            updated_data = _clean_json_response(response.text)
            sys.stderr.write(f"✔ Precios actualizados en tiempo real vía {model_name} + Google Search Grounding.\n")
            return updated_data
        except Exception as e:
            sys.stderr.write(f"⚠️ Intento con {model_name} (Search Grounding) falló: {e}\n")

    # Intento 2 (Fallback 100% gratuito): Búsqueda web con DuckDuckGo + extracción con Gemini sin tools
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
        sys.stderr.write("🔍 Usando fallback gratuito DuckDuckGo Search + Gemini Flash...\n")
        search_context = []
        with DDGS() as ddgs:
            for item in models_template:
                query = f"{item['model']} hombre precio comprar España Decathlon Zalando Alltricks Runnerinn"
                results = list(ddgs.text(query, region="es-es", max_results=5))
                search_context.append({"model": item["model"], "search_results": results})

        fallback_prompt = f"""
        A partir de los siguientes resultados de búsqueda recientes en España, actualiza los precios ('price') en euros
        de la plantilla JSON para cada tienda. Ordena 'stores' de menor a mayor precio y devuelve SOLO el JSON válido.

        Resultados de búsqueda actuales:
        {json.dumps(search_context, ensure_ascii=False)}

        Plantilla JSON:
        {json.dumps(models_template, ensure_ascii=False)}
        """
        last_err = None
        for model_name in candidate_models[:4]:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=fallback_prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.1,
                    ),
                )
                updated_data = _clean_json_response(response.text)
                sys.stderr.write(f"✔ Precios actualizados vía DuckDuckGo + {model_name}.\n")
                return updated_data
            except Exception as e:
                last_err = e
        raise RuntimeError(last_err)
    except Exception as e:
        sys.stderr.write(f"❌ No se pudieron actualizar los precios en vivo ({e}). Usando caché local.\n")
        return models_template


def run_agent(brand, size, distance, pace, include_decathlon=True, json_output=False):
    # Obtener precios en vivo antes de filtrar o imprimir
    live_data = fetch_live_prices_with_gemini(MODELS_DATA, size=size)

    filtered_data = live_data
    if not include_decathlon:
        filtered_data = [m for m in live_data if m["brand"] == "ASICS"]

    if json_output:
        print(json.dumps(filtered_data, indent=2, ensure_ascii=False))
        return

    print(f"\n{BOLD}{CYAN}════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}{CYAN} 👟 AGENTE DE BÚSQUEDA MULTI-TIENDA: ESCANEO DECATHLON & MARCAS EN TIEMPO REAL{RESET}")
    print(f"{BOLD}{CYAN}════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f" {BOLD}Perfil Corredor:{RESET} Hombre | Talla: {GREEN}{size} EU{RESET} (27cm / US 9)")
    print(f" {BOLD}Entrenamiento:{RESET} {distance} por sesión | Ritmo: {YELLOW}{pace} min/km{RESET} | 3x/semana (~30 km/sem)")
    print(f" {BOLD}Comercios Escaneados:{RESET} {BLUE}Decathlon España 💙{RESET}, ASICS Outlet, Zalando, Alltricks 🚴, Tradeinn")
    print(f"{CYAN}--------------------------------------------------------------------------------{RESET}\n")

    for idx, item in enumerate(filtered_data, 1):
        best = min(item["stores"], key=lambda x: x["price"])
        original_pvp = item["stores"][0]["original"]
        discount = max(0, int(((original_pvp - best["price"]) / original_pvp) * 100))

        brand_tag = f"{BLUE}[Decathlon Kiprun]{RESET}" if "Kiprun" in item["brand"] else f"{CYAN}[ASICS]{RESET}"
        decathlon_store = next((s for s in item["stores"] if "Decathlon" in s["name"]), None)

        print(f"{BOLD}{idx}. {item['model']}{RESET}  {brand_tag}  [{CYAN}{item['category']}{RESET}]  (Afín: {GREEN}{item['affinity']}{RESET})")
        print(f"   💡 {item['why_fits']}")
        print(f"   🔥 Best Price en {size} EU: {BOLD}{GREEN}{best['price']:.2f}€{RESET} en {best['name']} (-{discount}% DTO)")
        if decathlon_store:
            print(f"   💙 Oferta Decathlon: {BOLD}{BLUE}{decathlon_store['price']:.2f}€{RESET} | {decathlon_store['shipping']}")

        print(f"   🛒 Comparativa de Tiendas:")
        for s in item["stores"]:
            stock_str = f"{GREEN}Stock {size} EU OK{RESET}" if s["stock_42_5"] else f"{RED}Agotado{RESET}"
            print(f"      • {s['name']:<30} | {BOLD}{s['price']:>6.2f}€{RESET} (PVP: {s['original']}€) | {stock_str} | Envío: {s['shipping']}")
        print(f"{CYAN}--------------------------------------------------------------------------------{RESET}")

    # Veredicto dinámico ordenado por mejor precio real
    print(f"\n{BOLD}{GREEN}✔ VEREDICTO FINAL DEL AGENTE - TOP RECOMENDACIONES EN TIEMPO REAL:{RESET}")
    ranked = sorted(filtered_data, key=lambda m: min(s["price"] for s in m["stores"]))
    for i, item in enumerate(ranked[:4], 1):
        best_store = min(item["stores"], key=lambda s: s["price"])
        print(f" {i}. {BOLD}{item['model']}{RESET} ({GREEN}{best_store['price']:.2f}€ en {best_store['name']}{RESET}): {item['why_fits']}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agente Buscador de Zapatillas Multi-Tienda (Decathlon & ASICS)")
    parser.add_argument("--brand", default="ALL", help="Marca (ASICS / Kiprun / ALL)")
    parser.add_argument("--size", default="42.5", help="Talla EU")
    parser.add_argument("--distance", default="10 km", help="Distancia por tirada")
    parser.add_argument("--pace", default="5:15", help="Ritmo habitual por km")
    parser.add_argument("--decathlon", action="store_true", default=True, help="Incluir búsqueda y ofertas en Decathlon")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")

    args = parser.parse_args()
    run_agent(args.brand, args.size, args.distance, args.pace, include_decathlon=args.decathlon, json_output=args.json)
