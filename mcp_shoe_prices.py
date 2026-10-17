#!/usr/bin/env python3
"""
MCP Server & Extractor de Precios de Zapatillas en Tiempo Real (España)
=======================================================================
Funciona en doble modo:
1. Servidor MCP (Model Context Protocol, JSON-RPC 2.0 sobre stdio) para Antigravity.
2. Librería / CLI directo para actualizar `src/data/live_prices.json`, `agent_shoe_finder.py` y `send_report_email.py`.

Extrae precios reales, tallas disponibles en stock (ej. 42.5 EU) y URLs directas a fichas
de producto en tiendas verificadas de España (Alltricks / Grupo Decathlon, Decathlon,
i-Run, Top4Running, ASICS Oficial, El Corte Inglés, Running Emotion, Be Urban Running,
Ekosport, AtmosferaSport, Tradeinn/Runnerinn, Deporvillage, etc.).
"""

import argparse
import base64
from datetime import datetime
import json
import os
import re
import sys
import urllib.parse
import httpx

MEILISEARCH_URL = "https://search.runnea.com/indexes/products_1_prod/search"
MEILISEARCH_TOKEN = "3ea8a7b652c23b72e3b84da3d10ef0e603501047bb50cb3727b3d8310eb109ee"
RUNNEA_PRICES_API = "https://api.runnea.com/app/v1/prices/list"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "src", "data", "live_prices.json")

# Mapeo de los modelos monitoreados a sus IDs reales en el catálogo español
# Incluye tanto la versión exacta como la generación activa en tiendas si la anterior agota stock en 42.5 EU
MONITORED_MODELS_CONFIG = [
    {
        "id": "novablast-5",
        "model": "ASICS Novablast 5",
        "brand": "ASICS",
        "category": "Daily Trainer Reactiva Premium (Tu Modelo Actual)",
        "affinity": "99%",
        "pvp_default": 150.00,
        "why_fits": "👟 Tu zapatilla actual en uso. Nueva generación con espuma FlyteFoam Blast MAX, geometría en trampolín mejorada y máxima reactividad para tus 10 km a 5:15 min/km.",
        "decathlon_available": True,
        "product_ids": [("1039307", "ASICS Novablast 5"), ("1063395", "ASICS Novablast 6")],
        "whole_size_equiv": False,
        "fallback_stores": [
            {
                "name": "Decathlon España 💙",
                "price": 149.99,
                "original": 150.00,
                "stock_42_5": True,
                "shipping": "Envío gratis / Recogida 1h",
                "url": "https://www.decathlon.es/es/search?Ntt=asics+novablast+5",
            }
        ],
    },
    {
        "id": "novablast-4",
        "model": "ASICS Novablast 4 / Novablast 6",
        "brand": "ASICS",
        "category": "Daily Trainer Reactiva / Versátil",
        "affinity": "98%",
        "pvp_default": 150.00,
        "why_fits": "Perfecta para 5:15 min/km. Geometría trampolín y espuma FF Blast+ ECO / MAX para los 10 km.",
        "decathlon_available": True,
        "product_ids": [("1022029", "ASICS Novablast 4"), ("1063395", "ASICS Novablast 6")],
        "whole_size_equiv": False,
        "fallback_stores": [
            {
                "name": "Decathlon España 💙",
                "price": 119.99,
                "original": 150.00,
                "stock_42_5": True,
                "shipping": "Envío Domicilio",
                "url": "https://www.decathlon.es/es/search?Ntt=asics+novablast",
            },
        ],
    },
    {
        "id": "kiprun-kd900-light",
        "model": "Decathlon Kiprun KD900 Light / Kipstorm",
        "brand": "Decathlon Kiprun",
        "category": "Alternativa Decathlon a Novablast (Ligera y Reactiva)",
        "affinity": "96%",
        "pvp_default": 119.99,
        "why_fits": "⚡ Alternativa directa en Decathlon: Mediasuela reactiva VFOAM / Pebax® para volar a 5:15 pace con 60 días de prueba.",
        "decathlon_available": True,
        "product_ids": [
            ("1063149", "Kiprun Kipstorm Challenger"),
            ("1063147", "Kiprun Kipcore"),
            ("1032483", "Kiprun KD900 Light"),
        ],
        "whole_size_equiv": True,
        "fallback_stores": [
            {
                "name": "Decathlon España Oficial 💙",
                "price": 69.99,
                "original": 109.99,
                "stock_42_5": True,
                "shipping": "Recogida 1h gratis / 60 días prueba",
                "url": "https://www.decathlon.es/es/search?Ntt=kiprun+kd900+light",
            }
        ],
    },
    {
        "id": "cumulus-26",
        "model": "ASICS GEL-Cumulus (26 / 27 / 28)",
        "brand": "ASICS",
        "category": "Daily Trainer Equilibrada",
        "affinity": "95%",
        "pvp_default": 160.00,
        "why_fits": "Zapatilla super equilibrada (~255g) con PureGEL y FF Blast+ para rodajes diarios cómodos de 10 km.",
        "decathlon_available": True,
        "product_ids": [
            ("1022930", "ASICS GEL-Cumulus 26"),
            ("1044908", "ASICS GEL-Cumulus 27"),
            ("1062931", "ASICS GEL-Cumulus 28"),
        ],
        "whole_size_equiv": False,
        "fallback_stores": [
            {
                "name": "Decathlon España 💙",
                "price": 129.99,
                "original": 160.00,
                "stock_42_5": True,
                "shipping": "Envío a Domicilio",
                "url": "https://www.decathlon.es/es/search?Ntt=asics+cumulus",
            }
        ],
    },
    {
        "id": "nimbus-26",
        "model": "ASICS GEL-Nimbus (26 / 27 / 28)",
        "brand": "ASICS",
        "category": "Máxima Amortiguación Premium",
        "affinity": "94%",
        "pvp_default": 200.00,
        "why_fits": "Máxima protección PureGEL + FF Blast+ ECO para rodillas y articulaciones en asfalto duro.",
        "decathlon_available": True,
        "product_ids": [
            ("1022943", "ASICS GEL-Nimbus 26"),
            ("1039115", "ASICS GEL-Nimbus 27"),
            ("1058964", "ASICS GEL-Nimbus 28"),
        ],
        "whole_size_equiv": False,
        "fallback_stores": [
            {
                "name": "Decathlon España 💙",
                "price": 154.99,
                "original": 200.00,
                "stock_42_5": True,
                "shipping": "Envío gratis a domicilio",
                "url": "https://www.decathlon.es/es/search?Ntt=asics+nimbus",
            }
        ],
    },
    {
        "id": "kiprun-ks900-2",
        "model": "Decathlon Kiprun KS900 2 / Kipride",
        "brand": "Decathlon Kiprun",
        "category": "Alternativa Decathlon Amortiguación Total",
        "affinity": "93%",
        "pvp_default": 129.99,
        "why_fits": "☁️ La 'Nimbus' de Decathlon: Espuma MFOAM ultra amortiguada para proteger articulaciones por mucho menos.",
        "decathlon_available": True,
        "product_ids": [
            ("1063148", "Kiprun Kipride"),
            ("1031854", "Kiprun KS900 2"),
            ("1061975", "Kiprun Kipride Max"),
        ],
        "whole_size_equiv": True,
        "fallback_stores": [
            {
                "name": "Decathlon España Oficial 💙",
                "price": 79.99,
                "original": 129.99,
                "stock_42_5": True,
                "shipping": "Recogida 1h gratis / 60 días prueba",
                "url": "https://www.decathlon.es/es/search?Ntt=kiprun+ks900+2",
            }
        ],
    },
    {
        "id": "gt-2000-12",
        "model": "ASICS GT-2000 (12 / 13 / 14)",
        "brand": "ASICS",
        "category": "Estabilidad / Soporte de Pronación",
        "affinity": "90%",
        "pvp_default": 160.00,
        "why_fits": "Ideal si notas fatiga en el arco o tobillo en los últimos km de tu tirada de 10 km gracias al 3D Guidance System.",
        "decathlon_available": True,
        "product_ids": [
            ("1021462", "ASICS GT-2000 12"),
            ("1039116", "ASICS GT-2000 13"),
            ("1046127", "ASICS GT-2000 14"),
        ],
        "whole_size_equiv": False,
        "fallback_stores": [
            {
                "name": "Decathlon España 💙",
                "price": 124.99,
                "original": 160.00,
                "stock_42_5": True,
                "shipping": "Envío Domicilio",
                "url": "https://www.decathlon.es/es/search?Ntt=asics+gt-2000",
            }
        ],
    },
]


def unwrap_direct_url(item: dict) -> str:
    """Extrae la URL directa real de la tienda eliminando redirecciones de afiliados cuando es posible."""
    link_obj = item.get("link") or {}
    raw_url = link_obj.get("url") or ""

    # 1. Intentar decodificar el campo track (base64 con parámetros web= o url=)
    track = link_obj.get("track") or ""
    if track:
        try:
            padded = track + "=" * ((4 - len(track) % 4) % 4)
            decoded = base64.b64decode(padded).decode("utf-8", errors="ignore")
            qs = urllib.parse.parse_qs(decoded)
            if qs.get("web") and qs["web"][0].startswith("http"):
                return urllib.parse.unquote(qs["web"][0])
            if qs.get("url") and qs["url"][0].startswith("http"):
                candidate = urllib.parse.unquote(qs["url"][0])
                # Si el candidate a su vez tiene url= (ej. effiliation o awin)
                if "url=" in candidate:
                    inner_qs = urllib.parse.parse_qs(urllib.parse.urlparse(candidate).query)
                    if inner_qs.get("url"):
                        return urllib.parse.unquote(inner_qs["url"][0])
                return candidate
        except Exception:
            pass

    # 2. Si raw_url contiene parámetro url= o destination=
    if "url=" in raw_url or "ued=" in raw_url:
        try:
            inner_qs = urllib.parse.parse_qs(urllib.parse.urlparse(raw_url).query)
            for key in ("url", "ued", "destination"):
                if inner_qs.get(key) and inner_qs[key][0].startswith("http"):
                    return urllib.parse.unquote(inner_qs[key][0])
        except Exception:
            pass

    return raw_url


def is_valid_mens_running_offer(card: dict, min_valid_price: float = 55.0) -> bool:
    """
    Filtra resultados confusos:
    - Excluye modelos de Mujer (SKUs ASICS 1012B / 1012C, 'mujer', 'women', 'wmns', 'femme').
    - Excluye modelos Junior / Niño (SKUs ASICS 1014A, 'gs', 'junior', 'niño', 'kid').
    - Excluye precios absurdamente bajos o errores de catálogo (< 55€) o listings dudosos en Amazon.
    """
    price = float(card.get("price") or 0)
    if price < min_valid_price:
        return False

    name_lower = (card.get("name") or "").lower()
    url_lower = unwrap_direct_url(card).lower()
    combined = f"{name_lower} {url_lower}"

    # Excluir SKUs de mujer (1012b / 1012c) o niño (1014a) y palabras clave de mujer/niño
    forbidden_tokens = [
        "1012b",
        "1012c",
        "1014a",
        "mujer",
        "women",
        "wmns",
        "femme",
        "junior",
        "niño",
        "nino",
        "niña",
        "kids",
        "-gs-",
        " gs ",
    ]
    if any(tok in combined for tok in forbidden_tokens):
        return False

    # Filtrar ofertas falsas de terceros en Amazon (ej. Novablast 5 a 69.90€ con título genérico sin espacio "ZapatillasHombre")
    store_id = (card.get("store") or {}).get("id", "").lower()
    if store_id == "amazon" and ("zapatillashombre" in name_lower or price < 80.0):
        return False

    return True


def format_store_display_name(raw_name: str, variant_label: str = "") -> str:
    """Normaliza el nombre de la tienda con su icono característico."""
    name_map = {
        "Alltricks": "Alltricks España 🚴",
        "Decathlon": "Decathlon España 💙",
        "i-Run": "i-Run España 🏃",
        "Top4Running": "Top4Running 🏃",
        "ASICS": "ASICS Tienda Oficial 🏷️",
        "El Corte Ingles": "El Corte Inglés 🏬",
        "El Corte Inglés": "El Corte Inglés 🏬",
        "Running Emotion": "Running Emotion 👟",
        "Be Urban Running": "Be Urban Running 👟",
        "Ekosport": "Ekosport España ⛰️",
        "AtmosferaSport": "Atmósfera Sport 👟",
        "Tradeinn": "Runnerinn (Tradeinn) 📦",
        "Runnerinn": "Runnerinn (Tradeinn) 📦",
        "Deporvillage": "Deporvillage 🚴",
        "Zalando": "Zalando España 🛍️",
        "StreetProRunning": "StreetProRunning 👟",
        "Atleet": "Atleet Store 👟",
        "Amazon": "Amazon España 📦",
    }
    base = name_map.get(raw_name, raw_name)
    if variant_label:
        return f"{base} ({variant_label})"
    return base


def search_catalog(query: str, limit: int = 8) -> list:
    """Busca modelos de zapatillas en el índice Meilisearch en vivo."""
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {MEILISEARCH_TOKEN}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(
            MEILISEARCH_URL,
            headers=headers,
            json={"q": query, "limit": limit},
        )
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
        return [
            {
                "product_id": str(h.get("id")),
                "brand": h.get("brand"),
                "title": h.get("title"),
                "full_name": f"{h.get('brand', '')} {h.get('title', '')}".strip(),
                "best_price_eur": h.get("pvp_eur"),
                "surface": h.get("surface"),
                "path": h.get("path"),
            }
            for h in hits
        ]


def fetch_offers_for_product_id(
    product_id: str,
    size: str = "42.5",
    gender: str = "man",
    whole_size_equiv: bool = False,
    variant_label: str = "",
) -> list:
    """
    Consulta la API en tiempo real de precios y stock por talla para un `product_id`.
    Combina la consulta filtrada por talla exacta con la consulta general de hombre
    para obtener todas las tiendas con stock en la talla objetivo y las mejores alternativas.
    """
    target_sizes = {str(size)}
    if whole_size_equiv and size == "42.5":
        # Kiprun / Decathlon talla en enteros (42 EU / 43 EU para 27.0 cm)
        target_sizes.update({"42", "43"})

    offers = []
    seen_keys = set()

    urls_to_query = [
        f"{RUNNEA_PRICES_API}?_p=1&products_type=1&prices=1&filters=/gender-{gender}/size-{size}&products={product_id}&store_highlight=1",
        f"{RUNNEA_PRICES_API}?_p=1&products_type=1&prices=1&filters=/gender-{gender}&products={product_id}&store_highlight=1",
    ]

    with httpx.Client(timeout=10.0, headers=HEADERS) as client:
        for api_url in urls_to_query:
            try:
                resp = client.get(api_url)
                if resp.status_code != 200:
                    continue
                payload = resp.json()
                for card in payload.get("contents", []):
                    if not isinstance(card, dict) or "store" not in card:
                        continue
                    if not is_valid_mens_running_offer(card):
                        continue

                    raw_store_name = (card.get("store") or {}).get("name") or "Tienda"
                    price = round(float(card.get("price") or 0), 2)
                    pvp = round(float(card.get("pvp") or price), 2)
                    if pvp < price:
                        pvp = price

                    sizes_raw = []
                    for feat in card.get("features") or []:
                        if feat.get("id") == "size":
                            sizes_raw = feat.get("values") or []
                    sizes_str = [str(s) for s in sizes_raw]
                    has_target_size = any(ts in sizes_str for ts in target_sizes)

                    direct_url = unwrap_direct_url(card)
                    dedup_key = (raw_store_name, price, direct_url[:60])
                    if dedup_key in seen_keys:
                        continue
                    seen_keys.add(dedup_key)

                    shipping_val = card.get("shipping")
                    if shipping_val in (None, "", 0, "0"):
                        shipping_str = "Envío gratis"
                    else:
                        shipping_str = f"Envío {shipping_val}€"

                    if has_target_size:
                        size_note = f"En stock ({size} EU)"
                    elif sizes_str:
                        sample_sizes = ", ".join(sizes_str[:5])
                        size_note = f"Tallas: {sample_sizes} EU"
                    else:
                        size_note = "Consultar tallas"

                    offers.append(
                        {
                            "raw_store": raw_store_name,
                            "name": format_store_display_name(raw_store_name, variant_label),
                            "price": price,
                            "original": pvp,
                            "discount_pct": max(0, int(round(((pvp - price) / pvp) * 100))) if pvp > 0 else 0,
                            "stock_42_5": has_target_size,
                            "available_sizes": sizes_str,
                            "shipping": f"{shipping_str} • {size_note}",
                            "url": direct_url,
                            "offer_title": card.get("name") or "",
                            "product_id": str(product_id),
                            "variant_model": variant_label,
                        }
                    )
            except Exception as e:
                sys.stderr.write(f"⚠️ Error consultando API para product_id={product_id}: {e}\n")

    # Ordenar priorizando: 1) Con stock en la talla buscada, 2) Menor precio
    offers.sort(key=lambda o: (not o["stock_42_5"], o["price"]))
    return offers


def build_clean_store_list(raw_offers: list, fallback_stores: list, pvp_default: float, max_stores: int = 5) -> list:
    """
    Agrupa y selecciona las mejores ofertas verificadas por tienda:
    - Prioriza ofertas con stock confirmado en 42.5 EU (`stock_42_5=True`).
    - Deduplica por tienda + variante para no repetir 4 colores distintos de la misma tienda al mismo precio.
    - Garantiza presencia de Decathlon / tiendas clave si están en fallback.
    """
    selected = []
    seen_store_variant = set()

    # Primero ofertas con stock_42_5 = True ordenadas por precio
    in_stock = sorted([o for o in raw_offers if o["stock_42_5"]], key=lambda x: x["price"])
    out_stock = sorted([o for o in raw_offers if not o["stock_42_5"]], key=lambda x: x["price"])

    for offer in in_stock + out_stock:
        key = (offer["raw_store"], offer.get("variant_model", ""))
        if key in seen_store_variant:
            continue
        seen_store_variant.add(key)
        selected.append(
            {
                "name": offer["name"],
                "price": offer["price"],
                "original": offer["original"] or pvp_default,
                "stock_42_5": offer["stock_42_5"],
                "available_sizes": offer.get("available_sizes", []),
                "shipping": offer["shipping"],
                "url": offer["url"],
            }
        )
        if len(selected) >= max_stores:
            break

    # Asegurar que si no hay oferta directa de Decathlon pero existe fallback de Decathlon, se incluya para comparar
    has_decathlon = any("decathlon" in s["name"].lower() for s in selected)
    if not has_decathlon and fallback_stores:
        for fb in fallback_stores:
            if "decathlon" in fb["name"].lower():
                selected.append(fb)
                break

    if not selected:
        selected = list(fallback_stores)

    # Ordenar lista final por precio de menor a mayor (priorizando las que tienen stock en 42.5 EU)
    selected.sort(key=lambda s: (not s.get("stock_42_5", True), s["price"]))
    return selected


def refresh_all_monitored_shoes(size: str = "42.5", save_cache: bool = True) -> list:
    """
    Recorre todos los modelos del perfil del corredor, extrae los precios reales y el stock
    en talla `size` EU de las tiendas españolas, y guarda el resultado en `src/data/live_prices.json`.
    """
    results = []
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for cfg in MONITORED_MODELS_CONFIG:
        all_offers = []
        primary_name = cfg["product_ids"][0][1]
        for idx, (pid, label) in enumerate(cfg["product_ids"]):
            # Solo añadimos etiqueta de versión si es distinta de la primera opción principal
            v_label = label.replace("ASICS ", "").replace("Kiprun ", "") if idx > 0 else ""
            pid_offers = fetch_offers_for_product_id(
                product_id=pid,
                size=size,
                gender="man",
                whole_size_equiv=cfg.get("whole_size_equiv", False),
                variant_label=v_label,
            )
            all_offers.extend(pid_offers)
            # Si el modelo principal ya tiene >= 3 tiendas con stock en 42.5 EU, no hace falta mezclar otra generación
            in_stock_count = sum(1 for o in all_offers if o["stock_42_5"])
            if idx == 0 and in_stock_count >= 3:
                break

        stores = build_clean_store_list(
            raw_offers=all_offers,
            fallback_stores=cfg.get("fallback_stores", []),
            pvp_default=cfg["pvp_default"],
            max_stores=5,
        )

        results.append(
            {
                "id": cfg["id"],
                "model": cfg["model"],
                "brand": cfg["brand"],
                "category": cfg["category"],
                "affinity": cfg["affinity"],
                "why_fits": cfg["why_fits"],
                "decathlon_available": cfg["decathlon_available"],
                "updated_at": now_iso,
                "stores": stores,
            }
        )

    if save_cache:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        payload = {
            "updated_at": now_iso,
            "size_eu": size,
            "source": "MCP Live Shoe Price Extractor (Runnea + Multi-Store España)",
            "models": results,
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    return results


def load_cached_or_live_prices(size: str = "42.5", force_refresh: bool = False) -> list:
    """Devuelve los precios actualizados (refrescando en vivo o leyendo la caché si falla la red)."""
    if not force_refresh and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if isinstance(cached, dict) and cached.get("models"):
                    return cached["models"]
        except Exception:
            pass
    return refresh_all_monitored_shoes(size=size, save_cache=True)


# =====================================================================
# SERVIDOR MCP (JSON-RPC 2.0 sobre STDIO - Sin dependencias externas)
# =====================================================================

MCP_TOOLS = [
    {
        "name": "search_shoe_catalog",
        "description": "Busca cualquier modelo de zapatillas de running en el catálogo español en tiempo real y devuelve su ID, marca, nombre y precio mínimo actual.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Nombre de la zapatilla a buscar (ej. 'ASICS Novablast 5', 'Cumulus 28', 'Kiprun', 'Hoka Clifton').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Número máximo de resultados (por defecto 8).",
                    "default": 8,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_shoe_live_offers",
        "description": "Extrae en tiempo real todas las ofertas en tiendas de España para un modelo de zapatillas (por nombre o product_id), verificando el stock exacto en la talla EU indicada (por defecto 42.5 EU) y devolviendo enlaces directos a cada tienda.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_or_id": {
                    "type": "string",
                    "description": "Nombre del modelo (ej. 'ASICS Novablast 5') o su product_id numérico (ej. '1039307').",
                },
                "size": {
                    "type": "string",
                    "description": "Talla europea para comprobar disponibilidad en stock (por defecto '42.5').",
                    "default": "42.5",
                },
                "only_in_stock": {
                    "type": "boolean",
                    "description": "Si es true, filtra únicamente las tiendas con stock confirmado en esa talla.",
                    "default": False,
                },
            },
            "required": ["model_or_id"],
        },
    },
    {
        "name": "refresh_monitored_shoes",
        "description": "Actualiza en vivo los precios, stock en talla 42.5 EU y enlaces directos de todos los modelos del perfil del corredor y guarda la caché compartida en src/data/live_prices.json.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "size": {
                    "type": "string",
                    "description": "Talla EU objetivo (por defecto '42.5').",
                    "default": "42.5",
                }
            },
        },
    },
    {
        "name": "get_cached_deals",
        "description": "Lee inmediatamente la caché local de chollos verificados (src/data/live_prices.json) sin esperar a un nuevo escaneo de red.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]


def handle_mcp_tool_call(name: str, arguments: dict) -> dict:
    """Ejecuta la herramienta MCP solicitada y devuelve el bloque content estándar."""
    try:
        if name == "search_shoe_catalog":
            query = arguments.get("query", "")
            limit = int(arguments.get("limit", 8))
            hits = search_catalog(query, limit=limit)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(hits, indent=2, ensure_ascii=False),
                    }
                ]
            }

        elif name == "get_shoe_live_offers":
            model_or_id = str(arguments.get("model_or_id", "")).strip()
            size = str(arguments.get("size", "42.5")).strip()
            only_in_stock = bool(arguments.get("only_in_stock", False))

            product_id = model_or_id
            resolved_name = model_or_id
            if not model_or_id.isdigit():
                hits = search_catalog(model_or_id, limit=3)
                if not hits:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": f"No se encontró ningún modelo para '{model_or_id}'.",
                            }
                        ],
                        "isError": True,
                    }
                product_id = hits[0]["product_id"]
                resolved_name = hits[0]["full_name"]

            offers = fetch_offers_for_product_id(
                product_id=product_id,
                size=size,
                gender="man",
                whole_size_equiv=("kiprun" in resolved_name.lower()),
            )
            if only_in_stock:
                offers = [o for o in offers if o["stock_42_5"]]

            result = {
                "model": resolved_name,
                "product_id": product_id,
                "size_eu": size,
                "total_offers": len(offers),
                "in_stock_for_size": sum(1 for o in offers if o["stock_42_5"]),
                "offers": offers,
            }
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2, ensure_ascii=False),
                    }
                ]
            }

        elif name == "refresh_monitored_shoes":
            size = str(arguments.get("size", "42.5")).strip()
            data = refresh_all_monitored_shoes(size=size, save_cache=True)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            {
                                "status": "ok",
                                "cache_file": CACHE_FILE,
                                "models_updated": len(data),
                                "models": data,
                            },
                            indent=2,
                            ensure_ascii=False,
                        ),
                    }
                ]
            }

        elif name == "get_cached_deals":
            data = load_cached_or_live_prices(force_refresh=False)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(data, indent=2, ensure_ascii=False),
                    }
                ]
            }

        else:
            return {
                "content": [{"type": "text", "text": f"Herramienta desconocida: {name}"}],
                "isError": True,
            }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error ejecutando {name}: {e}"}],
            "isError": True,
        }


def run_mcp_stdio_server():
    """Bucle principal JSON-RPC 2.0 sobre stdio para el protocolo MCP."""
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue

        method = msg.get("method")
        msg_id = msg.get("id")

        # Notificaciones (sin id) no requieren respuesta
        if msg_id is None:
            continue

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                    },
                    "serverInfo": {
                        "name": "shoe-prices-mcp",
                        "version": "1.0.0",
                    },
                },
            }
        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": MCP_TOOLS,
                },
            }
        elif method == "tools/call":
            params = msg.get("params") or {}
            tool_name = params.get("name", "")
            tool_args = params.get("arguments") or {}
            tool_result = handle_mcp_tool_call(tool_name, tool_args)
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": tool_result,
            }
        elif method == "resources/list":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"resources": []},
            }
        elif method == "prompts/list":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"prompts": []},
            }
        elif method == "ping":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {},
            }
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}",
                },
            }

        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(description="MCP Server & Extractor de Precios de Zapatillas")
    parser.add_argument("--mcp", action="store_true", help="Ejecutar como servidor MCP sobre stdio")
    parser.add_argument("--refresh", action="store_true", help="Extraer precios en vivo y actualizar src/data/live_prices.json")
    parser.add_argument("--search", type=str, help="Buscar un modelo en el catálogo en vivo")
    parser.add_argument("--offers", type=str, help="Obtener ofertas en vivo para un modelo o ID")
    parser.add_argument("--size", type=str, default="42.5", help="Talla EU objetivo (por defecto 42.5)")
    args = parser.parse_args()

    if args.refresh:
        data = refresh_all_monitored_shoes(size=args.size, save_cache=True)
        print(f"✔ Caché actualizada en {CACHE_FILE} ({len(data)} modelos escaneados en talla {args.size} EU).")
        for m in data:
            best = m["stores"][0]
            print(f"  • {m['model']}: Mejor oferta {best['price']:.2f}€ en {best['name']} (Stock {args.size}: {best['stock_42_5']})")
        return

    if args.search:
        hits = search_catalog(args.search)
        print(json.dumps(hits, indent=2, ensure_ascii=False))
        return

    if args.offers:
        res = handle_mcp_tool_call("get_shoe_live_offers", {"model_or_id": args.offers, "size": args.size})
        print(res["content"][0]["text"])
        return

    # Por defecto, si se invoca sin argumentos o con --mcp, inicia el servidor MCP stdio
    run_mcp_stdio_server()


if __name__ == "__main__":
    main()
