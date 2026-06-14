<div align="center">
  <img src="FarmCromosLinux.png" alt="FarmCromos Linux Logo" width="400">
</div>

<h1 align="center">FarmCromos Linux</h1>
<p align="center"><b>v1.0.0</b> — Idle automático de cromos de Steam para Linux</p>

<p align="center">
  🌎 <a href="#english">English</a> &nbsp;|&nbsp; 🇦🇷 <a href="#español">Español</a>
</p>

---

<a name="english"></a>
# 🌎 English

**FarmCromos Linux** is an automatic Steam trading card idler for Linux. It connects to your Steam account, detects which of your games still have card drops available, and simulates them running in the background — without having to install or open a single game. A clean dark-mode GUI shows you everything in real time.

## 📋 How it works

1. You provide your Steam session cookies in `settings.conf`.
2. The script (`start.py`) logs into your Steam profile and scans your badge pages to find games with remaining card drops.
3. For each game found, it launches `steam-idle.py` in the background. This script uses the official Steam API (`libsteam_api.so`) to tell the Steam client that the game is "running", triggering the drop timer.
4. A single unified GUI window (dark mode) shows all your games, their remaining drop count, covers loaded from Steam, and their current status: **Queued → Farming… → Completed**.
5. When all cards have dropped, the program stops automatically. You can also stop it at any time with the red button.

> **Note:** `steam-idle.py` is **required** — it is the component that actually communicates with the Steam API. It runs invisibly ("headless") without creating extra windows on your desktop.

> [!IMPORTANT]
> **Security Notice:** This application **DOES NOT collect, read, or store** any personal information, passwords, or Steam data beyond what you manually enter in `settings.conf`. Your account is completely safe. The cookies you provide are used exclusively to read your badge page and check remaining card drops.

> [!TIP]
> **🌟 Support the Project:** This software is **100% free**! If it has been useful to you and you feel like supporting my work, any small gesture is more than welcome — some Steam Points on my profile, a "+rep" comment, or even a game if you're feeling generous. Truly appreciated, but never required!
> 👉 **[Visit TRN1's Steam profile](https://steamcommunity.com/id/TRNONE/)**

---

## 🖥️ System Requirements

| Requirement | Notes |
|---|---|
| **OS** | Linux (tested on Arch Linux) |
| **Steam** | Must be installed and running on your system |
| **Python 3** | `python3` must be available |
| **Tkinter** | For the GUI window |

### Python packages

```bash
# Arch Linux
sudo pacman -S python-beautifulsoup4 python-requests python-pillow tk

# Ubuntu / Debian
sudo apt install python3-bs4 python3-requests python3-pil python3-tk

# Generic (pip)
pip install -r requirements.txt
```

---

## ⚙️ Setup (First time)

### Step 1 — Get your Steam cookies

1. Open your browser and log in to **https://steamcommunity.com/**
2. Open the browser's developer tools and go to the **Storage / Cookies** section.
   - Firefox: press `Shift + F9` → select `steamcommunity.com`
   - Chrome: press `F12` → Application → Cookies → `steamcommunity.com`
3. Find and copy the values for these two cookies:
   - `sessionid`
   - `steamLoginSecure`

> [!IMPORTANT]
> Make sure you are using cookies from **steamcommunity.com** and **NOT** from store.steampowered.com — they are different and only the community ones will work.

### Step 2 — Configure `settings.conf`

Run the script once to auto-generate the file:
```bash
python start.py
```

Then open `settings.conf` and fill in your values:

```ini
sessionID = "paste_your_sessionid_here"
steamLoginSecure = "paste_your_steamLoginSecure_here"
steamParental = ""       # Only needed if you use Steam parental controls
sort = ""                # Options: "" | "mostcards" | "leastcards"
hasPlaytime = "false"    # Set to "true" to only idle games you've played before
```

### Step 3 — Run

```bash
python start.py
```

The GUI window will open. FarmCromos Linux will automatically detect all your games with remaining card drops and start farming them one by one.

---

## 🎮 Controls

| Control | Action |
|---|---|
| `Ctrl+C` in terminal | Stop farming safely |
| **Stop Farming** button (red) | Stops and closes the program |
| **Support TRN1** button (blue) | Opens TRN1's Steam profile |

### Optional: Blacklisting games

Create a `blacklist.txt` file in the same folder and add one AppID per line:
```
730
440
570
```
Any game in this list will be skipped. You can also blacklist games from the GUI while idling.

---

## 📁 Files included

| File | Description |
|---|---|
| `start.py` | Main script — GUI, login, badge scanning, idle manager |
| `steam-idle.py` | Background worker — communicates with the Steam API |
| `libsteam_api32.so` | Steam API library (32-bit) |
| `libsteam_api64.so` | Steam API library (64-bit) |
| `requirements.txt` | Python dependencies |
| `LICENSE` | MIT License |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details. Created by **TRN1 diego ledesma**.

---

<a name="español"></a>
# 🇦🇷 Español

**FarmCromos Linux** es un idler automático de cromos de Steam para Linux. Se conecta a tu cuenta de Steam, detecta cuáles de tus juegos todavía tienen cromos disponibles y simula que están corriendo en segundo plano — sin necesidad de instalar ni abrir ningún juego. Una interfaz gráfica en modo oscuro te muestra todo en tiempo real.

## 📋 ¿Cómo funciona?

1. Vos proporcionás tus cookies de sesión de Steam en el archivo `settings.conf`.
2. El script (`start.py`) inicia sesión en tu perfil de Steam y escanea tus páginas de insignias en busca de juegos con cromos disponibles.
3. Por cada juego encontrado, lanza `steam-idle.py` en segundo plano. Este script usa la API oficial de Steam (`libsteam_api.so`) para decirle al cliente de Steam que el juego está "en ejecución", activando el contador de drops.
4. Una sola ventana de interfaz gráfica (modo oscuro) muestra todos tus juegos, los cromos restantes, las carátulas cargadas desde Steam y el estado actual: **En cola → Farmeando... → Completado**.
5. Cuando todos los cromos se obtengan, el programa se detiene automáticamente. También podés detenerlo en cualquier momento con el botón rojo.

> **Nota:** `steam-idle.py` es **obligatorio** — es el componente que realmente se comunica con la API de Steam. Corre de forma invisible ("headless") sin crear ventanas extra en tu escritorio.

> [!IMPORTANT]
> **Aclaración de Seguridad:** Esta aplicación **NO recopila, lee ni almacena** ninguna información personal, contraseñas ni datos de Steam más allá de lo que vos ingresás manualmente en `settings.conf`. Tu cuenta está completamente segura. Las cookies que proporcionás se usan exclusivamente para leer tu página de insignias y verificar los cromos restantes.

> [!TIP]
> **🌟 Apoyo al Proyecto:** ¡Este software es **100% gratuito**! Si te fue útil y te nace apoyar mi trabajo, cualquier pequeño gesto es más que bienvenido — ya sean puntos de Steam en mi perfil, un comentario de "+rep", o hasta un juego si te sentís generoso. ¡Se agradece de corazón, pero para nada es obligatorio!
> 👉 **[Visitar perfil de TRN1 en Steam](https://steamcommunity.com/id/TRNONE/)**

---

## 🖥️ Requisitos del sistema

| Requisito | Detalles |
|---|---|
| **SO** | Linux (probado en Arch Linux) |
| **Steam** | Debe estar instalado y corriendo en tu sistema |
| **Python 3** | `python3` debe estar disponible |
| **Tkinter** | Para la ventana de la interfaz gráfica |

### Paquetes de Python

```bash
# Arch Linux
sudo pacman -S python-beautifulsoup4 python-requests python-pillow tk

# Ubuntu / Debian
sudo apt install python3-bs4 python3-requests python3-pil python3-tk

# Genérico (pip)
pip install -r requirements.txt
```

---

## ⚙️ Configuración (Primera vez)

### Paso 1 — Obtener tus cookies de Steam

1. Abrí tu navegador e iniciá sesión en **https://steamcommunity.com/**
2. Abrí las herramientas de desarrollador y andá a la sección de **Almacenamiento / Cookies**.
   - Firefox: presioná `Shift + F9` → seleccioná `steamcommunity.com`
   - Chrome: presioná `F12` → Aplicación → Cookies → `steamcommunity.com`
3. Buscá y copiá los valores de estas dos cookies:
   - `sessionid`
   - `steamLoginSecure`

> [!IMPORTANT]
> Asegurate de usar cookies de **steamcommunity.com** y **NO** de store.steampowered.com — son diferentes y solo las de la comunidad funcionarán.

### Paso 2 — Configurar `settings.conf`

Ejecutá el script una vez para que se genere el archivo automáticamente:
```bash
python start.py
```

Después abrí `settings.conf` y completá tus valores:

```ini
sessionID = "pegá_tu_sessionid_acá"
steamLoginSecure = "pegá_tu_steamLoginSecure_acá"
steamParental = ""       # Solo si usás controles parentales de Steam
sort = ""                # Opciones: "" | "mostcards" | "leastcards"
hasPlaytime = "false"    # "true" para farmear solo juegos que ya abriste antes
```

### Paso 3 — Ejecutar

```bash
python start.py
```

Se abrirá la ventana de la interfaz. FarmCromos Linux detectará automáticamente todos tus juegos con cromos disponibles y empezará a farmearlos uno por uno.

---

## 🎮 Controles

| Control | Acción |
|---|---|
| `Ctrl+C` en terminal | Detiene el farmeo de forma segura |
| Botón **Parar Farmeo** (rojo) | Detiene y cierra el programa |
| Botón **Apoyar a TRN1** (azul) | Abre el perfil de Steam de TRN1 |

### Opcional: Agregar juegos a la lista negra

Creá un archivo `blacklist.txt` en la misma carpeta y agregá un AppID por línea:
```
730
440
570
```
Cualquier juego en esta lista será omitido. También podés agregar juegos a la lista negra desde el menú mientras se farmean.

---

## 📁 Archivos incluidos

| Archivo | Descripción |
|---|---|
| `start.py` | Script principal — GUI, login, escaneo de insignias, gestor de idle |
| `steam-idle.py` | Worker en segundo plano — se comunica con la API de Steam |
| `libsteam_api32.so` | Librería de la API de Steam (32-bit) |
| `libsteam_api64.so` | Librería de la API de Steam (64-bit) |
| `requirements.txt` | Dependencias de Python |
| `LICENSE` | Licencia MIT |

---

## 📄 Licencia

Licencia MIT — ver [LICENSE](LICENSE) para más detalles. Creado por **TRN1 diego ledesma**.