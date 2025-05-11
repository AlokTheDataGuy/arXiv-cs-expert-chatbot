@echo off
echo Starting arXiv CS Expert Chatbot...

REM Check if Ollama is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo Starting Ollama...
    start "" ollama serve
    timeout /t 5 /nobreak > NUL
)

REM Start the backend server
echo Starting backend server...
start "Backend Server" cmd /c "cd backend && python run.py"

REM Wait for the backend to start
timeout /t 5 /nobreak > NUL

REM Start the frontend development server
echo Starting frontend server...
start "Frontend Server" cmd /c "cd frontend && npm run dev"

echo Servers are running. Close the command windows to stop.
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000

pause
