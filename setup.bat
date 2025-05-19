@echo off
echo Instalando entorno para el Keylogger Educativo...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no se encuentra en el PATH.
    echo Por favor, instala Python desde https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "env" (
    echo Creando entorno virtual...
    python -m venv env
) else (
    echo Entorno virtual ya existe.
)

REM Activar entorno virtual
call env\Scripts\activate.bat

REM Instalar dependencias
echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Configuración completada exitosamente!
echo.
echo Para iniciar el keylogger, ejecuta:
echo   ejecutar_keylogger.bat
echo.
echo Para analizar los datos capturados, ejecuta:
echo   analizar.bat
echo.
echo ADVERTENCIA: Esta herramienta es solo para fines educativos.
echo El uso de keyloggers sin consentimiento es ilegal y no ético.
echo.

pause
