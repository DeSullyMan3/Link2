# main.py
import sys
from pathlib import Path
from configparser import ConfigParser
from PySide6.QtWidgets import QApplication, QLabel, QListWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# Import the compiled resources
import ui.resources_rc

# Tell user to specify Swinxs path
if len(sys.argv) < 2:
    print("Gebruik: python main.py <pad naar swinxs>")
    print("Geef een pad naar de Swinxs door")
    sys.exit(1)

if len(sys.argv) > 2:
    print("Zet het pad tussen puntjes aub!")
    sys.exit(1)

swinxs_path = sys.argv[1]

# Read PRPs
properties = Path(f"{swinxs_path}SYSTEM.PRP")
propertiesslash = Path(f"{swinxs_path}/SYSTEM.PRP")
#link2 = f"{swinxs_path}LINK2.PRP"

if properties.is_file():
    with open(properties) as f:
        systemprp = "[DEFAULT]\n" + f.read()
    print(f"Loaded {properties}")
elif propertiesslash.is_file():
    with open(propertiesslash) as f:
        systemprp = "[DEFAULT]\n" + f.read()
    print(f"Loaded {propertiesslash}")
else:
    print(f"Geen SYSTEM.PRP gevonden in {swinxs_path}!")

if properties.is_file() or propertiesslash.is_file():
    config = ConfigParser()
    config.read_string(systemprp)

    language = config["DEFAULT"]["LANGUAGE"]
    firmware = config["DEFAULT"]["FIRMWARE"]
    sdcard = config["DEFAULT"]["SDCARD"]
    hardware = config["DEFAULT"]["HARDWARE"]
    serial = config["DEFAULT"]["SERIALNBR"]

# print(language, firmware, sdcard, hardware, serial)

app = QApplication(sys.argv)

# Load the UI file
ui_file = QFile("ui/main.ui")
ui_file.open(QFile.ReadOnly)

loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()

# Change some info stuff
if not(properties.is_file() or propertiesslash.is_file()):
    window.findChild(QLabel, "swinxs").setText(f"Geen Swinxs gevonden")
    window.findChild(QLabel, "lang").setText(f"Taal:")
    window.findChild(QLabel, "firm").setText(f"Firmware:")
    window.findChild(QLabel, "serialnbr").setText(f"Serienummer:")
    window.findChild(QLabel, "swinxs_image").setEnabled(False)
else:
    window.findChild(QLabel, "swinxs").setText(f"Swinxs {hardware}")
    window.findChild(QLabel, "lang").setText(f"Taal: {language}")
    window.findChild(QLabel, "firm").setText(f"Firmware: {firmware}")
    window.findChild(QLabel, "serialnbr").setText(f"Serienummer: {serial}")

window.findChild(QListWidget, "game_list").addItem("ardeaple")
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
    window.findChild(QLabel, "title").setText(f"plankje kaak")
    print("You clicked:", item.text())

window.findChild(QListWidget, "game_list").itemClicked.connect(on_item_clicked)

window.show()
sys.exit(app.exec())
