@echo off
echo Starting Building Materials Shop Management System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Start the application
echo Starting application...
echo.
echo The application will be available at: http://localhost:5000
echo Default login: admin / admin123
echo.
echo Press Ctrl+C to stop the application
echo.
python app.py

pause
