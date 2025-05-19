@echo off
echo Ejecutando el Keylogger Educativo...
cd /d "%~dp0"
if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat
    python keylogger.py
) else (
    echo El entorno virtual no está configurado.
    echo Ejecute primero setup.bat para configurar el entorno.
    pause
)
