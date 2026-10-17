#!/usr/bin/env python3
"""
Script para generar el Informe Semanal del Agente Buscador de Zapatillas
y enviarlo por correo electrónico HTML responsive a bretons@gmail.com.
"""

import os
import sys
import json
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Import agent module directly
import agent_shoe_finder

def generate_html_report(models_data, size="42.5", distance="10 km", pace="5:15"):
    now_str = datetime.now().strftime("%d/%m/%Y - %H:%M")

    # Calculate top recommendations
    models_with_best = []
    for item in models_data:
        best_store = min(item["stores"], key=lambda x: (not x.get("stock_42_5", True), x["price"]))
        orig_price = best_store.get("original") or item["stores"][0]["original"]
        discount_pct = max(0, int(((orig_price - best_store["price"]) / orig_price) * 100)) if orig_price else 0
        decathlon_store = next((s for s in item["stores"] if "Decathlon" in s["name"]), None)

        models_with_best.append({
            "data": item,
            "best_store": best_store,
            "original_price": orig_price,
            "discount_pct": discount_pct,
            "decathlon_store": decathlon_store
        })

    # Render HTML cards
    items_html = ""
    for idx, elem in enumerate(models_with_best, 1):
        m = elem["data"]
        best = elem["best_store"]
        dec_store = elem["decathlon_store"]

        is_kiprun = "Kiprun" in m["brand"]
        brand_badge_color = "#0284c7" if is_kiprun else "#06b6d4"
        brand_label = "Decathlon Kiprun" if is_kiprun else "ASICS"

        # Build stores table rows with direct buy buttons
        stores_rows = ""
        for s in m["stores"]:
            avail_sizes = s.get("available_sizes") or []
            sizes_preview = ", ".join(str(x) for x in avail_sizes[:6])
            if s.get("stock_42_5", True):
                sizes_sub = f'<div style="color: #64748b; font-size: 10px; margin-top: 2px;">Tallas: {sizes_preview}</div>' if sizes_preview else ''
                stock_badge = f'<span style="color: #10b981; font-weight: 700;">✓ Stock {size} EU OK</span>{sizes_sub}'
            else:
                sizes_sub = f'<div style="color: #94a3b8; font-size: 10px; margin-top: 2px;">Hay: {sizes_preview} EU</div>' if sizes_preview else ''
                stock_badge = f'<span style="color: #f59e0b; font-weight: 600;">Sin {size} EU</span>{sizes_sub}'

            dec_highlight = ' background-color: rgba(2, 132, 199, 0.15);' if "Decathlon" in s["name"] else ''
            store_url = s.get("url", "https://www.decathlon.es" if "Decathlon" in s["name"] else "https://www.zalando.es")

            stores_rows += f"""
            <tr style="border-bottom: 1px solid #1e293b;{dec_highlight}">
                <td style="padding: 10px 12px; font-weight: 600; color: #f8fafc;">{s['name']}</td>
                <td style="padding: 10px 12px; color: #38bdf8; font-weight: 700; font-size: 15px;">{s['price']:.2f}€</td>
                <td style="padding: 10px 12px; color: #94a3b8; text-decoration: line-through;">{s['original']:.2f}€</td>
                <td style="padding: 10px 12px;">{stock_badge}</td>
                <td style="padding: 10px 12px; color: #cbd5e1; font-size: 12px;">{s['shipping']}</td>
                <td style="padding: 10px 12px; text-align: right;">
                    <a href="{store_url}" target="_blank" style="background-color: #0284c7; color: #ffffff; text-decoration: none; padding: 6px 12px; border-radius: 6px; font-weight: 700; font-size: 11px; display: inline-block;">Ver Oferta →</a>
                </td>
            </tr>
            """

        decathlon_alert = ""
        if dec_store:
            dec_url = dec_store.get("url", "https://www.decathlon.es")
            decathlon_alert = f"""
            <div style="margin-top: 10px; background-color: #0369a1; background: linear-gradient(135deg, #0284c7, #0369a1); padding: 12px 16px; border-radius: 8px; color: #ffffff; font-size: 13px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    💙 <strong>Oferta Decathlon:</strong> <span style="font-size: 16px; font-weight: 800;">{dec_store['price']:.2f}€</span> | {dec_store['shipping']}
                </div>
                <a href="{dec_url}" target="_blank" style="background-color: #ffffff; color: #0369a1; text-decoration: none; padding: 6px 12px; border-radius: 6px; font-weight: 800; font-size: 11px;">Ver en Decathlon →</a>
            </div>
            """

        items_html += f"""
        <div style="background-color: #0f172a; border: 1px solid #334155; border-radius: 14px; padding: 20px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap;">
                <div>
                    <span style="background-color: {brand_badge_color}; color: #ffffff; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{brand_label}</span>
                    <span style="color: #94a3b8; font-size: 12px; margin-left: 8px;">Afinidad: <strong style="color: #10b981;">{m['affinity']}</strong></span>
                </div>
                <div style="background-color: #059669; color: #ffffff; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 800;">
                    🔥 Mejor Precio: {best['price']:.2f}€ (-{elem['discount_pct']}%)
                </div>
            </div>

            <h2 style="color: #f8fafc; margin: 8px 0; font-size: 20px; font-weight: 800;">{idx}. {m['model']}</h2>
            <p style="color: #38bdf8; font-size: 13px; font-weight: 600; margin-top: 0; margin-bottom: 12px;">{m['category']}</p>
            <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6; background-color: #1e293b; padding: 12px 14px; border-radius: 8px; margin-bottom: 16px;">
                💡 <strong>Por qué encaja:</strong> {m['why_fits']}
            </p>

            {decathlon_alert}

            <h4 style="color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 18px; margin-bottom: 8px;">Comparativa de Tiendas en Talla {size} EU:</h4>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
                    <thead>
                        <tr style="border-bottom: 2px solid #334155; color: #94a3b8; font-size: 11px; text-transform: uppercase;">
                            <th style="padding: 8px 12px;">Tienda</th>
                            <th style="padding: 8px 12px;">Precio Oferta</th>
                            <th style="padding: 8px 12px;">PVP Original</th>
                            <th style="padding: 8px 12px;">Stock {size} EU</th>
                            <th style="padding: 8px 12px;">Envío / Garantía</th>
                            <th style="padding: 8px 12px; text-align: right;">Acceso Directo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stores_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """

    # Build top summary table (1 row per model with its single best price in 42.5 EU)
    sorted_by_price = sorted(
        models_with_best,
        key=lambda x: (not x["best_store"].get("stock_42_5", True), x["best_store"]["price"])
    )
    top_summary_rows = ""
    for rank, deal in enumerate(sorted_by_price, 1):
        m = deal["data"]
        best = deal["best_store"]
        best_url = best.get("url", "https://www.decathlon.es")
        stock_pill = (
            f'<span style="color: #10b981; font-size: 11px; font-weight: 700;">✓ {size} EU en stock</span>'
            if best.get("stock_42_5", True)
            else f'<span style="color: #f59e0b; font-size: 11px;">Sin {size} EU</span>'
        )
        dto_badge = (
            f'<span style="background-color: rgba(16, 185, 129, 0.2); color: #34d399; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; margin-left: 6px;">-{deal["discount_pct"]}%</span>'
            if deal["discount_pct"] > 0
            else ""
        )
        row_bg = "background-color: rgba(16, 185, 129, 0.07);" if rank == 1 else ""

        top_summary_rows += f"""
        <tr style="border-bottom: 1px solid #1e293b; {row_bg}">
            <td style="padding: 12px 10px;">
                <div style="font-weight: 800; color: #f8fafc; font-size: 14px;">{m['model']}</div>
                <div style="color: #94a3b8; font-size: 11px; margin-top: 2px;">{m['category']}</div>
            </td>
            <td style="padding: 12px 10px; white-space: nowrap;">
                <span style="color: #34d399; font-weight: 900; font-size: 17px;">{best['price']:.2f}€</span>
                {dto_badge}
                <div style="color: #64748b; font-size: 11px; text-decoration: line-through;">PVP: {deal['original_price']:.2f}€</div>
            </td>
            <td style="padding: 12px 10px;">
                <div style="color: #e2e8f0; font-weight: 700; font-size: 13px;">{best['name']}</div>
                <div>{stock_pill}</div>
            </td>
            <td style="padding: 12px 10px; text-align: right; white-space: nowrap;">
                <a href="{best_url}" target="_blank" style="background-color: #10b981; color: #022c22; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-weight: 800; font-size: 12px; display: inline-block;">Comprar →</a>
            </td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>👟 Informe Semanal de Zapatillas - Agente AI</title>
</head>
<body style="margin: 0; padding: 0; background-color: #020617; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #e2e8f0;">
    <div style="max-width: 720px; margin: 0 auto; padding: 24px 16px;">

        <!-- Header -->
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 1px solid #38bdf8; border-radius: 16px; padding: 24px 20px; margin-bottom: 24px; text-align: center;">
            <div style="display: inline-block; background-color: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.4); color: #38bdf8; padding: 4px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-bottom: 10px;">
                🔌 MCP EXTRACTOR MULTI-TIENDA • STOCK {size} EU VERIFICADO
            </div>
            <h1 style="color: #ffffff; font-size: 24px; font-weight: 900; margin: 0 0 8px 0; letter-spacing: -0.5px;">
                👟 Mejores Precios de la Semana ({size} EU)
            </h1>
            <p style="color: #94a3b8; font-size: 13px; margin: 0 0 14px 0;">
                Actualizado el {now_str} • Perfil: <strong>{distance}</strong> a <strong>{pace} min/km</strong>
            </p>
        </div>

        <!-- TOP SUMMARY TABLE: BEST PRICE PER MODEL RIGHT AT THE TOP -->
        <div style="background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%); border: 2px solid #10b981; border-radius: 16px; padding: 20px; margin-bottom: 28px; box-shadow: 0 8px 24px rgba(16, 185, 129, 0.15);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap;">
                <h2 style="color: #34d399; margin: 0; font-size: 18px; font-weight: 900;">
                    ⚡ Resumen Directo: Mejor Precio por Modelo (Talla {size} EU)
                </h2>
                <span style="color: #a7f3d0; font-size: 12px; font-weight: 600;">Ordenado de más barato a más caro</span>
            </div>
            <div style="overflow-x: auto; background-color: #090d16; border-radius: 12px; border: 1px solid #1e293b;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
                    <thead>
                        <tr style="border-bottom: 2px solid #1e293b; color: #94a3b8; font-size: 11px; text-transform: uppercase;">
                            <th style="padding: 10px;">Zapatilla</th>
                            <th style="padding: 10px;">Mejor Precio</th>
                            <th style="padding: 10px;">Tienda Ganadora</th>
                            <th style="padding: 10px; text-align: right;">Enlace Directo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {top_summary_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Detailed Breakdown Header -->
        <h3 style="color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin: 32px 0 16px 4px;">
            📋 Detalle Completo por Modelo y Otras Tiendas:
        </h3>

        <!-- Shoe Cards -->
        {items_html}

        <!-- Footer -->
        <div style="text-align: center; font-size: 12px; color: #64748b; margin-top: 32px; border-t: 1px solid #1e293b; padding-top: 20px;">
            <p>Este correo ha sido generado por el <strong>Servidor MCP Extractor de Precios de Zapatillas (Decathlon & Multi-Tienda)</strong>.</p>
            <p style="font-size: 11px;">Ejecutado automáticamente todos los viernes por la mañana vía GitHub Actions.</p>
        </div>
    </div>
</body>
</html>
"""
    return html

def send_email(recipient, subject, html_content, smtp_server="smtp.gmail.com", smtp_port=465, sender_email=None, password=None):
    if not sender_email or not password:
        raise ValueError("Se requieren credenciales SMTP (sender_email y password/app_password).")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Agente Zapatillas <{sender_email}>"
    msg["To"] = recipient

    part_html = MIMEText(html_content, "html")
    msg.attach(part_html)

    print(f"📧 Conectando a {smtp_server}:{smtp_port}...")
    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient, msg.as_string())
    else:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient, msg.as_string())

    print(f"✅ ¡Correo enviado con éxito a {recipient}!")

def main():
    parser = argparse.ArgumentParser(description="Envía por correo el informe semanal del Agente Buscador de Zapatillas")
    parser.add_argument("--to", default="bretons@gmail.com", help="Correo destinatario")
    parser.add_argument("--sender", help="Correo remitente (o variable SMTP_USER / MAIL_USER)")
    parser.add_argument("--password", help="Contraseña de aplicación SMTP (o variable SMTP_PASSWORD / MAIL_PASSWORD)")
    parser.add_argument("--smtp-server", default="smtp.gmail.com", help="Servidor SMTP")
    parser.add_argument("--smtp-port", type=int, default=465, help="Puerto SMTP (465 para SSL, 587 para TLS)")
    parser.add_argument("--size", default="42.5", help="Talla EU")
    parser.add_argument("--preview", action="store_true", help="Guarda una vista previa local en report_preview.html")
    parser.add_argument("--dry-run", action="store_true", help="Genera el HTML y simula el proceso sin enviar")

    args = parser.parse_args()

    # Obtain credentials from flags or environment variables
    sender_email = args.sender or os.environ.get("SMTP_USER") or os.environ.get("MAIL_USER")
    password = args.password or os.environ.get("SMTP_PASSWORD") or os.environ.get("MAIL_PASSWORD")

    print("👟 Consultando precios en tiempo real con el Servidor MCP...")
    models_data = agent_shoe_finder.fetch_live_prices_with_gemini(
        agent_shoe_finder.MODELS_DATA,
        size=args.size
    )

    html_content = generate_html_report(models_data, size=args.size)

    preview_file = "report_preview.html"
    with open(preview_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"📄 Vista previa guardada con éxito en {preview_file}")

    if args.dry_run:
        print("🚀 Dry-run finalizado sin errores.")
        return

    subject = f"👟 Informe Semanal de Zapatillas ({args.size} EU) - Best Deals {datetime.now().strftime('%d/%m/%Y')}"

    try:
        send_email(
            recipient=args.to,
            subject=subject,
            html_content=html_content,
            smtp_server=args.smtp_server,
            smtp_port=args.smtp_port,
            sender_email=sender_email,
            password=password
        )
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        if not (args.preview or args.dry_run):
            sys.exit(1)

if __name__ == "__main__":
    main()
