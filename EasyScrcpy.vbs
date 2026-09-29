' ==============================================================================
' EasyScrcpy Silent Windows Launcher
' Launches main.py without spawning a command prompt window.
' ==============================================================================

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw main.py", 0, False