from configparser import ConfigParser

# Read the file with a fake section header
file_path = "SYSTEM.PRP"
with open(file_path) as f:
    file_content = "[DEFAULT]\n" + f.read()  # add a section header

config = ConfigParser()
config.read_string(file_content)

language = config["DEFAULT"]["LANGUAGE"]
firmware = config["DEFAULT"]["FIRMWARE"]
sdcard = config["DEFAULT"]["SDCARD"]
hardware = config["DEFAULT"]["HARDWARE"]
serial = config["DEFAULT"]["SERIALNBR"]

print(language, firmware, sdcard, hardware, serial)
