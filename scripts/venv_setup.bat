@echo off
setlocal

REM Create or Update Python Virtual Environment
title Creating/Updating Tool Environment...

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

REM Upgrade pip and install uv
python -m pip install --upgrade pip uv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to upgrade pip or install uv.
    popd
    pause
    exit /b 1
)

REM create/update venv using uv
uv venv --allow-existing
if %ERRORLEVEL% NEQ 0 (
    echo Failed to sync dependencies with uv.
    popd
    pause
    exit /b 1
)

echo Completed venv creation.
popd
endlocal
goto :EOF
