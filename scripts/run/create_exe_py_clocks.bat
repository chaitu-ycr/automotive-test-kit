@echo off
REM =============================================================================
REM Script: create_exe.bat
REM Purpose: Build a standalone executable.
REM
REM Requirements:
REM   - Python virtual environment in .venv
REM   - pyinstaller installed in .venv
REM
REM Usage:
REM   Double-click or run from command line.
REM =============================================================================

pushd %~dp0
cd ../..

REM --- Configuration ---
setlocal
set "VENV_PATH=.venv\Scripts"
set "PYTHON=%VENV_PATH%\python.exe"
set "PYINSTALLER=%VENV_PATH%\pyinstaller.exe"
set "MAIN_SCRIPT=packages\py_clocks\src\py_clocks\py_clocks.py"

REM --- Check virtual environment ---
if not exist "%PYTHON%" (
    echo [ERROR] Python virtual environment not found at "%VENV_PATH%".
    echo Please create a virtual environment using venv_setup.bat
    pause
    exit /b 1
)

REM --- Check PyInstaller installation ---
if not exist "%PYINSTALLER%" (
    echo [ERROR] PyInstaller not found at "%PYINSTALLER%".
    echo Please install PyInstaller in your virtual environment:
    echo     %PYTHON% -m pip install pyinstaller
    pause
    exit /b 2
)

REM --- Check main script existence ---
if not exist "%MAIN_SCRIPT%" (
    echo [ERROR] Main script "%MAIN_SCRIPT%" not found in current directory.
    pause
    exit /b 3
)

REM --- Build the executable ---
echo [INFO] Building executable using PyInstaller...
"%PYINSTALLER%" --onefile --noconsole "%MAIN_SCRIPT%"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create executable. PyInstaller exited with code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

REM --- Success message ---
echo.
echo [SUCCESS] Executable created successfully.
echo You can find the executable in the 'dist' directory.
echo.
echo To run the executable, use:
echo     dist\py_clocks.exe
echo.
exit /b
popd