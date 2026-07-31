import logging
import os
import sys 
import time
import pylast
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Módulo generador de reportes HTML
from reporter import generar_y_abrir_reporte

# ==========================================
# RUTAS DINÁMICAS Y CONFIGURACIÓN DE LOGS
# ==========================================
if getattr(sys, 'frozen', False):
  # Si está compilado en ejecutable (.exe)
  BASE_DIR = os.path.dirname(sys.executable)
else:
  # Si se ejecuta como script (.py)
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Crear carpeta 'logs' dentro del directorio del script/exe
CARPETA_LOGS = os.path.join(BASE_DIR, 'logs')
os.makedirs(CARPETA_LOGS, exist_ok=True)

# 2. Definir ruta absoluta para appcolombia.log
RUTA_LOG = os.path.join(CARPETA_LOGS, 'appcolombia.log')

# Configuración de logging
logging.basicConfig(
    filename=RUTA_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logging.info('Iniciando script de gestión de playlists (Global)...')

# ==========================================
# CONFIGURACIÓN DE APIs
# ==========================================

# Determinar el directorio base para ubicar el .env (soporta .py y .exe)
if getattr(sys, 'frozen', False):
  BASE_DIR = os.path.dirname(sys.executable)
else:
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar las variables del archivo .env
ruta_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=ruta_env)

# Cargar credenciales desde variables de entorno
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = os.getenv('SPOTIPY_SCOPE')

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
LASTFM_API_SECRET = os.getenv('LASTFM_API_SECRET')
LASTFM_USERNAME = os.getenv('LASTFM_USERNAME')
LASTFM_PASSWORD = os.getenv('LASTFM_PASSWORD_HASH')

# Inicialización de clientes
lastfm_network = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET,
    username=LASTFM_USERNAME,
    password_hash=LASTFM_PASSWORD,
)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
    )
)

# Géneros a excluir
generos_excluidos = {
    'reggaeton',
    'reggaeton colombiano',
    'trap latino',
    'música popular colombiana',
    'urbano latino',
    'pop reggaeton',
}


def get_playlist_tracks(playlist_id):
  """Obtiene todas las canciones de una playlist de Spotify gestionando la paginación."""
  try:
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
      results = sp.next(results)
      tracks.extend(results['items'])
    return tracks
  except spotipy.exceptions.SpotifyException as e:
    logging.error(
        f'Error al obtener las canciones de la playlist {playlist_id}: {e}'
    )
    return []


def get_lastfm_scrobbles(artist_name, track_name):
  """Obtiene cuántas veces has escuchado una canción en Last.fm con manejo de excepciones."""
  try:
    track = lastfm_network.get_track(artist_name, track_name)
    return track.get_userplaycount()
  except (pylast.WSError, Exception) as e:
    logging.error(
        f'Error al obtener scrobbles de Last.fm para {artist_name} -'
        f' {track_name}: {e}'
    )
    return 0


def add_tracks_to_playlists(tracks, playlist_ids):
  """Agrega canciones a múltiples playlists dividiendo en lotes de máximo 100 elementos."""
  track_ids = [track['id'] for track in tracks if track and track.get('id')]
  if not track_ids:
    return

  for playlist_id in playlist_ids:
    for i in range(0, len(track_ids), 100):
      chunk = track_ids[i : i + 100]
      try:
        sp.playlist_add_items(playlist_id, chunk)
      except spotipy.exceptions.SpotifyException as e:
        logging.error(
            f"Error agregando lote de canciones a la playlist '{playlist_id}':"
            f' {e}'
        )

    logging.info(
        f"Se agregaron {len(track_ids)} canciones a la playlist"
        f" '{playlist_id}'."
    )


def es_genero_excluido(artista_id):
  """Determina de forma segura si un artista pertenece a alguno de los géneros excluidos."""
  if not artista_id:
    return False, None

  try:
    artista = sp.artist(artista_id)
    generos_artista = set(artista.get('genres', []))

    for genero in generos_excluidos:
      for genero_artista in generos_artista:
        if genero in genero_artista:  # Coincidencia parcial
          logging.info(
              f"El artista {artista.get('name')} fue excluido por el género"
              f" '{genero_artista}'."
          )
          return True, genero_artista
    return False, None
  except spotipy.exceptions.SpotifyException as e:
    logging.error(f'Error al consultar el artista {artista_id}: {e}')
    return False, None


def esta_en_me_gusta(track_id):
  """Comprueba si una canción ya se encuentra guardada en la biblioteca de Spotify."""
  try:
    res = sp.current_user_saved_tracks_contains([track_id])
    return res[0] if res else False
  except Exception as e:
    logging.error(f'Error verificando "Me gusta" para {track_id}: {e}')
    return False


def clear_playlist(playlist_id):
  """Elimina todas las canciones de una playlist de manera segura."""
  try:
    tracks = get_playlist_tracks(playlist_id)
    track_ids = [
        track['track']['id']
        for track in tracks
        if track.get('track') and track['track'].get('id')
    ]

    if track_ids:
      for i in range(0, len(track_ids), 100):
        chunk = track_ids[i : i + 100]
        sp.playlist_remove_all_occurrences_of_items(playlist_id, chunk)
      logging.info(
          f"Todas las canciones se eliminaron de la playlist '{playlist_id}'."
      )
    else:
      logging.info(f"La playlist '{playlist_id}' ya está vacía.")
  except spotipy.exceptions.SpotifyException as e:
    logging.error(f'Error al limpiar la playlist {playlist_id}: {e}')


def main():
  # IDs de playlists específicas para Colombia
  global_top_50_id = '70IzpVOVUFemP6iIYyPxIx'
  filtro_playlist_id = '00mmJ0nCbTAFXCc3XCJ1Wm'
  new_playlist_id = '4NnFBsCAx4FR4FA2sXpWeg'

  # Estructuras para recolectar métricas del reporte visual HTML
  estadisticas = {
      'agregadas': 0,
      'guardadas': 0,
      'ya_en_megusta': 0,
      'excluidas': 0,
  }
  canciones_reporte = []

  logging.info(
      'Iniciando el proceso de actualización de playlists (Colombia)...'
  )

  # 1. Obtener canciones de origen y filtro
  top_50_global_tracks = get_playlist_tracks(global_top_50_id)
  filtro_tracks = get_playlist_tracks(filtro_playlist_id)

  filtro_track_ids = {
      track['track']['id']
      for track in filtro_tracks
      if track.get('track') and track['track'].get('id')
  }

  # 2. Filtrar canciones nuevas evitando géneros excluidos
  nuevas_canciones = []
  for track in top_50_global_tracks:
    if not track.get('track') or not track['track'].get('id'):
      continue

    track_obj = track['track']
    track_id = track_obj['id']
    artists = track_obj.get('artists', [])
    artist_id = artists[0]['id'] if artists else None

    if track_id not in filtro_track_ids:
      excluido, genero_coincidente = es_genero_excluido(artist_id)
      if excluido:
        estadisticas['excluidas'] += 1
        canciones_reporte.append({
            'accion_code': 'excluida',
            'accion_label': 'Excluida',
            'nombre': track_obj['name'],
            'artista': artists[0]['name'] if artists else 'Desconocido',
            'detalle': f'Género no deseado ({genero_coincidente})',
        })
      else:
        nuevas_canciones.append(track_obj)
        estadisticas['agregadas'] += 1
        canciones_reporte.append({
            'accion_code': 'agregada',
            'accion_label': 'Agregada',
            'nombre': track_obj['name'],
            'artista': artists[0]['name'] if artists else 'Desconocido',
            'detalle': 'Agregada a "Top 50 Colombia New"',
        })

  if nuevas_canciones:
    add_tracks_to_playlists(
        nuevas_canciones, [new_playlist_id, filtro_playlist_id]
    )

  # 3. Procesar reproducciones desde Last.fm en la playlist "Colombia New"
  bandeja_tracks = get_playlist_tracks(new_playlist_id)

  for track in bandeja_tracks:
    if not track.get('track') or not track['track'].get('id'):
      continue

    track_id = track['track']['id']
    artist_name = track['track']['artists'][0]['name']
    track_name = track['track']['name']

    play_count = get_lastfm_scrobbles(artist_name, track_name)

    # Si se escuchó 8 o más veces:
    if play_count >= 8:
      if esta_en_me_gusta(track_id):
        estadisticas['ya_en_megusta'] += 1
        canciones_reporte.append({
            'accion_code': 'ya-existia',
            'accion_label': 'Ya en Me Gusta',
            'nombre': track_name,
            'artista': artist_name,
            'detalle': (
                f'{play_count} escuchas. Eliminada de la playlist (ya la'
                ' tenías guardada).'
            ),
        })
      else:
        try:
          sp.current_user_saved_tracks_add([track_id])
          estadisticas['guardadas'] += 1
          canciones_reporte.append({
              'accion_code': 'guardada',
              'accion_label': 'Guardada',
              'nombre': track_name,
              'artista': artist_name,
              'detalle': (
                  f'{play_count} escuchas. Guardada en "Me Gusta" y'
                  ' eliminada.'
              ),
          })
        except Exception as e:
          logging.error(f'Error al guardar la canción {track_id}: {e}')

      # Remover de la playlist
      try:
        sp.playlist_remove_all_occurrences_of_items(new_playlist_id, [track_id])
      except spotipy.exceptions.SpotifyException as e:
        logging.error(f'Error al eliminar {track_id} de la playlist: {e}')

  # 4. Limpiar playlist origen
  clear_playlist(global_top_50_id)

  # 5. Generar y abrir el reporte HTML en el navegador para Colombia
  generar_y_abrir_reporte('Top 50 Colombia', estadisticas, canciones_reporte)

  logging.info('El programa (Colombia) ha finalizado correctamente.')
  logging.info('----------------------------------------------------------------------------------------------------------')

if __name__ == '__main__':
  main()