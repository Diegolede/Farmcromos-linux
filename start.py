#!/usr/bin/env python
# Author: TRN1 diego ledesma
import requests
import http.cookiejar
import bs4
import time
import re
import subprocess
import sys
import os
import json
import logging
import datetime
import ctypes

# Colors
colorGreen = "\033[32m"
colorRed = "\033[31m"
colorCyan = "\033[36m"
colorYellow = "\033[33m"
colorReset = "\033[39m"

# Version
version = "v1.0.0"

# Directory
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Log formatting
class log_text_clean(logging.Formatter):
    def format(self, text):
        logText = super().format(text)
        cleanText = re.sub(r"\033\[\d+m", "", logText)
        return cleanText

logFormat = logging.Formatter("[%(asctime)s] %(message)s", "%d %b %Y %I:%M:%S %p")
logFileFormat = log_text_clean("[%(asctime)s][%(levelname)s][%(lineno)d] %(message)s", "%d %b %Y %I:%M:%S %p")

# File logging
logFile = logging.FileHandler("idlemaster.log", mode="a")
logFile.setFormatter(logFileFormat)
logging.basicConfig( level = logging.DEBUG, handlers = [logFile])

# Console logging
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logFormat)
logger.addHandler(console)

logger.info(colorGreen + "BIENVENIDOS A FARMCROMOS LINUX - " + colorYellow + version + colorReset)
logger.info(colorCyan + "Creado por TRN1 diego ledesma" + colorReset)
logger.info(colorCyan + "Apoya mi perfil de Steam en: https://steamcommunity.com/id/TRNONE/" + colorReset)

# Check for python 3
pyLink = "python"
try:
    subprocess.call(["python3", "--version"], stdout = subprocess.DEVNULL)
except:
    logger.error(colorRed + "Python3 not installed" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

try:
    pyOut = subprocess.check_output(["python", "--version"])
    pyVer = re.search("Python 3", str(pyOut))

    if not pyVer:
        pyLink = "python3"
        logger.warning(colorYellow + "Python pointing to incorrect version, using Python3 instead" + colorReset)
except:
    pyLink = "python3"
    logger.warning(colorYellow + "Python link incorrect, using Python3 instead" + colorReset)

# Settings.conf
authData = {}
try:
    with open("settings.conf", "r") as f:
        logger.info("Settings.conf file found, reading data...")
        for line in f:
            cleanLine = re.sub(r"[\"\n]", "", line)
            if cleanLine and not cleanLine.startswith("#"):
                key, value = cleanLine.split(" = ")
                authData[key] = value
except FileNotFoundError:
    logger.warning(colorYellow + "Settings.conf file is missing, creating file..." + colorReset)
    try:
        with open("settings.conf", "w") as f:
            f.write("# FarmCromos Linux config file\n")
            f.write("# Open web browser and log in to https://steamcommunity.com/ to get cookie data\n\n")
            f.write("# sessionID - found in steam cookie data\n")
            f.write("sessionID = \"\"\n\n")
            f.write("# steamLoginSecure - found in steam cookie data\n")
            f.write("steamLoginSecure = \"\"\n\n")
            f.write("# steamParental - found in steam cookie data\n# !! Not needed unless using parental controls, otherwise leave blank !!\n")
            f.write("steamParental = \"\"\n\n")
            f.write("# (optional) sorting options: (\"\", mostcards, leastcards)\n")
            f.write("sort = \"\"\n\n")
            f.write("# hasPlaytime options: (true, false). If enabled(true) will only idle games previously played and not unplayed games\n")
            f.write("hasPlaytime = \"false\"")
    except:
        logger.error(colorRed + "Unable to generate settings.conf file" + colorReset)
        input("Press Enter to continue...")
        sys.exit()
    else:
        logger.info(colorGreen + "Settings.conf file successfully created" + colorReset)
        input("Press Enter to continue...")
        sys.exit()
except SystemExit:
    sys.exit()
except:
    logger.error(colorRed + "Unable to read settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

# Validate settings.conf data
for key in ["sessionID", "steamLoginSecure", "steamParental", "sort", "hasPlaytime"]:
    if not key in authData:
        logger.error(colorRed + "\"" + key + "\" missing in settings.conf file" + colorReset)
        input("Press Enter to continue...")
        sys.exit()

if authData["sessionID"] == "":
    logger.error(colorRed + "Missing \"sessionID\" value in settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

if authData["steamLoginSecure"] == "":
    logger.error(colorRed + "Missing \"steamLoginSecure\" value in settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

if not authData["sort"] in ["", "mostcards", "leastcards"]:
    logger.error(colorRed + "Invalid option for \"sort\" in settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

if not authData["hasPlaytime"].lower() in ["true", "false"]:
    logger.error(colorRed + "Invalid option for \"hasPlaytime\" in settings.conf file" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

myProfileURL = "https://steamcommunity.com/profiles/" + authData["steamLoginSecure"][:17]

# Generate cookies
def generate_cookies():
    global authData
    try:
        cookies = dict(sessionid = authData["sessionID"], steamLoginSecure = authData["steamLoginSecure"], steamparental = authData["steamParental"], Steam_Language = "english")
    except:
        logger.error(colorRed + "Unable to set cookies" + colorReset)
        input("Press Enter to continue...")
        sys.exit()
    return cookies

# Start idling game
def idle_open(appID, appName):
    try:
        logger.info("Starting game " + appName + " to idle cards")
        global processIdle
        global idleTime

        idleTime = time.time()
        processIdle = subprocess.Popen([pyLink, "steam-idle.py", str(appID)])
    except:
        logger.error(colorRed + "Can not launch " + appName + colorGreen + " [ AppID " + str(appID) + " ]" + colorReset)
        input("Press Enter to continue...")
        sys.exit()

# Stop idling game
def idle_close(appID, appName):
    try:
        logger.info("Closing game " + appName)
        processIdle.terminate()
        totalTime = int(time.time() - idleTime)
        logger.info(appName + " idled for " + colorGreen + str(datetime.timedelta(seconds = totalTime)) + colorReset)
    except:
        logger.error(colorRed + "Could not close game" + colorReset)
        input("Press Enter to continue...")
        sys.exit()

# Network issue idle
def chill_out(appID, appName):
    if processIdle.poll() is None:
        logger.warning(colorYellow + "Suspending operation for " + appName + colorReset)
        idle_close(appID, appName)
    stillDown = True
    while stillDown:
        try:
            logger.info("Sleeping for 5 minutes...")
            time.sleep(300)
            try:
                # Check if cookies still valid or steam is down (network issue)
                steamUp = requests.get("https://store.steampowered.com")
                rCode = steamUp.status_code
                if rCode == 200:
                    expired = cookie_test()
                    if expired:
                        idle_close(appID, appName)
                        logger.warning(colorYellow + "Cookie session expired" + colorReset)
                        input("Press Enter to continue...")
                        sys.exit()
                    else:
                        stillDown = False
                else:
                    logger.warning(colorYellow + "Still unable to connect to Steam" + colorReset)
            except SystemExit:
                sys.exit()
            except:
                logger.warning(colorYellow + "Still unable to find drop info" + colorReset)
        except:
            logger.error(colorRed + "Unknown network issue" + colorReset)
            input("Press Enter to continue...")
            sys.exit()
    logger.info(colorGreen + "Connection established, resuming idling" + colorReset)

# Get app name
def get_app_name(appID):
    try:
        api = requests.get("https://store.steampowered.com/api/appdetails/?appids=" + str(appID) + "&filters=basic")
        apiData = json.loads(api.text)
        return colorCyan + apiData[str(appID)]["data"]["name"] + colorReset
    except:
        logger.warning(colorYellow + "Unable to get app name" + colorReset)
        return colorCyan + "App " + str(appID) + colorReset

# Get blacklist
def get_blacklist():
    try:
        with open("blacklist.txt", "r") as f:
            lines = f.readlines()
        blacklist = [int(n.strip()) for n in lines]
    except:
        blacklist = [];

    if not blacklist:
        logger.info("No games have been blacklisted")

    return blacklist

# Add game to blacklist
def blacklist_game(appID):
    try:
        with open("blacklist.txt", "a") as f:
            f.write(str(appID) + "\n")
    except:
        logger.error(colorRed + "Failed to blacklist game" + colorReset)

# Check if cookies valid
def cookie_test():
    try:
        r = requests.get(myProfileURL + "/badges/", cookies = cookies)
        badgePageData = bs4.BeautifulSoup(r.text, "html.parser")
        userinfo = badgePageData.find("a", {"class": "user_avatar"})
        if userinfo:
            return False
        else:
            return True
    except:
        return True

# Get card drops
logger.info("Finding games that have card drops remaining...")
try:
    cookies = generate_cookies()
    r = requests.get(myProfileURL + "/badges/", cookies = cookies)
except SystemExit:
    sys.exit()
except:
    logger.error(colorRed + "Unable to read badge page" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

try:
    badgesLeft = []
    badgePageData = bs4.BeautifulSoup(r.text, "html.parser")
    badgeSet = badgePageData.find_all("div", {"class": "badge_title_stats"})
except:
    logger.error(colorRed + "Could not find drop info" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

# For profiles with multiple pages
try:
    badgePages = int(badgePageData.find_all("a", {"class": "pagelink"})[-1].text)
    if badgePages:
        logger.info(str(badgePages) + " badge pages found, gathering additional data...")
        currentpage = 2
        while currentpage <= badgePages:
            r = requests.get(myProfileURL + "/badges/?p=" + str(currentpage), cookies = cookies)
            badgePageData = bs4.BeautifulSoup(r.text, "html.parser")
            badgeSet = badgeSet + badgePageData.find_all("div", {"class": "badge_title_stats"})
            currentpage = currentpage + 1
except:
    logger.info("Reading badge page, please wait...")

# User badge page error checking
if not badgePageData.find("a", {"class": "user_avatar"}):
    logger.error(colorRed + "Invalid cookie data, cannot log in to Steam" + colorReset)
    input("Press Enter to continue...")
    sys.exit()

# Gather list of games to idle
blacklist = get_blacklist()
for badge in badgeSet:
    try:
        badgeText = badge.get_text()
        dropCount = badge.find_all("span", {"class": "progress_info_bold"})[0].contents[0]
        Playtime = re.search("hrs on record", badgeText) != None

        if "No card drops" in dropCount or (Playtime == False and authData["hasPlaytime"].lower() == "true"):
            continue
        else:
            # Remaining drops
            dropCountInt, junk = dropCount.split(" ", 1)
            dropCountInt = int(dropCountInt)
            linkGuess = badge.find_parent().find_parent().find_parent().find_all("a")[0]["href"]
            junk, badgeID = linkGuess.split("/gamecards/", 1)
            badgeID = int(badgeID.replace("/", ""))
            if badgeID in blacklist:
                logger.warning(colorCyan + "App " + str(badgeID) + colorYellow + " on blacklist, skipping game..." + colorReset)
                continue
            else:
                push = [badgeID, dropCountInt, 0]
                badgesLeft.append(push)
    except:
        continue

# Sort list of games to idle
if authData["sort"] == "":
    games = badgesLeft
if authData["sort"] == "mostcards":
    games = sorted(badgesLeft, key = lambda value: value[1], reverse = True)
if authData["sort"] == "leastcards":
    games = sorted(badgesLeft, key = lambda value: value[1], reverse = False)

import tkinter as tk
from tkinter import ttk
import threading
import webbrowser
import io
from PIL import Image, ImageTk

# Start idling games
logger.info("FarmCromos Linux necesita farmear " + colorGreen + str(len(badgesLeft)) + colorReset + " juegos")
numSkip = 0

class IdleGUI(tk.Tk):
    def __init__(self, games_list):
        super().__init__()
        self.title("FarmCromos Linux - Creado por TRN1 diego ledesma")
        self.geometry("800x550")
        self.configure(bg="#1e1e1e")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
            
        style.configure("Treeview", 
                        background="#2d2d2d", 
                        foreground="white", 
                        fieldbackground="#2d2d2d", 
                        rowheight=50,
                        bordercolor="#1e1e1e")
        style.configure("Treeview.Heading", 
                        background="#1e1e1e", 
                        foreground="white", 
                        relief="flat")
        style.map("Treeview", background=[('selected', '#4CAF50')])
        
        # Configure layout weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Frame for Treeview
        frame = tk.Frame(self, bg="#1e1e1e")
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        columns = ("appid", "name", "drops", "status")
        self.tree = ttk.Treeview(frame, columns=columns, show="tree headings")
        
        self.tree.heading("#0", text="Carátula")
        self.tree.heading("appid", text="AppID")
        self.tree.heading("name", text="Juego")
        self.tree.heading("drops", text="Cromos Restantes")
        self.tree.heading("status", text="Estado")
        
        self.tree.column("#0", width=120, anchor="center")
        self.tree.column("appid", width=80)
        self.tree.column("name", width=300)
        self.tree.column("drops", width=150)
        self.tree.column("status", width=130)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.images_cache = {}
        self.stop_event = threading.Event()
        
        # Populate
        for appID, drops, value in games_list:
            self.tree.insert("", tk.END, iid=str(appID), text="", values=(appID, "App " + str(appID), drops, "En cola"))
            
        # Support Button
        self.support_btn = tk.Button(self, text="Apoyar a TRN1 diego ledesma", command=self.support_profile, bg="#2196f3", fg="white", font=("Arial", 12, "bold"), relief="flat", activebackground="#1976D2", activeforeground="white")
        self.support_btn.grid(row=1, column=0, sticky="ew", ipady=10, padx=10)
        
        # Stop Button
        self.stop_btn = tk.Button(self, text="Parar Farmeo (Stop Idle)", command=self.on_close, bg="#f44336", fg="white", font=("Arial", 12, "bold"), relief="flat", activebackground="#D32F2F", activeforeground="white")
        self.stop_btn.grid(row=2, column=0, sticky="ew", ipady=10, padx=10, pady=(0, 10))
        
        # Start image loader thread
        self.image_thread = threading.Thread(target=self.load_images_thread, args=(games_list,), daemon=True)
        self.image_thread.start()

    def load_images_thread(self, games_list):
        for appID, _, _ in games_list:
            if self.stop_event.is_set():
                break
            try:
                url = "http://cdn.akamai.steamstatic.com/steam/apps/" + str(appID) + "/header_292x136.jpg"
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    image_bytes = r.content
                    data_stream = io.BytesIO(image_bytes)
                    pil_image = Image.open(data_stream)
                    # Resize while maintaining aspect ratio
                    pil_image = pil_image.resize((100, 46), Image.LANCZOS)
                    # Safely apply image to Tkinter from background thread
                    self.after(0, self._apply_image, str(appID), pil_image)
            except Exception as e:
                pass
            time.sleep(0.1)

    def _apply_image(self, appID_str, pil_image):
        if self.tree.exists(appID_str):
            tk_image = ImageTk.PhotoImage(pil_image)
            self.images_cache[appID_str] = tk_image
            self.tree.item(appID_str, image=tk_image)

    def update_item(self, appID, name=None, drops=None, status=None):
        if self.tree.exists(str(appID)):
            current = self.tree.item(str(appID), "values")
            new_name = name if name is not None else current[1]
            new_drops = drops if drops is not None else current[2]
            new_status = status if status is not None else current[3]
            self.tree.item(str(appID), values=(appID, new_name, new_drops, new_status))

    def support_profile(self):
        webbrowser.open("https://steamcommunity.com/id/TRNONE/")
        
    def on_close(self):
        self.stop_event.set()
        self.destroy()
        logger.info(colorYellow + "Farmeo detenido por el usuario." + colorReset)
        os._exit(0)

def run_idling_thread(games_list, gui):
    global numSkip
    for appID, drops, value in games_list:
        if gui.stop_event.is_set():
            break
            
        appName = get_app_name(appID)
        cleanAppName = re.sub(r"\033\[\d+m", "", appName)
        gui.update_item(appID, name=cleanAppName, status="Farmeando...")
        
        delay = (int(drops) * 600)
        stillHaveDrops = 1
        numCycles = 50
        maxFail = 2
        skip = False
        openApp = True
        
        while stillHaveDrops == 1:
            if gui.stop_event.is_set():
                if not openApp:
                    idle_close(appID, appName)
                return

            try:
                if numCycles < 1:
                    stillHaveDrops = 0

                expired = cookie_test()
                if expired:
                    steamUp = requests.get("https://store.steampowered.com")
                    if steamUp.status_code == 200:
                        if not openApp:
                            idle_close(appID, appName)
                        logger.warning(colorYellow + "Cookie session expired" + colorReset)
                        gui.on_close()
                        return
                else:
                    logger.info("Checking to see if " + appName + " has remaining card drops...")
                    rBadge = requests.get(myProfileURL + "/gamecards/" + str(appID) + "/", cookies=cookies)
                    indBadgeData = bs4.BeautifulSoup(rBadge.text, "html.parser")
                    spans = indBadgeData.find_all("span", {"class": "progress_info_bold"})
                    if spans:
                        badgeLeftString = spans[0].contents[0]
                        if " " in badgeLeftString:
                            dropCountInt, junk = badgeLeftString.split(" ", 1)
                            if dropCountInt.isdigit():
                                dropCountInt = int(dropCountInt)
                                delay = (dropCountInt * 600)
                                logger.info(appName + " has " + colorGreen + str(dropCountInt) + colorReset + " card drops remaining")
                                gui.update_item(appID, drops=dropCountInt)
                            else:
                                logger.info("No card drops remaining")
                                stillHaveDrops = 0
                                break
                        else:
                            stillHaveDrops = 0
                            break
                    else:
                        logger.info("No card drops remaining")
                        stillHaveDrops = 0
                        break

                if openApp:
                    idle_open(appID, appName)
                    openApp = False
                ftime = "{:n}".format(delay / 60)
                logger.info("Sleeping for " + str(ftime) + " minutes...")
                
                for _ in range(delay):
                    if gui.stop_event.is_set():
                        break
                    time.sleep(1)
                    
                numCycles -= 1
            except KeyboardInterrupt:
                if not openApp:
                    idle_close(appID, appName)
                gui.on_close()
                return
            except SystemExit:
                if not openApp:
                    idle_close(appID, appName)
                gui.on_close()
                return
            except Exception as e:
                try:
                    if maxFail >= 0:
                        logger.warning(colorYellow + "Steam unreachable or network down, tries left: " + colorReset + str(maxFail))
                        for _ in range(10):
                            if gui.stop_event.is_set(): return
                            time.sleep(1)
                        maxFail -= 1
                    else:
                        chill_out(appID, appName)
                        maxFail += 1
                        openApp = True
                except:
                    pass

        if gui.stop_event.is_set():
            break

        if not skip:
            if not openApp:
                idle_close(appID, appName)
            logger.info(colorGreen + "Successfully completed idling cards for " + appName + colorReset)
            gui.update_item(appID, status="Completado")

    if not gui.stop_event.is_set():
        logger.info(colorGreen + "Successfully completed idling process" + colorReset)
        logger.warning(colorYellow + str(numSkip) + " games skipped" + colorReset)

if games:
    gui = IdleGUI(games)
    t = threading.Thread(target=run_idling_thread, args=(games, gui), daemon=True)
    t.start()
    try:
        gui.mainloop()
    except KeyboardInterrupt:
        gui.on_close()
else:
    logger.info("No hay juegos para farmear.")
    input("Press Enter to continue...")
