import json
import os

SETTINGS_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "settings.json"
)

def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {"theme": "Light"}
    with open(SETTINGS_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_theme_stylesheet(theme_name):
    if theme_name == "Dark":
        return """
        QWidget {
            background-color: #2e2e2e;
            color: #f0f0f0;
        }
        QLineEdit, QTextEdit, QComboBox, QListWidget {
            background-color: #3e3e3e;
            color: #f0f0f0;
            border: 1px solid #555555;
        }
        QPushButton {
            background-color: #555555;
            color: #f0f0f0;
            border: 1px solid #888888;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #666666;
        }
        QTabWidget::pane {
            border: 1px solid #444444;
        }
        QTabBar::tab {
            background: #555555;
            color: #f0f0f0;
            padding: 5px;
            border: 1px solid #444444;
            border-bottom-color: #2e2e2e;
        }
        QTabBar::tab:selected {
            background: #777777;
        }
        QListWidget::item:selected {
            background-color: #555555;
            color: #ffffff;
        }
        """

    elif theme_name == "Hacker":
        return """
        QWidget {
            background-color: #363333;
            color: #66ff00;
        }

        QLineEdit, QTextEdit, QComboBox, QListWidget {
            background-color: #3e3e3e;
            color: #66ff00;
            border: none;
            border: 1px solid #457e1f;
        }

        QComboBox::item:selected {
            background-color: #555555;
            color: #66ff00;
            border: 2px solid #457e1f;
            padding: 5px;
        }
        QListWidget::item:selected {
            background-color: #555555;
            color: #66ff00;
            border: 2px solid #457e1f;
            padding: 5px;
        }

        QPushButton {
            background-color: #363333;
            color: #66ff00;
            border: 1px solid #457e1f;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #666666;
        }
        QTabWidget::pane {
            border: 1px solid #457e1f;
        }
        QTabBar::tab {
            background: #555555;
            color: #41bf24;
            padding: 5px;
            border: 1px solid #457e1f;
            border-bottom-color: #2e2e2e;
        }
        QTabBar::tab:selected {
            background: #777777;
        }
        QListWidget::item:selected {
            background-color: #555555;
            color: #66ff00;
        }
        """

    elif theme_name == "Blue":
        return """
        QWidget {
            background-color: #cce7ff;
            color: #003366;
        }
        QLineEdit, QTextEdit, QComboBox, QListWidget {
            background-color: #e6f3ff;
            color: #003366;
            border: 1px solid #99ccff;
        }
        QPushButton {
            background-color: #99ccff;
            color: #003366;
            border: 1px solid #66a3cc;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #66a3cc;
        }
        QTabWidget::pane {
            border: 1px solid #66a3cc;
        }
        QTabBar::tab {
            background: #99ccff;
            color: #003366;
            padding: 5px;
            border: 1px solid #66a3cc;
            border-bottom-color: #cce7ff;
        }
        QTabBar::tab:selected {
            background: #66a3cc;
        }
        QListWidget::item:selected {
            background-color: #66a3cc;
            color: #ffffff;
        }
        """

    elif theme_name == "Green":
        return """
        QWidget {
            background-color: #e7ffe7;
            color: #003300;
        }
        QLineEdit, QTextEdit, QComboBox, QListWidget {
            background-color: #f0fff0;
            color: #003300;
            border: 1px solid #99cc99;
        }
        QPushButton {
            background-color: #99cc99;
            color: #003300;
            border: 1px solid #66a366;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #66a366;
        }
        QTabWidget::pane {
            border: 1px solid #66a366;
        }
        QTabBar::tab {
            background: #99cc99;
            color: #003300;
            padding: 5px;
            border: 1px solid #66a366;
            border-bottom-color: #e7ffe7;
        }
        QTabBar::tab:selected {
            background: #66a366;
        }
        QListWidget::item:selected {
            background-color: #66a366;
            color: #ffffff;
        }
        """
    elif theme_name == "Pink":
        return """
        QWidget {
            background-color: #e9baeb;
            color: #ff0beb;
        }
        QLineEdit, QTextEdit, QComboBox, QListWidget {
            background-color: #fff0fe;
            color: #ff0beb;
            border: 1px solid #ca99cc;
        }
        QPushButton {
            background-color: #cc99c4;
            color: #ffffff;
            border: 1px solid #ca99cc;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #a3679e;
        }
        QTabWidget::pane {
            border: 1px solid #a167a3;
        }
        QTabBar::tab {
            background: #cc99ca;
            color: #ffffff;
            padding: 5px;
            border: 1px solid #a367a3;
            border-bottom-color: #ffe8ff;
        }
        QTabBar::tab:selected {
            background: #fba7ff;
        }
        QListWidget::item:selected {
            background-color: #e89ede;
            color: #ffffff;
        }
        """
    else:  # Light
        return """
        QWidget {
            background-color: #f0f0f0;
            color: #2e2e2e;
        }
        QLineEdit, QTextEdit, QComboBox, QListWidget {
            background-color: #ffffff;
            color: #2e2e2e;
            border: 1px solid #cccccc;
        }
        QPushButton {
            background-color: #dddddd;
            color: #2e2e2e;
            border: 1px solid #aaaaaa;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #cccccc;
        }
        QTabWidget::pane {
            border: 1px solid #aaaaaa;
        }
        QTabBar::tab {
            background: #dddddd;
            color: #2e2e2e;
            padding: 5px;
            border: 1px solid #cccccc;
            border-bottom-color: #f0f0f0;
        }
        QTabBar::tab:selected {
            background: #bbbbbb;
        }
        QListWidget::item:selected {
            background-color: #cccccc;
            color: #000000;
        }
        """
