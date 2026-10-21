@echo off
setlocal

set "PROJECT_ROOT=%~dp0"

where npm >nul 2>nul
if errorlevel 1 (
    echo npm was not found on PATH.
    pause
    exit /b 1
)

start "IntelliTender Backend" /D "%PROJECT_ROOT%backend" cmd /k npm run dev
start "IntelliTender Frontend" /D "%PROJECT_ROOT%frontend" cmd /k npm run dev

timeout /t 3 /nobreak >nul
start "" "http://localhost:5173"

endlocal
