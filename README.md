# Keylogger Educativo Mejorado

![Keylogger](https://t3.ftcdn.net/jpg/10/20/25/22/360_F_1020252214_jlf1xkZ2ZH75vSWwAFINeuU6iT4sVUJ0.jpg)

**Keylogger Educativo Mejorado** es un proyecto en Python diseñado para capturar y registrar pulsaciones de teclas. Este proyecto es un **fork mejorado** del [repositorio original de ramprasathmk](https://github.com/ramprasathmk/keylogger) con características adicionales implementadas para fines educativos y académicos.

Demuestra cómo el registro de teclas puede utilizarse para diversos propósitos, como monitorear actividad de escritura para investigación, solucionar problemas de teclado o aprender sobre ciberseguridad.

⚠️ **Nota**: Este proyecto es para **fines educativos únicamente**. Por favor, úselo responsablemente y solo en sistemas donde tenga permiso para monitorear.

---

## 🚀 Características

- **Registro de Oraciones**: Captura texto en formato de oraciones completas en lugar de teclas individuales.
- **Marcas de Tiempo (Timestamps)**: Cada registro incluye fecha y hora exacta de captura.
- **Detección de Ventanas Activas**: Identifica en qué aplicaciones se está escribiendo.
- **Interfaz Gráfica Mejorada**: Diseño limpio con opciones para iniciar/detener captura y ver registros.
- **Visualización de Datos**: Herramienta de análisis para visualizar la actividad de escritura.
- **Manejo Mejorado de Teclas Especiales**: Mejor interpretación de teclas como backspace, enter, etc.
- **Compatible con Reinicio**: Corregido el problema que impedía reiniciar el keylogger.
- **Documentación Detallada**: Incluye instrucciones claras y comentarios explicativos en el código.

---

## 📦 Estructura del Proyecto

El proyecto contiene los siguientes archivos principales:

- **`keylogger.py`** - Keylogger mejorado con registro de oraciones y timestamps.
- **`analizar_datos.py`** - Herramienta para visualizar y analizar los datos capturados.
- **`ejecutar_keylogger.bat`** - Ejecuta el keylogger mejorado.
- **`analizar.bat`** - Ejecuta el analizador de datos para generar visualizaciones.
- **`requirements.txt`** - Lista todas las bibliotecas de Python necesarias para este proyecto.

---

## </> Technologies Used

## [![Techs Used](https://skillicons.dev/icons?i=git,github,pycharm,py,md,bash&theme=light)](https://skillicons.dev)

## 🛠️ Configuración e Instalación

Sigue estos pasos para configurar el proyecto en tu máquina local.

### Requisitos Previos

- **Python 3.x**: Asegúrate de tener Python instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

### Instalación

#### 1. Clonar o Descargar el Repositorio

```bash
git clone https://github.com/TU-USUARIO/keylogger-educativo.git
cd keylogger-educativo
```

#### 2. Configuración Automática

Ejecuta el script de configuración que instalará todas las dependencias necesarias:

```bash
setup.bat
```

Este script creará un entorno virtual e instalará todas las bibliotecas requeridas.

#### 3. Ejecución

Una vez completada la instalación, puedes:

- **Ejecutar el keylogger**:

```bash
ejecutar_keylogger.bat
```

- **Analizar los datos capturados**:

```bash
analizar.bat
```

## 🔍 Uso

### Interfaz del Keylogger

La interfaz del keylogger es simple e intuitiva:

- **Iniciar Captura**: Comienza a registrar las pulsaciones de teclas.
- **Detener**: Pausa el registro de actividad.
- **Ver Registros**: Muestra los datos capturados hasta el momento.
- **Menú de Ayuda**: Información sobre el uso educativo de la herramienta.

### Analizador de Datos

El analizador de datos proporciona:

- **Visualizaciones gráficas**: Gráficos de actividad por ventana y hora.
- **Estadísticas de uso**: Resumen de aplicaciones más utilizadas.
- **Informe HTML interactivo**: Reporte detallado que se abre en el navegador.

Los archivos de registro se guardan automáticamente en el directorio `out`.

## ⚠️ Aviso Legal

Este keylogger está destinado exclusivamente para fines educativos y de investigación. El registro no autorizado de pulsaciones de teclas es ilegal y no ético. Utilícelo solo en sistemas donde tenga permiso para monitorear.

## 🔄 Mejoras Realizadas al Proyecto Original

Este fork ha realizado varias mejoras significativas sobre el keylogger original:

1. **Rediseño de la Arquitectura**: Código más modular y mantenible.
2. **Registro por Oraciones**: Ahora registra texto en formato de oraciones en lugar de teclas individuales.
3. **Detección de Ventanas**: Identifica en qué aplicación escribe el usuario.
4. **Interfaz Optimizada**: Interfaz gráfica mejorada y más intuitiva.
5. **Visualización de Datos**: Herramienta de análisis para las estadísticas de captura.
6. **Corregido el Error de Reinicio**: Solución al problema que impedía reiniciar el keylogger.
7. **Mejor Gestión de Archivos**: Verifica la existencia de directorios antes de escribir.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](./LICENSE) para más detalles.

## 🙋‍♂️ ¿Preguntas?

Si tienes preguntas o necesitas aclaraciones, no dudes en contactarme a través de la sección de Issues de GitHub.

---

Este README proporciona una visión general clara y ética del proyecto, y garantiza que los usuarios comprendan tanto la configuración como las consideraciones legales.

## ✨ Show your support

Give a ⭐ if you like this repository!

Happy Logging! 🔍

<!-- [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?&logo=buy-me-a-coffee&logoColor=black)]() -->
