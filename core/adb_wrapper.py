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

import os
import re
import subprocess
import sys

class ADBWrapper:
    """Executes ADB commands with complete suppression of CLI window popups."""
    def __init__(self, bin_dir="./bin"):
        self.bin_dir = bin_dir
        self.adb_path = self._find_adb_binary()

    def _find_adb_binary(self) -> str:
        local_adb = os.path.join(self.bin_dir, "adb.exe" if sys.platform == "win32" else "adb")
        if os.path.exists(local_adb):
            return os.path.abspath(local_adb)
        return "adb"  # Fallback to system PATH

    def _run_cmd(self, args: list) -> tuple[int, str, str]:
        cmd = [self.adb_path] + args
        kwargs = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True
        }
        # Zero-CLI Rule: Hide command window on Windows
        if sys.platform == "win32":
            kwargs["creationflags"] = 0x08000000  # CREATE_NO_WINDOW

        try:
            proc = subprocess.run(cmd, **kwargs)
            return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
        except Exception as e:
            return -1, "", str(e)

    def get_connected_devices(self) -> list[dict]:
        """Returns list of connected ADB devices: [{'serial': '...', 'state': 'device'}]"""
        code, stdout, _ = self._run_cmd(["devices"])
        devices = []
        if code == 0 and stdout:
            lines = stdout.splitlines()[1:]  # Skip "List of devices attached"
            for line in lines:
                if line.strip():
                    parts = re.split(r'\s+', line.strip())
                    if len(parts) >= 2:
                        devices.append({"serial": parts[0], "state": parts[1]})
        return devices

    def pair_wifi(self, ip: str, port: int, code: str) -> tuple[bool, str]:
        """Pairs an Android 11+ device over Wi-Fi using pairing port and 6-digit code."""
        target = f"{ip}:{port}"
        returncode, stdout, stderr = self._run_cmd(["pair", target, str(code)])
        if "successfully paired" in stdout.lower() or "successfully paired" in stderr.lower():
            return True, f"Successfully paired with {target}"
        return False, stderr or stdout or f"Failed to pair with {target}"

    def connect_wifi(self, ip: str, port: int = 5555) -> tuple[bool, str]:
        """Connects to a paired wireless ADB endpoint."""
        target = f"{ip}:{port}" if ":" not in ip else ip
        code, stdout, stderr = self._run_cmd(["connect", target])
        if "connected to" in stdout.lower():
            return True, f"Successfully connected to {target}"
        return False, stderr or stdout or f"Failed to connect to {target}"

    def disconnect_wifi(self, ip: str) -> tuple[bool, str]:
        code, stdout, stderr = self._run_cmd(["disconnect", ip])
        return code == 0, stdout or stderr

    def scan_mdns(self) -> list[dict]:
        """Scans local network for wireless ADB services using adb mdns."""
        code, stdout, _ = self._run_cmd(["mdns", "services"])
        found = []
        if code == 0 and stdout:
            for line in stdout.splitlines():
                # Matches patterns like 'adb-123456 _adb-tls-connect._tcp. 192.168.1.50:37123'
                match = re.search(r'(\d+\.\d+\.\d+\.\d+):(\d+)', line)
                if match:
                    found.append({"ip": match.group(1), "port": int(match.group(2))})
        return found

    def send_keyevent(self, serial: str, keycode: int) -> bool:
        """Sends physical key events like Home (3), Back (4), Vol Up (24), Vol Down (25)."""
        args = ["-s", serial, "shell", "input", "keyevent", str(keycode)] if serial else ["shell", "input", "keyevent", str(keycode)]
        code, _, _ = self._run_cmd(args)
        return code == 0