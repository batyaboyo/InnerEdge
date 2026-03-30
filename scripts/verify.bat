@echo off
setlocal enabledelayedexpansion

set ROOT_DIR=%~dp0..
set PYTHON_EXE=%ROOT_DIR%\.venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
  echo Python venv executable not found at: %PYTHON_EXE%
  echo Run setup first or adjust the script for your environment.
  exit /b 1
)

echo [1/3] Running backend tests
"%PYTHON_EXE%" -m pytest -q
if errorlevel 1 exit /b 1

echo [2/3] Running frontend verify
cd /d "%ROOT_DIR%\frontend"
call npm run verify
if errorlevel 1 exit /b 1

echo [3/3] Verification complete
exit /b 0
