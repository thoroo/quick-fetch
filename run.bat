@echo off
setlocal

set "CURRENT_DIR=%cd%"
set "VENV_DIR=%CURRENT_DIR%\venv"
set "REQUIREMENTS_FILE=%CURRENT_DIR%\requirements.txt"

rem Check if the virtual environment directory exists
if not exist "%VENV_DIR%" (
    echo:
    echo Virtual environment not found.
    choice /m "Do you want to create a virtual environment and install requirements?"
    if errorlevel 2 (
        echo Operation cancelled by user.
        exit /b 1
    )
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    echo Virtual environment created.

    rem Activate the virtual environment
    call "%VENV_DIR%\Scripts\activate.bat"

    echo Installing requirements...
    pip install -r "%REQUIREMENTS_FILE%" --quiet --disable-pip-version-check
    echo Requirements installed.
    
) else (
    rem Activate the virtual environment
    call "%VENV_DIR%\Scripts\activate.bat"
)

python -m quick_fetch
