#!/usr/bin/env bash
# Script para configurar una tarea cron local en Linux (Todos los viernes a las 9:00 AM)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_EXEC="$(which python3)"
CRON_CMD="0 9 * * 5 cd $PROJECT_DIR && $PYTHON_EXEC send_report_email.py --to bretons@gmail.com >> $PROJECT_DIR/cron_output.log 2>&1"

echo "👟 Configurando tarea Cron local en Linux..."
echo "Directorio del proyecto: $PROJECT_DIR"
echo "Comando a programar: $CRON_CMD"

# Check if cron job already exists
(crontab -l 2>/dev/null | grep -F "send_report_email.py") >/dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "⚠️ La tarea cron ya está instalada en tu sistema."
else
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✅ Tarea cron añadida con éxito. Se ejecutará todos los viernes a las 9:00 AM."
fi

echo ""
echo "Para verificar tus tareas cron actuales ejecuta: crontab -l"
