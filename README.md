# EasyScrcpy

**EasyScrcpy** is a friendly, accessible, and feature-packed Windows GUI launcher for Android screen mirroring and device control. 

Built on top of Genymobile's powerful command-line tool `scrcpy`, EasyScrcpy bridges the gap between complex command-line options and everyday usability. It completely eliminates the need to touch the Windows terminal, offering a clean point-and-click interface designed for everyone—from non-technical family members needing simple phone access on a PC to power users requiring wireless multi-device control and PC gamepad passthrough.

---

## ✨ Key Features

* **Zero-Terminal Setup**: Includes a fully automated installer (`setup.bat`) and a silent background launcher (`EasyScrcpy.vbs`). Non-technical users never see a command prompt.
* **One-Click Wireless & USB Launching**: Save device profiles (e.g., "Mom's Pixel") with local IP addresses for fast, single-click wireless connections. USB devices auto-launch smoothly when plugged in.
* **Dynamic Theme Engine**: Easily switch color palettes on the fly to match room lighting or accessibility needs (Catppuccin Dark, Clean Light, Nord Slate, Dracula, Emerald Night).
* **Floating Control Overlay**: A draggable, always-on-top floating toolbar providing instant access to Home, Back, Screen Rotation, Volume, and Screen Off actions.
* **PC Gamepad & Controller Passthrough**: Directly forward Xbox, PlayStation, or generic PC controllers to connected Android devices using native kernel UHID emulation or AOA mode.
* **Multi-Device Hub**: Wirelessly connect, monitor, and launch multiple phones simultaneously, with options to broadcast control actions across all active devices.
* **Secondary Display / Desktop Mode**: Run independent secondary virtual desktop displays on supported Android devices (`--new-display`).

---

## 🎨 Theme & Lighting Accessibility

EasyScrcpy features an integrated Theme Manager designed to accommodate different visual preferences, contrast sensitivities, and room lighting conditions:

| Theme Name | Description | Best Environment |
| :--- | :--- | :--- |
| **Catppuccin Dark** *(Default)* | Soothing obsidian background with pastel blue/mauve accents | Dimly lit rooms / Dark mode preference |
| **Clean Light** | Crisp white & slate background with rich indigo blue accents | Bright daylight / Direct sunlight offices |
| **Nord Slate** | Cool arctic gray background with soft ice-blue highlights | Balanced neutral day/night use |
| **Dracula / Purple** | Vibrant high-contrast dark palette with neon purple accents | High contrast legibility |
| **Emerald Night** | Deep forest green/black background with mint highlights | Low eye-strain late night use |

Themes can be selected instantly from the dropdown menu at the top of the application dashboard and automatically persist across launches.

---

## 🚀 First-Time Installation Guide (Fresh Windows PC)

EasyScrcpy is designed to be installed on a fresh Windows system in just a few clicks.

### Step 1: Install Python
1. Download Python 3.10 or higher from [python.org](https://www.python.org/downloads/).
2. Run the installer and **IMPORTANT**: Make sure to check the box that says **"Add Python to PATH"** before clicking Install.

### Step 2: Run the EasyScrcpy Setup Script
1. Download or clone this repository to your computer.
2. Open the project folder and double-click **`setup.bat`**.
3. The setup script will automatically:
   * Install the required PySide6 graphical interface libraries.
   * Download the official, tested `scrcpy` binaries directly from GitHub releases into a local `./bin/` folder.
   * Create a handy **EasyScrcpy** shortcut directly on your Windows Desktop.

---

## 📱 How to Use EasyScrcpy

### For Everyday Users (Simple Mode)
1. Double-click the **EasyScrcpy** shortcut on your Desktop. *(The app opens silently in the background without any command prompt windows).*
2. Connect your phone to your PC via USB cable.
3. Click **▶ Launch Target Phone**. Your phone screen will appear on your desktop instantly!
4. *(Optional Wireless)*: Once paired over Wi-Fi, select your phone from the **Saved Profile** dropdown and click **⚡ One-Click Connect**.

### For Power Users & Gaming
* **Wireless mDNS Scan**: Click **🔍 Scan Network** under the Wi-Fi section to automatically discover active wireless ADB endpoints broadcasted on your local network.
* **Gamepad Passthrough**: Set the Gamepad Mode to **UHID Emulation** to play Android games using your PC's connected Xbox or PlayStation controller as a native Android gamepad.
* **Multi-Device Control**: Connect multiple phones simultaneously, select **"🌐 All Devices"** in the floating toolbar, and enable **Broadcast All** to send inputs to all screens at once.

---

## 📁 Repository Structure

```text
Idiots-easy-scrcpy-wraper/
├── core/
│   ├── adb_wrapper.py        # ADB process wrapper & command execution
│   ├── auto_reconnect.py    # Background thread monitoring USB/Wi-Fi attachments
│   └── scrcpy_controller.py # Scrcpy process launcher & argument compiler
├── ui/
│   ├── main_window.py       # Primary PySide6 graphical interface
│   └── visual_toolbar.py    # Draggable floating control overlay
├── utils/
│   ├── config_manager.py    # Manages local config.json preferences
│   └── theme_manager.py     # Generates custom QSS stylesheets & color palettes
├── .gitignore               # Excludes binary downloads, cache, & local configs
├── EasyScrcpy.vbs           # Silent background launcher (no command prompt)
├── LICENSE                  # MIT License file
├── README.md                # Project documentation
├── main.py                  # Main program entry point
├── requirements.txt         # Python dependencies
└── setup.bat                # Automated fresh environment installer script
