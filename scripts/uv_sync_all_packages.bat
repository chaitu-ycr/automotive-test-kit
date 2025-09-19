@echo off
setlocal

REM ============================
REM sync all packages dependencies and create/update venv
REM ============================

title syncing all packages dependencies and create/update venv ...

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

REM Sync all dependencies using uv
uv sync --all-packages --link-mode=copy
if %ERRORLEVEL% NEQ 0 (
    echo Failed to sync dependencies with uv.
    popd
    pause
    exit /b 1
)

echo Completed sync.
popd
endlocal
goto :EOF
