@echo off
TITLE EasyScrcpy Launcher

:: 1. Force the script to look inside its own folder
cd /d "%~dp0"

:: 2. Launch the program detached from this console using pythonw (silent Python)
start "" pythonw main.py

:: 3. Instantly close this black command prompt window
exit