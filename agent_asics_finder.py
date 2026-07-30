#!/usr/bin/env python3
"""
Agente Buscador de Zapatillas ASICS y Decathlon
(Redirige a agent_shoe_finder.py con soporte de Decathlon)
"""

import sys
import agent_shoe_finder

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Agente Buscador de Zapatillas ASICS & Decathlon")
    parser.add_argument("--brand", default="ALL", help="Marca de zapatillas")
    parser.add_argument("--size", default="42.5", help="Talla EU")
    parser.add_argument("--distance", default="10 km", help="Distancia por tirada")
    parser.add_argument("--pace", default="5:15", help="Ritmo habitual por km")
    parser.add_argument("--decathlon", action="store_true", default=True, help="Buscar ofertas en Decathlon")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")
    
    args = parser.parse_args()
    agent_shoe_finder.run_agent(args.brand, args.size, args.distance, args.pace, include_decathlon=True, json_output=args.json)
