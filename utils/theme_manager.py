# ==============================================================================
# EasyScrcpy Custom Launcher
# Copyright (c) 2026 Au79
#
# Licensed under the MIT License.
# ==============================================================================

class ThemeManager:
    """Manages color palettes and QSS stylesheets across the application."""
    
    PALETTES = {
        "Catppuccin Dark": {
            "bg_main": "#1e1e2e",
            "bg_card": "#262637",
            "bg_input": "#313244",
            "bg_console": "#11111b",
            "accent": "#89b4fa",
            "accent_hover": "#b4befe",
            "text_main": "#cdd6f4",
            "text_muted": "#a6adc8",
            "text_console": "#a6adc8",
            "border": "#45475a",
            "btn_text": "#11111b",
            "btn_green": "#a6e3a1",
            "btn_blue": "#89dceb",
            "btn_red": "#f38ba8",
            "btn_yellow": "#f9e2af",
            "btn_purple": "#cba6f7",
        },
        "Clean Light": {
            "bg_main": "#f8f9fa",
            "bg_card": "#ffffff",
            "bg_input": "#e9ecef",
            "bg_console": "#1e293b",
            "accent": "#2563eb",
            "accent_hover": "#1d4ed8",
            "text_main": "#0f172a",
            "text_muted": "#64748b",
            "text_console": "#38bdf8",
            "border": "#cbd5e1",
            "btn_text": "#ffffff",
            "btn_green": "#16a34a",
            "btn_blue": "#0284c7",
            "btn_red": "#dc2626",
            "btn_yellow": "#d97706",
            "btn_purple": "#9333ea",
        },
        "Nord Slate": {
            "bg_main": "#2e3440",
            "bg_card": "#3b4252",
            "bg_input": "#434c5e",
            "bg_console": "#242933",
            "accent": "#88c0d0",
            "accent_hover": "#81a1c1",
            "text_main": "#eceff4",
            "text_muted": "#d8dee9",
            "text_console": "#a3be8c",
            "border": "#4c566a",
            "btn_text": "#2e3440",
            "btn_green": "#a3be8c",
            "btn_blue": "#81a1c1",
            "btn_red": "#bf616a",
            "btn_yellow": "#ebcb8b",
            "btn_purple": "#b48ead",
        },
        "Dracula / Purple": {
            "bg_main": "#282a36",
            "bg_card": "#343746",
            "bg_input": "#44475a",
            "bg_console": "#191a21",
            "accent": "#bd93f9",
            "accent_hover": "#d6acff",
            "text_main": "#f8f8f2",
            "text_muted": "#6272a4",
            "text_console": "#50fa7b",
            "border": "#6272a4",
            "btn_text": "#282a36",
            "btn_green": "#50fa7b",
            "btn_blue": "#8be9fd",
            "btn_red": "#ff5555",
            "btn_yellow": "#f1fa8c",
            "btn_purple": "#ff79c6",
        },
        "Emerald Night": {
            "bg_main": "#0d1b1e",
            "bg_card": "#162a2d",
            "bg_input": "#203a3e",
            "bg_console": "#070f11",
            "accent": "#2ec4b6",
            "accent_hover": "#3ab0a2",
            "text_main": "#e0f2f1",
            "text_muted": "#80cbc4",
            "text_console": "#2ec4b6",
            "border": "#2c5257",
            "btn_text": "#0d1b1e",
            "btn_green": "#2ec4b6",
            "btn_blue": "#70e0d6",
            "btn_red": "#e63946",
            "btn_yellow": "#ffb703",
            "btn_purple": "#a2d2ff",
        }
    }

    @classmethod
    def get_theme_names(cls) -> list:
        return list(cls.PALETTES.keys())

    @classmethod
    def get_main_window_qss(cls, theme_name: str) -> str:
        p = cls.PALETTES.get(theme_name, cls.PALETTES["Catppuccin Dark"])
        return f"""
            QMainWindow {{
                background-color: {p['bg_main']};
            }}
            QLabel {{
                color: {p['text_main']};
                font-size: 13px;
            }}
            QGroupBox {{
                color: {p['accent']};
                font-weight: bold;
                background-color: {p['bg_card']};
                border: 1px solid {p['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QPushButton {{
                background-color: {p['accent']};
                color: {p['btn_text']};
                font-weight: bold;
                border-radius: 6px;
                padding: 8px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {p['accent_hover']};
            }}
            QLineEdit, QComboBox {{
                background-color: {p['bg_input']};
                color: {p['text_main']};
                border: 1px solid {p['border']};
                border-radius: 6px;
                padding: 6px;
            }}
            QTextEdit {{
                background-color: {p['bg_console']};
                color: {p['text_console']};
                border: 1px solid {p['border']};
                border-radius: 6px;
                font-family: Consolas, monospace;
            }}
            QCheckBox {{
                color: {p['text_main']};
            }}
        """

    @classmethod
    def get_toolbar_qss(cls, theme_name: str) -> str:
        p = cls.PALETTES.get(theme_name, cls.PALETTES["Catppuccin Dark"])
        return f"""
            QWidget#ToolbarContainer {{
                background-color: {p['bg_main']};
                border-radius: 12px;
                border: 1px solid {p['border']};
            }}
            QLabel {{
                color: {p['text_main']};
                font-weight: bold;
                font-size: 11px;
            }}
            QComboBox {{
                background-color: {p['bg_input']};
                color: {p['text_main']};
                border: 1px solid {p['border']};
                border-radius: 4px;
                padding: 4px;
            }}
            QPushButton {{
                background-color: {p['bg_input']};
                color: {p['text_main']};
                border: none;
                padding: 6px 10px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {p['border']};
            }}
            QPushButton:pressed {{
                background-color: {p['accent']};
                color: {p['btn_text']};
            }}
            QCheckBox {{
                color: {p['accent']};
                font-weight: bold;
                font-size: 11px;
            }}
        """

    @classmethod
    def get_palette_dict(cls, theme_name: str) -> dict:
        return cls.PALETTES.get(theme_name, cls.PALETTES["Catppuccin Dark"])
