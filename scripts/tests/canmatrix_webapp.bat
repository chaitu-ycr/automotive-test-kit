@echo off
setlocal

REM ============================
REM Run canmatrix_webapp package Pytests with Reports
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
uv build --package canmatrix_webapp
if %ERRORLEVEL% NEQ 0 (
    echo Failed to Build the Package.
    popd
    pause
    exit /b 1
)

REM Run Pytest with Reports
uv run pytest packages/canmatrix_webapp/tests/ ^
    --html=packages/canmatrix_webapp/tests/report/test_reports/full_test_report.html --self-contained-html ^
    --cov=src ^
    --cov-report=html:packages/canmatrix_webapp/tests/report/cov/htmlcov ^
    --cov-report=xml:packages/canmatrix_webapp/tests/report/cov/coverage.xml ^
    --cov-report=json:packages/canmatrix_webapp/tests/report/cov/coverage.json ^
    --maxfail=5 ^
    --tb=short ^
    -n auto
if %ERRORLEVEL% NEQ 0 (
    echo Failed to Build the Package.
    popd
    pause
    exit /b 1
)

echo Tests executed successfully. Reports generated in packages/canmatrix_webapp/tests/report/
popd
endlocal
goto :EOF
