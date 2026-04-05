import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLineEdit, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from utils.theme_manager import get_theme_stylesheet, load_settings, SETTINGS_PATH
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import QEasingCurve

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "config.json"
)

class ConfigEditor(QWidget):
    def __init__(self, t, on_close_callback=None):
        super().__init__()
        self.t = t   # 🔥 BELANGRIJK

        self.on_close_callback = on_close_callback
        self.setWindowTitle(self.t("config_editor"))
        self.resize(1200, 600)
        self.restore_window_position()
        self.show()
        self.fade_in()
        self.apply_saved_theme()
        self.load_config()
        self.build_ui()
        self.populate_categories()
        self.populate_customers()
        self.retranslate_ui()
        self._is_closing = False
    # ------------------------
    # Translate
    # ------------------------
    def retranslate_ui(self):
        self.setWindowTitle(self.t("config_editor"))

        self.categories_label.setText(self.t("categories"))
        self.subcategories_label.setText(self.t("subcategories"))
        self.actions_label.setText(self.t("actions"))
        self.customers_label.setText(self.t("customers"))
        self.links_label.setText(self.t("links"))
        self.tags_label.setText(self.t("tags"))

        self.add_category_btn.setText(self.t("add_category"))
        self.remove_category_btn.setText(self.t("remove_category"))

        self.add_subcategory_btn.setText(self.t("add_subcategory"))
        self.remove_subcategory_btn.setText(self.t("remove_subcategory"))

        self.add_action_btn.setText(self.t("add_action"))
        self.remove_action_btn.setText(self.t("remove_action"))

        self.add_customer_btn.setText(self.t("add_customer"))
        self.remove_customer_btn.setText(self.t("remove_customer"))

        self.add_link_btn.setText(self.t("add_link"))
        self.remove_link_btn.setText(self.t("remove_link"))

        self.add_tag_btn.setText(self.t("add_tag"))
        self.remove_tag_btn.setText(self.t("remove_tag"))

        self.add_link_tag_btn.setText(self.t("add_tag"))
        self.remove_link_tag_btn.setText(self.t("remove_tag"))

        # placeholders
        self.new_category_input.setPlaceholderText(self.t("new_category"))
        self.new_subcategory_input.setPlaceholderText(self.t("new_subcategory"))
        self.new_action_input.setPlaceholderText(self.t("new_action"))
        self.new_customer_input.setPlaceholderText(self.t("new_customer"))

        self.customer_search_input.setPlaceholderText(self.t("search_customer"))

        self.new_link_name_input.setPlaceholderText(self.t("link_name"))
        self.new_link_url_input.setPlaceholderText(self.t("link_url"))

        self.new_tag_input.setPlaceholderText(self.t("new_tag"))
        self.new_link_tag_input.setPlaceholderText(self.t("new_tag"))

    # ------------------------
    # Screen Location
    # ------------------------

    def fade_in(self):
        self.setWindowOpacity(0)

        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(300)  # 🔥 snelheid (ms)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def center_top(self):
        screen = self.screen().availableGeometry()

        x = screen.x() + (screen.width() - self.width()) // 2
        y = screen.y() + 0

        self.move(x, y)

    # ------------------------
    # Themes
    # ------------------------
    def apply_saved_theme(self):
        settings = load_settings()
        theme = settings.get("theme", "Light")
        style = get_theme_stylesheet(theme)
        self.setStyleSheet(style)
    # ------------------------
    # CLOSE EVENT
    # ------------------------
    def closeEvent(self, event):
        if self._is_closing:
            self.save_window_position()
            if self.on_close_callback:
                self.on_close_callback()
            event.accept()
            return

        event.ignore()
        self.fade_out()
    # ------------------------
    # LOAD / SAVE
    # ------------------------
    def load_config(self):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            self.data = json.load(f)

    def save_window_position(self):
        settings = load_settings()

        settings["config_editor_pos"] = {
            "x": self.x(),
            "y": self.y(),
            "width": self.width(),
            "height": self.height()
        }

        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

    def restore_window_position(self):
        settings = load_settings()
        pos = settings.get("config_editor_pos")

        if pos:
            self.setGeometry(
                pos.get("x", 100),
                pos.get("y", 100),
                pos.get("width", 1200),
                pos.get("height", 600)
            )
        else:
            self.center_top()  # fallback

    def save_config(self):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def fade_out(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.setDuration(300)
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)

        # Wanneer animatie klaar is → echt sluiten
        self.anim.finished.connect(self.finish_close)

        self.anim.start()

    def finish_close(self):
        self._is_closing = True
        self.close()
    # ------------------------
    # BUILD UI
    # ------------------------
    def build_ui(self):
        main_layout = QHBoxLayout()

        # ------------------------
        # LEFT: Categories
        # ------------------------
        left = QVBoxLayout()

        self.categories_label = QLabel()
        left.addWidget(self.categories_label)

        self.category_list = QListWidget()
        left.addWidget(self.category_list)

        self.new_category_input = QLineEdit()
        self.add_category_btn = QPushButton()
        self.remove_category_btn = QPushButton()

        left.addWidget(self.new_category_input)
        left.addWidget(self.add_category_btn)
        left.addWidget(self.remove_category_btn)

        # ------------------------
        # MIDDLE: Subcategories
        # ------------------------
        middle = QVBoxLayout()

        self.subcategories_label = QLabel()
        middle.addWidget(self.subcategories_label)

        self.subcategory_list = QListWidget()
        middle.addWidget(self.subcategory_list)

        self.new_subcategory_input = QLineEdit()
        self.add_subcategory_btn = QPushButton()
        self.remove_subcategory_btn = QPushButton()

        middle.addWidget(self.new_subcategory_input)
        middle.addWidget(self.add_subcategory_btn)
        middle.addWidget(self.remove_subcategory_btn)

        # ------------------------
        # RIGHT: Actions + Tags
        # ------------------------
        right = QVBoxLayout()

        self.actions_label = QLabel()
        right.addWidget(self.actions_label)

        self.action_list = QListWidget()
        right.addWidget(self.action_list)

        self.new_action_input = QLineEdit()
        self.add_action_btn = QPushButton()
        self.remove_action_btn = QPushButton()

        right.addWidget(self.new_action_input)
        right.addWidget(self.add_action_btn)
        right.addWidget(self.remove_action_btn)

        # Tags voor Actions
        self.tags_label = QLabel()
        right.addWidget(self.tags_label)

        self.tag_list = QListWidget()
        right.addWidget(self.tag_list)

        self.new_tag_input = QLineEdit()
        self.add_tag_btn = QPushButton()
        self.remove_tag_btn = QPushButton()

        right.addWidget(self.new_tag_input)
        right.addWidget(self.add_tag_btn)
        right.addWidget(self.remove_tag_btn)

        # ------------------------
        # CUSTOMER COLUMN
        # ------------------------
        customer_col = QVBoxLayout()

        self.customers_label = QLabel()
        customer_col.addWidget(self.customers_label)

        self.customer_search_input = QLineEdit()
        customer_col.addWidget(self.customer_search_input)

        self.customer_list = QListWidget()
        customer_col.addWidget(self.customer_list)

        self.new_customer_input = QLineEdit()
        self.add_customer_btn = QPushButton()
        self.remove_customer_btn = QPushButton()

        customer_col.addWidget(self.new_customer_input)
        customer_col.addWidget(self.add_customer_btn)
        customer_col.addWidget(self.remove_customer_btn)

        # Links
        self.links_label = QLabel()
        customer_col.addWidget(self.links_label)

        self.link_list = QListWidget()
        customer_col.addWidget(self.link_list)

        self.new_link_name_input = QLineEdit()
        self.new_link_url_input = QLineEdit()
        self.add_link_btn = QPushButton()
        self.remove_link_btn = QPushButton()

        customer_col.addWidget(self.new_link_name_input)
        customer_col.addWidget(self.new_link_url_input)
        customer_col.addWidget(self.add_link_btn)
        customer_col.addWidget(self.remove_link_btn)

        # Link tags
        self.link_tags_label = QLabel()
        customer_col.addWidget(self.link_tags_label)

        self.link_tag_list = QListWidget()
        customer_col.addWidget(self.link_tag_list)

        self.new_link_tag_input = QLineEdit()
        self.add_link_tag_btn = QPushButton()
        self.remove_link_tag_btn = QPushButton()

        customer_col.addWidget(self.new_link_tag_input)
        customer_col.addWidget(self.add_link_tag_btn)
        customer_col.addWidget(self.remove_link_tag_btn)

        # ------------------------
        # ADD TO MAIN
        # ------------------------
        main_layout.addLayout(left)
        main_layout.addLayout(middle)
        main_layout.addLayout(right)
        main_layout.addLayout(customer_col)

        self.setLayout(main_layout)

        # ------------------------
        # EVENTS
        # ------------------------
        self.customer_search_input.textChanged.connect(self.filter_customers)
        self.category_list.currentTextChanged.connect(self.load_subcategories)
        self.subcategory_list.currentTextChanged.connect(self.load_actions)
        self.action_list.currentTextChanged.connect(self.load_tags)
        self.customer_list.currentTextChanged.connect(self.load_links)
        self.link_list.currentTextChanged.connect(self.load_link_tags)

        # Add / Remove buttons
        self.add_category_btn.clicked.connect(self.add_category)
        self.remove_category_btn.clicked.connect(self.remove_category)
        self.add_subcategory_btn.clicked.connect(self.add_subcategory)
        self.remove_subcategory_btn.clicked.connect(self.remove_subcategory)
        self.add_action_btn.clicked.connect(self.add_action)
        self.remove_action_btn.clicked.connect(self.remove_action)
        self.add_tag_btn.clicked.connect(self.add_tag)
        self.remove_tag_btn.clicked.connect(self.remove_tag)
        self.add_customer_btn.clicked.connect(self.add_customer)
        self.remove_customer_btn.clicked.connect(self.remove_customer)
        self.add_link_btn.clicked.connect(self.add_link)
        self.remove_link_btn.clicked.connect(self.remove_link)
        self.add_link_tag_btn.clicked.connect(self.add_link_tag)
        self.remove_link_tag_btn.clicked.connect(self.remove_link_tag)

    # ------------------------
    # POPULATE / LOAD
    # ------------------------
    def populate_categories(self):
        self.category_list.clear()
        for cat in self.data.get("categories", {}):
            self.category_list.addItem(cat)

    def load_subcategories(self):
        self.subcategory_list.clear()
        self.action_list.clear()
        self.tag_list.clear()
        cat = self.category_list.currentItem()
        if not cat:
            return
        cat_name = cat.text()
        cat_data = self.data["categories"].get(cat_name, {})
        for sub in cat_data:
            self.subcategory_list.addItem(sub)

    def load_actions(self):
        self.action_list.clear()
        self.tag_list.clear()
        cat = self.category_list.currentItem()
        sub = self.subcategory_list.currentItem()
        if not cat or not sub:
            return
        cat_name = cat.text()
        sub_name = sub.text()
        actions = self.data["categories"][cat_name][sub_name].get("actions", [])
        for act in actions:
            self.action_list.addItem(act["name"])

    def load_tags(self):
        self.tag_list.clear()
        cat = self.category_list.currentItem()
        sub = self.subcategory_list.currentItem()
        action_item = self.action_list.currentItem()
        if not cat or not sub or not action_item:
            return
        cat_name = cat.text()
        sub_name = sub.text()
        action_name = action_item.text()
        actions = self.data["categories"][cat_name][sub_name]["actions"]
        for act in actions:
            if act["name"] == action_name:
                for tag in act.get("tags", []):
                    self.tag_list.addItem(tag)
                break

    def populate_customers(self):
        self.customer_list.clear()
        for cust in self.data.get("customers", {}):
            self.customer_list.addItem(cust)

    def filter_customers(self, text):
        current_cust = self.customer_list.currentItem()
        current_name = current_cust.text() if current_cust else None

        text = text.lower().strip()
        self.customer_list.clear()
        for cust in self.data.get("customers", {}):
            if text in cust.lower():
                self.customer_list.addItem(cust)

        # Probeer de oude selectie te behouden
        if current_name:
            matches = self.customer_list.findItems(current_name, Qt.MatchExactly)
            if matches:
                self.customer_list.setCurrentItem(matches[0])

    def load_links(self):
        self.link_list.clear()
        self.link_tag_list.clear()
        cust_item = self.customer_list.currentItem()
        if not cust_item:
            return
        cust_name = cust_item.text()
        links = self.data["customers"][cust_name].get("links", [])
        for link in links:
            self.link_list.addItem(f"{link['name']} ({link['url']})")

    def load_link_tags(self):
        self.link_tag_list.clear()
        cust_item = self.customer_list.currentItem()
        link_item = self.link_list.currentItem()
        if not cust_item or not link_item:
            return
        cust_name = cust_item.text()
        link_text = link_item.text()
        link_name = link_text.split(" (")[0]
        links = self.data["customers"][cust_name].get("links", [])
        for link in links:
            if link["name"] == link_name:
                for tag in link.get("tags", []):
                    self.link_tag_list.addItem(tag)
                break

    # ------------------------
    # ACTIONS: Add / Remove
    # ------------------------
    # Categories
    def add_category(self):
        name = self.new_category_input.text().strip()
        if not name: return
        if name in self.data["categories"]:
            QMessageBox.warning(self, self.t("exists"), self.t("category_exists"))
            return
        self.data["categories"][name] = {"General": {"actions": [], "template": {"actions": [], "notes": ""}}}
        self.save_config()
        self.category_list.addItem(name)
        self.new_category_input.clear()

    def remove_category(self):
        cat = self.category_list.currentItem()
        if not cat: return
        cat_name = cat.text()
        del self.data["categories"][cat_name]
        self.save_config()
        self.populate_categories()
        self.subcategory_list.clear()
        self.action_list.clear()
        self.tag_list.clear()

    # Subcategories
    def add_subcategory(self):
        cat = self.category_list.currentItem()
        if not cat:
            QMessageBox.warning(self, self.t("error"), self.t("select_category"))
            return
        cat_name = cat.text()
        sub_name = self.new_subcategory_input.text().strip()
        if not sub_name: return
        if sub_name in self.data["categories"][cat_name]:
            QMessageBox.warning(self, self.t("exists"), self.t("subcategory_exists"))
            return
        self.data["categories"][cat_name][sub_name] = {"actions": [], "template": {"actions": [], "notes": ""}}
        self.save_config()
        self.subcategory_list.addItem(sub_name)
        self.new_subcategory_input.clear()

    def remove_subcategory(self):
        cat = self.category_list.currentItem()
        sub = self.subcategory_list.currentItem()
        if not cat or not sub: return
        cat_name = cat.text()
        sub_name = sub.text()
        del self.data["categories"][cat_name][sub_name]
        self.save_config()
        self.load_subcategories()
        self.action_list.clear()
        self.tag_list.clear()

    # Actions
    def add_action(self):
        text = self.new_action_input.text().strip()
        if not text: return
        cat = self.category_list.currentItem()
        sub = self.subcategory_list.currentItem()
        if not cat or not sub:
            QMessageBox.warning(self, self.t("error"), self.t("select_category_subcategory"))
            return
        cat_name = cat.text()
        sub_name = sub.text()
        actions = self.data["categories"][cat_name][sub_name]["actions"]
        for act in actions:
            if act["name"].lower() == text.lower():
                QMessageBox.information(self, self.t("exists"), self.t("action_exists"))
                return
        new_action = {"name": text, "favorite": False, "tags": [cat_name, sub_name]}
        actions.append(new_action)
        self.save_config()
        self.load_actions()
        self.new_action_input.clear()

    def remove_action(self):
        cat = self.category_list.currentItem()
        sub = self.subcategory_list.currentItem()
        action_item = self.action_list.currentItem()
        if not cat or not sub or not action_item: return
        cat_name = cat.text()
        sub_name = sub.text()
        action_name = action_item.text()
        actions = self.data["categories"][cat_name][sub_name]["actions"]
        self.data["categories"][cat_name][sub_name]["actions"] = [a for a in actions if a["name"] != action_name]
        self.save_config()
        self.load_actions()
        self.tag_list.clear()

    # Tags
    def add_tag(self):
        new_tag = self.new_tag_input.text().strip()
        if not new_tag: return
        cat = self.category_list.currentItem()
        sub = self.subcategory_list.currentItem()
        action_item = self.action_list.currentItem()
        if not cat or not sub or not action_item: return
        cat_name = cat.text()
        sub_name = sub.text()
        action_name = action_item.text()
        actions = self.data["categories"][cat_name][sub_name]["actions"]
        for act in actions:
            if act["name"] == action_name:
                if new_tag in act.get("tags", []):
                    QMessageBox.information(self, self.t("exists"), self.t("tag_exists"))
                    return
                act["tags"].append(new_tag)
                break
        self.save_config()
        self.load_tags()
        self.new_tag_input.clear()

    def remove_tag(self):
        tag_item = self.tag_list.currentItem()
        if not tag_item: return
        tag_text = tag_item.text()
        cat = self.category_list.currentItem()
        sub = self.subcategory_list.currentItem()
        action_item = self.action_list.currentItem()
        if not cat or not sub or not action_item: return
        cat_name = cat.text()
        sub_name = sub.text()
        action_name = action_item.text()
        actions = self.data["categories"][cat_name][sub_name]["actions"]
        for act in actions:
            if act["name"] == action_name:
                act["tags"] = [t for t in act.get("tags", []) if t != tag_text]
                break
        self.save_config()
        self.load_tags()

    # ------------------------
    # Customers + Links
    # ------------------------
    def add_customer(self):
        name = self.new_customer_input.text().strip()
        if not name: return
        if name in self.data["customers"]:
            QMessageBox.warning(self, self.t("exists"), self.t("customer_exists"))
            return
        self.data["customers"][name] = {"links": [], "used_categories": []}
        self.save_config()
        self.populate_customers()
        self.new_customer_input.clear()

    def remove_customer(self):
        cust = self.customer_list.currentItem()
        if not cust: return
        cust_name = cust.text()
        del self.data["customers"][cust_name]
        self.save_config()
        self.populate_customers()
        self.link_list.clear()
        self.link_tag_list.clear()

    def add_link(self):
        cust_item = self.customer_list.currentItem()
        if not cust_item: return
        cust_name = cust_item.text()
        link_name = self.new_link_name_input.text().strip()
        link_url = self.new_link_url_input.text().strip()
        if not link_name or not link_url: return
        links = self.data["customers"][cust_name].get("links", [])
        links.append({"name": link_name, "url": link_url, "tags": [], "customer_specific": False})
        self.save_config()
        self.load_links()
        self.new_link_name_input.clear()
        self.new_link_url_input.clear()

    def remove_link(self):
        cust_item = self.customer_list.currentItem()
        link_item = self.link_list.currentItem()
        if not cust_item or not link_item: return
        cust_name = cust_item.text()
        link_name = link_item.text().split(" (")[0]
        links = self.data["customers"][cust_name].get("links", [])
        self.data["customers"][cust_name]["links"] = [l for l in links if l["name"] != link_name]
        self.save_config()
        self.load_links()
        self.link_tag_list.clear()

    # ------------------------
    # Link Tags
    # ------------------------
    def add_link_tag(self):
        new_tag = self.new_link_tag_input.text().strip()
        cust_item = self.customer_list.currentItem()
        link_item = self.link_list.currentItem()
        if not new_tag or not cust_item or not link_item: return
        cust_name = cust_item.text()
        link_name = link_item.text().split(" (")[0]
        links = self.data["customers"][cust_name].get("links", [])
        for link in links:
            if link["name"] == link_name:
                if new_tag in link.get("tags", []):
                    QMessageBox.information(self, self.t("exists"), self.t("tag_exists"))
                    return
                link["tags"].append(new_tag)
                break
        self.save_config()
        self.load_link_tags()
        self.new_link_tag_input.clear()

    def remove_link_tag(self):
        tag_item = self.link_tag_list.currentItem()
        cust_item = self.customer_list.currentItem()
        link_item = self.link_list.currentItem()
        if not tag_item or not cust_item or not link_item: return
        tag_text = tag_item.text()
        cust_name = cust_item.text()
        link_name = link_item.text().split(" (")[0]
        links = self.data["customers"][cust_name].get("links", [])
        for link in links:
            if link["name"] == link_name:
                link["tags"] = [t for t in link.get("tags", []) if t != tag_text]
                break
        self.save_config()
        self.load_link_tags()
