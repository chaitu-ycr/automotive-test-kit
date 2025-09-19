@echo off
setlocal

REM ============================
REM Build All Packages
REM ============================

REM Move to script directory and then project root
pushd %~dp0
cd ..

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    popd
    pause
    exit /b 1
)

REM Check if uv is installed
python -m uv --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo uv is not installed. Please install it with: python -m pip install uv
    popd
    pause
    exit /b 1
)

REM Build the All Packages
uv build --all-packages
if %ERRORLEVEL% NEQ 0 (
    echo Failed to Build the All Packages.
    popd
    pause
    exit /b 1
)

echo All packages built successfully.
popd
endlocal
goto :EOF