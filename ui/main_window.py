# ==============================================================================
# EasyScrcpy Custom Launcher
# Copyright (c) 2026 Au79
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QCheckBox, QTextEdit, QGroupBox, QMessageBox
)

from utils.theme_manager import ThemeManager

class MainWindow(QMainWindow):
    """Primary User Dashboard for EasyScrcpy supporting Multi-Device, Gamepad Control, & Color Themes."""
    
    theme_changed = Signal(str)

    def __init__(self, config_mgr, adb, scrcpy_ctrl):
        super().__init__()
        self.cfg = config_mgr
        self.adb = adb
        self.scrcpy = scrcpy_ctrl

        self.setWindowTitle("EasyScrcpy Multi-Device & Gamepad Hub")
        self.resize(760, 700)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Header Title, Theme Selector & Status Badge
        header_layout = QHBoxLayout()
        title_label = QLabel("🎮 EasyScrcpy Multi-Device Hub")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # Color Palette Dropdown Selector
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        header_layout.addWidget(QLabel("🎨 Theme:"))
        self.combo_theme = QComboBox()
        for theme_name in ThemeManager.get_theme_names():
            self.combo_theme.addItem(theme_name)
        
        saved_theme = self.cfg.get_preference("theme", "Catppuccin Dark")
        idx = self.combo_theme.findText(saved_theme)
        if idx >= 0:
            self.combo_theme.setCurrentIndex(idx)

        self.combo_theme.currentTextChanged.connect(self.on_theme_changed)
        header_layout.addWidget(self.combo_theme)

        self.status_badge = QLabel("● Disconnected")
        self.status_badge.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(self.status_badge)
        main_layout.addLayout(header_layout)

        # Active ADB Connected Devices Row (Target Switcher)
        target_group = QGroupBox("Active Connected Phone Switcher")
        target_layout = QHBoxLayout(target_group)
        target_layout.addWidget(QLabel("Target Phone:"))
        self.active_device_combo = QComboBox()
        target_layout.addWidget(self.active_device_combo, stretch=2)

        self.btn_refresh_devices = QPushButton("🔄 Refresh List")
        self.btn_refresh_devices.clicked.connect(self.refresh_active_devices)
        target_layout.addWidget(self.btn_refresh_devices)
        main_layout.addWidget(target_group)

        # Wi-Fi Connection & Pairing Section
        wifi_group = QGroupBox("Wi-Fi Connection & Pairing Manager")
        wifi_layout = QVBoxLayout(wifi_group)

        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("Saved Profile:"))
        self.device_combo = QComboBox()
        self.update_saved_devices_combo()
        profile_layout.addWidget(self.device_combo, stretch=2)

        self.btn_connect_saved = QPushButton("⚡ One-Click Connect")
        self.btn_connect_saved.clicked.connect(self.on_connect_saved_clicked)
        profile_layout.addWidget(self.btn_connect_saved)
        wifi_layout.addLayout(profile_layout)

        manual_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Phone IP:Port (e.g. 192.168.1.210:5555)")
        self.alias_input = QLineEdit()
        self.alias_input.setPlaceholderText("Alias (e.g. Moto Gaming Phone)")
        
        self.btn_direct_connect = QPushButton("🔌 Connect")
        self.btn_direct_connect.clicked.connect(self.on_direct_connect_clicked)

        self.btn_save_profile = QPushButton("💾 Save Profile")
        self.btn_save_profile.clicked.connect(self.on_save_profile_clicked)

        manual_layout.addWidget(self.ip_input, stretch=2)
        manual_layout.addWidget(self.alias_input, stretch=1)
        manual_layout.addWidget(self.btn_direct_connect)
        manual_layout.addWidget(self.btn_save_profile)
        wifi_layout.addLayout(manual_layout)

        pairing_layout = QHBoxLayout()
        self.pair_port_input = QLineEdit()
        self.pair_port_input.setPlaceholderText("Pairing Port")
        self.pair_code_input = QLineEdit()
        self.pair_code_input.setPlaceholderText("6-Digit Code")

        self.btn_pair = QPushButton("🔑 Pair Device")
        self.btn_pair.clicked.connect(self.on_pair_clicked)

        self.btn_scan = QPushButton("🔍 Scan Network")
        self.btn_scan.clicked.connect(self.on_scan_clicked)

        pairing_layout.addWidget(self.pair_port_input, stretch=1)
        pairing_layout.addWidget(self.pair_code_input, stretch=1)
        pairing_layout.addWidget(self.btn_pair)
        pairing_layout.addWidget(self.btn_scan)
        wifi_layout.addLayout(pairing_layout)

        main_layout.addWidget(wifi_group)

        # Gamepad Controller Passthrough Engine Section
        gamepad_group = QGroupBox("🎮 PC Gamepad / Controller Forwarding Engine")
        gamepad_layout = QHBoxLayout(gamepad_group)

        gamepad_layout.addWidget(QLabel("Gamepad Mode:"))
        self.combo_gamepad = QComboBox()
        self.combo_gamepad.addItem("UHID Emulation (Kernel - Best Compatibility)", "uhid")
        self.combo_gamepad.addItem("AOA (Android Open Accessory Mode)", "aoa")
        self.combo_gamepad.addItem("Disabled", "disabled")
        self.combo_gamepad.setCurrentIndex(0)
        gamepad_layout.addWidget(self.combo_gamepad, stretch=2)

        info_label = QLabel("Natively forwards connected PC controllers to phone")
        info_label.setStyleSheet("font-style: italic; font-size: 11px;")
        gamepad_layout.addWidget(info_label)
        main_layout.addWidget(gamepad_group)

        # Resolution & Display Engine Section
        video_group = QGroupBox("Display Resolution & Video Performance Controls")
        video_layout = QHBoxLayout(video_group)

        video_layout.addWidget(QLabel("Max Res:"))
        self.combo_resolution = QComboBox()
        self.combo_resolution.addItem("Native (Full)", 0)
        self.combo_resolution.addItem("1080p", 1080)
        self.combo_resolution.addItem("720p (Recommended)", 720)
        self.combo_resolution.addItem("540p", 540)
        self.combo_resolution.setCurrentIndex(2)
        video_layout.addWidget(self.combo_resolution)

        video_layout.addWidget(QLabel("Bitrate:"))
        self.combo_bitrate = QComboBox()
        self.combo_bitrate.addItem("4 Mbps (Default)", "4M")
        self.combo_bitrate.addItem("8 Mbps (High Quality)", "8M")
        self.combo_bitrate.addItem("2 Mbps (Fast Multi-Stream)", "2M")
        video_layout.addWidget(self.combo_bitrate)

        video_layout.addWidget(QLabel("FPS Cap:"))
        self.combo_fps = QComboBox()
        self.combo_fps.addItem("60 FPS", 60)
        self.combo_fps.addItem("30 FPS", 30)
        self.combo_fps.addItem("Uncapped", 0)
        video_layout.addWidget(self.combo_fps)

        main_layout.addWidget(video_group)

        # Mode Toggles
        mode_group = QGroupBox("Display Mode Options")
        mode_layout = QHBoxLayout(mode_group)
        self.chk_desktop_mode = QCheckBox("🖥️ Secondary Display / Desktop Mode (--new-display=1920x1080/210)")
        self.chk_desktop_mode.setChecked(self.cfg.get_preference("desktop_mode", False))
        self.chk_desktop_mode.toggled.connect(lambda v: self.cfg.set_preference("desktop_mode", v))

        self.chk_auto_reconnect = QCheckBox("🔄 USB Auto-Reconnect")
        self.chk_auto_reconnect.setChecked(self.cfg.get_preference("auto_reconnect", True))
        self.chk_auto_reconnect.toggled.connect(lambda v: self.cfg.set_preference("auto_reconnect", v))

        mode_layout.addWidget(self.chk_desktop_mode)
        mode_layout.addWidget(self.chk_auto_reconnect)
        main_layout.addWidget(mode_group)

        # Multi-Window Action Buttons
        action_layout = QHBoxLayout()
        self.btn_launch_target = QPushButton("▶ Launch Target Phone")
        self.btn_launch_target.clicked.connect(self.on_launch_target_clicked)

        self.btn_launch_all = QPushButton("🚀 Launch ALL Phones")
        self.btn_launch_all.clicked.connect(self.on_launch_all_clicked)

        self.btn_stop = QPushButton("⏹ Stop Selected")
        self.btn_stop.clicked.connect(self.on_stop_clicked)

        self.btn_toolbar = QPushButton("🛠 Floating Toolbar")

        action_layout.addWidget(self.btn_launch_target)
        action_layout.addWidget(self.btn_launch_all)
        action_layout.addWidget(self.btn_stop)
        action_layout.addWidget(self.btn_toolbar)
        main_layout.addLayout(action_layout)

        # Console Output
        main_layout.addWidget(QLabel("Activity Log:"))
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        main_layout.addWidget(self.log_console)

        self.setCentralWidget(central_widget)
        
        # Apply Saved Palette & Initial State
        self.apply_theme(saved_theme)
        self.refresh_active_devices()

    def apply_theme(self, theme_name: str):
        """Re-styles the window dynamically based on chosen color palette."""
        self.setStyleSheet(ThemeManager.get_main_window_qss(theme_name))
        p = ThemeManager.get_palette_dict(theme_name)

        # Apply specific dynamic highlight colors to action buttons
        self.btn_launch_target.setStyleSheet(f"background-color: {p['btn_green']}; color: {p['btn_text']}; font-size: 14px; padding: 10px; font-weight: bold;")
        self.btn_launch_all.setStyleSheet(f"background-color: {p['btn_blue']}; color: {p['btn_text']}; font-size: 14px; padding: 10px; font-weight: bold;")
        self.btn_stop.setStyleSheet(f"background-color: {p['btn_red']}; color: {p['btn_text']}; font-size: 14px; padding: 10px; font-weight: bold;")
        self.btn_toolbar.setStyleSheet(f"background-color: {p['btn_yellow']}; color: {p['btn_text']}; font-size: 14px; padding: 10px; font-weight: bold;")
        self.btn_save_profile.setStyleSheet(f"background-color: {p['btn_yellow']}; color: {p['btn_text']}; font-weight: bold;")
        self.btn_pair.setStyleSheet(f"background-color: {p['btn_purple']}; color: {p['btn_text']}; font-weight: bold;")

    @Slot(str)
    def on_theme_changed(self, theme_name: str):
        self.cfg.set_preference("theme", theme_name)
        self.apply_theme(theme_name)
        self.theme_changed.emit(theme_name)
        self.log(f"Color theme changed to: '{theme_name}'")

    def log(self, message: str):
        self.log_console.append(f"> {message}")

    def update_saved_devices_combo(self):
        self.device_combo.clear()
        devices = self.cfg.get_saved_devices()
        for dev in devices:
            port = dev.get("port", 5555)
            self.device_combo.addItem(f"{dev['alias']} ({dev['ip']}:{port})", f"{dev['ip']}:{port}")

    def refresh_active_devices(self):
        self.active_device_combo.clear()
        devices = self.adb.get_connected_devices()
        current_theme = self.combo_theme.currentText()
        p = ThemeManager.get_palette_dict(current_theme)

        if devices:
            for dev in devices:
                self.active_device_combo.addItem(f"📱 {dev['serial']} ({dev['state']})", dev["serial"])
            self.status_badge.setText(f"● {len(devices)} Device(s) Connected")
            self.status_badge.setStyleSheet(f"color: {p['btn_green']}; font-weight: bold;")
        else:
            self.active_device_combo.addItem("No active ADB devices detected", "")
            self.status_badge.setText("● Disconnected")
            self.status_badge.setStyleSheet(f"color: {p['btn_red']}; font-weight: bold;")

    @Slot()
    def on_connect_saved_clicked(self):
        target = self.device_combo.currentData()
        if not target:
            QMessageBox.warning(self, "Warning", "No saved profile selected.")
            return
        self.log(f"Connecting to saved target: {target}...")
        ok, msg = self.adb.connect_wifi(target)
        self.log(msg)
        self.refresh_active_devices()

    @Slot()
    def on_direct_connect_clicked(self):
        raw_ip = self.ip_input.text().strip()
        alias = self.alias_input.text().strip() or "Wireless Phone"
        if not raw_ip:
            QMessageBox.warning(self, "Warning", "Enter a valid IP or IP:Port.")
            return

        self.log(f"Connecting to {raw_ip}...")
        ok, msg = self.adb.connect_wifi(raw_ip)
        self.log(msg)
        if ok:
            parts = raw_ip.split(":")
            ip = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 5555
            self.cfg.add_saved_device(alias, ip, port)
            self.update_saved_devices_combo()
            self.log(f"Saved device profile: '{alias}' ({raw_ip})")
        self.refresh_active_devices()

    @Slot()
    def on_save_profile_clicked(self):
        raw_ip = self.ip_input.text().strip()
        alias = self.alias_input.text().strip() or "Wireless Phone"
        if not raw_ip:
            QMessageBox.warning(self, "Warning", "Please enter an IP address.")
            return

        parts = raw_ip.split(":")
        ip = parts[0]
        port = int(parts[1]) if len(parts) > 1 else 5555
        self.cfg.add_saved_device(alias, ip, port)
        self.update_saved_devices_combo()
        self.log(f"Saved profile: '{alias}' -> {ip}:{port}")

    @Slot()
    def on_pair_clicked(self):
        raw_ip = self.ip_input.text().strip().split(":")[0]
        pair_port = self.pair_port_input.text().strip()
        pair_code = self.pair_code_input.text().strip()

        if not raw_ip or not pair_port or not pair_code:
            QMessageBox.warning(self, "Warning", "Enter Phone IP, Pairing Port, and 6-Digit Code.")
            return

        self.log(f"Pairing with {raw_ip}:{pair_port}...")
        ok, msg = self.adb.pair_wifi(raw_ip, int(pair_port), pair_code)
        self.log(msg)

    @Slot()
    def on_scan_clicked(self):
        self.log("Scanning local network for active wireless ADB instances...")
        found = self.adb.scan_mdns()
        if found:
            self.log(f"Discovered wireless devices: {found}")
            first = found[0]
            self.ip_input.setText(f"{first['ip']}:{first['port']}")
        else:
            self.log("No mDNS broadcast endpoints detected on local subnet.")

    @Slot()
    def on_launch_target_clicked(self):
        serial = self.active_device_combo.currentData()
        if not serial:
            QMessageBox.warning(self, "Warning", "No target phone selected from active list.")
            return

        ok, msg = self.scrcpy.launch(
            serial=serial,
            desktop_mode=self.chk_desktop_mode.isChecked(),
            max_size=self.combo_resolution.currentData(),
            bitrate=self.combo_bitrate.currentData(),
            max_fps=self.combo_fps.currentData(),
            gamepad_mode=self.combo_gamepad.currentData()
        )
        self.log(msg)

    @Slot()
    def on_launch_all_clicked(self):
        devices = self.adb.get_connected_devices()
        if not devices:
            QMessageBox.warning(self, "Warning", "No active connected devices to launch.")
            return

        for dev in devices:
            serial = dev["serial"]
            ok, msg = self.scrcpy.launch(
                serial=serial,
                desktop_mode=self.chk_desktop_mode.isChecked(),
                max_size=self.combo_resolution.currentData(),
                bitrate=self.combo_bitrate.currentData(),
                max_fps=self.combo_fps.currentData(),
                gamepad_mode=self.combo_gamepad.currentData()
            )
            self.log(msg)

    @Slot()
    def on_stop_clicked(self):
        serial = self.active_device_combo.currentData()
        self.scrcpy.stop(serial)
        self.log(f"Stopped session for target: {serial or 'All'}")