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

import json
import os

DEFAULT_CONFIG = {
    "saved_devices": [
        {"alias": "Mom's Pixel", "ip": "192.168.1.100", "port": 5555}
    ],
    "last_connected_ip": "",
    "desktop_mode": False,
    "auto_reconnect": True,
    "bin_path": "./bin"
}

class ConfigManager:
    """Manages reading and writing saved Wi-Fi profiles and preferences in config.json."""
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CONFIG

    def save_config(self, data: dict = None):
        if data is not None:
            self.config = data
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get_saved_devices(self) -> list:
        return self.config.get("saved_devices", [])

    def add_saved_device(self, alias: str, ip: str, port: int = 5555):
        devices = self.get_saved_devices()
        # Update existing IP if alias/IP matches
        for dev in devices:
            if dev["ip"] == ip:
                dev["alias"] = alias
                dev["port"] = port
                self.save_config()
                return
        devices.append({"alias": alias, "ip": ip, "port": port})
        self.config["saved_devices"] = devices
        self.save_config()

    def remove_saved_device(self, ip: str):
        devices = [d for d in self.get_saved_devices() if d["ip"] != ip]
        self.config["saved_devices"] = devices
        self.save_config()

    def get_preference(self, key: str, default=None):
        return self.config.get(key, default)

    def set_preference(self, key: str, value):
        self.config[key] = value
        self.save_config()
