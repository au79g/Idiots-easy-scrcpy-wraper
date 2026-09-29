# Change Log - EasyScrcpy Custom Launcher

All project changes and custom wrapper developments are documented below under Apache License 2.0.

## [v1.4.0] - 2026-09-28 - Isolated Controller Assignment Matrix (Au79)

### Added
- **Hardware Controller Enumeration (`core/gamepad_manager.py`)**: Added automated scanning of host PC gamepads with Hardware VIDs/PIDs.
- **Dedicated Controller Assignment Matrix (`ui/main_window.py`)**: Users can explicitly select which PC controller(s) map to which connected phone (up to 8 controller slots per phone).
- **Process-Level Input Isolation (`core/scrcpy_controller.py`)**: Automatically injects `SDL_HINT_GAMECONTROLLER_IGNORE_DEVICES` into each Scrcpy session, preventing input leakage/bleeding between phones or virtual controller ports.

## [v1.3.0] - 2026-09-28 - Draggable Toolbar & PC Gamepad Passthrough Engine (Au79)

### Added
- **Draggable Floating Toolbar (`ui/visual_toolbar.py`)**: Added mouse press/move handlers allowing users to drag the toolbar across multi-monitor setups.
- **Default Position Reset (`ui/visual_toolbar.py`)**: Added "?? Reset Pos" button to instantly snap the floating toolbar back to the top-right screen anchor.
- **Gamepad Passthrough Engine (`core/scrcpy_controller.py`)**: Integrated native Linux/Android UHID (`--gamepad=uhid`) and AOA (`--gamepad=aoa`) driver emulation for low-latency PC controller forwarding to phones.
- **Gamepad Routing Configuration (`ui/main_window.py`)**: Added Gamepad Mode selection dropdown in the UI supporting up to 8 gamepads per phone session for multi-player and emulation setups.

## [v1.2.0] - 2026-09-28 - Multi-Device Simultaneous Sessions & Resolution Scaling (Au79)

### Added
- **Multi-Instance Controller (`core/scrcpy_controller.py`)**: Converted process management to a dictionary structure, enabling multiple simultaneous Scrcpy windows for different connected devices.
- **Explicit Target Selector (`ui/main_window.py`)**: Added "Active Device Target" selector dropdown to resolve device-switching conflicts when multiple phones are connected.
- **Resolution & Video Scaling (`ui/main_window.py`)**: Added resolution limits (`--max-size`), bitrate limits (`--video-bit-rate`), and frame rate caps (`--max-fps`) to save bandwidth and system resources during multi-window streaming.
- **Multi-Device Toolbar Controls (`ui/visual_toolbar.py`)**: Added device targeting dropdown and "Broadcast Action to All Devices" toggle to control specific or all mirrored devices simultaneously.
- **"Launch All Devices" Action**: Added single-click action to open mirrored windows for every connected device at once.

### Fixed
- **Device Switching Bug**: Resolved issue where Scrcpy defaulted to ADB device index 0 instead of the user's selected Wi-Fi target.

## [v1.1.0] - 2026-09-28 - Feedback Updates & Wireless Pairing Engine (Au79)

### Added
- **Android 11+ Wireless Pairing**: Added `pair_wifi()` in `core/adb_wrapper.py` and pairing UI fields (Pairing Port & 6-Digit Code) in `ui/main_window.py`.
- **Wireless Auto-Save**: Implemented automatic profile persistence for wireless connections (`IP:Port`) into `config.json` upon successful attach or manual connection.
- **Explicit Save Button**: Added "?? Save Profile" button in the dashboard for manual IP profile saving.

### Changed
- **Renamed Desktop Mode**: Changed UI toggle label from "Pixel Desktop Mode" to "Secondary Display / Desktop Mode" to reflect universal multi-display compatibility across Samsung OneUI, Motorola Smart Connect, and Pixel devices.
- **Device Log Categorization**: Updated `main.py` daemon listener to distinguish between "Wireless Device Attached" and "USB Device Attached".

## [v1.0.3] - 2026-09-28 - Drop Shadow API Fix (Au79)

### Fixed
- **`ui/visual_toolbar.py`**: Corrected `QGraphicsDropShadowEffect` method call from `setOffsetY()` to `setYOffset()` to align with PySide6 API specifications.

## [v1.0.2] - 2026-09-28 - PySide6 Import Bugfix (Au79)

### Fixed
- **`ui/main_window.py`**: Corrected PySide6 import from `QSlot` to `Slot` to ensure Qt signal-slot bindings function properly across Python 3.10 environments.

## [v1.0.1] - 2026-09-28 - Syntax Bugfix (Au79)

### Fixed
- **`utils/config_manager.py`**: Fixed a syntax error in `get_saved_devices()` method signature by removing an extra opening parenthesis.

## [v1.0.0] - 2026-09-28 - Full Initial Release (Au79)

### Added
- **`utils/config_manager.py`**: Created JSON persistence layer for saving Wi-Fi connection profiles, device aliases, and user preferences.
- **`core/adb_wrapper.py`**: Built background ADB interface with zero-CLI popup window suppression (`CREATE_NO_WINDOW`), supporting device enumeration, mDNS network discovery, and input keyevent execution.
- **`core/scrcpy_controller.py`**: Built Scrcpy process lifecycle controller, including support for Pixel Desktop Environment flags (`--new-display=1920x1080/210`).
- **`core/auto_reconnect.py`**: Implemented background `QThread` auto-reconnect daemon to track USB device status and trigger automatic session re-attaches (F-01).
- **`ui/visual_toolbar.py`**: Created floating PySide6 overlay toolbar for visual shortcuts (Home, Back, Rotate, Screen Off, Volume Up/Down) (F-03).
- **`ui/main_window.py`**: Designed unified PySide6 GUI dashboard featuring Wi-Fi Quick-Connect, mDNS network scanner, Desktop Mode toggle switch, and live visual log console (F-02, F-04).
- **`main.py`**: Created application entry point with signal wiring and graceful subprocess termination on window exit.