import os
import sys
import webbrowser

# Determinar el directorio base dinámicamente (para script .py o ejecutable .exe)
if getattr(sys, 'frozen', False):
  BASE_DIR = os.path.dirname(sys.executable)
else:
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def generar_y_abrir_reporte(titulo, estadisticas, canciones_procesadas):
  """Genera un archivo HTML estético y lo abre en el navegador predeterminado."""

  # 1. Crear la subcarpeta 'reportes_html' si no existe
  carpeta_reportes = os.path.join(BASE_DIR, 'reportes_html')
  os.makedirs(carpeta_reportes, exist_ok=True)

  # 2. Definir nombre y ruta completa del archivo HTML
  nombre_archivo = f'reporte_{titulo.lower().replace(" ", "_")}.html'
  ruta_html = os.path.join(carpeta_reportes, nombre_archivo)

  # 3. Construcción del contenido HTML
  html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte - {titulo}</title>
    <style>
        :root {{
            --bg-color: #121212;
            --card-bg: #181818;
            --card-hover: #282828;
            --accent-green: #1db954;
            --accent-red: #e91429;
            --accent-blue: #2e77d0;
            --text-main: #ffffff;
            --text-sub: #b3b3b3;
            --border: #333333;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 900px;
            width: 100%;
        }}
        header {{
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            margin: 0;
            color: var(--accent-green);
            font-size: 2rem;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: var(--card-bg);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border);
            text-align: center;
        }}
        .stat-value {{
            font-size: 1.8rem;
            font-weight: bold;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--card-bg);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
        }}
        th {{
            background-color: #222222;
            color: var(--text-sub);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        tr {{
            border-bottom: 1px solid var(--border);
        }}
        tr:hover {{
            background-color: var(--card-hover);
        }}
        .badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            display: inline-block;
        }}
        .badge-agregada {{ background: rgba(29, 185, 84, 0.2); color: var(--accent-green); }}
        .badge-guardada {{ background: rgba(46, 119, 208, 0.2); color: var(--accent-blue); }}
        .badge-excluida {{ background: rgba(233, 20, 41, 0.2); color: var(--accent-red); }}
        .badge-ya-existia {{ background: rgba(255, 255, 255, 0.1); color: var(--text-sub); }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎵 Reporte de Ejecución: {titulo}</h1>
            <p style="color: var(--text-sub); margin-top: 5px;">Sincronización de playlists y análisis de Last.fm</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div style="color: var(--text-sub);">Canciones Nuevas</div>
                <div class="stat-value" style="color: var(--accent-green);">{estadisticas.get('agregadas', 0)}</div>
            </div>
            <div class="stat-card">
                <div style="color: var(--text-sub);">Enviadas a "Me Gusta"</div>
                <div class="stat-value" style="color: var(--accent-blue);">{estadisticas.get('guardadas', 0)}</div>
            </div>
            <div class="stat-card">
                <div style="color: var(--text-sub);">Ya estaban en "Me Gusta"</div>
                <div class="stat-value" style="color: var(--text-sub);">{estadisticas.get('ya_en_megusta', 0)}</div>
            </div>
            <div class="stat-card">
                <div style="color: var(--text-sub);">Excluidas por Género</div>
                <div class="stat-value" style="color: var(--accent-red);">{estadisticas.get('excluidas', 0)}</div>
            </div>
        </div>

        <h2>Detalle de Canciones Procesadas</h2>
        <table>
            <thead>
                <tr>
                    <th>Acción</th>
                    <th>Canción</th>
                    <th>Artista</th>
                    <th>Detalle / Escuchas</th>
                </tr>
            </thead>
            <tbody>
"""

  if not canciones_procesadas:
    html_content += """
                <tr>
                    <td colspan="4" style="text-align: center; color: var(--text-sub);">No hubo cambios ni canciones procesadas en esta ejecución.</td>
                </tr>
    """
  else:
    for item in canciones_procesadas:
      badge_class = f"badge-{item['accion_code']}"
      html_content += f"""
                <tr>
                    <td><span class="badge {badge_class}">{item['accion_label']}</span></td>
                    <td><strong>{item['nombre']}</strong></td>
                    <td style="color: var(--text-sub);">{item['artista']}</td>
                    <td>{item['detalle']}</td>
                </tr>
      """

  html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""

  # 4. Guardar archivo en la subcarpeta 'reportes_html' y abrirlo
  try:
    with open(ruta_html, 'w', encoding='utf-8') as f:
      f.write(html_content)

    webbrowser.open('file://' + os.path.realpath(ruta_html))
  except Exception as e:
    print(f'Error al generar el reporte HTML: {e}')