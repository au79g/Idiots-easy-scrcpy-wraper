@echo off
TITLE EasyScrcpy - First Time Setup Engine
:: ==============================================================================
:: EasyScrcpy Automated Windows Environment Installer
:: Copyright (c) 2026 Au79
:: ==============================================================================

echo ====================================================================
echo                   EasyScrcpy - Setup Engine
echo ====================================================================
echo.

:: 1. Check Python Availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found on this system!
    echo.
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo IMPORTANT: Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

echo [1/5] Python installation detected.
echo.

:: 2. Upgrade pip and Install Dependencies
echo [2/5] Installing required Python packages (PySide6)...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies. Check internet connection.
    pause
    exit /b
)
echo.

:: 3. Prepare Bin Directory
echo [3/5] Setting up local bin directory...
if not exist "bin" mkdir bin

:: 4. Download and Extract scrcpy Binaries dynamically
echo [4/5] Fetching scrcpy binaries from GitHub releases...
set "SCRCPY_URL=https://github.com/Genymobile/scrcpy/releases/download/v2.4/scrcpy-win64-v2.4.zip"
set "ZIP_PATH=%TEMP%\scrcpy_temp.zip"
set "EXTRACT_PATH=%TEMP%\scrcpy_extracted"

powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Write-Host 'Downloading scrcpy...'; Invoke-WebRequest -Uri '%SCRCPY_URL%' -OutFile '%ZIP_PATH%'"

if exist "%ZIP_PATH%" (
    echo Extracting binaries into local ./bin folder...
    powershell -Command "Expand-Archive -Path '%ZIP_PATH%' -DestinationPath '%EXTRACT_PATH%' -Force"
    
    :: Move contents of subfolder directly into ./bin/
    for /d %%D in ("%EXTRACT_PATH%\scrcpy-win64*") do (
        xcopy "%%D\*" "bin\" /E /Y /Q >nul
    )
    
    :: Cleanup Temp Files
    del /f /q "%ZIP_PATH%"
    rd /s /q "%EXTRACT_PATH%"
    echo scrcpy binaries successfully deployed to ./bin/
) else (
    echo [WARNING] Could not download scrcpy binaries automatically.
    echo Please manually place adb.exe and scrcpy.exe into the bin/ folder.
)
echo.

:: 5. Create Desktop Shortcut for Non-Tech Users
echo [5/5] Creating EasyScrcpy Desktop Shortcut...
set "SCRIPT_DIR=%~dp0"
:: Strip trailing backslash for clean shortcut creation
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

set "BAT_PATH=%SCRIPT_DIR%\Run_EasyScrcpy.bat"
set "DESKTOP_DIR=%USERPROFILE%\Desktop"
set "SHORTCUT_PATH=%DESKTOP_DIR%\EasyScrcpy.lnk"

:: WindowStyle = 7 runs the batch file minimized so it doesn't flash on the screen
powershell -Command "$s = (New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%BAT_PATH%'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.WindowStyle = 7; $s.IconLocation = 'imageres.dll,109'; $s.Save()"

echo.
echo ====================================================================
echo Setup Completed Successfully!
echo A shortcut 'EasyScrcpy' has been created on your Desktop.
echo ====================================================================
echo.
pause