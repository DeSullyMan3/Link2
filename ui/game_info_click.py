def on_item_clicked(item: QListWidget):
    folder_name = item.data(Qt.UserRole)  # get the actual folder name
    game_prp = Path(swinxs_path) / language.lower() / "games" / folder_name / "game.prp"

    if game_prp.is_file():
        with open(game_prp) as f:
            systemprp = "[DEFAULT]\n" + f.read()
        config = ConfigParser()
        config.read_string(systemprp)

        title = config["DEFAULT"].get("TITLE", folder_name)
        author = config["DEFAULT"].get("AUTHOR", "")
    else:
        title = item.text()
        author = ""

    window.findChild(QLabel, "title").setText(title)
    window.findChild(QLabel, "author").setText(author)
    print("You clicked:", folder_name)

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
