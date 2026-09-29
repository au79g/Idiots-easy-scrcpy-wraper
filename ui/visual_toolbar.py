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

from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QComboBox, QCheckBox, QLabel,
    QGraphicsDropShadowEffect, QApplication
)
from PySide6.QtGui import QColor, QMouseEvent

from utils.theme_manager import ThemeManager

class VisualToolbar(QWidget):
    """Floating Visual Control Overlay with Click-and-Drag positioning & Color Theme Syncing."""
    action_triggered = Signal(str, str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._drag_position = QPoint()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        self.container = QWidget()
        self.container.setObjectName("ToolbarContainer")

        btn_layout = QHBoxLayout(self.container)

        # Drag Handle Indicator
        drag_label = QLabel("⣿")
        drag_label.setStyleSheet("font-size: 14px; padding-right: 4px;")
        drag_label.setToolTip("Click and drag here or anywhere on toolbar to move")
        btn_layout.addWidget(drag_label)

        # Multi-Device Target Selector Dropdown
        btn_layout.addWidget(QLabel("Target:"))
        self.target_combo = QComboBox()
        self.target_combo.addItem("🌐 All Devices", "ALL")
        btn_layout.addWidget(self.target_combo)

        # Broadcast Toggle Checkbox
        self.chk_broadcast = QCheckBox("Broadcast All")
        self.chk_broadcast.setToolTip("Send control actions to every connected phone simultaneously")
        btn_layout.addWidget(self.chk_broadcast)

        # Quick Control Buttons
        buttons = [
            ("🏠 Home", "home"),
            ("◀ Back", "back"),
            ("🔄 Rotate", "rotate"),
            ("💡 Screen Off", "screen_off"),
            ("🔊 Vol +", "vol_up"),
            ("🔉 Vol -", "vol_down"),
        ]

        for label, code in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, c=code: self._emit_action(c))
            btn_layout.addWidget(btn)

        # Reset Position Button
        self.btn_reset = QPushButton("🎯 Reset Pos")
        self.btn_reset.setToolTip("Reset floating toolbar to top-right screen anchor")
        self.btn_reset.clicked.connect(self.reset_to_default_position)
        btn_layout.addWidget(self.btn_reset)

        # Close toolbar button
        self.close_btn = QPushButton("✖")
        self.close_btn.clicked.connect(self.hide)
        btn_layout.addWidget(self.close_btn)

        layout.addWidget(self.container)
        self.setLayout(layout)

        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setYOffset(5)
        self.container.setGraphicsEffect(shadow)

    def apply_theme(self, theme_name: str):
        """Dynamic palette sync for the floating toolbar."""
        self.setStyleSheet(ThemeManager.get_toolbar_qss(theme_name))
        p = ThemeManager.get_palette_dict(theme_name)
        
        self.btn_reset.setStyleSheet(f"background-color: {p['btn_blue']}; color: {p['btn_text']}; font-weight: bold;")
        self.close_btn.setStyleSheet(f"background-color: {p['btn_red']}; color: {p['btn_text']}; font-weight: bold;")

    # Mouse Events for Smooth Window Dragging
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and not self._drag_position.isNull():
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_position = QPoint()

    def reset_to_default_position(self):
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 40
        y = 60
        self.move(x, y)

    def update_device_list(self, devices: list):
        current_target = self.target_combo.currentData()
        self.target_combo.clear()
        self.target_combo.addItem("🌐 All Devices", "ALL")
        for dev in devices:
            self.target_combo.addItem(f"📱 {dev['serial']}", dev["serial"])
        
        idx = self.target_combo.findData(current_target)
        if idx >= 0:
            self.target_combo.setCurrentIndex(idx)

    def _emit_action(self, action_code: str):
        target = self.target_combo.currentData()
        is_broadcast = self.chk_broadcast.isChecked() or target == "ALL"
        self.action_triggered.emit(action_code, target, is_broadcast)