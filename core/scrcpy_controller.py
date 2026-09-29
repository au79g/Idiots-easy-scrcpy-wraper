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
import subprocess
import sys

class ScrcpyController:
    """Manages launching, configuring, and stopping multiple concurrent Scrcpy sessions with Gamepad Forwarding."""
    def __init__(self, bin_dir="./bin"):
        self.bin_dir = bin_dir
        self.scrcpy_path = self._find_scrcpy_binary()
        self.processes = {}

    def _find_scrcpy_binary(self) -> str:
        local_bin = os.path.join(self.bin_dir, "scrcpy.exe" if sys.platform == "win32" else "scrcpy")
        if os.path.exists(local_bin):
            return os.path.abspath(local_bin)
        return "scrcpy"

    def is_running(self, serial: str = None) -> bool:
        if serial:
            proc = self.processes.get(serial)
            return proc is not None and proc.poll() is None
        return any(proc.poll() is None for proc in self.processes.values())

    def launch(
        self,
        serial: str = None,
        desktop_mode: bool = False,
        max_size: int = None,
        bitrate: str = None,
        max_fps: int = None,
        gamepad_mode: str = "uhid",
        extra_flags: list = None
    ) -> tuple[bool, str]:
        target_serial = serial or "default"
        
        if self.is_running(target_serial):
            return False, f"Scrcpy session for device [{target_serial}] is already active."

        cmd = [self.scrcpy_path]

        if serial:
            cmd.extend(["-s", serial])
            cmd.extend(["--window-title", f"EasyScrcpy - {serial}"])

        # Display Mode Flag
        if desktop_mode:
            cmd.append("--new-display=1920x1080/210")

        # Resolution Scaling Engine Flags
        if max_size and max_size > 0:
            cmd.append(f"--max-size={max_size}")

        if bitrate:
            cmd.append(f"--video-bit-rate={bitrate}")

        if max_fps and max_fps > 0:
            cmd.append(f"--max-fps={max_fps}")

        # Gamepad / Controller Passthrough Flags
        if gamepad_mode in ["uhid", "aoa"]:
            cmd.append(f"--gamepad={gamepad_mode}")
        elif gamepad_mode == "disabled":
            cmd.append("--gamepad=disabled")

        if extra_flags:
            cmd.extend(extra_flags)

        kwargs = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = 0x08000000  # CREATE_NO_WINDOW

        try:
            proc = subprocess.Popen(cmd, **kwargs)
            self.processes[target_serial] = proc
            mode_str = "Secondary Display" if desktop_mode else "Standard Mirror"
            pad_str = f" | Gamepad: {gamepad_mode.upper()}" if gamepad_mode != "disabled" else ""
            return True, f"Started {mode_str} for [{target_serial}]{pad_str}"
        except Exception as e:
            return False, f"Failed to start Scrcpy for [{target_serial}]: {str(e)}"

    def stop(self, serial: str = None):
        if serial:
            proc = self.processes.get(serial)
            if proc and proc.poll() is None:
                try:
                    proc.terminate()
                    proc.wait(timeout=2)
                except Exception:
                    proc.kill()
            self.processes.pop(serial, None)
        else:
            for s, proc in list(self.processes.items()):
                if proc.poll() is None:
                    try:
                        proc.terminate()
                        proc.wait(timeout=1)
                    except Exception:
                        proc.kill()
            self.processes.clear()