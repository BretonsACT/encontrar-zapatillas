# 👟 Agente Buscador de Zapatillas Multi-Tienda (Decathlon + ASICS + Alltricks)

Aplicación web interactiva y agente CLI de búsqueda automática de chollos en zapatillas para **Decathlon España**, **ASICS Outlet**, **Alltricks**, **Zalando**, **Deporvillage**, **Top4Running** y **Tradeinn**.

---

## 👤 Perfil del Corredor (Configuración por Defecto)
* **Género:** Hombre
* **Talla:** 42.5 EU (27.0 cm / US 9)
* **Distancia:** 10 km por sesión
* **Ritmo:** 5:15 min/km
* **Frecuencia:** 3 salidas/semana (~30 km/semana)
* **Destinatario de Informes:** `bretons@gmail.com`

---

## 🚀 Tareas y Scripts Incluidos

### 1. Ejecutar el Agente en Consola CLI
```bash
python3 agent_shoe_finder.py --decathlon --size 42.5 --distance "10 km" --pace "5:15"
```

### 2. Generar y Probar el Informe HTML por Correo
```bash
# Vista previa sin enviar correo (guarda report_preview.html)
python3 send_report_email.py --to bretons@gmail.com --dry-run --preview

# Enviar correo real (requiere credenciales SMTP en variables de entorno)
MAIL_USER="tu_correo@gmail.com" MAIL_PASSWORD="tu_app_password" python3 send_report_email.py --to bretons@gmail.com
```

### 3. Programación Automática los Viernes a las 9:00 AM (GitHub Actions)
El repositorio incluye un workflow en [`.github/workflows/weekly_shoe_finder.yml`](.github/workflows/weekly_shoe_finder.yml) que ejecuta el agente todos los **viernes por la mañana** (07:00 UTC / 09:00 AM en España) y envía los chollos actualizados a `bretons@gmail.com`.

---

## ⚙️ Pasos para Conectar con tu Repositorio de GitHub

1. **Crear un Repositorio en GitHub:**
   Crea un nuevo repositorio en [GitHub.com](https://github.com/new) llamado `encontrar-zapatillas`.

2. **Subir el Código:**
   ```bash
   git remote add origin https://github.com/TU_USUARIO/encontrar-zapatillas.git
   git branch -M main
   git push -u origin main
   ```

3. **Configurar los Secretos en GitHub:**
   Ve a **Settings > Secrets and variables > Actions** en tu repositorio de GitHub y añade dos secretos:
   - `MAIL_USER`: Tu dirección de correo Gmail remitente.
   - `MAIL_PASSWORD`: Tu **Contraseña de Aplicación de Google** (Generada en `myaccount.google.com/apppasswords`).

¡Y listo! Cada viernes a las 9:00 AM recibirás automáticamente el informe de chollos en `bretons@gmail.com`.
