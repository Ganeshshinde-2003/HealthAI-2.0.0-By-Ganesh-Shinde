@echo off
REM HealthAI - Start Backend & Frontend
REM This script starts both the Flask backend and Next.js frontend servers

setlocal enabledelayedexpansion

REM Colors setup (using basic ASCII art for Windows)
cls
echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║                                                       ║
echo ║     Starting HealthAI Backend ^& Frontend              ║
echo ║                                                       ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Get the root directory
set ROOT_DIR=%~dp0
set BACKEND_DIR=%ROOT_DIR%backend
set FRONTEND_DIR=%ROOT_DIR%frontend
set LOGS_DIR=%ROOT_DIR%logs

REM Check if directories exist
if not exist "%BACKEND_DIR%" (
  echo X Backend directory not found at %BACKEND_DIR%
  pause
  exit /b 1
)

if not exist "%FRONTEND_DIR%" (
  echo X Frontend directory not found at %FRONTEND_DIR%
  pause
  exit /b 1
)

REM Create logs directory
if not exist "%LOGS_DIR%" mkdir "%LOGS_DIR%"

REM Start Backend
echo [*] Starting Backend Server (with auto-reload)...
cd /d "%BACKEND_DIR%"

REM Check if virtual environment exists
if not exist "venv" (
  echo Creating virtual environment...
  python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update requirements
if exist "requirements.txt" (
  echo Installing backend dependencies...
  pip install -q -r requirements.txt
)

REM Start backend server in a new window
start "HealthAI Backend" cmd /k python run.py
echo [+] Backend started
echo     API: http://localhost:5000
echo     Restart manually to reload code changes

REM Wait a moment
timeout /t 2 /nobreak

REM Start Frontend
echo [*] Starting Frontend Server...
cd /d "%FRONTEND_DIR%"

REM Check if node_modules exists
if not exist "node_modules" (
  echo Installing frontend dependencies...
  call npm install --legacy-peer-deps
  if errorlevel 1 (
    call npm install
  )
)

REM Start frontend dev server in a new window
start "HealthAI Frontend" npm run dev
echo [+] Frontend started
echo     App: http://localhost:3000

REM Wait for servers to start
timeout /t 2 /nobreak

REM Display status
cls
echo.
echo ╔─────────────────────────────────────────────────────╗
echo ║  Both servers are running!                          ║
echo ├─────────────────────────────────────────────────────┤
echo ║  Frontend:  http://localhost:3000                   ║
echo ║  Backend:   http://localhost:5000                   ║
echo ├─────────────────────────────────────────────────────┤
echo ║  Logs: %LOGS_DIR%
echo ║  Two terminal windows are open for backend/frontend ║
echo ║  Close them to stop the servers                     ║
echo ╚─────────────────────────────────────────────────────╝
echo.

pause
