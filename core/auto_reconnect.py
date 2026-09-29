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

import time
from PySide6.QtCore import QThread, Signal

class AutoReconnectWorker(QThread):
    """
    F-01: Background thread monitoring ADB devices.
    Emits signals when USB or wireless devices attach/detach.
    """
    device_attached = Signal(str)
    device_detached = Signal(str)
    status_changed = Signal(str)

    def __init__(self, adb_wrapper, poll_interval=2.0):
        super().__init__()
        self.adb = adb_wrapper
        self.poll_interval = poll_interval
        self._running = True
        self.known_devices = set()

    def run(self):
        while self._running:
            try:
                current_devices = self.adb.get_connected_devices()
                active_serials = {d["serial"] for d in current_devices if d["state"] == "device"}

                # New device connected
                for serial in active_serials - self.known_devices:
                    self.device_attached.emit(serial)

                # Device disconnected
                for serial in self.known_devices - active_serials:
                    self.device_detached.emit(serial)

                self.known_devices = active_serials
            except Exception as e:
                self.status_changed.emit(f"Auto-Reconnect error: {str(e)}")

            time.sleep(self.poll_interval)

    def stop(self):
        self._running = False
        self.wait()