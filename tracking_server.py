#!/usr/bin/env python3
"""
SERVIDOR DE TRACKING DE EMAILS - RAILWAY.APP
- Registra aperturas de email mediante pixel 1x1
- Guarda: ID, timestamp, IP, user-agent en SQLite
- Puerto configurable para Railway
- Persistencia en base de datos
"""

from flask import Flask, request, send_file, render_template_string
from datetime import datetime
import os
import sqlite3
from pathlib import Path
import base64

app = Flask(__name__)

# Base de datos SQLite (persistente en Railway)
DB_PATH = os.environ.get('DB_PATH', 'tracking.db')

# Puerto configurable (Railway usa PORT env variable)
PORT = int(os.environ.get('PORT', 8888))

# Crear pixel transparente 1x1
PIXEL_PATH = "pixel.gif"
if not os.path.exists(PIXEL_PATH):
    pixel_data = base64.b64decode(
        "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    )
    with open(PIXEL_PATH, "wb") as f:
        f.write(pixel_data)

def init_db():
    """Inicializar base de datos SQLite"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            referer TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inicializar DB al arrancar
init_db()

@app.route('/track/<tracking_id>')
def track(tracking_id):
    """Endpoint de tracking - sirve pixel y registra apertura"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'None')

    # Registrar en base de datos
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO tracking (tracking_id, timestamp, ip_address, user_agent, referer)
        VALUES (?, ?, ?, ?, ?)
    ''', (tracking_id, timestamp, ip_address, user_agent, referer))
    conn.commit()
    conn.close()

    # Servir pixel transparente
    return send_file(PIXEL_PATH, mimetype='image/gif')

@app.route('/stats')
def stats():
    """Ver estadísticas de aperturas"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Obtener todos los trackings
    c.execute('SELECT tracking_id, timestamp, ip_address, user_agent FROM tracking ORDER BY timestamp DESC')
    rows = c.fetchall()

    # Contar únicos
    c.execute('SELECT COUNT(DISTINCT tracking_id) FROM tracking')
    unique_count = c.fetchone()[0]

    total_count = len(rows)

    conn.close()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email Tracking Stats</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Monaco', 'Courier New', monospace;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            h1 {{
                color: white;
                margin-bottom: 30px;
                font-size: 32px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .summary {{
                background: white;
                padding: 30px;
                margin-bottom: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            }}
            .summary h2 {{
                color: #667eea;
                margin-bottom: 20px;
            }}
            .stat-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}
            .stat-box {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 8px;
                color: white;
                text-align: center;
            }}
            .stat-number {{
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .stat-label {{
                font-size: 14px;
                opacity: 0.9;
            }}
            table {{
                background: white;
                border-collapse: collapse;
                width: 100%;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            }}
            th, td {{
                padding: 16px;
                text-align: left;
                border-bottom: 1px solid #e5e7eb;
            }}
            th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 1px;
            }}
            tr:hover {{
                background: #f9fafb;
            }}
            .tracking-id {{
                font-weight: bold;
                color: #667eea;
                font-family: 'Monaco', monospace;
            }}
            .timestamp {{
                color: #6b7280;
            }}
            .ip {{
                color: #059669;
            }}
            .no-data {{
                text-align: center;
                padding: 40px;
                color: #9ca3af;
            }}
            .refresh-btn {{
                background: white;
                color: #667eea;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                font-size: 14px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .refresh-btn:hover {{
                background: #f3f4f6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Email Tracking Dashboard</h1>

            <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>

            <div class="summary">
                <h2>Resumen</h2>
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="stat-number">{total_count}</div>
                        <div class="stat-label">Total Aperturas</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{unique_count}</div>
                        <div class="stat-label">Emails Únicos</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{round(total_count/max(unique_count,1), 1)}</div>
                        <div class="stat-label">Promedio Aperturas</div>
                    </div>
                </div>
            </div>

            <h2 style="color: white; margin-bottom: 20px;">Detalle de Aperturas</h2>
            <table>
                <tr>
                    <th>ID Email</th>
                    <th>Timestamp</th>
                    <th>IP</th>
                    <th>User-Agent</th>
                </tr>
    """

    if rows:
        for row in rows:
            tracking_id, timestamp, ip_address, user_agent = row
            user_agent_short = user_agent[:80] + "..." if len(user_agent) > 80 else user_agent
            html += f"""
                <tr>
                    <td class="tracking-id">{tracking_id}</td>
                    <td class="timestamp">{timestamp}</td>
                    <td class="ip">{ip_address}</td>
                    <td>{user_agent_short}</td>
                </tr>
            """
    else:
        html += """
                <tr>
                    <td colspan="4" class="no-data">No hay aperturas registradas aún</td>
                </tr>
        """

    html += """
            </table>
        </div>
    </body>
    </html>
    """

    return html

@app.route('/')
def index():
    """Página de inicio"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email Tracking Server</title>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Monaco', monospace;
                padding: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .card {{
                background: white;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                max-width: 600px;
            }}
            h1 {{
                color: #667eea;
                margin-bottom: 20px;
            }}
            .status {{
                background: #10b981;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                display: inline-block;
                margin-bottom: 30px;
                font-weight: bold;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            li {{
                padding: 12px 0;
                border-bottom: 1px solid #e5e7eb;
            }}
            a {{
                color: #667eea;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            code {{
                background: #f3f4f6;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>✅ Email Tracking Server</h1>
            <div class="status">🟢 Servidor Activo</div>

            <h3>Endpoints Disponibles:</h3>
            <ul>
                <li>📊 <a href="/stats">Ver Estadísticas de Aperturas</a></li>
                <li>📍 Pixel de tracking: <code>/track/&lt;email_id&gt;</code></li>
            </ul>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">

            <p style="color: #6b7280; font-size: 14px;">
                <strong>Uso:</strong> Incluir en emails HTML:<br>
                <code style="display: block; margin-top: 10px;">
                &lt;img src="https://TU-URL.railway.app/track/ID_UNICO" width="1" height="1" /&gt;
                </code>
            </p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check para Railway"""
    return {'status': 'ok', 'service': 'email-tracking'}

if __name__ == '__main__':
    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║   📊 EMAIL TRACKING SERVER - RAILWAY                              ║
║                                                                   ║
║   ✅ Puerto: {PORT}
║   ✅ Base de datos: {DB_PATH}
║   ✅ Endpoints: /track/<id>, /stats, /health                      ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=PORT, debug=False)
