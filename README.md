# PRO Support Logger

**PRO Support Logger** is a Python-based support logging tool designed to help support teams quickly generate, manage, and track customer logs. It includes category/subcategory management, smart suggestions, auto-saving, history tracking, and multi-language support, all wrapped in a user-friendly PySide6 GUI.

---

## Features

- Create detailed support logs for customers with categories, subcategories, and actions.
- Smart suggestions powered by customer-specific learning and favorite actions.
- Auto-save logs and learn from user actions to improve future suggestions.
- Manage customers and their links, integrated directly in the UI.
- Multi-language support:
  - 🇳🇱 Dutch
  - 🇬🇧 English
  - 🇫🇷 French
  - 🇩🇪 German
  - 🇪🇸 Spanish
  - 🧠 Hacker / Mr Robot style
  - 👾 l33t style
  - 🏴‍☠️ Pirate style
  - 💼 Corporate Buzzword style
- Theme support: Light, Dark, Hacker, Blue, Green, Pink.
- Persistent window position, settings, and history.
- Export logs as text files or copy to clipboard.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/pro-support-logger.git
cd pro-support-logger
Install dependencies
pip install PySide6
```
Optional: If you use virtual environments, it's recommended to create one first:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
Run the application
```bash
python main.py
```
Make sure data/config.json exists. A template config will be provided in the repo.

---

## Usage

**1. Log Builder Tab**
 - Select a customer or enter a new one.
 - Choose the type of log: Incident, RFI, or Change.
 - Enter a title, select category and subcategory.
 - Add actions to your log. Favorites are marked with ⭐.
 - Add notes and use smart suggestions to quickly populate actions.
 - Generate, copy, or export logs.

**2. History Tab** 
 - View previously generated logs with timestamps.
 - Double-click an entry to open it in a read-only window.

**3. Settings Tab**
 - Change language and theme.
 - Toggle "Always on Top" and "Auto-save Logs".
 - Open the config editor to customize categories, actions, templates, and global links.

---

## File Structure
```
pro-support-logger/
├── main.py                # Main application
├── utils/
│   ├── config_editor.py   # GUI for editing config.json
│   ├── theme_manager.py   # Load themes and settings
├── data/
│   ├── config.json        # Categories, actions, templates, links
│   ├── settings.json      # User preferences (theme, language, autosave)
│   ├── history.json       # Saved logs
│   └── learning.json      # Customer-specific learning data
├── README.md
└── requirements.txt       # Optional
```
# Configuration
- **config.json**: Contains categories, subcategories, actions, templates, and links. Must exist before running the app.
- **settings.json**: Created automatically on first run. Stores language, theme, and UI preferences.
- **history.json**: Stores generated logs for viewing in the History tab.
- **learning.json**: Tracks user action choices to improve suggestions over time.

---

# Screenshots

**UI**

<img src="https://raw.githubusercontent.com/Dcnigma/PRO-Support-Logger/refs/heads/main/Screenshots/UI.png" width=50% height=50%>

**Themes**

<img src="https://raw.githubusercontent.com/Dcnigma/PRO-Support-Logger/refs/heads/main/Screenshots/Pro_Support_Loggin_skins.gif" width=50% height=50%>

Colours are not accurate because of gif file.

**Config Editor**

<img src="https://raw.githubusercontent.com/Dcnigma/PRO-Support-Logger/refs/heads/main/Screenshots/Config_Editor.png" width=80% height=80%>


---
Feel free to submit issues, fork the repository, or create pull requests.
If you add new languages, themes, or features, update languages.json and the UI accordingly.
