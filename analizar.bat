@echo off
echo Ejecutando el analizador de datos del keylogger...
cd /d "%~dp0"
if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat
    python analizar_datos.py
    pause
) else (    echo El entorno virtual no está configurado.
    echo Ejecute primero setup.bat para configurar el entorno.
    pause
)
