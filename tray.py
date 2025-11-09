from pystray import Icon, MenuItem, Menu
from PIL import Image

icon = Icon("MyApp", Image.open("ui/swinxs-green.png"), "SwinxsLink 2")
icon.menu = Menu(MenuItem('Quit', lambda icon, item: icon.stop()))
icon.run()
