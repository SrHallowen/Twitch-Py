@echo off
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    echo Please install Python 3.12+ from: https://www.python.org/downloads/
    pause
    exit /b 1
)

python -c "import sys; exit(1) if sys.version_info < (3, 12) else exit(0)"
if %errorlevel% neq 0 (
    echo Python 3.12 or newer is required.
    echo Current version:
    python --version
    echo Please update Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

python main.py
pause