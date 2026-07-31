Aquí tienes una plantilla completa y profesional para tu archivo **`README.md`**, redactada pensando exactamente en esa documentación clara que tu "yo del futuro" (o cualquier otro desarrollador) te agradecerá.

Puedes copiar este contenido directamente en un archivo llamado `README.md` en la raíz de tu proyecto en GitHub.

---

```markdown
# 🎵 Playlist Orchestrator & Automatic Curator

**Playlist Orchestrator** es un sistema automatizado en Python para gestionar, filtrar y curar listas de reproducción de Spotify mediante métricas de escucha reales obtenidas de **Last.fm**. 

El sistema toma canciones de listas de descubrimiento/tendencias, realiza un seguimiento de cuántas veces las has escuchado y, si superan un umbral de escuchas (por ejemplo, 8 scrobbles), las guarda automáticamente en tu biblioteca de **"Me gusta"** de Spotify, manteniéndote la lista limpia y actualizada. Además, genera reportes visuales en HTML con los resultados de cada ejecución.

---

## 📋 Tabla de Contenidos
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Obtención de Credenciales (APIs)](#-obtención-de-credenciales-apis)
  - [1. Spotify for Developers](#1-spotify-for-developers)
  - [2. Last.fm API](#2-lastfm-api)
- [Configuración del Entorno (`.env`)](#-configuración-del-entorno-env)
- [Configuración de las Listas de Reproducción](#-configuración-de-las-listas-de-reproducción)
- [Ejecución e Instalación de Dependencias](#-ejecución-e-instalación-de-dependencias)
- [Compilación a Ejecutables (`.exe`)](#-compilación-a-ejecutables-exe)
- [Organización de la Carpeta de Producción](#-organización-de-la-carpeta-de-producción)
- [Automatización con el Programador de Tareas de Windows](#-automatización-con-el-programador-de-tareas-de-windows)

---

## 📁 Estructura del Proyecto

```text
Playlist Orchestrator/
├── scripts/
│   ├── spotify_global.py         # Script para gestionar Top 50 Global
│   ├── spotify_colombia.py       # Script para gestionar Top 50 Colombia
│   ├── spotify_brasil.py          # Script para gestionar Top 50 Brasil
│   ├── playlist_orchestrator.py # Script orquestador/gestor principal
│   ├── reporter.py               # Módulo generador de reportes visuales HTML
│   ├── .env                      # Variables de entorno y credenciales (local)
│   └── requirements.txt          # Lista de dependencias de Python
└── README.md

```

---

## 🔑 Obtención de Credenciales (APIs)

Para usar este programa necesitas registrar aplicaciones gratuitas en Spotify y Last.fm para obtener las claves de acceso.

### 1. Spotify for Developers

1. Ve al portal de desarrolladores de Spotify: [developer.spotify.com](https://developer.spotify.com/).
2. Inicia sesión con tu cuenta de Spotify y entra a tu **Dashboard**.
3. Haz clic en **Create app**.
4. Completa el formulario:
* **App name**: `Playlist Orchestrator` (o el nombre que prefieras).
* **App description**: Herramienta de automatización de listas.
* **Redirect URIs**: Añade estrictamente `http://127.0.0.1:8080/callback` (o `http://localhost:8888/callback`).
* En **Which API/SDKs are you planning to use?**, selecciona **Web API**.


5. Guarda los cambios.
6. Dentro de la configuración de tu nueva app, ve a la pestaña **Settings** y copia:
* **Client ID**
* **Client Secret**



### 2. Last.fm API

1. Ingresa a la página de desarrollo de Last.fm: [last.fm/api/account/create](https://www.last.fm/api/account/create).
2. Inicia sesión con tu cuenta de Last.fm.
3. Completa los datos requeridos (Nombre de la App, Descripción, etc.).
4. Al finalizar, la página te entregará:
* **API Key**
* **Shared Secret**


5. Ten a la mano también tu **Nombre de usuario** y **Contraseña** de Last.fm.

---

## ⚙️ Configuración del Entorno (`.env`)

El sistema utiliza un archivo `.env` para almacenar tus claves de forma segura y separada del código. 

### 💡 Generación Automática (Recomendado)
No necesitas crear este archivo manualmente. La primera vez que ejecutes **`playlist_orchestrator.exe`** (o `.py`):
1. El programa detectará que no existe el archivo `.env`.
2. Creará una plantilla automáticamente.
3. **Abrirá una interfaz gráfica (GUI)** pidiéndote los datos. Solo debes pegar tus claves en los campos correspondientes y hacer clic en **Guardar**.

---

### 📝 Creación Manual (Opcional)
Si prefieres configurarlo manualmente antes de ejecutar, simplemente crea un archivo llamado `.env` en la misma carpeta del ejecutable con la siguiente estructura (sin comillas ni espacios al lado del `=`):

```env
SPOTIPY_CLIENT_ID=tu_client_id_de_spotify
SPOTIPY_CLIENT_SECRET=tu_client_secret_de_spotify
SPOTIPY_REDIRECT_URI=[http://127.0.0.1:8080/callback](http://127.0.0.1:8080/callback)
SPOTIPY_SCOPE=user-library-read user-library-modify playlist-modify-public playlist-modify-private playlist-read-private

LASTFM_API_KEY=tu_api_key_de_lastfm
LASTFM_API_SECRET=tu_api_secret_de_lastfm
LASTFM_USERNAME=tu_usuario_de_lastfm
LASTFM_PASSWORD=tu_contraseña_de_lastfm

```

---

## 🎧 Configuración de las Listas de Reproducción

Los IDs de las listas de reproducción están definidos en la función `main()` de cada script (`spotify_global.py`, `spotify_colombia.py`, etc.):

```python
# Ejemplo en spotify_global.py
global_top_50_id = '2xhU4k2pIT2uyNKT707qJW'
filtro_playlist_id = '4xjkt2anQITfaLcqknNAdo'
new_playlist_id = '5sVemGIcCKXNJTdotcLDvy'

```

### ¿Cómo obtener el ID de una Playlist?

Abre Spotify, haz clic derecho en la playlist → **Compartir** → **Copiar enlace a la lista de reproducción**.
El enlace se verá así:
`https://open.spotify.com/playlist/5sVemGIcCKXNJTdotcLDvy?si=12345`

El ID es únicamente el texto de caracteres alfanuméricos entre `/playlist/` y el signo `?` (en este caso: `5sVemGIcCKXNJTdotcLDvy`).

---

## 🐍 Ejecución e Instalación de Dependencias

Para ejecutar los scripts directamente en Python:

1. Abrir terminal en la carpeta `scripts/`.
2. Instalar las librerías necesarias:
```bash
pip install spotipy pylast python-dotenv pyinstaller

```


3. Ejecutar cualquiera de los módulos:
```bash
python spotify_global.py

```



*(Nota: La primera vez que ejecutes el programa, Spotify abrirá una ventana de navegador para pedirte autorización. Una vez aceptado, se creará un archivo caché `.cache` con el token de autenticación).*

---

## 🛠️ Compilación a Ejecutables (`.exe`)

Para empaquetar los scripts y poder ejecutarlos en Windows sin necesidad de tener Python abierto:

1. Abre la terminal en la carpeta `scripts/`.
2. Compila los cuatro archivos usando PyInstaller (se incluye `--copy-metadata pylast` para prevenir errores de la API de Last.fm):

```bash
pyinstaller --onefile --noconsole --copy-metadata pylast spotify_global.py
pyinstaller --onefile --noconsole --copy-metadata pylast spotify_colombia.py
pyinstaller --onefile --noconsole --copy-metadata pylast spotify_brasil.py
pyinstaller --onefile --noconsole --copy-metadata pylast playlist_orchestrator.py

```

3. **Limpieza posterior:**
* Puedes eliminar las carpetas `build/` y `__pycache__/`, así como los archivos `.spec` que se hayan generado.
* Todo lo que necesitas estará guardado dentro de la nueva carpeta **`dist/`**.



---

## 📂 Organización de la Carpeta de Producción

Para que **`playlist_orchestrator.exe`** pueda localizar y ejecutar correctamente los scripts regionales con sus credenciales, la carpeta de producción debe mantener la siguiente estructura modular:

```text
Mi_Proyecto_Compilado/
├── playlist_orchestrator.exe     <-- Ejecutable principal (Orquestador)
├── ultima_ejecucion.txt          <-- Archivo de control (Se crea solo)
└── scripts/
    ├── .env                      <-- CRUCIAL: Debe residir dentro de la carpeta scripts/
    ├── spotify_global.exe        <-- Módulo ejecutable
    ├── spotify_brasil.exe        <-- Módulo ejecutable
    ├── spotify_colombia.exe      <-- Módulo ejecutable
    │
    ├── logs/                     <-- Se crea automáticamente
    │   ├── appglobal.log
    │   ├── appbrasil.log
    │   └── appcolombia.log
    │
    └── reportes_html/            <-- Se crea automáticamente
        ├── reporte_top_50_global.html
        ├── reporte_top_50_brasil.html
        └── reporte_top_50_colombia.html

> **¡Importante!** El archivo `.env` DEBE estar guardado en la misma carpeta donde estén alojados los archivos `spotify_***.exe`.

---

## ⏰ Automatización con el Programador de Tareas de Windows

Para que los scripts se ejecuten solos en segundo plano todos los días:

1. Presiona la tecla `Windows` y busca **Programador de tareas** (*Task Scheduler*).
2. En el panel derecho, haz clic en **Crear tarea...** (*Create Task...*).
3. **Pestaña General:**
* Nombre: `Spotify Playlist Orchestrator`
* Selecciona: **Ejecutar solo cuando el usuario haya iniciado sesión** (o la opción según tu preferencia).


4. **Pestaña Desencadenadores (*Triggers*):**
* Haz clic en **Nuevo...**
* Configura la frecuencia (ejemplo: *Diariamente*, a las 08:00 AM).


5. **Pestaña Acciones (*Actions*):**
* Haz clic en **Nueva...**
* Accion: *Iniciar un programa*.
* **Programa o script:** Examina y selecciona tu ejecutable (ejemplo: `C:\Ruta\A\TuCarpeta\playlist_orchestrator.exe`).
* **Iniciar en (opcional):** Pega la ruta completa de la carpeta donde está el ejecutable (ejemplo: `C:\Ruta\A\TuCarpeta\`). *¡Este paso evita errores de rutas relativas!*


6. Haz clic en **Aceptar** para guardar la tarea.

---

```

```