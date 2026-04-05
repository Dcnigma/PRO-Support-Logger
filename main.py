import sys, json, webbrowser
from datetime import datetime
from collections import Counter
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit,
    QTextEdit, QPushButton, QLabel, QListWidget, QTabWidget, QFileDialog,
    QMessageBox, QDialog, QScrollArea, QCompleter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QTextCursor
from utils.config_editor import ConfigEditor
from utils.theme_manager import get_theme_stylesheet, load_settings, SETTINGS_PATH
# ------------------------
# Substring Completer
# ------------------------
class SubstringCompleter(QCompleter):
    def __init__(self, items):
        super().__init__(items)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)

# ------------------------
# Log Window
# ------------------------
class LogWindow(QDialog):
    def __init__(self, log_text, t):
        super().__init__()
        self.t = t

        self.setWindowTitle(self.t("generated_log"))
        self.resize(600,600)

        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.raise_()
        self.activateWindow()

        layout = QVBoxLayout()
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setText(log_text)
        self.log_view.moveCursor(QTextCursor.Start)
        layout.addWidget(self.log_view)
        self.setLayout(layout)

# ------------------------
# Main Logger
# ------------------------
class SupportLogger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRO Support Logger – By Dcnigma")
        self.resize(650,850)
        self.restore_window_position()
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.raise_()
        self.activateWindow()

        # Tabs
        self.tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        self.open_logs = []
        # Data
        self.load_data()
        self.load_settings()
        self.load_language()
        self.load_learning()
        self.load_history()

        # UI
        self.build_log_tab()
        self.build_history_tab()
        self.build_settings_tab()
        # Translate
        self.retranslate_ui()
        # Events
        self.setup_events()

    # ------------------------
    # JSON LOAD/SAVE
    # ------------------------
    def load_settings(self):
        import os

        os.makedirs("data", exist_ok=True)

        if not os.path.exists("data/settings.json"):
            self.settings = {
                "theme": "Light",
                "always_on_top": True,
                "autosave": True
            }
            self.save_settings()
        else:
            with open("data/settings.json", encoding="utf-8") as f:
                self.settings = json.load(f)

    def load_language(self):
        try:
            with open("data/language.json", encoding="utf-8") as f:
                self.languages = json.load(f)
        except:
            self.languages = {}

        self.current_lang = self.settings.get("language", "🇳🇱 Nederlands")


    def t(self, key):
        return self.languages.get(self.current_lang, {}).get(key, key)

    def save_window_position(self):
        settings = load_settings()

        settings["main_pos"] = {
            "x": self.x(),
            "y": self.y(),
            "width": self.width(),
            "height": self.height()
        }

        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

    def restore_window_position(self):
        settings = load_settings()
        pos = settings.get("main_pos")

        if pos:
            self.setGeometry(
                pos.get("x", 0),
                pos.get("y", 0),
                pos.get("width", 650),
                pos.get("height", 850)
            )


    def save_settings(self):
        with open("data/settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)

    def load_data(self):
        import os

        os.makedirs("data", exist_ok=True)

        if not os.path.exists("data/config.json"):
            QMessageBox.critical(self, self.t("error"), self.t("config_missing"))
            sys.exit(1)

        with open("data/config.json", encoding="utf-8") as f:
            self.data = json.load(f)

    def load_learning(self):
        import os

        os.makedirs("data", exist_ok=True)

        if not os.path.exists("data/learning.json"):
            self.learning = {}
            self.save_learning()
        else:
            with open("data/learning.json", encoding="utf-8") as f:
                self.learning = json.load(f)

    def save_learning(self):
        with open("data/learning.json", "w", encoding="utf-8") as f:
            json.dump(self.learning, f, indent=2, ensure_ascii=False)

    def load_history(self):
        import os

        os.makedirs("data", exist_ok=True)

        if not os.path.exists("data/history.json"):
            self.history_logs = []
            self.save_history()
        else:
            with open("data/history.json", encoding="utf-8") as f:
                self.history_logs = json.load(f)

    def save_history(self):
        with open("data/history.json", "w", encoding="utf-8") as f:
            json.dump(self.history_logs, f, indent=2, ensure_ascii=False)

    def save_config(self):
        try:
            with open("data/config.json", "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, self.t("error"),f"{self.t('config_save_error')}:\n{e}")

    def is_autosave_enabled(self):
        return self.settings.get("autosave", True)
    # ------------------------
    # Helper Functions
    # ------------------------
    def find_customer(self, name):
        for cust in self.data.get("customers", {}):
            if cust.lower() == name.lower():
                return cust
        return None

    def ensure_customer_exists(self, customer_name):
        if not customer_name.strip():
            return
        cust = self.find_customer(customer_name)
        if not cust:
            self.data.setdefault("customers", {})[customer_name] = {
                "links": [],
                "used_categories": []
            }

    def update_customer_completer(self):
        completer = SubstringCompleter(list(self.data.get("customers", {}).keys()))
        self.customer_input.setCompleter(completer)

    def add_customer_if_new(self, cust_name):
        cust_name = cust_name.strip()
        if not cust_name:
            return
        if not self.find_customer(cust_name):
            self.data.setdefault("customers", {})[cust_name] = {
                "links": [],
                "used_categories": []
            }
            self.save_config()
            self.update_customer_completer()
            self.update_links()

    # ------------------------
    # CATEGORY / SUBCATEGORY / ACTIONS
    # ------------------------
    def update_subcategories(self):
        self.subcategory_box.clear()
        cat = self.category_box.currentText()
        if not cat: return
        cat_data = self.data["categories"].get(cat, {})
        if "actions" in cat_data:
            self.subcategory_box.addItem("General")
        else:
            self.subcategory_box.addItems(cat_data.keys())
        self.update_actions()

    def update_actions(self):
        self.available_list.clear()
        self.selected_list.clear()
        self.search_input.clear()
        cat = self.category_box.currentText()
        sub = self.subcategory_box.currentText()
        if not cat: return
        cat_data = self.data["categories"].get(cat, {})
        if "actions" in cat_data:
            actions = cat_data.get("actions", [])
            template = cat_data.get("template", {})
        else:
            sub_data = cat_data.get(sub, {})
            actions = sub_data.get("actions", [])
            template = sub_data.get("template", {})

        sorted_actions = sorted(actions, key=lambda x: not x.get("favorite", False))
        for act in sorted_actions:
            self.available_list.addItem(("⭐ " if act.get("favorite", False) else "") + act["name"])
        for a in template.get("actions", []):
            self.selected_list.addItem(a)
        self.notes_input.setText(template.get("notes", ""))
        self.update_links()
        self.update_suggestions()

    # ------------------------
    # LINKS
    # ------------------------
    def update_links(self):
        for i in reversed(range(self.links_layout.count())):
            w = self.links_layout.itemAt(i).widget()
            if w: w.deleteLater()
        cust_input = self.customer_input.text()
        cust = self.find_customer(cust_input)
        cat = self.category_box.currentText()
        sub = self.subcategory_box.currentText()
        if not cust or not cat: return

        for link in self.data.get("customers", {}).get(cust, {}).get("links", []):
            if cat in link.get("tags", []):
                self.add_link_button(link)
        for link in self.data.get("global_links", []):
            if cat in link.get("tags", []) or sub in link.get("tags", []):
                self.add_link_button(link)

    def add_link_button(self, link):
        btn = QPushButton(link["name"])
        btn.clicked.connect(lambda _, url=link["url"]: webbrowser.open(url))
        self.links_layout.addWidget(btn)

    # ------------------------
    # UI BUILD
    # ------------------------
    def build_log_tab(self):
        self.tab1 = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)

        # Customer
        self.customer_input = QLineEdit()
        self.update_customer_completer()

        self.customer_label = QLabel()
        layout.addWidget(self.customer_label)
        layout.addWidget(self.customer_input)

        # Type + Titel
        self.type_box = QComboBox()
        self.type_box.addItems(["Incident","RFI","Change"])

        self.title_input = QLineEdit()

        self.type_label = QLabel()
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_box)

        self.title_label = QLabel()
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)

        # Category
        self.category_box = QComboBox()
        self.subcategory_box = QComboBox()

        self.category_label = QLabel()
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_box)

        self.subcategory_label = QLabel()
        layout.addWidget(self.subcategory_label)
        layout.addWidget(self.subcategory_box)

        # Search
        self.search_input = QLineEdit()
        self.suggestions_list = QListWidget()

        self.search_label = QLabel()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)

        self.suggestions_label = QLabel()
        layout.addWidget(self.suggestions_label)
        layout.addWidget(self.suggestions_list)

        # New action
        self.new_action_input = QLineEdit()
        self.add_new_action_btn = QPushButton()

        new_action_layout = QHBoxLayout()
        new_action_layout.addWidget(self.new_action_input)
        new_action_layout.addWidget(self.add_new_action_btn)
        layout.addLayout(new_action_layout)

        # Actions
        self.available_list = QListWidget()
        self.selected_list = QListWidget()
        self.selected_list.setDragDropMode(QListWidget.InternalMove)
        self.add_btn = QPushButton(">>")
        self.remove_btn = QPushButton("<<")
        self.pin_btn = QPushButton("⭐ Pin")

        lists_layout = QHBoxLayout()
        lists_layout.addWidget(self.available_list)
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.pin_btn)
        btn_layout.addStretch()
        lists_layout.addLayout(btn_layout)
        lists_layout.addWidget(self.selected_list)
        layout.addLayout(lists_layout)

        # Notes
        self.notes_input = QTextEdit()
        self.notes_label = QLabel()
        layout.addWidget(self.notes_label)
        layout.addWidget(self.notes_input)

        # Links
        self.links_layout = QVBoxLayout()
        self.links_label = QLabel()
        layout.addWidget(self.links_label)
        layout.addLayout(self.links_layout)

        # Buttons
        btns = QHBoxLayout()
        self.generate_btn = QPushButton("Genereer")
        self.copy_btn = QPushButton("Copy + Save")
        self.export_btn = QPushButton("Export")
        self.clear_btn = QPushButton("Clear")
        btns.addWidget(self.generate_btn)
        btns.addWidget(self.copy_btn)
        btns.addWidget(self.export_btn)
        btns.addWidget(self.clear_btn)
        layout.addLayout(btns)

        scroll.setWidget(container)
        wrapper = QVBoxLayout()
        wrapper.addWidget(scroll)
        self.tab1.setLayout(wrapper)
        self.tabs.addTab(self.tab1, "Log Builder")

        #  Add Categorys
        self.category_box.addItems(self.data["categories"].keys())
        self.update_subcategories()

    def build_history_tab(self):
        self.tab2 = QWidget()
        layout = QVBoxLayout()
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        for log in self.history_logs:
            ts = log.get("timestamp","")
            cust = log.get("customer","")
            title = log.get("title","")
            self.history_list.addItem(f"[{ts}] {cust} - {title}")
        self.tab2.setLayout(layout)
        self.tabs.addTab(self.tab2, "History")

    def build_settings_tab(self):
        self.tab3 = QWidget()
        layout = QVBoxLayout()

        # Open Config Editor
        self.open_config_btn = QPushButton()
        layout.addWidget(self.open_config_btn)
        self.open_config_btn.clicked.connect(self.open_config_editor)

        # Language Selector
        self.language_label = QLabel()
        layout.addWidget(self.language_label)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["🇳🇱 Nederlands", "🇬🇧 Engels","🇫🇷 Français","🇩🇪 Deutsch","🇪🇸 Español","🧠 Hacker","👾 l33t","🏴‍☠️ Pirate","💼 Corporate Buzzword"])
        layout.addWidget(self.language_combo)

        self.language_combo.setCurrentText(self.settings.get("language", "🇳🇱 Nederlands"))
        self.language_combo.currentTextChanged.connect(self.change_language)

        # Theme Selector
        self.theme_label = QLabel()
        layout.addWidget(self.theme_label)
        self.theme_combo = QComboBox()
        self.themes = ["Light", "Dark", "Hacker", "Blue", "Green", "Pink"]

        self.theme_combo.clear()
        for theme in self.themes:
            self.theme_combo.addItem(self.t(f"theme_{theme.lower()}"), theme)

        layout.addWidget(self.theme_combo)
        self.theme_combo.currentTextChanged.connect(self.apply_theme)

        # Always on Top Toggle
        self.always_on_top_btn = QPushButton()
        layout.addWidget(self.always_on_top_btn)
        self.always_on_top_btn.clicked.connect(self.toggle_always_on_top)

        # Auto-save toggle
        self.autosave_checkbox = QPushButton()
        self.autosave_checkbox.setCheckable(True)
        layout.addWidget(self.autosave_checkbox)
        self.autosave_checkbox.clicked.connect(self.toggle_autosave)

        layout.addStretch()
        self.tab3.setLayout(layout)
        self.tabs.addTab(self.tab3, "Settings")

        # ------------------------
        # APPLY SETTINGS
        # ------------------------

        # Theme
        theme = self.settings.get("theme", "Light")
        self.theme_combo.setCurrentText(theme)
        index = self.theme_combo.findData(theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        self.apply_theme()

        # Autosave
        autosave = self.settings.get("autosave", True)
        self.autosave_checkbox.setChecked(autosave)
        self.autosave_checkbox.setText(f"💾 Auto-save Logs: {'ON' if autosave else 'OFF'}")

        # Always on top
        always_on_top = self.settings.get("always_on_top", True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, always_on_top)
        self.always_on_top_btn.setText(
            f"📌 Always on Top: {'ON' if always_on_top else 'OFF'}"
        )

    # ------------------------
    # Events
    # ------------------------
    def setup_events(self):

        self.category_box.currentTextChanged.connect(self.update_subcategories)
        self.subcategory_box.currentTextChanged.connect(self.update_actions)

        self.add_btn.clicked.connect(self.add_action)
        self.remove_btn.clicked.connect(self.remove_action)
        self.pin_btn.clicked.connect(self.toggle_favorite_selected)

        self.search_input.textChanged.connect(self.update_suggestions)
        self.suggestions_list.itemClicked.connect(self.add_suggestion)

        self.customer_input.textChanged.connect(self.update_links)

        self.customer_input.textChanged.connect(self.on_customer_changed)
        self.generate_btn.clicked.connect(self.generate_log)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.export_btn.clicked.connect(self.export_log)
        self.clear_btn.clicked.connect(self.clear_all)

        self.history_list.itemDoubleClicked.connect(self.open_history_log)

        self.available_list.itemDoubleClicked.connect(self.quick_add_action)
        self.selected_list.itemDoubleClicked.connect(self.quick_remove_action)
        self.add_new_action_btn.clicked.connect(self.add_new_action)
        self.new_action_input.returnPressed.connect(self.add_new_action)

    # ------------------------
    # CUSTOMER EVENTS
    # ------------------------
    def on_customer_changed(self, text):
        self.update_customer_completer()
        self.update_links()

    def on_customer_entered(self):
        cust_name = self.customer_input.text().strip()
        if not cust_name:
            return

        if not self.find_customer(cust_name):
            self.data.setdefault("customers", {})[cust_name] = {
                "links": [],
                "used_categories": []
            }
            self.save_config()
        self.update_customer_completer()
        self.update_links()

    # ------------------------
    # ACTIONS EVENTS
    # ------------------------
    def add_action(self):
        item = self.available_list.currentItem()
        if item:
            self.selected_list.addItem(item.text())

    def remove_action(self):
        item = self.selected_list.currentItem()
        if item:
            self.selected_list.takeItem(self.selected_list.row(item))

    def quick_add_action(self, item):
        self.selected_list.addItem(item.text())

    def quick_remove_action(self, item):
        self.selected_list.takeItem(self.selected_list.row(item))

    def toggle_favorite_selected(self):
        item = self.available_list.currentItem()
        if not item:
            return

        text = item.text()
        act_name = text.lstrip("⭐ ").strip()
        cat = self.category_box.currentText()
        sub = self.subcategory_box.currentText()
        cat_data = self.data["categories"].get(cat, {})

        if "actions" in cat_data:
            actions_list = cat_data["actions"]
        else:
            actions_list = cat_data.get(sub, {}).get("actions", [])

        for act in actions_list:
            if act["name"] == act_name:
                act["favorite"] = not act.get("favorite", False)
                break

        if text.startswith("⭐ "):
            item.setText(act_name)
        else:
            item.setText("⭐ " + act_name)

        self.save_config()

    def add_new_action(self):
        text = self.new_action_input.text().strip()

        if not text:
            return

        cat = self.category_box.currentText()
        sub = self.subcategory_box.currentText()

        if not cat:
            QMessageBox.warning(self, self.t("error"), self.t("category_exists"))
            return

        cat_data = self.data["categories"].get(cat, {})

        if "actions" in cat_data:
            actions_list = cat_data["actions"]
        else:
            if sub not in cat_data:
                cat_data[sub] = {"actions": [], "template": {"actions": [], "notes": ""}}

            actions_list = cat_data[sub]["actions"]

        # Duplicate check
        # check config
        for act in actions_list:
            if act["name"].lower() == text.lower():
                QMessageBox.information(self, self.t("error"), self.t("action_exists"))
                return

        # check UI (extra safety)
        all_ui_actions = {
            self.available_list.item(i).text().replace("⭐ ", "")
            for i in range(self.available_list.count())
        }.union({
            self.selected_list.item(i).text()
            for i in range(self.selected_list.count())
        })
        if text in all_ui_actions:
            QMessageBox.information(self, self.t("error"), self.t("action_exists"))
            return

        # tags (categorie + subcategorie)
        tags = [cat]
        if sub and sub != "General":
            tags.append(sub)

        new_action = {
            "name": text,
            "favorite": False,
            "tags": tags
        }

        actions_list.append(new_action)

        self.save_config()

        # UI update
        self.available_list.addItem(text)
        self.new_action_input.clear()

        existing = [self.selected_list.item(i).text() for i in range(self.selected_list.count())]
        if text not in existing:
            self.selected_list.addItem(text)
    # ------------------------
    # Change Language
    # ------------------------
    def change_language(self, lang):
        self.settings["language"] = lang
        self.save_settings()
        self.current_lang = lang
        self.retranslate_ui()

    def retranslate_ui(self):
        # Tabs
        self.tabs.setTabText(0, self.t("tab_log"))
        self.tabs.setTabText(1, self.t("tab_history"))
        self.tabs.setTabText(2, self.t("tab_settings"))

        # Labels
        self.customer_label.setText(self.t("customer"))
        self.type_label.setText(self.t("type"))
        self.title_label.setText(self.t("title"))
        self.category_label.setText(self.t("category"))
        self.subcategory_label.setText(self.t("subcategory"))
        self.search_label.setText(self.t("search"))
        self.suggestions_label.setText(self.t("suggestions"))
        self.notes_label.setText(self.t("notes"))
        self.links_label.setText(self.t("links"))

        # Buttons
        self.generate_btn.setText(self.t("generate"))
        self.copy_btn.setText(self.t("copy_save"))
        self.export_btn.setText(self.t("export"))
        self.clear_btn.setText(self.t("clear"))
        self.add_new_action_btn.setText(self.t("add"))
        self.pin_btn.setText(self.t("pin"))

        # Placeholders
        self.customer_input.setPlaceholderText(self.t("customer_placeholder"))
        self.new_action_input.setPlaceholderText(self.t("new_action"))

        # Settings
        always_on_top = self.settings.get("always_on_top", True)
        autosave = self.settings.get("autosave", True)

        self.always_on_top_btn.setText(
            f"{self.t('always_on_top')}: {self.bool_text(always_on_top)}"
        )

        self.autosave_checkbox.setText(
            f"{self.t('autosave')}: {self.bool_text(autosave)}"
        )
        self.open_config_btn.setText(self.t("open_config"))

        self.language_label.setText(self.t("language"))
        self.theme_label.setText(self.t("theme"))
        # Theme dropdown refresh
        current_theme = self.theme_combo.currentData()
        self.theme_combo.clear()

        for theme in self.themes:
            self.theme_combo.addItem(self.t(f"theme_{theme.lower()}"), theme)

        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
    # ------------------------
    # LOG GENERATION
    # ------------------------
    def generate_log(self):
        cust = self.customer_input.text()
        if not cust:
            QMessageBox.warning(self, self.t("warning"), self.t("no_customer"))
            return
        self.add_customer_if_new(cust)
        type_ = self.type_box.currentText()
        title = self.title_input.text()
        category = self.category_box.currentText()
        subcategory = self.subcategory_box.currentText()
        actions = [self.selected_list.item(i).text().lstrip("⭐ ") for i in range(self.selected_list.count())]
        notes = self.notes_input.toPlainText()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_text = f"[{timestamp}] {cust} - {type_} - {title}\n"
        log_text += f"Categorie: {category} / {subcategory}\n\n"
        log_text += "Acties:\n" + "\n".join(f"- {a}" for a in actions) + "\n\n"
        log_text += f"Notities:\n{notes}\n"

        # Add to history
        log_entry = {
            "timestamp": timestamp,
            "customer": cust,
            "type": type_,
            "title": title,
            "category": category,
            "subcategory": subcategory,
            "actions": actions,
            "notes": notes
        }

        self.history_list.addItem(f"[{timestamp}] {cust} - {title}")
        self.history_logs.append(log_entry)
        #self.save_history()
        self.search_input.clear()

        # Show in new window
        win = LogWindow(log_text, self.t)
        win.show()
        self.open_logs.append(win)

        # Auto-save learning
        if self.autosave_checkbox.isChecked():
            self.update_learning(cust, actions)

    def copy_to_clipboard(self):
        self.generate_log()
        if not self.open_logs:
            QMessageBox.warning(self, self.t("warning"), self.t("no_log_available"))
            return

        last_log = self.open_logs[-1]

        cust_name = self.customer_input.text().strip()
        self.add_customer_if_new(cust_name)

        QGuiApplication.clipboard().setText(last_log.log_view.toPlainText())

        QMessageBox.information(self, "Info", self.t("copied"))

        self.learn_from_actions()

    def export_log(self):
        if not hasattr(self, "log_window"):
            QMessageBox.warning(self, "Warning", self.t("no_log"))
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export Log", "", "Text Files (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.log_window.log_view.toPlainText())
            QMessageBox.information(self, "Export", f"Log opgeslagen als {path}")

    def clear_all(self):
        self.customer_input.clear()
        self.title_input.clear()
        self.selected_list.clear()
        self.notes_input.clear()
        self.search_input.clear()

    def bool_text(self, value):
        return self.t("on") if value else self.t("off")
    # ------------------------
    # HISTORY
    # ------------------------
    def open_history_log(self, item):
        idx = self.history_list.row(item)
        log = self.history_logs[idx]
        log_text = f"[{log['timestamp']}] {log['customer']} - {log['type']} - {log['title']}\n"
        log_text += f"Categorie: {log['category']} / {log['subcategory']}\n\n"
        log_text += "Acties:\n" + "\n".join(f"- {a}" for a in log['actions']) + "\n\n"
        log_text += f"Notities:\n{log['notes']}\n"

        win = LogWindow(log_text, self.t)
        win.show()

        self.open_logs.append(win)
    # ------------------------
    # LEARNING ENGINE
    # ------------------------
    def learn_from_actions(self):
        cat = self.category_box.currentText()
        actions = [self.selected_list.item(i).text() for i in range(self.selected_list.count())]
        if cat not in self.learning:
            self.learning[cat] = {}
        for a in actions:
            if a not in self.learning[cat]:
                self.learning[cat][a] = {}
            for b in actions:
                if a == b: continue
                self.learning[cat][a][b] = self.learning[cat][a].get(b,0)+1
        self.save_learning()


    # ------------------------
    # LEARNING
    # ------------------------
    def update_learning(self, customer, actions):
        cust_learning = self.learning.setdefault(customer, {})
        clean_actions = [a.lstrip("⭐ ") for a in actions]
        for act in clean_actions:
            cust_learning[act] = cust_learning.get(act, 0) + 1
        self.save_learning()
    # ------------------------
    # SMART SUGGESTIONS
    # ------------------------
    def update_suggestions(self):
        typed = self.search_input.text().lower()
        self.suggestions_list.clear()

        cat = self.category_box.currentText()
        sub = self.subcategory_box.currentText()
        cust = self.customer_input.text().strip()

        if not cat:
            return

        selected = [
            self.selected_list.item(i).text().replace("⭐ ", "")
            for i in range(self.selected_list.count())
        ]

        suggestions = {}

        # ------------------------
        # 1. Only Actions from current category/subcategory
        # ------------------------
        cat_data = self.data["categories"].get(cat, {})

        if "actions" in cat_data:
            actions_data = cat_data.get("actions", [])
        else:
            actions_data = cat_data.get(sub, {}).get("actions", [])

        valid_actions = {act["name"] for act in actions_data}

        # base score
        for act in valid_actions:
            suggestions[act] = 1

        # ------------------------
        # 2. CUSTOMER LEARNING
        # ------------------------
        if cust in self.learning:
            for act, count in self.learning[cust].items():
                if act in valid_actions:
                    suggestions[act] = suggestions.get(act, 0) + (count * 3)

        # ------------------------
        # 3. COMBO LEARNING (category-based)
        # ------------------------
        if cat in self.learning:
            for sel in selected:
                related = self.learning[cat].get(sel, {})
                for act, count in related.items():
                    if act in valid_actions:
                        suggestions[act] = suggestions.get(act, 0) + (count * 5)

        # ------------------------
        # 4. BOOST FAVORITES ⭐
        # ------------------------
        for act in actions_data:
            if act.get("favorite", False):
                name = act["name"]
                if name in suggestions:
                    suggestions[name] += 10

        # ------------------------
        # 5. SORT + FILTER
        # ------------------------
        sorted_suggestions = sorted(
            suggestions.items(),
            key=lambda x: x[1],
            reverse=True
        )
        if not typed:
            for act, score in sorted_suggestions[:5]:
                if act not in selected:
                    self.suggestions_list.addItem(f"🔥 {act}  ({score})")
            return
        for act, score in sorted_suggestions:
            if typed in act.lower() and act not in selected:
                self.suggestions_list.addItem(f"{act}  ({score})")

    def add_suggestion(self, item):
        raw = item.text()

        clean = raw.replace("🔥", "").strip()
        clean = clean.rsplit("(", 1)[0].strip()

        self.selected_list.addItem(clean)

        self.update_suggestions()


    # ------------------------
    # SETTINGS
    # ------------------------
    def toggle_always_on_top(self):
        always_on_top = not bool(self.windowFlags() & Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, always_on_top)
        self.show()
        self.settings["always_on_top"] = always_on_top
        self.save_settings()
        self.always_on_top_btn.setText(
            f"{self.t('always_on_top')}: {self.bool_text(always_on_top)}"
        )

    def toggle_autosave(self):
        state = self.autosave_checkbox.isChecked()
        self.settings["autosave"] = state
        self.save_settings()
        self.autosave_checkbox.setText(
            f"{self.t('autosave')}: {self.bool_text(state)}"
        )

    def apply_theme(self, *_):
        theme = self.theme_combo.currentData()
        self.settings["theme"] = theme
        self.save_settings()

        style = get_theme_stylesheet(theme)
        QApplication.instance().setStyleSheet(style)

    def open_config_editor(self):
        self.showMinimized()
        self.config_window = ConfigEditor(self.t, on_close_callback=self.restore_main_window)
        self.config_window.show()

    def closeEvent(self, event):
        self.save_window_position()
        event.accept()
        return

    def restore_main_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()
        self.load_data()

        # ------------------------
        # Update Categories & Subcategories
        # ------------------------
        self.category_box.clear()
        self.category_box.addItems(self.data["categories"].keys())
        self.update_subcategories()

        # ------------------------
        # Update Links
        # ------------------------
        self.update_links()

        # ------------------------
        # Update Customer autocomplete
        # ------------------------
        completer = QCompleter(list(self.data.get("customers", {}).keys()))
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.customer_input.setCompleter(completer)

        # ------------------------
        # Reset / Update Selected Lists
        # ------------------------
        self.available_list.clear()
        self.selected_list.clear()
        self.notes_input.clear()
        self.search_input.clear()

        if self.category_box.count() > 0:
            self.category_box.setCurrentIndex(0)
            self.update_subcategories()


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = SupportLogger()
    window.show()
    sys.exit(app.exec())
