# main.py
import sys
import psutil
from pystray import Icon, MenuItem, Menu
from PIL import Image
from pathlib import Path
from configparser import ConfigParser
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QListWidget, QListWidgetItem, QStatusBar
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile, QDirIterator
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
import threading

def start_tray():
    Icon.run()

tray_thread = threading.Thread(target=start_tray, daemon=True)
tray_thread.start()


# Import the compiled resources
import ui.resources_rc

icon = Icon("link2", Image.open("ui/swinxs-green.png"), "SwinxsLink 2")
icon.menu = Menu(MenuItem('Quit', lambda icon, item: icon.stop()))

def swinxs_find(filename="SYSTEM.PRP"):
    """
    Automagically searching for a Swinxs
    """
    for partition in psutil.disk_partitions(all=False):
        mount = Path(partition.mountpoint)
        target_file = mount / filename
        if target_file.exists():
            return mount
    return None

if __name__ == "__main__":
    result = swinxs_find()
    if result:
        swinxs_path = result
        print(f"Swinxs gevonden in: {result}")
        auto_swinxs=True
    else:
        print("Swinxs niet gevonden.")
        auto_swinxs=False

if len(sys.argv) > 2:
    print("Zet het pad tussen puntjes aub!")
    sys.exit(1)
if len(sys.argv) > 1:
    swinxs_path = sys.argv[1]
elif not(auto_swinxs):
    swinxs_path = "/"

# Read PRPs
properties = Path(swinxs_path) / "SYSTEM.PRP"

# maybe a special link2.prp for the future
link2_check = Path(swinxs_path) / "LINK2.PRP"
if link2_check.exists():
    link2 = f"{swinxs_path}LINK2.PRP"
    link2_exist = True
else:
    link2_exist = False

if properties.is_file():
    with open(properties) as f:
        systemprp = "[DEFAULT]\n" + f.read()
    print(f"{properties} Geladen")
else:
    print(f"Geen SYSTEM.PRP gevonden in {swinxs_path}!")

if properties.is_file():
    config = ConfigParser()
    config.read_string(systemprp)

    language = config["DEFAULT"]["LANGUAGE"]
    firmware = config["DEFAULT"]["FIRMWARE"]
    sdcard = config["DEFAULT"]["SDCARD"]
    hardware = config["DEFAULT"]["HARDWARE"]
    serial = config["DEFAULT"]["SERIALNBR"]
    game_dir = Path(swinxs_path) / language.lower() / "games"
    games = [f.name for f in game_dir.iterdir() if f.is_dir()]

# print(language, firmware, sdcard, hardware, serial)

app = QApplication(sys.argv)

# Load the UI file
ui_file = QFile("ui/main.ui")
ui_file.open(QFile.ReadOnly)

loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()
app.aboutToQuit.connect(lambda: icon.stop())

# Get status bar
status = window.findChild(QStatusBar, "statusbar")

# Create a QLabel specifically for the status bar
status_icon = QLabel()


# Add it to the status bar
status.addPermanentWidget(status_icon)  # right side

# Change some info stuff
if not(properties.is_file()):
    status.showMessage("Geen Swinxs gevonden")
    window.findChild(QLabel, "swinxs").setText(f"Geen Swinxs gevonden")
    window.findChild(QLabel, "lang").setText(f"Taal:")
    window.findChild(QLabel, "firm").setText(f"Firmware:")
    window.findChild(QLabel, "serialnbr").setText(f"Serienummer:")
    window.findChild(QLabel, "swinxs_image").setEnabled(False)
    window.findChild(QWidget, "games").setEnabled(False)
    status_icon_pixmap = QPixmap(":/swinxs/swinxs-gray.svg").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    status_icon.setPixmap(status_icon_pixmap)
    window.findChild(QLabel, "title").setText("Geen Swinxs gevonden")
else:
    status.showMessage("Swinxs Klaar")
    window.findChild(QLabel, "swinxs").setText(f"Swinxs {hardware}")
    window.findChild(QLabel, "lang").setText(f"Taal: {language}")
    window.findChild(QLabel, "firm").setText(f"Firmware: {firmware}")
    window.findChild(QLabel, "serialnbr").setText(f"Serienummer: {serial}")
    status_icon_pixmap = QPixmap(":/swinxs/swinxs-green.svg").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    status_icon.setPixmap(status_icon_pixmap)
    window.findChild(QLabel, "title").setText("Selecteer een spel")

window.findChild(QLabel, "author").setText("")

window.findChild(QListWidget, "game_list").setStyleSheet("""
    QListWidget {
        padding: 6px;           /* space inside the label */
        margin: 2px;            /* space outside (relative to layout) */
        background-color: #333; /* optional, to see the padding visually */
        color: white;
        border-radius: 6px;
    }
""")

def on_item_clicked(item: QListWidget):
    folder_name = item.data(Qt.UserRole)
    game_prp = Path(swinxs_path) / language.lower() / "games" / folder_name / "game.prp"

    if game_prp.is_file():
        with open(game_prp) as f:
            systemprp = "[DEFAULT]\n" + f.read()
        config = ConfigParser()
        config.read_string(systemprp)

        title = config["DEFAULT"].get("TITLE", folder_name)
        author = config["DEFAULT"].get("AUTHOR", "")

        pixmap_path = ":/swinxs/games/00000.png"

        it = QDirIterator(":/swinxs/games", QDirIterator.Subdirectories)
        while it.hasNext():
            path = it.next()
            if path.endswith(f"{folder_name}.png"):
                pixmap_path = f":/swinxs/games/{folder_name}.png"
                break

        window.findChild(QLabel, "game_ico").setPixmap(QPixmap(pixmap_path))

    else:
        title = item.text()
        author = ""
        window.findChild(QLabel, "game_ico").setPixmap(QPixmap(":/swinxs/games/00000.png"))

    window.findChild(QLabel, "title").setText(title)
    window.findChild(QLabel, "author").setText(author)
    # print("You clicked:", folder_name)

if properties.is_file():
    for g in games:
        game_prp = Path(swinxs_path) / language.lower() / "games" / g / "game.prp"
        if game_prp.is_file():
            with open(game_prp) as f:
                systemprp = "[DEFAULT]\n" + f.read()
            config = ConfigParser()
            config.read_string(systemprp)
            title = config["DEFAULT"].get("TITLE", g)
        else:
            title = g

        item = QListWidgetItem(title)  # display title in list
        item.setData(Qt.UserRole, g)   # store folder name for later
        if not(g == "00001"):
            window.findChild(QListWidget, "game_list").addItem(item)

window.findChild(QListWidget, "game_list").itemClicked.connect(on_item_clicked)

window.show()

# Start tray icon in background thread
tray_thread = threading.Thread(target=lambda: icon.run(), daemon=True)
tray_thread.start()

# Ensure tray icon stops when Qt closes
app.aboutToQuit.connect(lambda: icon.stop())

# Start Qt event loop
sys.exit(app.exec())
