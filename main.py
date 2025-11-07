# main.py
import sys
from pathlib import Path
from configparser import ConfigParser
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# Import the compiled resources
import ui.resources_rc

# Tell user to specify Swinxs path
if len(sys.argv) < 2:
    print("Gebruik: python main.py <pad naar swinxs>")
    print("Geef een pad naar de Swinxs door")
    sys.exit(1)

swinxs_path = sys.argv[1]

# Read PRPs
properties = f"{swinxs_path}SYSTEM.PRP"
#link2 = f"{swinxs_path}LINK2.PRP"

with open(properties) as f:
    systemprp = "[DEFAULT]\n" + f.read()
print(f"Loaded {properties}")

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
window.findChild(QLabel, "swinxs").setText(f"Swinxs {hardware}")
window.findChild(QLabel, "lang").setText(f"Taal: {language}")
window.findChild(QLabel, "firm").setText(f"Firmware: {firmware}")

window.show()
sys.exit(app.exec())
