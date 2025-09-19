@echo off
setlocal

REM ============================
REM Build py_uds_demo Package
REM ============================

REM Move to script directory and then project root
pushd %~dp0
cd ../..

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

REM Build the Package
uv build --package py_uds_demo
if %ERRORLEVEL% NEQ 0 (
    echo Failed to Build the Package.
    popd
    pause
    exit /b 1
)

echo Package built successfully.
popd
endlocal
goto :EOF