# ==============================================================================
# EasyScrcpy Custom Launcher
# Copyright (c) 2026 Au79
#
# Licensed under the MIT License.
# ==============================================================================
import sys
from PySide6.QtWidgets import QApplication

from utils.config_manager import ConfigManager
from core.adb_wrapper import ADBWrapper
from core.scrcpy_controller import ScrcpyController
from core.auto_reconnect import AutoReconnectWorker
from ui.main_window import MainWindow
from ui.visual_toolbar import VisualToolbar

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("EasyScrcpy")

    # Initialize Backend Modules
    cfg = ConfigManager("config.json")
    adb = ADBWrapper(bin_dir=cfg.get_preference("bin_path", "./bin"))
    scrcpy_ctrl = ScrcpyController(bin_dir=cfg.get_preference("bin_path", "./bin"))

    # Initialize Interfaces
    window = MainWindow(cfg, adb, scrcpy_ctrl)
    toolbar = VisualToolbar()

    # Apply saved theme to floating toolbar & connect dynamic switcher
    initial_theme = cfg.get_preference("theme", "Catppuccin Dark")
    toolbar.apply_theme(initial_theme)
    window.theme_changed.connect(toolbar.apply_theme)

    # Position Floating Toolbar Initially at Top-Right Anchor
    toolbar.reset_to_default_position()

    # Wire Visual Toolbar Sync & Toggle
    def toggle_toolbar():
        if toolbar.isHidden():
            devices = adb.get_connected_devices()
            toolbar.update_device_list(devices)
            toolbar.show()
        else:
            toolbar.hide()

    window.btn_toolbar.clicked.connect(toggle_toolbar)

    # Wire Toolbar Shortcut Actions to Targeted ADB Execution
    def handle_toolbar_action(action: str, target: str, is_broadcast: bool):
        devices = adb.get_connected_devices()
        active_serials = [d["serial"] for d in devices]

        if not active_serials:
            window.log("Toolbar action ignored: No connected devices.")
            return

        targets_to_send = active_serials if (is_broadcast or target == "ALL") else [target]

        keymap = {
            "home": 3,
            "back": 4,
            "vol_up": 24,
            "vol_down": 25,
            "screen_off": 223
        }

        for s in targets_to_send:
            if s in active_serials:
                if action in keymap:
                    adb.send_keyevent(s, keymap[action])
                elif action == "rotate":
                    window.log(f"Screen rotation requested for device [{s}].")

    toolbar.action_triggered.connect(handle_toolbar_action)

    # Auto-Reconnect Daemon Thread Wiring
    auto_worker = AutoReconnectWorker(adb)

    def on_device_attached(serial):
        if ":" in serial:
            window.log(f"Wireless Device Attached: {serial}")
            parts = serial.split(":")
            cfg.add_saved_device("Wireless Phone", parts[0], int(parts[1]))
            window.update_saved_devices_combo()
        else:
            window.log(f"USB Device Attached: {serial}")

        window.refresh_active_devices()
        toolbar.update_device_list(adb.get_connected_devices())

        # USB Auto-launch if single device attached
        if not ":" in serial and cfg.get_preference("auto_reconnect", True) and not scrcpy_ctrl.is_running(serial):
            window.log(f"Auto-launching session for attached device [{serial}]...")
            scrcpy_ctrl.launch(
                serial=serial,
                desktop_mode=cfg.get_preference("desktop_mode", False),
                max_size=window.combo_resolution.currentData(),
                bitrate=window.combo_bitrate.currentData(),
                max_fps=window.combo_fps.currentData(),
                gamepad_mode=window.combo_gamepad.currentData()
            )

    def on_device_detached(serial):
        conn_type = "Wireless" if ":" in serial else "USB"
        window.log(f"{conn_type} Device Detached: {serial}")
        window.refresh_active_devices()
        toolbar.update_device_list(adb.get_connected_devices())

    auto_worker.device_attached.connect(on_device_attached)
    auto_worker.device_detached.connect(on_device_detached)
    auto_worker.start()

    window.show()

    # Clean subprocess termination on quit
    def cleanup():
        auto_worker.stop()
        scrcpy_ctrl.stop()

    app.aboutToQuit.connect(cleanup)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
