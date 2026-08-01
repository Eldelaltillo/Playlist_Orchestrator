from datetime import datetime
import os
import subprocess
import sys
import tkinter as tk
from tkinter import simpledialog
import win32api
import win32con

# 1. Rutas base dinámicas
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FECHA_PATH = os.path.join(BASE_DIR, 'ultima_ejecucion.txt')

# Ubicación del .env dentro de la subcarpeta 'scripts'
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')
ENV_PATH = os.path.join(SCRIPTS_DIR, '.env')

PLANTILLA_ENV = """# Configuración de Spotify
SPOTIPY_CLIENT_ID=
SPOTIPY_CLIENT_SECRET=
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIPY_SCOPE=playlist-modify-public playlist-modify-private playlist-read-private user-library-modify

# Configuración de Last.fm
LASTFM_API_KEY=
LASTFM_API_SECRET=
LASTFM_USERNAME=
LASTFM_PASSWORD=
"""


def verificar_y_configurar_env():
    """Verifica si el archivo .env existe dentro de /scripts y está configurado.

    Si no, guía al usuario para crearlo o editarlo.
    """
    # Aseguramos que la carpeta scripts exista
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Si no existe el .env en scripts/, lo creamos
    if not os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, 'w', encoding='utf-8') as f:
                f.write(PLANTILLA_ENV)
        except Exception as e:
            mostrar_alerta_error(f'No se pudo crear el archivo .env en scripts:\n{e}')
            return False

    # Leer para validar si las claves están vacías
    with open(ENV_PATH, 'r', encoding='utf-8') as f:
        contenido = f.read()

    claves_vacias = any(
        line.strip().endswith('=')
        for line in contenido.splitlines()
        if '=' in line and not line.startswith('#')
    )

    if claves_vacias or not contenido.strip():
        pregunta = (
            'Es la primera vez que ejecutas el programa o faltan credenciales'
            ' en scripts/.env.\n\n'
            '• Presiona [Aceptar] si ya tienes tus API Keys para ingresarlas ahora'
            ' mismo.\n'
            '• Presiona [Cancelar] si aún no las tienes (se abrirá el archivo .env'
            ' para que lo edites luego).'
        )
        respuesta = win32api.MessageBox(
            0,
            pregunta,
            'Configuración Inicial Requerida',
            win32con.MB_OKCANCEL | win32con.MB_ICONINFORMATION,
        )

        if respuesta == win32con.IDOK:
            return solicitar_credenciales_gui()
        else:
            os.system(f'notepad.exe "{ENV_PATH}"')
            win32api.MessageBox(
                0,
                'Se ha abierto el archivo scripts/.env en el Bloc de Notas.\n\nCompleta'
                ' las credenciales, guarda los cambios (Ctrl+S) y vuelve a ejecutar'
                ' el programa.',
                'Configuración Pendiente',
                win32con.MB_OK | win32con.MB_ICONEXCLAMATION,
            )
            return False

    return True


def solicitar_credenciales_gui():
    """Abre pequeños cuadros de texto para pedir las claves si el usuario seleccionó Aceptar."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    campos = [
        ('SPOTIPY_CLIENT_ID', 'Spotify Client ID:'),
        ('SPOTIPY_CLIENT_SECRET', 'Spotify Client Secret:'),
        ('LASTFM_API_KEY', 'Last.fm API Key:'),
        ('LASTFM_API_SECRET', 'Last.fm API Secret:'),
        ('LASTFM_USERNAME', 'Last.fm Username:'),
        ('LASTFM_PASSWORD', 'Last.fm Password:'),
    ]

    datos_ingresados = {}

    for clave, prompt in campos:
        valor = simpledialog.askstring(
            'Configuración de API', prompt, parent=root
        )
        if not valor:
            win32api.MessageBox(
                0,
                'Configuración cancelada. El programa se detendrá.',
                'Aviso',
                win32con.MB_OK | win32con.MB_ICONWARNING,
            )
            return False
        datos_ingresados[clave] = valor.strip()

    nuevo_env = f"""# Configuración de Spotify
SPOTIPY_CLIENT_ID={datos_ingresados.get('SPOTIPY_CLIENT_ID', '')}
SPOTIPY_CLIENT_SECRET={datos_ingresados.get('SPOTIPY_CLIENT_SECRET', '')}
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIPY_SCOPE=playlist-modify-public playlist-modify-private playlist-read-private user-library-modify

# Configuración de Last.fm
LASTFM_API_KEY={datos_ingresados.get('LASTFM_API_KEY', '')}
LASTFM_API_SECRET={datos_ingresados.get('LASTFM_API_SECRET', '')}
LASTFM_USERNAME={datos_ingresados.get('LASTFM_USERNAME', '')}
LASTFM_PASSWORD={datos_ingresados.get('LASTFM_PASSWORD', '')}
"""
    with open(ENV_PATH, 'w', encoding='utf-8') as f:
        f.write(nuevo_env)

    win32api.MessageBox(
        0,
        '¡Credenciales guardadas correctamente en scripts/.env!',
        'Éxito',
        win32con.MB_OK | win32con.MB_ICONINFORMATION,
    )
    return True


def ya_se_ejecuto_hoy():
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    if os.path.exists(LOG_FECHA_PATH):
        try:
            with open(LOG_FECHA_PATH, 'r') as f:
                if f.read().strip() == fecha_hoy:
                    return True
        except Exception:
            pass
    return False


def registrar_ejecucion_hoy():
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    try:
        with open(LOG_FECHA_PATH, 'w') as f:
            f.write(fecha_hoy)
    except Exception as e:
        print(f'Error al guardar registro de fecha: {e}')


def mostrar_alerta_inicio():
    mensaje = (
        '¿Deseas iniciar la actualización de las playlists de Spotify?\n\n'
        '• Presiona Aceptar para continuar.\n'
        '• Presiona Cancelar para omitir la ejecución por hoy.'
    )
    respuesta = win32api.MessageBox(
        0,
        mensaje,
        'Gestor de Playlists',
        win32con.MB_OKCANCEL | win32con.MB_ICONQUESTION,
    )
    return respuesta == win32con.IDOK


def mostrar_alerta_error(mensaje):
    win32api.MessageBox(
        0, mensaje, 'Error de Ejecución', win32con.MB_OK | win32con.MB_ICONERROR
    )


def mostrar_alerta_final(hubo_errores=False):
    if hubo_errores:
        mensaje = (
            'La ejecución finalizó, pero uno o más procesos tuvieron errores.\nRevisa'
            ' los archivos de log para más detalles.'
        )
        icono = win32con.MB_ICONWARNING
    else:
        mensaje = 'Todas las playlists han sido actualizadas con éxito.'
        icono = win32con.MB_ICONINFORMATION

    win32api.MessageBox(0, mensaje, 'Gestor de Playlists', win32con.MB_OK | icono)


def ejecutar_programa(ruta_programa):
    nombre_script = os.path.basename(ruta_programa)

    if not os.path.exists(ruta_programa):
        mostrar_alerta_error(
            f'No se encontró el archivo ejecutable:\n{ruta_programa}'
        )
        return False

    try:
        proceso = subprocess.Popen(
            ruta_programa, shell=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        proceso.wait()

        if proceso.returncode != 0:
            mostrar_alerta_error(
                f'El ejecutable "{nombre_script}" finalizó con un código de error:'
                f' {proceso.returncode}.'
            )
            return False

        return True

    except Exception as e:
        mostrar_alerta_error(
            f'Ocurrió un fallo inesperado al intentar lanzar "{nombre_script}":\n{e}'
        )
        return False


def main():
    # 1. Validar/Configurar credenciales .env dentro de la carpeta /scripts
    if not verificar_y_configurar_env():
        sys.exit(0)

    # 2. Control de ejecución diaria
    if ya_se_ejecuto_hoy():
        sys.exit(0)

    if not mostrar_alerta_inicio():
        sys.exit(0)

    programas = [
        os.path.join(SCRIPTS_DIR, 'spotify_global.exe'),
        os.path.join(SCRIPTS_DIR, 'spotify_brasil.exe'),
        os.path.join(SCRIPTS_DIR, 'spotify_colombia.exe'),
    ]

    hubo_errores = False

    for programa in programas:
        exito = ejecutar_programa(programa)
        if not exito:
            hubo_errores = True

    registrar_ejecucion_hoy()
    mostrar_alerta_final(hubo_errores)


if __name__ == '__main__':
    main()